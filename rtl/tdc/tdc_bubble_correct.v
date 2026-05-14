module tdc_bubble_correct #(
    parameter TAP_NUM = 64
) (
    input  wire [TAP_NUM-1:0]   thermo_raw_i,
    output wire [TAP_NUM-1:0]   thermo_corr_o,
    output reg                  bubble_seen_o
);

    reg [TAP_NUM-1:0] corr;
    integer i;

    always @(*) begin
        corr = thermo_raw_i;
        bubble_seen_o = 1'b0;
        for (i = 1; i < TAP_NUM-1; i = i + 1) begin
            corr[i] = (thermo_raw_i[i-1] & thermo_raw_i[i]) |
                      (thermo_raw_i[i-1] & thermo_raw_i[i+1]) |
                      (thermo_raw_i[i]   & thermo_raw_i[i+1]);
            if (thermo_raw_i[i-1] != thermo_raw_i[i+1]) begin
                bubble_seen_o = 1'b1;
            end
        end
    end

    assign thermo_corr_o = corr;

endmodule
