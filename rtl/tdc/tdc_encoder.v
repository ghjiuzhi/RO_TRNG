module tdc_encoder #(
    parameter TAP_NUM = 64,
    parameter BIN_W = 8
) (
    input  wire [TAP_NUM-1:0]   thermo_i,
    output reg  [BIN_W-1:0]     bin_o,
    output wire                 empty_o,
    output wire                 full_o
);

    integer i;
    reg [BIN_W-1:0] ones_count;

    always @(*) begin
        ones_count = {BIN_W{1'b0}};
        for (i = 0; i < TAP_NUM; i = i + 1) begin
            ones_count = ones_count + {{(BIN_W-1){1'b0}}, thermo_i[i]};
        end
        bin_o = ones_count;
    end

    assign empty_o = ~|thermo_i;
    assign full_o  = &thermo_i;

endmodule
