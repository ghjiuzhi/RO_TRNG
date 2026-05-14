module carry4_tdc_chain #(
    parameter CARRY4_NUM = 16,
    parameter TAP_NUM = CARRY4_NUM * 4
) (
    input  wire                 hit_i,
    output wire [TAP_NUM-1:0]   tap_o
);

    (* DONT_TOUCH = "TRUE" *) wire [TAP_NUM-1:0] carry_co;

    genvar i;
    generate
        for (i = 0; i < CARRY4_NUM; i = i + 1) begin : CARRY4_LOOP
            if (i == 0) begin : FIRST
                (* DONT_TOUCH = "TRUE" *) CARRY4 u_carry4 (
                    .CI     (1'b0),
                    .CYINIT (hit_i),
                    .DI     (4'b0000),
                    .S      (4'b1111),
                    .CO     (carry_co[3:0]),
                    .O      ()
                );
            end else begin : NEXT
                (* DONT_TOUCH = "TRUE" *) CARRY4 u_carry4 (
                    .CI     (carry_co[i*4-1]),
                    .CYINIT (1'b0),
                    .DI     (4'b0000),
                    .S      (4'b1111),
                    .CO     (carry_co[i*4 +: 4]),
                    .O      ()
                );
            end
        end
    endgenerate

    assign tap_o = carry_co;

endmodule
