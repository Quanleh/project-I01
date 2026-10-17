`default_nettype none

module tt_um_eee703128_24100556 (
    input  wire [7:0] ui_in,    // Dividend (8-bit)
    output wire [7:0] uo_out,   // Quotient (8-bit)
    input  wire [7:0] uio_in,   // uio_in[3:0] = Divisor, uio_in[4] = Start
    output wire [7:0] uio_out,  // uio_out[3:0] = Remainder, uio_out[4] = Div_by_zero
    output wire [7:0] uio_oe,   // OE config
    input  wire       ena,      
    input  wire       clk,      
    input  wire       rst_n     
);

    reg [7:0] quotient;
    reg [4:0] remainder;
    reg [3:0] divisor;
    reg [3:0] count;
    reg busy;
    reg start_d;
    reg error_div0;
    reg result_ready;

    // Phát hiện sườn lên của tín hiệu Start (uio_in[4])
    wire start_pulse = uio_in[4] & ~start_d;

    // Logic tính toán thuật toán chia khôi phục (Restoring Division)
    wire [4:0] shifted_remainder = {remainder[3:0], quotient[7]};
    wire subtract_ok = (shifted_remainder >= {1'b0, divisor});
    wire [4:0] next_remainder = subtract_ok 
                                ? (shifted_remainder - {1'b0, divisor}) 
                                : shifted_remainder;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            quotient     <= 8'd0;
            remainder    <= 5'd0;
            divisor      <= 4'd0;
            count        <= 4'd0;
            busy         <= 1'b0;
            start_d      <= 1'b0;
            error_div0   <= 1'b0;
            result_ready <= 1'b0;
        end else begin
            start_d <= uio_in[4];

            if (start_pulse && !busy) begin
                if (uio_in[3:0] == 4'd0) begin
                    // Xử lý chia cho 0
                    error_div0   <= 1'b1;
                    quotient     <= 8'd0;
                    remainder    <= 5'd0;
                    busy         <= 1'b0;
                    result_ready <= 1'b1;
                end else begin
                    // Khởi tạo phép chia
                    error_div0   <= 1'b0;
                    quotient     <= ui_in;
                    remainder    <= 5'd0;
                    divisor      <= uio_in[3:0];
                    count        <= 4'd0;
                    busy         <= 1'b1;
                    result_ready <= 1'b0;
                end
            end else if (busy) begin
                remainder <= next_remainder;
                quotient  <= {quotient[6:0], subtract_ok};

                if (count == 4'd7) begin
                    busy         <= 1'b0;
                    result_ready <= 1'b1;
                end else begin
                    count <= count + 1'b1;
                end
            end
        end
    end

    // Gán đầu ra
    assign uo_out  = quotient;
    assign uio_out = {3'b000, error_div0, remainder[3:0]};
    
    // Khi có kết quả (hoặc lỗi chia 0), kích hoạt uio_out[4:0] làm output (0x1F)
    // Nếu chưa xong, duy trì uio_out[3:0] làm output (0x0F)
    assign uio_oe  = result_ready ? 8'b00011111 : 8'b00001111;

endmodule

`default_nettype wire
