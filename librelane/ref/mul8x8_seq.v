`default_nettype none
// Bo nhan 8x8 tuan tu dich-cong, dung lam doi chung dien tich cho bo chia I01.
module mul8x8_seq (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        start,
    input  wire [7:0]  a,
    input  wire [7:0]  b,
    output wire [15:0] product,
    output wire        done
);
    reg [7:0]  a_reg;
    reg [15:0] acc;
    reg [3:0]  count;
    reg        busy, start_d, done_r;

    wire start_pulse = start & ~start_d;
    wire [8:0]  sum  = {1'b0, acc[15:8]} + {1'b0, a_reg};
    wire [15:0] next = acc[0] ? {sum, acc[7:1]} : {1'b0, acc[15:1]};

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            a_reg <= 8'd0; acc <= 16'd0; count <= 4'd0;
            busy <= 1'b0; start_d <= 1'b0; done_r <= 1'b0;
        end else begin
            start_d <= start;
            if (start_pulse && !busy) begin
                a_reg  <= a;
                acc    <= {8'd0, b};
                count  <= 4'd0;
                busy   <= 1'b1;
                done_r <= 1'b0;
            end else if (busy) begin
                acc <= next;
                if (count == 4'd7) begin
                    busy   <= 1'b0;
                    done_r <= 1'b1;
                end else begin
                    count <= count + 1'b1;
                end
            end
        end
    end

    assign product = acc;
    assign done    = done_r;
endmodule
`default_nettype wire
