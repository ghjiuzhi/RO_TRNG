module bin_to_gray (
    input  [7:0] bin_in,
    output [7:0] gray_out
);

    assign gray_out[7] = bin_in[7];                        // MSB stays the same
    assign gray_out[6] = bin_in[7] ^ bin_in[6];
    assign gray_out[5] = bin_in[6] ^ bin_in[5];
    assign gray_out[4] = bin_in[5] ^ bin_in[4];
    assign gray_out[3] = bin_in[4] ^ bin_in[3];
    assign gray_out[2] = bin_in[3] ^ bin_in[2];
    assign gray_out[1] = bin_in[2] ^ bin_in[1];
    assign gray_out[0] = bin_in[1] ^ bin_in[0];

endmodule