module CU #(
    parameter WINDOW_CYCLE = 30  // multiple of clk_i cycle
) (
    input clk_i,
    input rst_n_i,
    input [7:0] rx_data_i,
    output rx_data_ready_o,
    input rx_data_valid_i,
    input [7:0] cnt0_i,
    input [7:0] cnt1_i,
    input [7:0] cnt2_i,
    output en_o,
    output rst_n_o,
    output vld_o,
    output [7:0] cnt_o
);

    localparam TOTAL_NUM = 1000000;

    reg        en;
    reg        vld;
    reg        rst_n;
    reg [31:0] state;
    reg [ 7:0] cnt;
    reg [31:0] total_num;
    reg [7:0] window_size;
    reg rx_data_ready;

    always @(posedge clk_i or negedge rst_n_i) begin
        if (~rst_n_i) begin
            window_size <= 'd100;
            rx_data_ready <= 1'b0;
        end else if (total_num == TOTAL_NUM && rx_data_valid_i) begin
            window_size <= rx_data_i;
            rx_data_ready <= 1'b1;
        end
        else begin
            window_size <= window_size;
            rx_data_ready <= 1'b0;
        end
    end

    always @(posedge clk_i or negedge rst_n_i) begin
        if (~rst_n_i) begin
            state <= 'b0;
        end else if (state == (window_size + 3)) begin
            state <= 'b0;
        end else if (total_num != TOTAL_NUM) begin
            state <= state + 1'b1;
        end
    end

    always @(posedge clk_i or negedge rst_n_i) begin
        if (~rst_n_i) begin
            total_num <= 'b0;
        end else if (total_num != TOTAL_NUM && state == (window_size + 3)) begin
            total_num <= total_num + 1'b1;
        end else if (total_num == TOTAL_NUM && rx_data_valid_i) begin
            total_num <= 'b0;
        end
    end

    always @(posedge clk_i or negedge rst_n_i) begin
        if (~rst_n_i) begin
            en <= 1'b0;
        end else if (state == 'd1) begin
            en <= 1'b1;
        end else if (state == (window_size + 1)) begin
            en <= 1'b0;
        end
    end

    always @(posedge clk_i or negedge rst_n_i) begin
        if (~rst_n_i) begin
            rst_n <= 1'b0;
        end else if (state == (window_size + 3)) begin
            rst_n <= 1'b0;
        end else begin
            rst_n <= 1'b1;
        end
    end

    always @(posedge clk_i or negedge rst_n_i) begin
        if (~rst_n_i) begin
            vld <= 1'b0;
            cnt <= 'b0;
        end else if (state == (window_size + 2)) begin
            vld <= 1'b1;
            if (cnt0_i != (cnt2_i + 'd2)) begin
                cnt <= cnt1_i + 'd2;
            end
            else begin
                cnt <= cnt0_i;
            end
        end else begin
            vld <= 1'b0;
            cnt <= cnt;
        end
    end

    assign en_o = en;
    assign vld_o = vld;
    assign cnt_o = cnt;
    assign rst_n_o = rst_n;
    assign rx_data_ready_o = rx_data_ready;

endmodule
