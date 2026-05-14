module RO_TRNG_health_top (
    input  clk_100M_p,
    input  clk_100M_n,
    input  por_n_i,
    output UART_TX_o
);

    wire rand_bit;
    wire rand_clk;
    wire locked;
    wire clk_200m;
    wire rst_n_200m;
    wire empty;
    wire tx_data_ready;
    wire [7:0] tx_data;
    wire full;
    wire en;
    wire rand_bit_healthy_o;

    clk_wiz_0 u_clk_wiz_0 (
        // Clock out ports
        .clk_out1(clk_200m),     // output clk_out1
        // Status and control signals
        .reset(~por_n_i), // input reset
        .locked(locked),       // output locked
        // Clock in ports
        .clk_in1_p(clk_100M_p),    // input clk_in1_p
        .clk_in1_n(clk_100M_n)    // input clk_in1_n
    );

    proc_sys_reset_0 u_proc_sys_reset_0 (
        .slowest_sync_clk(clk_200m),          // input wire slowest_sync_clk
        .ext_reset_in(~por_n_i),                  // input wire ext_reset_in
        .aux_reset_in(1'b0),                  // input wire aux_reset_in
        .mb_debug_sys_rst(1'b0),          // input wire mb_debug_sys_rst
        .dcm_locked(locked),                      // input wire dcm_locked
        .mb_reset(),                          // output wire mb_reset
        .bus_struct_reset(),          // output wire [0 : 0] bus_struct_reset
        .peripheral_reset(),          // output wire [0 : 0] peripheral_reset
        .interconnect_aresetn(),  // output wire [0 : 0] interconnect_aresetn
        .peripheral_aresetn(rst_n_200m)      // output wire [0 : 0] peripheral_aresetn
    );

    entropy_source #(
        .RO_NUM         (8),       // RO number
        .RO_STAGES      (2),    // RO stages
        .SAMPLE_STAGES  (9) // sample clock stages
    ) u_entropy_source (
        .en             (1'b1),  // enable signal
        .rand_bit       (rand_bit), // random bit output
        .clk_o          (rand_clk)
    );
    
    health_test u_health_test (
        .en_o              (en),
        .es_bit_i          (rand_bit),
        .es_clk_i          (rand_clk),
        .rand_bit_healthy_o(rand_bit_healthy_o),
        .rst_n_i           (rst_n_200m)
    );

    fifo_generator_0 u_fifo_generator_0 (
        .wr_clk(rand_clk),  // input wire wr_clk
        .rd_clk(clk_200m),  // input wire rd_clk
        .din   (rand_bit_healthy_o),     // input wire [0 : 0] din
        .wr_en (~full & en),   // input wire wr_en
        .rd_en (tx_data_ready),   // input wire rd_en
        .dout  (tx_data),    // output wire [7 : 0] dout
        .full  (full),    // output wire full
        .empty (empty)    // output wire empty
    );

    uart_tx #(
        .CLK_FRE  (200),
        .BAUD_RATE(115200)
    ) u_uart_tx (
        .clk          (clk_200m),
        .rst_n        (rst_n_200m),
        .tx_data      (tx_data),
        .tx_data_valid(~empty),
        .tx_data_ready(tx_data_ready),
        .tx_pin       (UART_TX_o)
    );

endmodule
