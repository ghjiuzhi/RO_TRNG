module RO_FREQ_trng_probe_top #(
    parameter FAMILY_ID = 0,
    parameter WINDOW_CYCLES = 100,
    parameter SETTLE_CYCLES = 1000,
    parameter RO_NUM = 8
) (
    input  wire sys_clk,
    input  wire por_n_i,
    output wire UART_TX_o
);

    localparam MODE_ALL_ON = 8'd0;
    localparam MODE_SINGLE_ON = 8'd1;

    localparam ST_SETTLE = 3'd0;
    localparam ST_MEASURE = 3'd1;
    localparam ST_LATCH0 = 3'd2;
    localparam ST_LATCH1 = 3'd3;
    localparam ST_SEND_LOAD = 3'd4;
    localparam ST_SEND_WAIT_LOW = 3'd5;
    localparam ST_SEND_WAIT_HIGH = 3'd6;
    localparam ST_ADVANCE = 3'd7;

    wire locked;
    wire clk_200m;
    wire rst_n_200m;
    wire [RO_NUM-1:0] data_clk;
    wire sample_clk;
    wire selected_clk;
    wire tx_ready;
    wire [7:0] cnt0;
    wire [7:0] cnt1;
    wire [7:0] cnt2;

    reg [2:0] state;
    reg [31:0] state_count;
    reg [7:0] mode;
    reg [3:0] target_idx;
    reg [15:0] seq;
    reg [7:0] count_latched;
    reg [7:0] tx_data;
    reg tx_valid;
    reg counter_en;
    reg counter_rst_n;
    reg [3:0] send_idx;

    wire [7:0] active_data_mask =
        (mode == MODE_ALL_ON) ? 8'hff :
        (target_idx < 4'd8) ? (8'h01 << target_idx[2:0]) :
        8'h00;
    wire active_sample =
        (mode == MODE_ALL_ON) ? 1'b1 :
        (target_idx == 4'd8);

    assign selected_clk = (target_idx == 4'd8) ? sample_clk : data_clk[target_idx[2:0]];

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

    ro_freq_entropy_probe #(
        .RO_NUM(RO_NUM),
        .RO_STAGES(2),
        .SAMPLE_STAGES(9)
    ) u_entropy_source (
        .data_en_i(active_data_mask[RO_NUM-1:0]),
        .sample_en_i(active_sample),
        .data_clk_o(data_clk),
        .sample_clk_o(sample_clk)
    );

    counter u_counter (
        .clk_i(selected_clk),
        .rst_n_i(counter_rst_n),
        .en_i(counter_en),
        .cnt0_o(cnt0),
        .cnt1_o(cnt1),
        .cnt2_o(cnt2)
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

    function [7:0] frame_byte;
        input [3:0] idx;
        begin
            case (idx)
                4'd0:  frame_byte = 8'h52;  // R
                4'd1:  frame_byte = 8'h46;  // F
                4'd2:  frame_byte = 8'd1;
                4'd3:  frame_byte = FAMILY_ID[7:0];
                4'd4:  frame_byte = mode;
                4'd5:  frame_byte = {4'b0000, target_idx};
                4'd6:  frame_byte = active_data_mask;
                4'd7:  frame_byte = {7'b0000000, active_sample};
                4'd8:  frame_byte = WINDOW_CYCLES[7:0];
                4'd9:  frame_byte = WINDOW_CYCLES[15:8];
                4'd10: frame_byte = count_latched;
                4'd11: frame_byte = seq[7:0];
                4'd12: frame_byte = seq[15:8];
                default: frame_byte =
                    8'h52 ^ 8'h46 ^ 8'd1 ^ FAMILY_ID[7:0] ^ mode ^
                    {4'b0000, target_idx} ^ active_data_mask ^
                    {7'b0000000, active_sample} ^
                    WINDOW_CYCLES[7:0] ^ WINDOW_CYCLES[15:8] ^
                    count_latched ^ seq[7:0] ^ seq[15:8];
            endcase
        end
    endfunction

    always @(posedge clk_200m or negedge rst_n_200m) begin
        if (~rst_n_200m) begin
            state <= ST_SETTLE;
            state_count <= 32'd0;
            mode <= MODE_ALL_ON;
            target_idx <= 4'd0;
            seq <= 16'd0;
            count_latched <= 8'd0;
            tx_data <= 8'd0;
            tx_valid <= 1'b0;
            counter_en <= 1'b0;
            counter_rst_n <= 1'b0;
            send_idx <= 4'd0;
        end
        else begin
            tx_valid <= 1'b0;

            case (state)
                ST_SETTLE: begin
                    counter_en <= 1'b0;
                    counter_rst_n <= 1'b0;
                    if (state_count >= SETTLE_CYCLES - 1) begin
                        state_count <= 32'd0;
                        state <= ST_MEASURE;
                    end
                    else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_MEASURE: begin
                    counter_rst_n <= 1'b1;
                    counter_en <= 1'b1;
                    if (state_count >= WINDOW_CYCLES - 1) begin
                        state_count <= 32'd0;
                        counter_en <= 1'b0;
                        state <= ST_LATCH0;
                    end
                    else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_LATCH0: begin
                    state <= ST_LATCH1;
                end

                ST_LATCH1: begin
                    if (cnt0 != (cnt2 + 8'd2)) begin
                        count_latched <= cnt1 + 8'd2;
                    end
                    else begin
                        count_latched <= cnt0;
                    end
                    send_idx <= 4'd0;
                    state <= ST_SEND_LOAD;
                end

                ST_SEND_LOAD: begin
                    if (tx_ready) begin
                        tx_data <= frame_byte(send_idx);
                        tx_valid <= 1'b1;
                        state <= ST_SEND_WAIT_LOW;
                    end
                end

                ST_SEND_WAIT_LOW: begin
                    if (!tx_ready) begin
                        state <= ST_SEND_WAIT_HIGH;
                    end
                end

                ST_SEND_WAIT_HIGH: begin
                    if (tx_ready) begin
                        if (send_idx == 4'd13) begin
                            state <= ST_ADVANCE;
                        end
                        else begin
                            send_idx <= send_idx + 1'b1;
                            state <= ST_SEND_LOAD;
                        end
                    end
                end

                ST_ADVANCE: begin
                    seq <= seq + 1'b1;
                    if (target_idx == 4'd8) begin
                        target_idx <= 4'd0;
                        mode <= (mode == MODE_ALL_ON) ? MODE_SINGLE_ON : MODE_ALL_ON;
                    end
                    else begin
                        target_idx <= target_idx + 1'b1;
                    end
                    state <= ST_SETTLE;
                end

                default: begin
                    state <= ST_SETTLE;
                end
            endcase
        end
    end

endmodule
