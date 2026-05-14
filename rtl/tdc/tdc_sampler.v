module tdc_sampler #(
    parameter TAP_NUM = 64
) (
    input  wire                 clk_i,
    input  wire                 rst_n_i,
    input  wire [TAP_NUM-1:0]   tap_i,
    output reg  [TAP_NUM-1:0]   thermo_raw_o,
    output reg                  sample_vld_o
);

    always @(posedge clk_i or negedge rst_n_i) begin
        if (!rst_n_i) begin
            thermo_raw_o <= {TAP_NUM{1'b0}};
            sample_vld_o <= 1'b0;
        end else begin
            thermo_raw_o <= tap_i;
            sample_vld_o <= 1'b1;
        end
    end

endmodule
