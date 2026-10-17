
`default_nettype none
`timescale 1ns / 1ps

module tb;
    reg [7:0] ui_in, uio_in;
    reg ena, clk, rst_n;
    wire [7:0] uo_out, uio_out, uio_oe;

    integer so_ca = 0;
    integer so_sai = 0;

    tt_um_eee703128_24100556 dut (
        .ui_in(ui_in), .uo_out(uo_out),
        .uio_in(uio_in), .uio_out(uio_out),
        .uio_oe(uio_oe), .ena(ena),
        .clk(clk), .rst_n(rst_n)
    );

    initial clk = 0;
    always #5 clk = ~clk;

    task kiem;
        input [7:0] a;
        input [3:0] b;
        input [7:0] q_mong_doi;
        input [3:0] r_mong_doi;
        input loi_mong_doi;
        input [255:0] ten;
        integer timeout;
        begin
            @(negedge clk);
            ui_in = a;
            uio_in = {3'b000, 1'b1, b};

            @(negedge clk);
            uio_in[4] = 1'b0;

            timeout = 0;
            while (dut.busy && timeout < 12) begin
                @(negedge clk);
                timeout = timeout + 1;
            end

            repeat (2) @(negedge clk);
            so_ca = so_ca + 1;

            if (uo_out === q_mong_doi &&
                uio_out[3:0] === r_mong_doi &&
                uio_out[4] === loi_mong_doi &&
                uio_oe[4] === 1'b1) begin
                $display("PASS %0s: Q=%0d R=%0d ERR=%b OE4=%b",
                         ten, uo_out, uio_out[3:0],
                         uio_out[4], uio_oe[4]);
            end else begin
                so_sai = so_sai + 1;
                $display("FAIL %0s: Q=%0d R=%0d ERR=%b OE4=%b",
                         ten, uo_out, uio_out[3:0],
                         uio_out[4], uio_oe[4]);
            end

            @(negedge clk);
            uio_in[4] = 1'b0;
            repeat (2) @(negedge clk);
        end
    endtask

    initial begin
        $dumpfile("tb.vcd");
        $dumpvars(0, tb);

        ena = 1;
        rst_n = 0;
        ui_in = 0;
        uio_in = 0;

        #20 rst_n = 1;
        repeat (2) @(negedge clk);

        $display("=== KIEM THU BO CHIA I01 ===");

        kiem(10, 2, 5, 0, 0, "10 chia 2");
        kiem(17, 5, 3, 2, 0, "17 chia 5");
        kiem(255, 15, 17, 0, 0, "255 chia 15");
        kiem(7, 2, 3, 1, 0, "7 chia 2");
        kiem(0, 3, 0, 0, 0, "0 chia 3");
        kiem(100, 1, 100, 0, 0, "100 chia 1");
        kiem(3, 5, 0, 3, 0, "3 nho hon 5");
        kiem(9, 0, 0, 0, 1, "chia cho 0");

        $display("=== KET QUA: %0d ca, %0d sai ===",
                 so_ca, so_sai);
        if (so_sai == 0)
            $display("TAT CA CA KIEM THU DEU DAT");
        else
            $display("CAN KIEM TRA LAI RTL");

        #20 $finish;
    end
endmodule

`default_nettype wire

