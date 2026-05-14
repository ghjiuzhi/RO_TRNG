module health_test (
    input es_clk_i,
    input rst_n_i,
    input es_bit_i,
    output rand_bit_healthy_o,
    output en_o

);

    wire es_rst_n;
    wire alarm;

    reg [2:0] rst_n_sync;
    reg [2047:0] pipe;
    reg [11:0] ones_counter;
    reg [11:0] bit_counter;
    reg en;

    assign es_rst_n = rst_n_sync[2];
    assign alarm = (ones_counter < 'd953) || (ones_counter > 'd1095);

    always @(posedge es_clk_i or negedge rst_n_i) begin
        if (~rst_n_i) begin
            rst_n_sync <= 'b0;
        end
        else begin
            rst_n_sync <= {rst_n_sync[1:0], 1'b1};
        end
    end

    always @(posedge es_clk_i or negedge es_rst_n) begin
        if (~es_rst_n) begin
            pipe <= 'b0;
        end
        else if (alarm)  begin 
            pipe <= 'b0;
        end
        else begin
            pipe <= {pipe[2046:0], es_bit_i};
        end
    end

    always @(posedge es_clk_i or negedge es_rst_n) begin
        if (~es_rst_n) begin
            ones_counter <= 'b0;
        end
        else if (alarm) begin
            ones_counter <= 'b0;
        end
        else if ({es_bit_i, pipe[2047]} == 2'b10) begin
            ones_counter <= ones_counter + 1'b1;
        end
        else if ({es_bit_i, pipe[2047]} == 2'b01) begin
            ones_counter <= ones_counter - 1'b1;
        end
    end

    always @(posedge es_clk_i or negedge es_rst_n) begin
        if (~es_rst_n) begin
            bit_counter <= 'b0;
        end
        else if (alarm)  begin 
            bit_counter <= 'b0;
        end
        else if (bit_counter != 'd2047) begin
            bit_counter <= bit_counter + 'b1;
        end
    end

    always @(posedge es_clk_i or negedge es_rst_n) begin
        if (~es_rst_n) begin
            en <= 1'b0;
        end
        else if (alarm)  begin 
            en <= 1'b0;
        end
        else if (bit_counter == 'd2047) begin
            en <= 1'b1;
        end
    end

    assign en_o = en;
    assign rand_bit_healthy_o = pipe[2047];
    
endmodule