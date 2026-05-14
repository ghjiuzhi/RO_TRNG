module tdc_lane #(
    parameter CARRY4_NUM = 16,
    parameter TAP_NUM = CARRY4_NUM * 4,
    parameter BIN_W = 8
) (
    input  wire                 clk_i,
    input  wire                 rst_n_i,
    input  wire                 hit_i,
    output reg  [BIN_W-1:0]     bin_o,
    output reg                  sample_vld_o,
    output reg                  bubble_seen_o,
    output reg                  empty_o,
    output reg                  full_o
);

    wire [TAP_NUM-1:0] tap;
    wire [TAP_NUM-1:0] raw;
    wire [TAP_NUM-1:0] corr_next;
    wire [BIN_W-1:0] bin_next;
    wire sample_vld_raw;
    wire bubble_seen_next;
    wire empty_next;
    wire full_next;

    reg [TAP_NUM-1:0] corr_q;
    reg corr_vld_q;
    reg bubble_seen_q;

    carry4_tdc_chain #(
        .CARRY4_NUM(CARRY4_NUM),
        .TAP_NUM(TAP_NUM)
    ) u_chain (
        .hit_i(hit_i),
        .tap_o(tap)
    );

    tdc_sampler #(
        .TAP_NUM(TAP_NUM)
    ) u_sampler (
        .clk_i(clk_i),
        .rst_n_i(rst_n_i),
        .tap_i(tap),
        .thermo_raw_o(raw),
        .sample_vld_o(sample_vld_raw)
    );

    tdc_bubble_correct #(
        .TAP_NUM(TAP_NUM)
    ) u_bubble_correct (
        .thermo_raw_i(raw),
        .thermo_corr_o(corr_next),
        .bubble_seen_o(bubble_seen_next)
    );

    tdc_encoder #(
        .TAP_NUM(TAP_NUM),
        .BIN_W(BIN_W)
    ) u_encoder (
        .thermo_i(corr_q),
        .bin_o(bin_next),
        .empty_o(empty_next),
        .full_o(full_next)
    );

    always @(posedge clk_i or negedge rst_n_i) begin
        if (!rst_n_i) begin
            corr_q <= {TAP_NUM{1'b0}};
            corr_vld_q <= 1'b0;
            bubble_seen_q <= 1'b0;
            bin_o <= {BIN_W{1'b0}};
            sample_vld_o <= 1'b0;
            bubble_seen_o <= 1'b0;
            empty_o <= 1'b1;
            full_o <= 1'b0;
        end else begin
            corr_q <= corr_next;
            corr_vld_q <= sample_vld_raw;
            bubble_seen_q <= bubble_seen_next;
            bin_o <= bin_next;
            sample_vld_o <= corr_vld_q;
            bubble_seen_o <= bubble_seen_q;
            empty_o <= empty_next;
            full_o <= full_next;
        end
    end

endmodule
