module tdc_ro_mask_matrix #(
    parameter RO_NUM = 8,
    parameter RO_STAGES = 2,
    parameter SAMPLE_STAGES = 9
) (
    input  wire [RO_NUM-1:0] data_en_i,
    input  wire              sample_en_i,
    output wire [RO_NUM-1:0] data_clk_o,
    output wire              sample_clk_o
);

    (* DONT_TOUCH = "TRUE" *) wire [RO_STAGES-1:0] ro_chain[RO_NUM-1:0];
    (* DONT_TOUCH = "TRUE" *) wire [SAMPLE_STAGES-1:0] ro_sample_chain;
    genvar i;
    genvar j;

    generate
        for (i = 0; i < RO_NUM; i = i + 1) begin : RO_NUM_LOOP
            if (RO_STAGES % 2 == 0) begin : RO_AND
                LUT6_and2_1 u_LUT6_and2_1 (
                    .i1(data_en_i[i]),
                    .i2(ro_chain[i][RO_STAGES-1]),
                    .o(ro_chain[i][0])
                );
            end else begin : RO_NAND
                LUT6_nand2_1 u_LUT6_nand2_1 (
                    .i1(data_en_i[i]),
                    .i2(ro_chain[i][RO_STAGES-1]),
                    .o(ro_chain[i][0])
                );
            end

            for (j = 0; j < RO_STAGES-1; j = j + 1) begin : RO_STAGE_LOOP
                LUT6_not1 u_LUT6_not1 (
                    .i1(ro_chain[i][j]),
                    .o(ro_chain[i][j+1])
                );
            end

            assign data_clk_o[i] = ro_chain[i][RO_STAGES-1];
        end
    endgenerate

    generate
        if (SAMPLE_STAGES % 2 == 0) begin : RO_SAMPLE_AND
            LUT6_and2_1 u_LUT6_and2_1 (
                .i1(sample_en_i),
                .i2(ro_sample_chain[SAMPLE_STAGES-1]),
                .o(ro_sample_chain[0])
            );
        end else begin : RO_SAMPLE_NAND
            LUT6_nand2_1 u_LUT6_nand2_1 (
                .i1(sample_en_i),
                .i2(ro_sample_chain[SAMPLE_STAGES-1]),
                .o(ro_sample_chain[0])
            );
        end

        for (i = 0; i < SAMPLE_STAGES-1; i = i + 1) begin : RO_SAMPLE_LOOP
            LUT6_not1 u_LUT6_not1 (
                .i1(ro_sample_chain[i]),
                .o(ro_sample_chain[i+1])
            );
        end
    endgenerate

    assign sample_clk_o = ro_sample_chain[SAMPLE_STAGES-1];

endmodule
