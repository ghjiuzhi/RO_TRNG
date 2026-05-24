module RO_TRNG_restart_aligned_snapshot_top #(
    parameter RO_NUM = 8,
    parameter RO_STAGES = 2,
    parameter SAMPLE_STAGES = 9,
    parameter WARMUP_SNAPSHOTS = 0,
    parameter CAPTURE_SNAPSHOTS = 1024,
    parameter HOLD_CYCLES = 32'd200000,
    parameter SETTLE_CYCLES = 32'd200000,
    parameter START_DELAY_CYCLES = 64'd16000000000,
    parameter VARIANT_ID = 16'h5201
) (
    input  wire sys_clk,
    input  wire por_n_i,
    output wire UART_TX_o
);

    localparam SAMPLE_BITS = RO_NUM * (SAMPLE_STAGES - 1);
    localparam SAMPLE_BYTES = SAMPLE_BITS / 8;
    localparam CAPTURE_ADDR_W = (CAPTURE_SNAPSHOTS <= 2) ? 1 : $clog2(CAPTURE_SNAPSHOTS);
    localparam HEADER_BYTES = 16;
    localparam FRAME_BYTES = 16;

    localparam ST_START_DELAY = 4'd0;
    localparam ST_HOLD = 4'd1;
    localparam ST_SETTLE = 4'd2;
    localparam ST_CAPTURE = 4'd3;
    localparam ST_WAIT_CAPTURE = 4'd4;
    localparam ST_STOP_ROW = 4'd5;
    localparam ST_HEADER = 4'd6;
    localparam ST_LOAD_FRAME = 4'd7;
    localparam ST_SEND = 4'd8;
    localparam ST_DONE = 4'd9;

    localparam SEND_IDLE = 2'd0;
    localparam SEND_WAIT_ACCEPT = 2'd1;
    localparam SEND_WAIT_READY = 2'd2;

    wire locked;
    wire clk_200m;
    wire rst_n_200m;
    wire rand_clk;
    wire rand_bit;
    wire [SAMPLE_BITS-1:0] sampled_data;
    wire [SAMPLE_STAGES-2:0] stage_xor;
    wire tx_ready;
    wire [127:0] bram_dout;

    reg ro_en;
    reg [3:0] state;
    reg [1:0] send_state;
    reg [63:0] delay_cnt;
    reg [31:0] state_count;
    reg [31:0] warmup_count;
    reg [31:0] capture_count;
    reg [31:0] row_index;
    reg [31:0] frame_index;
    reg [CAPTURE_ADDR_W-1:0] read_addr;
    reg [CAPTURE_ADDR_W-1:0] write_addr;
    reg [4:0] byte_index;
    reg [7:0] tx_data;
    reg tx_valid;
    reg [7:0] send_byte;
    reg [127:0] read_frame;
    reg [127:0] write_frame;
    reg write_enable;
    reg capture_done_rand;
    reg capture_pending;
    reg capture_ack_200m;
    reg capture_ack_sync1;
    reg capture_ack_sync2;
    reg capture_ack_sync3;
    reg capture_done_sync1;
    reg capture_done_sync2;
    reg capture_done_seen;

    clk_wiz_0 u_clk_wiz_0 (
        .clk_out1(clk_200m),
        .reset(~por_n_i),
        .locked(locked),
        .clk_in1(sys_clk)
    );

    proc_sys_reset_0 u_proc_sys_reset_0 (
        .slowest_sync_clk(clk_200m),
        .ext_reset_in(~por_n_i),
        .aux_reset_in(1'b0),
        .mb_debug_sys_rst(1'b0),
        .dcm_locked(locked),
        .mb_reset(),
        .bus_struct_reset(),
        .peripheral_reset(),
        .interconnect_aresetn(),
        .peripheral_aresetn(rst_n_200m)
    );

    entropy_source_probe #(
        .RO_NUM(RO_NUM),
        .RO_STAGES(RO_STAGES),
        .SAMPLE_STAGES(SAMPLE_STAGES)
    ) u_entropy_source (
        .en(ro_en),
        .rand_bit(rand_bit),
        .clk_o(rand_clk),
        .sampled_data_o(sampled_data),
        .stage_xor_o(stage_xor)
    );

    xpm_memory_sdpram #(
        .ADDR_WIDTH_A(CAPTURE_ADDR_W),
        .ADDR_WIDTH_B(CAPTURE_ADDR_W),
        .AUTO_SLEEP_TIME(0),
        .BYTE_WRITE_WIDTH_A(128),
        .CASCADE_HEIGHT(0),
        .CLOCKING_MODE("independent_clock"),
        .ECC_MODE("no_ecc"),
        .MEMORY_INIT_FILE("none"),
        .MEMORY_INIT_PARAM("0"),
        .MEMORY_OPTIMIZATION("true"),
        .MEMORY_PRIMITIVE("block"),
        .MEMORY_SIZE(CAPTURE_SNAPSHOTS * 128),
        .MESSAGE_CONTROL(0),
        .READ_DATA_WIDTH_B(128),
        .READ_LATENCY_B(2),
        .READ_RESET_VALUE_B("0"),
        .RST_MODE_A("SYNC"),
        .RST_MODE_B("SYNC"),
        .USE_EMBEDDED_CONSTRAINT(0),
        .USE_MEM_INIT(0),
        .WAKEUP_TIME("disable_sleep"),
        .WRITE_DATA_WIDTH_A(128),
        .WRITE_MODE_B("read_first")
    ) u_snapshot_bram (
        .dbiterrb(),
        .doutb(bram_dout),
        .sbiterrb(),
        .addra(write_addr),
        .addrb(read_addr),
        .clka(rand_clk),
        .clkb(clk_200m),
        .dina(write_frame),
        .ena(1'b1),
        .enb(1'b1),
        .injectdbiterra(1'b0),
        .injectsbiterra(1'b0),
        .regceb(1'b1),
        .rstb(~rst_n_200m),
        .sleep(1'b0),
        .wea(write_enable)
    );

    always @(posedge rand_clk or negedge rst_n_200m) begin
        if (!rst_n_200m) begin
            warmup_count <= 32'd0;
            write_enable <= 1'b0;
            write_addr <= {CAPTURE_ADDR_W{1'b0}};
            write_frame <= 128'd0;
            capture_done_rand <= 1'b0;
            capture_pending <= 1'b0;
            capture_ack_sync1 <= 1'b0;
            capture_ack_sync2 <= 1'b0;
            capture_ack_sync3 <= 1'b0;
        end else begin
            capture_ack_sync1 <= capture_ack_200m;
            capture_ack_sync2 <= capture_ack_sync1;
            capture_ack_sync3 <= capture_ack_sync2;
            write_enable <= 1'b0;

            if (!ro_en) begin
                warmup_count <= 32'd0;
                capture_pending <= 1'b0;
                capture_done_rand <= 1'b0;
            end else if (capture_ack_sync2 != capture_ack_sync3) begin
                capture_pending <= 1'b0;
                capture_done_rand <= 1'b0;
            end else if (!capture_pending) begin
                if (warmup_count < WARMUP_SNAPSHOTS) begin
                    warmup_count <= warmup_count + 1'b1;
                end else begin
                    write_addr <= row_index[CAPTURE_ADDR_W-1:0];
                    write_frame <= {
                        8'ha5,
                        16'h0000,
                        sampled_data,
                        stage_xor,
                        {7'd0, rand_bit},
                        row_index[15:0],
                        8'h5a
                    };
                    write_enable <= 1'b1;
                    capture_pending <= 1'b1;
                    capture_done_rand <= 1'b1;
                end
            end
        end
    end

    always @(*) begin
        if (state == ST_HEADER) begin
            case (byte_index)
                5'd0: send_byte = 8'h53; // S
                5'd1: send_byte = 8'h4e; // N
                5'd2: send_byte = 8'h41; // A
                5'd3: send_byte = 8'h50; // P
                5'd4: send_byte = 8'h02;
                5'd5: send_byte = VARIANT_ID[7:0];
                5'd6: send_byte = VARIANT_ID[15:8];
                5'd7: send_byte = WARMUP_SNAPSHOTS[7:0];
                5'd8: send_byte = WARMUP_SNAPSHOTS[15:8];
                5'd9: send_byte = CAPTURE_SNAPSHOTS[7:0];
                5'd10: send_byte = CAPTURE_SNAPSHOTS[15:8];
                5'd11: send_byte = SAMPLE_BYTES[7:0];
                5'd12: send_byte = RO_NUM[7:0];
                5'd13: send_byte = SAMPLE_STAGES[7:0];
                5'd14: send_byte = 8'h55;
                5'd15: send_byte = 8'haa;
                default: send_byte = 8'd0;
            endcase
        end else begin
            case (byte_index)
                5'd0: send_byte = read_frame[7:0];
                5'd1: send_byte = read_frame[15:8];
                5'd2: send_byte = read_frame[23:16];
                5'd3: send_byte = read_frame[31:24];
                5'd4: send_byte = read_frame[39:32];
                5'd5: send_byte = read_frame[47:40];
                5'd6: send_byte = read_frame[55:48];
                5'd7: send_byte = read_frame[63:56];
                5'd8: send_byte = read_frame[71:64];
                5'd9: send_byte = read_frame[79:72];
                5'd10: send_byte = read_frame[87:80];
                5'd11: send_byte = read_frame[95:88];
                5'd12: send_byte = read_frame[103:96];
                5'd13: send_byte = read_frame[111:104];
                5'd14: send_byte = read_frame[119:112];
                5'd15: send_byte = read_frame[127:120];
                default: send_byte = 8'd0;
            endcase
        end
    end

    always @(posedge clk_200m or negedge rst_n_200m) begin
        if (!rst_n_200m) begin
            capture_done_sync1 <= 1'b0;
            capture_done_sync2 <= 1'b0;
            read_frame <= 128'd0;
        end else begin
            capture_done_sync1 <= capture_done_rand;
            capture_done_sync2 <= capture_done_sync1;
            read_frame <= bram_dout;
        end
    end

    always @(posedge clk_200m or negedge rst_n_200m) begin
        if (!rst_n_200m) begin
            ro_en <= 1'b0;
            state <= ST_START_DELAY;
            send_state <= SEND_IDLE;
            delay_cnt <= 64'd0;
            state_count <= 32'd0;
            capture_count <= 32'd0;
            row_index <= 32'd0;
            frame_index <= 32'd0;
            read_addr <= {CAPTURE_ADDR_W{1'b0}};
            byte_index <= 5'd0;
            tx_data <= 8'd0;
            tx_valid <= 1'b0;
            capture_ack_200m <= 1'b0;
            capture_done_seen <= 1'b0;
        end else begin
            tx_valid <= 1'b0;
            case (state)
                ST_START_DELAY: begin
                    ro_en <= 1'b0;
                    if (delay_cnt >= START_DELAY_CYCLES) begin
                        delay_cnt <= 64'd0;
                        state <= ST_HOLD;
                    end else begin
                        delay_cnt <= delay_cnt + 1'b1;
                    end
                end

                ST_HOLD: begin
                    ro_en <= 1'b0;
                    capture_done_seen <= 1'b0;
                    if (state_count >= HOLD_CYCLES) begin
                        state_count <= 32'd0;
                        state <= ST_SETTLE;
                    end else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_SETTLE: begin
                    ro_en <= 1'b1;
                    if (state_count >= SETTLE_CYCLES) begin
                        state_count <= 32'd0;
                        state <= ST_CAPTURE;
                    end else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_CAPTURE: begin
                    ro_en <= 1'b1;
                    if (capture_done_sync2 && !capture_done_seen) begin
                        capture_done_seen <= 1'b1;
                        capture_ack_200m <= ~capture_ack_200m;
                        capture_count <= capture_count + 1'b1;
                        state <= ST_STOP_ROW;
                    end
                end

                ST_STOP_ROW: begin
                    ro_en <= 1'b0;
                    if (row_index + 1'b1 >= CAPTURE_SNAPSHOTS) begin
                        row_index <= 32'd0;
                        read_addr <= {CAPTURE_ADDR_W{1'b0}};
                        byte_index <= 5'd0;
                        send_state <= SEND_IDLE;
                        state <= ST_HEADER;
                    end else begin
                        row_index <= row_index + 1'b1;
                        state <= ST_HOLD;
                    end
                end

                ST_LOAD_FRAME: begin
                    ro_en <= 1'b0;
                    byte_index <= 5'd0;
                    send_state <= SEND_IDLE;
                    state <= ST_SEND;
                end

                ST_HEADER, ST_SEND: begin
                    ro_en <= 1'b0;
                    case (send_state)
                        SEND_IDLE: begin
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
                                if (byte_index == HEADER_BYTES - 1) begin
                                    byte_index <= 5'd0;
                                    send_state <= SEND_IDLE;
                                    if (state == ST_HEADER) begin
                                        frame_index <= 32'd0;
                                        read_addr <= {CAPTURE_ADDR_W{1'b0}};
                                        state <= ST_LOAD_FRAME;
                                    end else if (frame_index == CAPTURE_SNAPSHOTS - 1) begin
                                        state <= ST_DONE;
                                    end else begin
                                        frame_index <= frame_index + 1'b1;
                                        read_addr <= frame_index[CAPTURE_ADDR_W-1:0] + 1'b1;
                                        state <= ST_LOAD_FRAME;
                                    end
                                end else begin
                                    byte_index <= byte_index + 1'b1;
                                    send_state <= SEND_WAIT_READY;
                                end
                            end
                        end
                        SEND_WAIT_READY: begin
                            if (tx_ready) begin
                                tx_data <= send_byte;
                                tx_valid <= 1'b1;
                                send_state <= SEND_WAIT_ACCEPT;
                            end
                        end
                        default: send_state <= SEND_IDLE;
                    endcase
                end

                ST_DONE: begin
                    ro_en <= 1'b0;
                    tx_valid <= 1'b0;
                end

                default: begin
                    ro_en <= 1'b0;
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
