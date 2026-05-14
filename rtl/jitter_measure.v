module jitter_measure (
    input  clk_100M_p,
    input  clk_100M_n,
    input  por_n_i,
    input  UART_RX_i,
    output UART_TX_o
);

    wire       ro_clk;
    wire       locked;
    wire       clk_200m;
    wire       clk_100m;
    wire       rst_n_100m;
    wire       ro_en;
    wire [7:0] counter_cu_cnt0;
    wire [7:0] counter_cu_cnt1;
    wire [7:0] counter_cu_cnt2;
    wire [7:0] cu_fifo_cnt;
    wire       cu_fifo_vld;
    wire       counter_rst_n;
    wire       rx_full;

    wire       empty;
    wire       tx_data_ready;
    wire [7:0] tx_data;
    wire [7:0] rx_data;
    wire rx_data_valid;
    wire rx_data_ready;


    clk_wiz_0 u_clk_wiz_0 (
        // Clock out ports
        .clk_out1 (clk_200m),    // output clk_out1
        .clk_out2 (clk_100m),    // output clk_out1
        // Status and control signals
        .reset    (~por_n_i),    // input reset
        .locked   (locked),      // output locked
        // Clock in ports
        .clk_in1_p(clk_100M_p),  // input clk_in1_p
        .clk_in1_n(clk_100M_n)   // input clk_in1_n
    );

    proc_sys_reset_0 u_proc_sys_reset_0 (
        .slowest_sync_clk    (clk_100m),   // input wire slowest_sync_clk
        .ext_reset_in        (~por_n_i),   // input wire ext_reset_in
        .aux_reset_in        (1'b0),       // input wire aux_reset_in
        .mb_debug_sys_rst    (1'b0),       // input wire mb_debug_sys_rst
        .dcm_locked          (locked),     // input wire dcm_locked
        .mb_reset            (),           // output wire mb_reset
        .bus_struct_reset    (),           // output wire [0 : 0] bus_struct_reset
        .peripheral_reset    (),           // output wire [0 : 0] peripheral_reset
        .interconnect_aresetn(),           // output wire [0 : 0] interconnect_aresetn
        .peripheral_aresetn  (rst_n_100m)  // output wire [0 : 0] peripheral_aresetn
    );

    RO #(
        .RO_STAGES(9)
    ) u_RO (
        .en   (ro_en),
        .clk_o(ro_clk)
    );

    counter u_counter (
        .clk_i  (ro_clk),
        .en_i   (ro_en),
        .cnt0_o (counter_cu_cnt0),
        .cnt1_o (counter_cu_cnt1),
        .rst_n_i(counter_rst_n),
        .cnt2_o (counter_cu_cnt2)
    );

    // the period of en_o is half of clk_i
    CU u_CU (
        .clk_i          (clk_200m),
        .rx_data_i      (rx_data),
        .rx_data_ready_o(rx_data_ready),
        .rx_data_valid_i(rx_data_valid),
        .cnt0_i         (counter_cu_cnt0),
        .cnt1_i         (counter_cu_cnt1),
        .cnt2_i         (counter_cu_cnt2),
        .cnt_o          (cu_fifo_cnt),
        .en_o           (ro_en),
        .rst_n_i        (rst_n_100m),
        .vld_o          (cu_fifo_vld),
        .rst_n_o        (counter_rst_n)
    );

    fifo_generator_1 u_fifo_generator_1 (
        .clk  (clk_200m),                // input wire clk
        .din  (cu_fifo_cnt),             // input wire [7 : 0] din
        .wr_en(cu_fifo_vld & ~rx_full),  // input wire wr_en
        .rd_en(tx_data_ready),           // input wire rd_en
        .dout (tx_data),                 // output wire [7 : 0] dout
        .full (rx_full),                 // output wire full
        .empty(empty)                    // output wire empty
    );

    uart_tx #(
        .CLK_FRE  (200),
        .BAUD_RATE(115200)
    ) u_uart_tx (
        .clk          (clk_200m),
        .rst_n        (rst_n_100m),
        .tx_data      (tx_data),
        .tx_data_valid(~empty),
        .tx_data_ready(tx_data_ready),
        .tx_pin       (UART_TX_o)
    );

    
    
    uart_rx #(
        .CLK_FRE  (200),
        .BAUD_RATE(115200)
    )
    u_uart_rx (
        .clk          (clk_200m), //clock input
        .rst_n        (rst_n_100m), //asynchronous reset input, low active
        .rx_data      (rx_data), //received serial data
        .rx_data_ready(rx_data_ready), //data receiver module ready
        .rx_data_valid(rx_data_valid), //received serial data is valid
        .rx_pin       (UART_RX_i) //serial data input
    );

endmodule
