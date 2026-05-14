module tdc_uart_packetizer #(
    parameter SAMPLE_DIV = 16'd5000
) (
    input  wire         clk_i,
    input  wire         rst_n_i,
    input  wire [7:0]   bin_a_i,
    input  wire [7:0]   bin_b_i,
    input  wire [7:0]   flags_i,
    input  wire         tx_ready_i,
    output reg  [7:0]   tx_data_o,
    output reg          tx_valid_o
);

    localparam PKT_BYTES = 8;
    localparam SEND_IDLE = 2'd0;
    localparam SEND_WAIT_ACCEPT = 2'd1;
    localparam SEND_WAIT_READY = 2'd2;

    reg [15:0] div_cnt;
    reg [15:0] seq;
    reg [31:0] coarse;
    reg [15:0] pkt_seq;
    reg [31:0] pkt_coarse;
    reg [7:0] pkt_bin_a;
    reg [7:0] pkt_bin_b;
    reg [7:0] pkt_flags;
    reg [7:0] pkt_byte;
    reg [3:0] index;
    reg sending;
    reg [1:0] send_state;

    always @(*) begin
        case (index)
            4'd0: pkt_byte = 8'hA5;
            4'd1: pkt_byte = pkt_seq[7:0];
            4'd2: pkt_byte = pkt_seq[15:8];
            4'd3: pkt_byte = pkt_coarse[7:0];
            4'd4: pkt_byte = pkt_coarse[15:8];
            4'd5: pkt_byte = pkt_bin_a;
            4'd6: pkt_byte = pkt_bin_b;
            4'd7: pkt_byte = pkt_flags;
            default: pkt_byte = 8'd0;
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
            send_state <= SEND_IDLE;
            tx_data_o <= 8'd0;
            tx_valid_o <= 1'b0;
        end else begin
            coarse <= coarse + 1'b1;

            if (!sending) begin
                tx_valid_o <= 1'b0;
                send_state <= SEND_IDLE;
                if (div_cnt == SAMPLE_DIV) begin
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
            end else begin
                case (send_state)
                    SEND_IDLE: begin
                        tx_valid_o <= 1'b0;
                        if (tx_ready_i) begin
                            tx_data_o <= pkt_byte;
                            tx_valid_o <= 1'b1;
                            send_state <= SEND_WAIT_ACCEPT;
                        end
                    end
                    SEND_WAIT_ACCEPT: begin
                        tx_valid_o <= 1'b1;
                        if (!tx_ready_i) begin
                            tx_valid_o <= 1'b0;
                            if (index == PKT_BYTES-1) begin
                                sending <= 1'b0;
                                index <= 4'd0;
                                send_state <= SEND_IDLE;
                            end else begin
                                index <= index + 1'b1;
                                send_state <= SEND_WAIT_READY;
                            end
                        end
                    end
                    SEND_WAIT_READY: begin
                        tx_valid_o <= 1'b0;
                        if (tx_ready_i) begin
                            tx_data_o <= pkt_byte;
                            tx_valid_o <= 1'b1;
                            send_state <= SEND_WAIT_ACCEPT;
                        end
                    end
                    default: begin
                        tx_valid_o <= 1'b0;
                        send_state <= SEND_IDLE;
                    end
                endcase
            end
        end
    end

endmodule
