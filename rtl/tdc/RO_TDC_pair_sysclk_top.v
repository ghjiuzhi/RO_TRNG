module RO_TDC_pair_sysclk_top #(
    parameter CARRY4_NUM = 16,
    parameter TAP_NUM = CARRY4_NUM * 4,
    parameter BIN_W = 8,
    parameter RO_A_STAGES = 2,
    parameter RO_B_STAGES = 2,
    parameter PAIR_ID = 0,
    parameter FAMILY_ID = 0
) (
    input  wire sys_clk,
    input  wire por_n_i,
    output wire UART_TX_o
);

    wire locked;
    wire clk_200m;
    wire rst_n_200m;
    wire ro_a_clk;
    wire ro_b_clk;
    wire [BIN_W-1:0] bin_a;
    wire [BIN_W-1:0] bin_b;
    wire vld_a;
    wire vld_b;
    wire bubble_a;
    wire bubble_b;
    wire empty_a;
    wire empty_b;
    wire full_a;
    wire full_b;
    wire [7:0] flags;
    wire [7:0] tx_data;
    wire tx_valid;
    wire tx_ready;

    clk_wiz_0 u_clk_wiz_0 (
        .clk_out1(clk_200m),
        .reset(1'b0),
        .locked(locked),
        .clk_in1(sys_clk)
    );

    proc_sys_reset_0 u_proc_sys_reset_0 (
        .slowest_sync_clk(clk_200m),
        .ext_reset_in(1'b0),
        .aux_reset_in(1'b0),
        .mb_debug_sys_rst(1'b0),
        .dcm_locked(locked),
        .mb_reset(),
        .bus_struct_reset(),
        .peripheral_reset(),
        .interconnect_aresetn(),
        .peripheral_aresetn(rst_n_200m)
    );

    RO #(
        .RO_STAGES(RO_A_STAGES)
    ) u_ro_a (
        .en(1'b1),
        .clk_o(ro_a_clk)
    );

    RO #(
        .RO_STAGES(RO_B_STAGES)
    ) u_ro_b (
        .en(1'b1),
        .clk_o(ro_b_clk)
    );

    tdc_lane #(
        .CARRY4_NUM(CARRY4_NUM),
        .TAP_NUM(TAP_NUM),
        .BIN_W(BIN_W)
    ) u_tdc_a (
        .clk_i(clk_200m),
        .rst_n_i(rst_n_200m),
        .hit_i(ro_a_clk),
        .bin_o(bin_a),
        .sample_vld_o(vld_a),
        .bubble_seen_o(bubble_a),
        .empty_o(empty_a),
        .full_o(full_a)
    );

    tdc_lane #(
        .CARRY4_NUM(CARRY4_NUM),
        .TAP_NUM(TAP_NUM),
        .BIN_W(BIN_W)
    ) u_tdc_b (
        .clk_i(clk_200m),
        .rst_n_i(rst_n_200m),
        .hit_i(ro_b_clk),
        .bin_o(bin_b),
        .sample_vld_o(vld_b),
        .bubble_seen_o(bubble_b),
        .empty_o(empty_b),
        .full_o(full_b)
    );

    assign flags = {vld_a & vld_b, bubble_b, bubble_a, full_b, full_a, empty_b, empty_a, 1'b0};

    tdc_uart_packetizer #(
        .SAMPLE_DIV(16'd5000)
    ) u_packetizer (
        .clk_i(clk_200m),
        .rst_n_i(rst_n_200m),
        .bin_a_i(bin_a),
        .bin_b_i(bin_b),
        .flags_i(flags),
        .tx_ready_i(tx_ready),
        .tx_data_o(tx_data),
        .tx_valid_o(tx_valid)
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

endmodule
