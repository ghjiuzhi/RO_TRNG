module RO_TRNG_restart_reduced_xor_top #(
    parameter RESTART_COUNT = 1000,
    parameter ROW_BYTES     = 125,
    parameter HOLD_CYCLES   = 32'd200000,
    parameter SETTLE_CYCLES = 32'd200000,
    parameter [63:0] START_DELAY_CYCLES = 64'd0,
    parameter DEBUG_HEADER  = 1,
    parameter WARMUP_BYTES  = 0,
    parameter REDUCED_MODE  = 1,
    parameter REDUCED_INDEX = 0,
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

    localparam HEADER_BYTES = 8;
    localparam [63:0] START_DELAY_LAST =
        (START_DELAY_CYCLES <= 1) ? 64'd0 : START_DELAY_CYCLES - 1;
    localparam [31:0] HOLD_LAST =
        (HOLD_CYCLES <= 1) ? 32'd0 : HOLD_CYCLES - 1;
    localparam [31:0] SETTLE_LAST =
        (SETTLE_CYCLES <= 1) ? 32'd0 : SETTLE_CYCLES - 1;

    wire       all_xor_bit;
    wire [RO_NUM-1:0]        data_ro_xor_bits;
    wire [SAMPLE_STAGES-2:0] line_xor_bits;
    wire       reduced_bit;
    wire       rand_clk;
    wire       locked;
    wire       clk_200m;
    wire       rst_n_200m;
    wire       fifo_full;
    wire       fifo_empty;
    wire       tx_data_ready;
    wire [7:0] fifo_dout;
    wire [RO_NUM*(SAMPLE_STAGES-1)-1:0] sampled_data_unused;

    reg        ro_en;
    reg  [3:0] state;
    reg [63:0] state_count;
    reg [31:0] row_index;
    reg [31:0] warmup_count;
    reg [31:0] send_count;
    reg  [3:0] header_index;

    wire do_drain =
        (state == ST_DRAIN) && ~fifo_empty;
    wire do_warmup =
        (state == ST_WARMUP) && ~fifo_empty && (warmup_count < WARMUP_BYTES);
    wire do_send =
        (state == ST_SEND) && tx_data_ready && ~fifo_empty;

    wire fifo_wr_en = ro_en & ~fifo_full;
    wire do_header_send = (state == ST_HEADER) && tx_data_ready;
    wire fifo_rd_en = do_drain | do_warmup | do_send;
    wire tx_data_valid =
        ((state == ST_HEADER) && tx_data_ready) ||
        ((state == ST_SEND) && ~fifo_empty);

    wire [7:0] tx_data =
        (state == ST_HEADER) ? header_byte(header_index) : fifo_dout;

    assign reduced_bit = select_reduced_bit(
        all_xor_bit,
        data_ro_xor_bits,
        line_xor_bits
    );

    function [7:0] header_byte;
        input [3:0] idx;
        begin
            case (idx)
                4'd0: header_byte = 8'ha5;
                4'd1: header_byte = 8'h5a;
                4'd2: header_byte = RESTART_COUNT[15:8];
                4'd3: header_byte = RESTART_COUNT[7:0];
                4'd4: header_byte = ROW_BYTES[15:8];
                4'd5: header_byte = ROW_BYTES[7:0];
                4'd6: header_byte = 8'h01;
                4'd7: header_byte = 8'hd0;
                default: header_byte = 8'h00;
            endcase
        end
    endfunction

    function select_reduced_bit;
        input all_bit;
        input [RO_NUM-1:0] data_bits;
        input [SAMPLE_STAGES-2:0] line_bits;
        integer idx;
        begin
            idx = REDUCED_INDEX;
            if (REDUCED_MODE == 0) begin
                select_reduced_bit = all_bit;
            end
            else if (REDUCED_MODE == 1) begin
                if (idx >= 0 && idx < RO_NUM) begin
                    select_reduced_bit = data_bits[idx];
                end
                else begin
                    select_reduced_bit = 1'b0;
                end
            end
            else if (REDUCED_MODE == 2) begin
                if (idx >= 0 && idx < SAMPLE_STAGES-1) begin
                    select_reduced_bit = line_bits[idx];
                end
                else begin
                    select_reduced_bit = 1'b0;
                end
            end
            else if (REDUCED_MODE == 3) begin
                if (idx >= 0 && idx < RO_NUM) begin
                    select_reduced_bit = all_bit ^ data_bits[idx];
                end
                else begin
                    select_reduced_bit = all_bit;
                end
            end
            else begin
                select_reduced_bit = all_bit;
            end
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

    entropy_source_reduced_probe #(
        .RO_NUM(RO_NUM),
        .RO_STAGES(RO_STAGES),
        .SAMPLE_STAGES(SAMPLE_STAGES)
    ) u_entropy_source (
        .en(ro_en),
        .all_xor_bit(all_xor_bit),
        .data_ro_xor_bits(data_ro_xor_bits),
        .line_xor_bits(line_xor_bits),
        .clk_o(rand_clk),
        .sampled_data_o(sampled_data_unused)
    );

    fifo_generator_0 u_fifo_generator_0 (
        .wr_clk(rand_clk),
        .rd_clk(clk_200m),
        .din(reduced_bit),
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
        .tx_data_valid(tx_data_valid),
        .tx_data_ready(tx_data_ready),
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
            header_index <= 4'd0;
        end
        else begin
            case (state)
                ST_START_WAIT: begin
                    ro_en <= 1'b0;
                    row_index <= 32'd0;
                    warmup_count <= 32'd0;
                    send_count <= 32'd0;
                    header_index <= 4'd0;
                    if (START_DELAY_CYCLES == 0 || state_count >= START_DELAY_LAST) begin
                        state_count <= 64'd0;
                        if (DEBUG_HEADER != 0) begin
                            state <= ST_HEADER;
                        end
                        else begin
                            state <= ST_HOLD;
                        end
                    end
                    else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_HEADER: begin
                    ro_en <= 1'b0;
                    state_count <= 64'd0;
                    if (do_header_send) begin
                        if (header_index >= HEADER_BYTES - 1) begin
                            header_index <= 4'd0;
                            state <= ST_HOLD;
                        end
                        else begin
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
                    end
                    else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_DRAIN: begin
                    ro_en <= 1'b0;
                    state_count <= 64'd0;
                    if (fifo_empty) begin
                        if (row_index >= RESTART_COUNT) begin
                            state <= ST_DONE;
                        end
                        else begin
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
                        end
                        else begin
                            state <= ST_WARMUP;
                        end
                    end
                    else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_WARMUP: begin
                    ro_en <= 1'b1;
                    if (do_warmup) begin
                        if (warmup_count >= WARMUP_BYTES - 1) begin
                            warmup_count <= 32'd0;
                            state <= ST_SEND;
                        end
                        else begin
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
                            end
                            else begin
                                state <= ST_HOLD;
                            end
                        end
                        else begin
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
                    warmup_count <= 32'd0;
                    send_count <= 32'd0;
                    header_index <= 4'd0;
                end
            endcase
        end
    end

endmodule
