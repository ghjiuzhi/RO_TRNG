module uart_selftest_sysclk_top (
    input  wire sys_clk,
    output wire UART_TX_o
);

    wire clk_200m;
    wire locked;
    wire tx_ready;
    reg [7:0] tx_data = 8'h55;
    reg tx_valid = 1'b0;
    reg [31:0] wait_cnt = 32'd0;
    reg [3:0] index = 4'd0;

    clk_wiz_0 u_clk_wiz_0 (
        .clk_out1(clk_200m),
        .reset(1'b0),
        .locked(locked),
        .clk_in1(sys_clk)
    );

    always @(posedge clk_200m) begin
        if (!locked) begin
            wait_cnt <= 32'd0;
            tx_valid <= 1'b0;
            tx_data <= 8'h55;
            index <= 4'd0;
        end else begin
            tx_valid <= 1'b0;
            if (wait_cnt != 32'd0) begin
                wait_cnt <= wait_cnt - 1'b1;
            end else if (tx_ready) begin
                case (index)
                    4'd0: tx_data <= 8'h55;
                    4'd1: tx_data <= 8'hA5;
                    4'd2: tx_data <= 8'h5A;
                    4'd3: tx_data <= 8'hC3;
                    4'd4: tx_data <= 8'h3C;
                    4'd5: tx_data <= 8'h0D;
                    4'd6: tx_data <= 8'h0A;
                    default: tx_data <= 8'h55;
                endcase
                tx_valid <= 1'b1;
                index <= (index == 4'd6) ? 4'd0 : index + 1'b1;
                wait_cnt <= 32'd200000;
            end
        end
    end

    uart_tx #(
        .CLK_FRE(200),
        .BAUD_RATE(115200)
    ) u_uart_tx (
        .clk(clk_200m),
        .rst_n(locked),
        .tx_data(tx_data),
        .tx_data_valid(tx_valid),
        .tx_data_ready(tx_ready),
        .tx_pin(UART_TX_o)
    );

endmodule
