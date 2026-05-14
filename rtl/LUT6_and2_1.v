module LUT6_and2_1(
    input  wire       i1,
    input  wire       i2,
    output wire       o
);

    (* DONT_TOUCH= "TRUE" *) LUT6 #(
        .INIT(64'h0000000000000008)  // Specify LUT Contents
    ) u_LUT6 (
        .O(o),   // LUT general output
        .I0(i1), // LUT input
        .I1(i2), // LUT input
        .I2(1'b0), // LUT input
        .I3(1'b0), // LUT input
        .I4(1'b0), // LUT input
        .I5(1'b0)  // LUT input
    );

endmodule