module entropy_source_probe #(
    parameter RO_NUM = 8,
    parameter RO_STAGES = 2,
    parameter SAMPLE_STAGES = 9
)(
    input  wire                                en,
    output reg                                 rand_bit,
    output wire                                clk_o,
    output wire [RO_NUM*(SAMPLE_STAGES-1)-1:0] sampled_data_o,
    output wire [SAMPLE_STAGES-2:0]            stage_xor_o
);

    (* DONT_TOUCH= "TRUE" *) wire [RO_STAGES-1:0] ro_chain[RO_NUM-1:0];
    (* DONT_TOUCH= "TRUE" *) wire [SAMPLE_STAGES-1:0] ro_sample_chain;
    (* DONT_TOUCH= "TRUE" *) reg  [RO_NUM*(SAMPLE_STAGES-1)-1:0] sampled_data;
    genvar i, j;

    generate
        for (i = 0; i < RO_NUM; i = i + 1) begin : RO_NUM_LOOP
            if (RO_STAGES % 2 == 0) begin: RO_AND
                LUT6_and2_1 u_LUT6_and2_1(.i1(en), .i2(ro_chain[i][RO_STAGES-1]), .o(ro_chain[i][0]));
            end
            else begin: RO_NAND
                LUT6_nand2_1 u_LUT6_nand2_1(.i1(en), .i2(ro_chain[i][RO_STAGES-1]), .o(ro_chain[i][0]));
            end
            for (j = 0; j < RO_STAGES-1; j = j + 1) begin : RO_STAGE_LOOP
                LUT6_not1 u_LUT6_not1(.i1(ro_chain[i][j]), .o(ro_chain[i][j+1]));
            end
        end
    endgenerate

    generate
        if (SAMPLE_STAGES % 2 == 0) begin: RO_SAMPLE_AND
            LUT6_and2_1 u_LUT6_and2_1(.i1(en), .i2(ro_sample_chain[SAMPLE_STAGES-1]), .o(ro_sample_chain[0]));
        end
        else begin: RO_SAMPLE_NAND
            LUT6_nand2_1 u_LUT6_nand2_1(.i1(en), .i2(ro_sample_chain[SAMPLE_STAGES-1]), .o(ro_sample_chain[0]));
        end
        for (i = 0; i < SAMPLE_STAGES-1; i = i + 1) begin : RO_SAMPLE_LOOP
            LUT6_not1 u_LUT6_not1(.i1(ro_sample_chain[i]), .o(ro_sample_chain[i+1]));
        end
    endgenerate

    generate
        for (i = 0; i < SAMPLE_STAGES-1; i = i + 1) begin : SAMPLE_DATA_LINE_LOOP
            for (j = 0; j < RO_NUM; j = j + 1) begin : SAMPLE_DATA_BIT_LOOP
                always @(posedge ro_sample_chain[i]) begin
                    sampled_data[i*RO_NUM+j] <= ro_chain[j][RO_STAGES-1];
                end
            end
            assign stage_xor_o[i] = ^sampled_data[i*RO_NUM +: RO_NUM];
        end
    endgenerate

    always @(posedge ro_sample_chain[SAMPLE_STAGES-1]) begin
        rand_bit <= ^sampled_data;
    end

    assign sampled_data_o = sampled_data;

    BUFG u_BUFG (
        .O(clk_o),
        .I(ro_sample_chain[SAMPLE_STAGES-1])
    );

endmodule
