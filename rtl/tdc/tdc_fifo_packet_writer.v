module tdc_fifo_packet_writer #(
    parameter SAMPLE_DIV = 16'd5000
) (
    input  wire       clk_i,
    input  wire       rst_n_i,
    input  wire [7:0] bin_a_i,
    input  wire [7:0] bin_b_i,
    input  wire [7:0] flags_i,
    input  wire       fifo_full_i,
    output reg  [7:0] fifo_din_o,
    output reg        fifo_wr_en_o
);

    localparam PKT_BYTES = 8;

    reg [15:0] div_cnt;
    reg [15:0] seq;
    reg [31:0] coarse;
    reg [15:0] pkt_seq;
    reg [31:0] pkt_coarse;
    reg [7:0] pkt_bin_a;
    reg [7:0] pkt_bin_b;
    reg [7:0] pkt_flags;
    reg [3:0] index;
    reg sending;

    always @(*) begin
        case (index)
            4'd0: fifo_din_o = 8'hA5;
            4'd1: fifo_din_o = pkt_seq[7:0];
            4'd2: fifo_din_o = pkt_seq[15:8];
            4'd3: fifo_din_o = pkt_coarse[7:0];
            4'd4: fifo_din_o = pkt_coarse[15:8];
            4'd5: fifo_din_o = pkt_bin_a;
            4'd6: fifo_din_o = pkt_bin_b;
            4'd7: fifo_din_o = pkt_flags;
            default: fifo_din_o = 8'd0;
        endcase
    end

    always @(posedge clk_i or negedge rst_n_i) begin
        if (!rst_n_i) begin
            div_cnt <= 16'd0;
            seq <= 16'd0;
            coarse <= 32'd0;
            pkt_seq <= 16'd0;
            pkt_coarse <= 32'd0;
            pkt_bin_a <= 8'd0;
            pkt_bin_b <= 8'd0;
            pkt_flags <= 8'd0;
            index <= 4'd0;
            sending <= 1'b0;
            fifo_wr_en_o <= 1'b0;
        end else begin
            coarse <= coarse + 1'b1;
            fifo_wr_en_o <= 1'b0;

            if (sending) begin
                if (!fifo_full_i) begin
                    fifo_wr_en_o <= 1'b1;
                    if (index == PKT_BYTES - 1) begin
                        index <= 4'd0;
                        sending <= 1'b0;
                    end else begin
                        index <= index + 1'b1;
                    end
                end
            end else if (div_cnt == SAMPLE_DIV) begin
                div_cnt <= 16'd0;
                seq <= seq + 1'b1;
                pkt_seq <= seq;
                pkt_coarse <= coarse;
                pkt_bin_a <= bin_a_i;
                pkt_bin_b <= bin_b_i;
                pkt_flags <= flags_i;
                index <= 4'd0;
                sending <= 1'b1;
            end else begin
                div_cnt <= div_cnt + 1'b1;
            end
        end
    end

endmodule
