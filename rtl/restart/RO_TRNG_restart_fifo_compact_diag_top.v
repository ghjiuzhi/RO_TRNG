module RO_TRNG_restart_fifo_compact_diag_top #(
    parameter RESTART_COUNT = 1000,
    parameter ROW_BYTES     = 125,
    parameter HOLD_CYCLES   = 32'd200000,
    parameter SETTLE_CYCLES = 32'd200000,
    parameter [63:0] START_DELAY_CYCLES = 64'd0,
    parameter DEBUG_HEADER   = 1,
    parameter WARMUP_BYTES  = 0,
    parameter RO_NUM        = 8,
    parameter RO_STAGES     = 2,
    parameter SAMPLE_STAGES = 9
) (
    input  wire sys_clk,
    input  wire por_n_i,
    output wire UART_TX_o
);

    localparam ST_START_WAIT = 4'd0;
    localparam ST_HEADER     = 4'd1;
    localparam ST_HOLD       = 4'd2;
    localparam ST_DRAIN      = 4'd3;
    localparam ST_SETTLE     = 4'd4;
    localparam ST_WARMUP     = 4'd5;
    localparam ST_SEND       = 4'd6;
    localparam ST_DONE       = 4'd7;

    localparam HEADER_BYTES = 16;
    localparam TOTAL_BYTES = RESTART_COUNT * ROW_BYTES;
    localparam [63:0] START_DELAY_LAST =
        (START_DELAY_CYCLES <= 1) ? 64'd0 : START_DELAY_CYCLES - 1;
    localparam [31:0] HOLD_LAST =
        (HOLD_CYCLES <= 1) ? 32'd0 : HOLD_CYCLES - 1;
    localparam [31:0] SETTLE_LAST =
        (SETTLE_CYCLES <= 1) ? 32'd0 : SETTLE_CYCLES - 1;

    wire       rand_bit;
    wire       rand_clk;
    wire       locked;
    wire       clk_200m;
    wire       rst_n_200m;
    wire       fifo_full;
    wire       fifo_empty;
    wire       tx_ready;
    wire [7:0] fifo_dout;

    reg        ro_en;
    reg  [3:0] state;
    reg [63:0] state_count;
    reg [31:0] row_index;
    reg [31:0] warmup_count;
    reg [31:0] send_count;
    reg  [4:0] header_index;

    wire do_drain = (state == ST_DRAIN) && ~fifo_empty;
    wire do_warmup = (state == ST_WARMUP) && ~fifo_empty && (warmup_count < WARMUP_BYTES);
    wire do_send = (state == ST_SEND) && tx_ready && ~fifo_empty;
    wire fifo_wr_en = ro_en & ~fifo_full;
    wire fifo_rd_en = do_drain | do_warmup | do_send;
    wire do_header_send = (state == ST_HEADER) && tx_ready;
    wire tx_valid = do_header_send | ((state == ST_SEND) && ~fifo_empty);
    wire [7:0] tx_data = (state == ST_HEADER) ? header_byte(header_index) : fifo_dout;

    function [7:0] header_byte;
        input [4:0] idx;
        begin
            case (idx)
                5'd0: header_byte = 8'h46; // F
                5'd1: header_byte = 8'h44; // D
                5'd2: header_byte = 8'h49; // I
                5'd3: header_byte = 8'h43; // C
                5'd4: header_byte = 8'h01;
                5'd5: header_byte = RESTART_COUNT[7:0];
                5'd6: header_byte = RESTART_COUNT[15:8];
                5'd7: header_byte = ROW_BYTES[7:0];
                5'd8: header_byte = ROW_BYTES[15:8];
                5'd9: header_byte = WARMUP_BYTES[7:0];
                5'd10: header_byte = WARMUP_BYTES[15:8];
                5'd11: header_byte = TOTAL_BYTES[7:0];
                5'd12: header_byte = TOTAL_BYTES[15:8];
                5'd13: header_byte = TOTAL_BYTES[23:16];
                5'd14: header_byte = TOTAL_BYTES[31:24];
                5'd15: header_byte = 8'haa;
                default: header_byte = 8'h00;
            endcase
        end
    endfunction

    clk_wiz_0 u_clk_wiz_0 (
        .clk_out1(clk_200m),
        .reset(~por_n_i),
        .locked(locked),
        .clk_in1(sys_clk)
    );

    proc_sys_reset_0 u_proc_sys_reset_0 (
        .slowest_sync_clk(clk_200m),
        .ext_reset_in(~por_n_i),
        .aux_reset_in(1'b0),
        .mb_debug_sys_rst(1'b0),
        .dcm_locked(locked),
        .mb_reset(),
        .bus_struct_reset(),
        .peripheral_reset(),
        .interconnect_aresetn(),
        .peripheral_aresetn(rst_n_200m)
    );

    entropy_source #(
        .RO_NUM(RO_NUM),
        .RO_STAGES(RO_STAGES),
        .SAMPLE_STAGES(SAMPLE_STAGES)
    ) u_entropy_source (
        .en(ro_en),
        .rand_bit(rand_bit),
        .clk_o(rand_clk)
    );

    fifo_generator_0 u_fifo_generator_0 (
        .wr_clk(rand_clk),
        .rd_clk(clk_200m),
        .din(rand_bit),
        .wr_en(fifo_wr_en),
        .rd_en(fifo_rd_en),
        .dout(fifo_dout),
        .full(fifo_full),
        .empty(fifo_empty)
    );

    uart_tx #(
        .CLK_FRE(200),
        .BAUD_RATE(115200)
    ) u_uart_tx (
        .clk(clk_200m),
        .rst_n(rst_n_200m),
        .tx_data(tx_data),
        .tx_data_valid(tx_valid),
        .tx_data_ready(tx_ready),
        .tx_pin(UART_TX_o)
    );

    always @(posedge clk_200m) begin
        if (~rst_n_200m) begin
            ro_en <= 1'b0;
            state <= ST_START_WAIT;
            state_count <= 64'd0;
            row_index <= 32'd0;
            warmup_count <= 32'd0;
            send_count <= 32'd0;
            header_index <= 5'd0;
        end else begin
            case (state)
                ST_START_WAIT: begin
                    ro_en <= 1'b0;
                    row_index <= 32'd0;
                    warmup_count <= 32'd0;
                    send_count <= 32'd0;
                    header_index <= 5'd0;
                    if (START_DELAY_CYCLES == 0 || state_count >= START_DELAY_LAST) begin
                        state_count <= 64'd0;
                        if (DEBUG_HEADER != 0) begin
                            state <= ST_HEADER;
                        end else begin
                            state <= ST_HOLD;
                        end
                    end else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_HEADER: begin
                    ro_en <= 1'b0;
                    state_count <= 64'd0;
                    if (do_header_send) begin
                        if (header_index >= HEADER_BYTES - 1) begin
                            header_index <= 5'd0;
                            state <= ST_HOLD;
                        end else begin
                            header_index <= header_index + 1'b1;
                        end
                    end
                end

                ST_HOLD: begin
                    ro_en <= 1'b0;
                    warmup_count <= 32'd0;
                    send_count <= 32'd0;
                    if (HOLD_CYCLES == 0 || state_count >= HOLD_LAST) begin
                        state_count <= 64'd0;
                        state <= ST_DRAIN;
                    end else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_DRAIN: begin
                    ro_en <= 1'b0;
                    state_count <= 64'd0;
                    if (fifo_empty) begin
                        if (row_index >= RESTART_COUNT) begin
                            state <= ST_DONE;
                        end else begin
                            state <= ST_SETTLE;
                        end
                    end
                end

                ST_SETTLE: begin
                    ro_en <= 1'b1;
                    warmup_count <= 32'd0;
                    send_count <= 32'd0;
                    if (SETTLE_CYCLES == 0 || state_count >= SETTLE_LAST) begin
                        state_count <= 64'd0;
                        if (WARMUP_BYTES == 0) begin
                            state <= ST_SEND;
                        end else begin
                            state <= ST_WARMUP;
                        end
                    end else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_WARMUP: begin
                    ro_en <= 1'b1;
                    if (do_warmup) begin
                        if (warmup_count >= WARMUP_BYTES - 1) begin
                            warmup_count <= 32'd0;
                            state <= ST_SEND;
                        end else begin
                            warmup_count <= warmup_count + 1'b1;
                        end
                    end
                end

                ST_SEND: begin
                    ro_en <= 1'b1;
                    if (do_send) begin
                        if (send_count >= ROW_BYTES - 1) begin
                            ro_en <= 1'b0;
                            send_count <= 32'd0;
                            row_index <= row_index + 1'b1;
                            state_count <= 64'd0;
                            if (row_index + 1'b1 >= RESTART_COUNT) begin
                                state <= ST_DONE;
                            end else begin
                                state <= ST_HOLD;
                            end
                        end else begin
                            send_count <= send_count + 1'b1;
                        end
                    end
                end

                ST_DONE: begin
                    ro_en <= 1'b0;
                    state_count <= 64'd0;
                    warmup_count <= 32'd0;
                    send_count <= 32'd0;
                end

                default: begin
                    ro_en <= 1'b0;
                    state <= ST_START_WAIT;
                    state_count <= 64'd0;
                end
            endcase
        end
    end

endmodule
