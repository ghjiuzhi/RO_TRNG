module counter (
    input clk_i,
    input rst_n_i,
    input en_i,
    output [7:0] cnt0_o,
    output [7:0] cnt1_o,
    output [7:0] cnt2_o
);

    reg [7:0] cnt[2:0];
    reg [1:0] en_sync;

    always @(posedge clk_i or negedge rst_n_i) begin
        if (~rst_n_i) begin
            en_sync <= 'b0;
        end
        else begin
            en_sync[0] <= en_i;
            en_sync[1] <= en_sync[0];
        end
    end

    always @(posedge clk_i or negedge rst_n_i) begin
        if (~rst_n_i) begin
            cnt[0] <= 'b0;
        end
        else if (en_i) begin
            cnt[0] <= cnt[0] + 1'b1;
        end
    end

    always @(posedge clk_i or negedge rst_n_i) begin
        if (~rst_n_i) begin
            cnt[1] <= 'b0;
            cnt[2] <= 'b0;
        end
        else begin
            cnt[1] <= cnt[0];
            cnt[2] <= cnt[1];
        end
    end

    assign cnt0_o = cnt[0];
    assign cnt1_o = cnt[1];
    assign cnt2_o = cnt[2];

endmodule