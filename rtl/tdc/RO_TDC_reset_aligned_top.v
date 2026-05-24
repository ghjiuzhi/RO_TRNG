module RO_TDC_reset_aligned_top #(
    parameter CARRY4_NUM = 16,
    parameter TAP_NUM = CARRY4_NUM * 4,
    parameter BIN_W = 8,
    parameter RO_A_STAGES = 9,
    parameter RO_B_STAGES = 2,
    parameter PAIR_ID = 0,
    parameter FAMILY_ID = 0,
    parameter SAMPLE_DIV = 16'd5000,
    parameter START_DELAY_CYCLES = 64'd200000,
    parameter RO_ENABLE_DELAY_CYCLES = 64'd200000,
    parameter WARMUP_PACKETS = 32'd0,
    parameter CAPTURE_PACKETS = 32'd4096,
    parameter USE_POR_RESET = 0
) (
    input  wire sys_clk,
    input  wire por_n_i,
    output wire UART_TX_o
);

    localparam PKT_BYTES = 8;
    localparam HEADER_BYTES = 16;

    localparam ST_START_DELAY = 3'd0;
    localparam ST_HEADER = 3'd1;
    localparam ST_ENABLE_DELAY = 3'd2;
    localparam ST_STREAM = 3'd3;
    localparam ST_DONE = 3'd4;

    localparam SEND_NONE = 1'b0;
    localparam SEND_HEADER = 1'b0;
    localparam SEND_PACKET = 1'b1;

    localparam SEND_IDLE = 2'd0;
    localparam SEND_WAIT_ACCEPT = 2'd1;
    localparam SEND_WAIT_READY = 2'd2;

    wire locked;
    wire clk_200m;
    wire rst_n_200m;
    wire ro_a_clk;
    wire ro_b_clk;
    wire [BIN_W-1:0] bin_a;
    wire [BIN_W-1:0] bin_b;
    wire vld_a;
    wire vld_b;
    wire bubble_a;
    wire bubble_b;
    wire empty_a;
    wire empty_b;
    wire full_a;
    wire full_b;
    wire [7:0] flags;
    wire tx_ready;
    wire ext_reset;

    reg ro_enable;
    reg [2:0] state;
    reg [63:0] delay_cnt;
    reg [15:0] div_cnt;
    reg [15:0] seq;
    reg [31:0] coarse;
    reg [31:0] warmup_count;
    reg [31:0] capture_count;

    reg [15:0] pkt_seq;
    reg [31:0] pkt_coarse;
    reg [7:0] pkt_bin_a;
    reg [7:0] pkt_bin_b;
    reg [7:0] pkt_flags;

    reg send_active;
    reg send_kind;
    reg send_start;
    reg send_start_kind;
    reg [4:0] send_index;
    reg [1:0] send_state;
    reg [7:0] tx_data;
    reg tx_valid;
    reg send_done;
    reg [7:0] send_byte;
    reg header_started;

    assign ext_reset = USE_POR_RESET ? ~por_n_i : 1'b0;

    clk_wiz_0 u_clk_wiz_0 (
        .clk_out1(clk_200m),
        .reset(ext_reset),
        .locked(locked),
        .clk_in1(sys_clk)
    );

    proc_sys_reset_0 u_proc_sys_reset_0 (
        .slowest_sync_clk(clk_200m),
        .ext_reset_in(ext_reset),
        .aux_reset_in(1'b0),
        .mb_debug_sys_rst(1'b0),
        .dcm_locked(locked),
        .mb_reset(),
        .bus_struct_reset(),
        .peripheral_reset(),
        .interconnect_aresetn(),
        .peripheral_aresetn(rst_n_200m)
    );

    RO #(
        .RO_STAGES(RO_A_STAGES)
    ) u_ro_a (
        .en(ro_enable),
        .clk_o(ro_a_clk)
    );

    RO #(
        .RO_STAGES(RO_B_STAGES)
    ) u_ro_b (
        .en(ro_enable),
        .clk_o(ro_b_clk)
    );

    tdc_lane #(
        .CARRY4_NUM(CARRY4_NUM),
        .TAP_NUM(TAP_NUM),
        .BIN_W(BIN_W)
    ) u_tdc_a (
        .clk_i(clk_200m),
        .rst_n_i(rst_n_200m),
        .hit_i(ro_a_clk),
        .bin_o(bin_a),
        .sample_vld_o(vld_a),
        .bubble_seen_o(bubble_a),
        .empty_o(empty_a),
        .full_o(full_a)
    );

    tdc_lane #(
        .CARRY4_NUM(CARRY4_NUM),
        .TAP_NUM(TAP_NUM),
        .BIN_W(BIN_W)
    ) u_tdc_b (
        .clk_i(clk_200m),
        .rst_n_i(rst_n_200m),
        .hit_i(ro_b_clk),
        .bin_o(bin_b),
        .sample_vld_o(vld_b),
        .bubble_seen_o(bubble_b),
        .empty_o(empty_b),
        .full_o(full_b)
    );

    assign flags = {vld_a & vld_b, bubble_b, bubble_a, full_b, full_a, empty_b, empty_a, ro_enable};

    always @(*) begin
        if (send_kind == SEND_HEADER) begin
            case (send_index)
                5'd0: send_byte = 8'h54; // T
                5'd1: send_byte = 8'h44; // D
                5'd2: send_byte = 8'h43; // C
                5'd3: send_byte = 8'h52; // R
                5'd4: send_byte = 8'h01;
                5'd5: send_byte = PAIR_ID[7:0];
                5'd6: send_byte = PAIR_ID[15:8];
                5'd7: send_byte = FAMILY_ID[7:0];
                5'd8: send_byte = FAMILY_ID[15:8];
                5'd9: send_byte = WARMUP_PACKETS[7:0];
                5'd10: send_byte = WARMUP_PACKETS[15:8];
                5'd11: send_byte = CAPTURE_PACKETS[7:0];
                5'd12: send_byte = CAPTURE_PACKETS[15:8];
                5'd13: send_byte = SAMPLE_DIV[7:0];
                5'd14: send_byte = SAMPLE_DIV[15:8];
                5'd15: send_byte = 8'h52;
                default: send_byte = 8'd0;
            endcase
        end else begin
            case (send_index)
                5'd0: send_byte = 8'hA5;
                5'd1: send_byte = pkt_seq[7:0];
                5'd2: send_byte = pkt_seq[15:8];
                5'd3: send_byte = pkt_coarse[7:0];
                5'd4: send_byte = pkt_coarse[15:8];
                5'd5: send_byte = pkt_bin_a;
                5'd6: send_byte = pkt_bin_b;
                5'd7: send_byte = pkt_flags;
                default: send_byte = 8'd0;
            endcase
        end
    end

    always @(posedge clk_200m or negedge rst_n_200m) begin
        if (!rst_n_200m) begin
            send_active <= 1'b0;
            send_kind <= SEND_HEADER;
            send_index <= 5'd0;
            send_state <= SEND_IDLE;
            tx_data <= 8'd0;
            tx_valid <= 1'b0;
            send_done <= 1'b0;
        end else begin
            send_done <= 1'b0;

            if (!send_active && send_start) begin
                send_active <= 1'b1;
                send_kind <= send_start_kind;
                send_index <= 5'd0;
                send_state <= SEND_IDLE;
                tx_valid <= 1'b0;
            end else if (!send_active) begin
                tx_valid <= 1'b0;
                send_state <= SEND_IDLE;
            end else begin
                case (send_state)
                    SEND_IDLE: begin
                        tx_valid <= 1'b0;
                        if (tx_ready) begin
                            tx_data <= send_byte;
                            tx_valid <= 1'b1;
                            send_state <= SEND_WAIT_ACCEPT;
                        end
                    end
                    SEND_WAIT_ACCEPT: begin
                        tx_valid <= 1'b1;
                        if (!tx_ready) begin
                            tx_valid <= 1'b0;
                            if ((send_kind == SEND_HEADER && send_index == HEADER_BYTES-1) ||
                                (send_kind == SEND_PACKET && send_index == PKT_BYTES-1)) begin
                                send_active <= 1'b0;
                                send_index <= 5'd0;
                                send_state <= SEND_IDLE;
                                send_done <= 1'b1;
                            end else begin
                                send_index <= send_index + 1'b1;
                                send_state <= SEND_WAIT_READY;
                            end
                        end
                    end
                    SEND_WAIT_READY: begin
                        tx_valid <= 1'b0;
                        if (tx_ready) begin
                            tx_data <= send_byte;
                            tx_valid <= 1'b1;
                            send_state <= SEND_WAIT_ACCEPT;
                        end
                    end
                    default: begin
                        tx_valid <= 1'b0;
                        send_state <= SEND_IDLE;
                    end
                endcase
            end
        end
    end

    always @(posedge clk_200m or negedge rst_n_200m) begin
        if (!rst_n_200m) begin
            ro_enable <= 1'b0;
            state <= ST_START_DELAY;
            delay_cnt <= 64'd0;
            div_cnt <= 16'd0;
            seq <= 16'd0;
            coarse <= 32'd0;
            warmup_count <= 32'd0;
            capture_count <= 32'd0;
            pkt_seq <= 16'd0;
            pkt_coarse <= 32'd0;
            pkt_bin_a <= 8'd0;
            pkt_bin_b <= 8'd0;
            pkt_flags <= 8'd0;
            send_start <= 1'b0;
            send_start_kind <= SEND_HEADER;
            header_started <= 1'b0;
        end else begin
            coarse <= coarse + 1'b1;
            send_start <= 1'b0;

            case (state)
                ST_START_DELAY: begin
                    ro_enable <= 1'b0;
                    if (delay_cnt >= START_DELAY_CYCLES) begin
                        delay_cnt <= 64'd0;
                        state <= ST_HEADER;
                    end else begin
                        delay_cnt <= delay_cnt + 1'b1;
                    end
                end
                ST_HEADER: begin
                    ro_enable <= 1'b0;
                    if (!header_started && !send_active) begin
                        send_start_kind <= SEND_HEADER;
                        send_start <= 1'b1;
                        header_started <= 1'b1;
                    end else if (send_done) begin
                        delay_cnt <= 64'd0;
                        ro_enable <= 1'b1;
                        state <= ST_ENABLE_DELAY;
                    end
                end
                ST_ENABLE_DELAY: begin
                    ro_enable <= 1'b1;
                    if (delay_cnt >= RO_ENABLE_DELAY_CYCLES) begin
                        delay_cnt <= 64'd0;
                        div_cnt <= 16'd0;
                        state <= ST_STREAM;
                    end else begin
                        delay_cnt <= delay_cnt + 1'b1;
                    end
                end
                ST_STREAM: begin
                    ro_enable <= 1'b1;
                    if (capture_count >= CAPTURE_PACKETS) begin
                        state <= ST_DONE;
                    end else if (send_done) begin
                        capture_count <= capture_count + 1'b1;
                    end else if (!send_active) begin
                        if (div_cnt >= SAMPLE_DIV) begin
                            div_cnt <= 16'd0;
                            if (warmup_count < WARMUP_PACKETS) begin
                                warmup_count <= warmup_count + 1'b1;
                            end else begin
                                pkt_seq <= seq;
                                pkt_coarse <= coarse;
                                pkt_bin_a <= bin_a;
                                pkt_bin_b <= bin_b;
                                pkt_flags <= flags;
                                seq <= seq + 1'b1;
                                send_start_kind <= SEND_PACKET;
                                send_start <= 1'b1;
                            end
                        end else begin
                            div_cnt <= div_cnt + 1'b1;
                        end
                    end
                end
                ST_DONE: begin
                    ro_enable <= 1'b1;
                end
                default: begin
                    ro_enable <= 1'b0;
                    state <= ST_DONE;
                end
            endcase
        end
    end

    uart_tx #(
        .CLK_FRE(200),
        .BAUD_RATE(115200)
    ) u_uart_tx (
        .clk(clk_200m),
        .rst_n(rst_n_200m),
        .tx_data(tx_data),
        .tx_data_valid(tx_valid),
        .tx_data_ready(tx_ready),
        .tx_pin(UART_TX_o)
    );

endmodule
