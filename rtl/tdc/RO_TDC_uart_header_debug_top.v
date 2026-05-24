module RO_TDC_uart_header_debug_top #(
    parameter PAIR_ID = 16'hD001,
    parameter FAMILY_ID = 16'h00D0,
    parameter REPEAT_COUNT = 16'd8
) (
    input  wire sys_clk,
    input  wire por_n_i,
    output wire UART_TX_o
);

    localparam HEADER_BYTES = 16;
    localparam START_DELAY_CYCLES = 64'd16000000000;
    localparam ST_START_DELAY = 2'd0;
    localparam ST_SEND = 2'd1;
    localparam ST_DONE = 2'd2;
    localparam SEND_IDLE = 2'd0;
    localparam SEND_WAIT_ACCEPT = 2'd1;
    localparam SEND_WAIT_READY = 2'd2;

    wire locked;
    wire clk_200m;
    wire rst_n_200m;
    wire tx_ready;
    reg [7:0] tx_data;
    reg tx_valid;
    reg [1:0] send_state;
    reg [1:0] main_state;
    reg [63:0] delay_cnt;
    reg [4:0] byte_index;
    reg [15:0] repeat_index;
    reg [7:0] send_byte;

    clk_wiz_0 u_clk_wiz_0 (
        .clk_out1(clk_200m),
        .reset(1'b0),
        .locked(locked),
        .clk_in1(sys_clk)
    );

    proc_sys_reset_0 u_proc_sys_reset_0 (
        .slowest_sync_clk(clk_200m),
        .ext_reset_in(1'b0),
        .aux_reset_in(1'b0),
        .mb_debug_sys_rst(1'b0),
        .dcm_locked(locked),
        .mb_reset(),
        .bus_struct_reset(),
        .peripheral_reset(),
        .interconnect_aresetn(),
        .peripheral_aresetn(rst_n_200m)
    );

    always @(*) begin
        case (byte_index)
            5'd0: send_byte = 8'h54; // T
            5'd1: send_byte = 8'h44; // D
            5'd2: send_byte = 8'h43; // C
            5'd3: send_byte = 8'h52; // R
            5'd4: send_byte = 8'hD0;
            5'd5: send_byte = PAIR_ID[7:0];
            5'd6: send_byte = PAIR_ID[15:8];
            5'd7: send_byte = FAMILY_ID[7:0];
            5'd8: send_byte = FAMILY_ID[15:8];
            5'd9: send_byte = repeat_index[7:0];
            5'd10: send_byte = repeat_index[15:8];
            5'd11: send_byte = REPEAT_COUNT[7:0];
            5'd12: send_byte = REPEAT_COUNT[15:8];
            5'd13: send_byte = 8'h55;
            5'd14: send_byte = 8'hAA;
            5'd15: send_byte = 8'h52;
            default: send_byte = 8'd0;
        endcase
    end

    always @(posedge clk_200m or negedge rst_n_200m) begin
        if (!rst_n_200m) begin
            tx_data <= 8'd0;
            tx_valid <= 1'b0;
            send_state <= SEND_IDLE;
            main_state <= ST_START_DELAY;
            delay_cnt <= 64'd0;
            byte_index <= 5'd0;
            repeat_index <= 16'd0;
        end else begin
            case (main_state)
                ST_START_DELAY: begin
                    tx_valid <= 1'b0;
                    if (delay_cnt >= START_DELAY_CYCLES) begin
                        main_state <= ST_SEND;
                    end else begin
                        delay_cnt <= delay_cnt + 1'b1;
                    end
                end
                ST_SEND: begin
                    case (send_state)
                        SEND_IDLE: begin
                            tx_valid <= 1'b0;
                            if (repeat_index >= REPEAT_COUNT) begin
                                main_state <= ST_DONE;
                            end else if (tx_ready) begin
                                tx_data <= send_byte;
                                tx_valid <= 1'b1;
                                send_state <= SEND_WAIT_ACCEPT;
                            end
                        end
                        SEND_WAIT_ACCEPT: begin
                            tx_valid <= 1'b1;
                            if (!tx_ready) begin
                                tx_valid <= 1'b0;
                                if (byte_index == HEADER_BYTES-1) begin
                                    byte_index <= 5'd0;
                                    repeat_index <= repeat_index + 1'b1;
                                    send_state <= SEND_IDLE;
                                end else begin
                                    byte_index <= byte_index + 1'b1;
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
                            main_state <= ST_DONE;
                        end
                    endcase
                end
                ST_DONE: begin
                    tx_valid <= 1'b0;
                end
                default: begin
                    tx_valid <= 1'b0;
                    main_state <= ST_DONE;
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
