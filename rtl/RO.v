module RO #(
    parameter RO_STAGES = 1    // RO stages
)(
    input  wire        en,  // enable signal
    output wire        clk_o
);

    (* DONT_TOUCH= "TRUE" *) wire [RO_STAGES-1:0] ro_chain; // RO chain
    genvar j;

    // generate multiple high frequency RO
    generate
        // single RO
        if (RO_STAGES % 2 == 0) begin: RO_AND
            LUT6_and2_1 u_LUT6_and2_1(.i1(en), .i2(ro_chain[RO_STAGES-1]), .o(ro_chain[0]));
        end
        else begin: RO_NAND
            LUT6_nand2_1 u_LUT6_nand2_1(.i1(en), .i2(ro_chain[RO_STAGES-1]), .o(ro_chain[0]));
        end
        for (j = 0; j < RO_STAGES-1; j = j + 1) begin : RO_STAGE_LOOP
            LUT6_not1 u_LUT6_not1(.i1(ro_chain[j]), .o(ro_chain[j+1]));
        end
        // LUT6_nand2_1 u_LUT6_nand2_1(.i1(en), .i2(ro_chain[RO_STAGES-1]), .o(ro_chain[0]));
        // for (j = 0; j < RO_STAGES-2; j = j + 1) begin : RO_STAGE_LOOP
        //     LUT6_not1 u_LUT6_not1(.i1(ro_chain[j]), .o(ro_chain[j+1]));
        // end
        // if (RO_STAGES != 1) begin
        //     if (RO_STAGES % 2 == 0) begin
        //         LUT6_buf1 u_LUT6_buf1(.i1(ro_chain[RO_STAGES-2]), .o(ro_chain[RO_STAGES-1]));
        //     end
        //     else begin
        //         LUT6_not1 u_LUT6_not1(.i1(ro_chain[RO_STAGES-2]), .o(ro_chain[RO_STAGES-1]));
        //     end
        // end
    endgenerate

    assign clk_o = ro_chain[RO_STAGES-1];

endmodule