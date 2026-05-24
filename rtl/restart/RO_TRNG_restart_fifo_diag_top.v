module RO_TRNG_restart_fifo_diag_top #(
    parameter RESTART_COUNT = 1000,
    parameter ROW_BYTES     = 32,
    parameter HOLD_CYCLES   = 32'd200000,
    parameter SETTLE_CYCLES = 32'd200000,
    parameter [63:0] START_DELAY_CYCLES = 64'd0,
    parameter DEBUG_HEADER   = 1,
    parameter WARMUP_BYTES  = 0,
    parameter RO_NUM        = 8,
    parameter RO_STAGES     = 2,
    parameter SAMPLE_STAGES = 9,
    parameter PRE_WARMUP_BYTES = 4,
    parameter UART_BYTE_CYCLES = 32'd17362
) (
    input  wire sys_clk,
    input  wire por_n_i,
    output wire UART_TX_o
);

    localparam ST_START_WAIT = 4'd0;
    localparam ST_HEADER     = 4'd1;
    localparam ST_HOLD       = 4'd2;
    localparam ST_DRAIN      = 4'd3;
    localparam ST_SETTLE     = 4'd4;
    localparam ST_WARMUP     = 4'd5;
    localparam ST_SEND       = 4'd6;
    localparam ST_LOAD_FRAME = 4'd7;
    localparam ST_UART_SEND  = 4'd8;
    localparam ST_DONE       = 4'd9;

    localparam PHASE_WARMUP = 8'h01;
    localparam PHASE_SEND   = 8'h02;
    localparam HEADER_BYTES = 16;
    localparam FRAME_BYTES = 16;
    localparam TOTAL_FRAMES =
        RESTART_COUNT * (ROW_BYTES + ((WARMUP_BYTES < PRE_WARMUP_BYTES) ? WARMUP_BYTES : PRE_WARMUP_BYTES));
    localparam ADDR_W = (TOTAL_FRAMES <= 2) ? 1 : $clog2(TOTAL_FRAMES);
    localparam [63:0] START_DELAY_LAST =
        (START_DELAY_CYCLES <= 1) ? 64'd0 : START_DELAY_CYCLES - 1;
    localparam [31:0] HOLD_LAST =
        (HOLD_CYCLES <= 1) ? 32'd0 : HOLD_CYCLES - 1;
    localparam [31:0] SETTLE_LAST =
        (SETTLE_CYCLES <= 1) ? 32'd0 : SETTLE_CYCLES - 1;
    localparam [31:0] UART_BYTE_LAST =
        (UART_BYTE_CYCLES <= 1) ? 32'd0 : UART_BYTE_CYCLES - 1;
    localparam [31:0] WARMUP_CAPTURE_START =
        (WARMUP_BYTES > PRE_WARMUP_BYTES) ? (WARMUP_BYTES - PRE_WARMUP_BYTES) : 0;

    wire       rand_bit;
    wire       rand_clk;
    wire       locked;
    wire       clk_200m;
    wire       rst_n_200m;
    wire       fifo_full;
    wire       fifo_empty;
    wire       tx_ready;
    wire [7:0] fifo_dout;
    wire [127:0] bram_dout;

    reg        ro_en;
    reg  [3:0] state;
    reg [63:0] state_count;
    reg [31:0] row_index;
    reg [31:0] warmup_count;
    reg [31:0] send_count;
    reg [31:0] frame_index;
    reg [31:0] virtual_uart_count;
    reg [ADDR_W-1:0] write_addr;
    reg [ADDR_W-1:0] read_addr;
    reg [127:0] write_frame;
    reg [127:0] read_frame;
    reg write_enable;
    reg [4:0] byte_index;
    reg [7:0] tx_data;
    reg tx_valid;
    reg [7:0] send_byte;
    reg [1:0] send_state;

    wire do_drain = (state == ST_DRAIN) && ~fifo_empty;
    wire virtual_uart_ready = (virtual_uart_count >= UART_BYTE_LAST);
    wire do_warmup = (state == ST_WARMUP) && ~fifo_empty && (warmup_count < WARMUP_BYTES);
    wire do_send = (state == ST_SEND) && virtual_uart_ready && ~fifo_empty;
    wire fifo_wr_en = ro_en & ~fifo_full;
    wire fifo_rd_en = do_drain | do_warmup | do_send;
    wire capture_warmup = do_warmup && (warmup_count >= WARMUP_CAPTURE_START);
    wire capture_send = do_send && (send_count < ROW_BYTES);
    wire capture_event = capture_warmup | capture_send;
    wire [31:0] event_index = capture_warmup ? warmup_count : send_count;
    wire [7:0] event_phase = capture_warmup ? PHASE_WARMUP : PHASE_SEND;

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

    entropy_source #(
        .RO_NUM(RO_NUM),
        .RO_STAGES(RO_STAGES),
        .SAMPLE_STAGES(SAMPLE_STAGES)
    ) u_entropy_source (
        .en(ro_en),
        .rand_bit(rand_bit),
        .clk_o(rand_clk)
    );

    fifo_generator_0 u_fifo_generator_0 (
        .wr_clk(rand_clk),
        .rd_clk(clk_200m),
        .din(rand_bit),
        .wr_en(fifo_wr_en),
        .rd_en(fifo_rd_en),
        .dout(fifo_dout),
        .full(fifo_full),
        .empty(fifo_empty)
    );

    xpm_memory_sdpram #(
        .ADDR_WIDTH_A(ADDR_W),
        .ADDR_WIDTH_B(ADDR_W),
        .AUTO_SLEEP_TIME(0),
        .BYTE_WRITE_WIDTH_A(128),
        .CLOCKING_MODE("common_clock"),
        .ECC_MODE("no_ecc"),
        .MEMORY_INIT_FILE("none"),
        .MEMORY_INIT_PARAM("0"),
        .MEMORY_OPTIMIZATION("true"),
        .MEMORY_PRIMITIVE("block"),
        .MEMORY_SIZE(TOTAL_FRAMES * 128),
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
    ) u_diag_bram (
        .dbiterrb(),
        .doutb(bram_dout),
        .sbiterrb(),
        .addra(write_addr),
        .addrb(read_addr),
        .clka(clk_200m),
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

    always @(*) begin
        if (state == ST_HEADER) begin
            case (byte_index)
                5'd0: send_byte = 8'h46;
                5'd1: send_byte = 8'h44;
                5'd2: send_byte = 8'h49;
                5'd3: send_byte = 8'h41;
                5'd4: send_byte = 8'h03;
                5'd5: send_byte = RESTART_COUNT[7:0];
                5'd6: send_byte = RESTART_COUNT[15:8];
                5'd7: send_byte = ROW_BYTES[7:0];
                5'd8: send_byte = ROW_BYTES[15:8];
                5'd9: send_byte = WARMUP_BYTES[7:0];
                5'd10: send_byte = WARMUP_BYTES[15:8];
                5'd11: send_byte = PRE_WARMUP_BYTES[7:0];
                5'd12: send_byte = PRE_WARMUP_BYTES[15:8];
                5'd13: send_byte = TOTAL_FRAMES[7:0];
                5'd14: send_byte = TOTAL_FRAMES[15:8];
                5'd15: send_byte = 8'haa;
                default: send_byte = 8'h00;
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
                default: send_byte = 8'h00;
            endcase
        end
    end

    always @(posedge clk_200m) begin
        if (~rst_n_200m) begin
            read_frame <= 128'd0;
        end else begin
            read_frame <= bram_dout;
        end
    end

    always @(posedge clk_200m) begin
        if (~rst_n_200m) begin
            ro_en <= 1'b0;
            state <= ST_START_WAIT;
            state_count <= 64'd0;
            row_index <= 32'd0;
            warmup_count <= 32'd0;
            send_count <= 32'd0;
            frame_index <= 32'd0;
            virtual_uart_count <= 32'd0;
            write_addr <= {ADDR_W{1'b0}};
            read_addr <= {ADDR_W{1'b0}};
            write_frame <= 128'd0;
            write_enable <= 1'b0;
            byte_index <= 5'd0;
            tx_data <= 8'd0;
            tx_valid <= 1'b0;
            send_state <= 2'd0;
        end else begin
            write_enable <= 1'b0;
            tx_valid <= 1'b0;

            case (state)
                ST_START_WAIT: begin
                    ro_en <= 1'b0;
                    row_index <= 32'd0;
                    warmup_count <= 32'd0;
                    send_count <= 32'd0;
                    frame_index <= 32'd0;
                    virtual_uart_count <= 32'd0;
                    write_addr <= {ADDR_W{1'b0}};
                    read_addr <= {ADDR_W{1'b0}};
                    byte_index <= 5'd0;
                    send_state <= 2'd0;
                    if (START_DELAY_CYCLES == 0 || state_count >= START_DELAY_LAST) begin
                        state_count <= 64'd0;
                        state <= ST_HOLD;
                    end else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_HOLD: begin
                    ro_en <= 1'b0;
                    warmup_count <= 32'd0;
                    send_count <= 32'd0;
                    virtual_uart_count <= 32'd0;
                    if (HOLD_CYCLES == 0 || state_count >= HOLD_LAST) begin
                        state_count <= 64'd0;
                        state <= ST_DRAIN;
                    end else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_DRAIN: begin
                    ro_en <= 1'b0;
                    state_count <= 64'd0;
                    if (fifo_empty) begin
                        if (row_index >= RESTART_COUNT) begin
                            state <= ST_HEADER;
                            read_addr <= {ADDR_W{1'b0}};
                            byte_index <= 5'd0;
                            send_state <= 2'd0;
                        end else begin
                            state <= ST_SETTLE;
                        end
                    end
                end

                ST_SETTLE: begin
                    ro_en <= 1'b1;
                    warmup_count <= 32'd0;
                    send_count <= 32'd0;
                    virtual_uart_count <= 32'd0;
                    if (SETTLE_CYCLES == 0 || state_count >= SETTLE_LAST) begin
                        state_count <= 64'd0;
                        if (WARMUP_BYTES == 0) begin
                            state <= ST_SEND;
                        end else begin
                            state <= ST_WARMUP;
                        end
                    end else begin
                        state_count <= state_count + 1'b1;
                    end
                end

                ST_WARMUP: begin
                    ro_en <= 1'b1;
                    virtual_uart_count <= 32'd0;
                    if (do_warmup) begin
                        if (capture_warmup) begin
                            write_addr <= frame_index[ADDR_W-1:0];
                            write_frame <= {
                                8'ha5,
                                {5'd0, fifo_full, fifo_empty, ro_en},
                                fifo_dout,
                                event_index[15:0],
                                event_phase,
                                row_index[15:0],
                                56'd0,
                                8'h5a
                            };
                            write_enable <= 1'b1;
                            frame_index <= frame_index + 1'b1;
                        end
                        if (warmup_count >= WARMUP_BYTES - 1) begin
                            warmup_count <= 32'd0;
                            state <= ST_SEND;
                        end else begin
                            warmup_count <= warmup_count + 1'b1;
                        end
                    end
                end

                ST_SEND: begin
                    ro_en <= 1'b1;
                    if (!virtual_uart_ready) begin
                        virtual_uart_count <= virtual_uart_count + 1'b1;
                    end else if (do_send) begin
                        virtual_uart_count <= 32'd0;
                        if (capture_send) begin
                            write_addr <= frame_index[ADDR_W-1:0];
                            write_frame <= {
                                8'ha5,
                                {5'd0, fifo_full, fifo_empty, ro_en},
                                fifo_dout,
                                event_index[15:0],
                                event_phase,
                                row_index[15:0],
                                56'd0,
                                8'h5a
                            };
                            write_enable <= 1'b1;
                            frame_index <= frame_index + 1'b1;
                        end
                        if (send_count >= ROW_BYTES - 1) begin
                            ro_en <= 1'b0;
                            send_count <= 32'd0;
                            virtual_uart_count <= 32'd0;
                            row_index <= row_index + 1'b1;
                            state_count <= 64'd0;
                            if (row_index + 1'b1 >= RESTART_COUNT) begin
                                state <= ST_HEADER;
                                read_addr <= {ADDR_W{1'b0}};
                                byte_index <= 5'd0;
                                send_state <= 2'd0;
                            end else begin
                                state <= ST_HOLD;
                            end
                        end else begin
                            send_count <= send_count + 1'b1;
                        end
                    end
                end

                ST_HEADER, ST_UART_SEND: begin
                    ro_en <= 1'b0;
                    case (send_state)
                        2'd0: begin
                            if (tx_ready) begin
                                tx_data <= send_byte;
                                tx_valid <= 1'b1;
                                send_state <= 2'd1;
                            end
                        end
                        2'd1: begin
                            tx_valid <= 1'b1;
                            if (!tx_ready) begin
                                tx_valid <= 1'b0;
                                if (byte_index == FRAME_BYTES - 1) begin
                                    byte_index <= 5'd0;
                                    send_state <= 2'd0;
                                    if (state == ST_HEADER) begin
                                        state <= ST_LOAD_FRAME;
                                        frame_index <= 32'd0;
                                        read_addr <= {ADDR_W{1'b0}};
                                    end else if (frame_index == TOTAL_FRAMES - 1) begin
                                        state <= ST_DONE;
                                    end else begin
                                        frame_index <= frame_index + 1'b1;
                                        read_addr <= frame_index[ADDR_W-1:0] + 1'b1;
                                        state <= ST_LOAD_FRAME;
                                    end
                                end else begin
                                    byte_index <= byte_index + 1'b1;
                                    send_state <= 2'd2;
                                end
                            end
                        end
                        2'd2: begin
                            if (tx_ready) begin
                                tx_data <= send_byte;
                                tx_valid <= 1'b1;
                                send_state <= 2'd1;
                            end
                        end
                        default: send_state <= 2'd0;
                    endcase
                end

                ST_LOAD_FRAME: begin
                    ro_en <= 1'b0;
                    byte_index <= 5'd0;
                    send_state <= 2'd0;
                    state <= ST_UART_SEND;
                end

                ST_DONE: begin
                    ro_en <= 1'b0;
                    state_count <= 64'd0;
                    warmup_count <= 32'd0;
                    send_count <= 32'd0;
                    virtual_uart_count <= 32'd0;
                    tx_valid <= 1'b0;
                end

                default: begin
                    ro_en <= 1'b0;
                    state <= ST_START_WAIT;
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
