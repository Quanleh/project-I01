## Thiết kế này làm gì

Mạch thực hiện phép chia số nguyên không dấu: số bị chia 8 bit chia cho số chia 4 bit,
cho ra thương 8 bit và số dư 4 bit, thỏa `số bị chia = thương × số chia + số dư` với
`0 ≤ số dư < số chia`. Người dùng đặt số bị chia vào `ui_in`, số chia vào `uio_in[3:0]`
rồi đưa `uio_in[4]` (start) từ 0 lên 1. Sau một số chu kỳ cố định, thương ở `uo_out`,
số dư ở `uio_out[3:0]`. Nếu số chia bằng 0, mạch không tính mà bật cờ lỗi `uio_out[4]`.

## Cách hoạt động

Mạch dùng thuật toán chia khôi phục (restoring division) tuần tự, cơ số 2, chỉ có một bộ
so sánh–trừ 5 bit được dùng lại ở mọi bước.

- Một bộ phát hiện sườn lên (`start_d`) biến tín hiệu start thành xung một chu kỳ; xung
  start xuất hiện khi mạch đang bận thì bị bỏ qua.
- Khi nhận start với số chia khác 0: thanh ghi `quotient` được nạp số bị chia, thanh ghi
  số dư xóa về 0, số chia được lưu lại, bộ đếm `count` về 0, cờ `busy` lên 1.
- Mỗi bước lặp (8 chu kỳ, `count` từ 0 đến 7): ghép số dư dịch trái với bit cao nhất
  còn lại của `quotient`; nếu giá trị này ≥ số chia thì trừ số chia và bit thương là 1,
  ngược lại giữ nguyên và bit thương là 0. `quotient` dịch trái một bit và đưa bit thương
  vào đầu thấp, nên bit cao của số bị chia được thay dần bằng bit thương. Số dư không
  bao giờ âm nên không cần bước cộng khôi phục riêng.
- Sau bước thứ 8, `busy` về 0 và `result_ready` lên 1.
- Chia cho 0 được phát hiện ngay tại chu kỳ nhận start: thương và số dư bằng 0, cờ lỗi
  bật, `result_ready` lên ngay.
- Số chu kỳ không phụ thuộc giá trị đầu vào: 9 chu kỳ kể từ cạnh start (1 nạp + 8 lặp)
  với phép chia thường, 1 chu kỳ với chia cho 0 (đã đo bằng mô phỏng).
- Mạch không có máy trạng thái đặt tên; điều khiển bằng các cờ `busy`, `result_ready` và
  bộ đếm `count`. Reset bất đồng bộ, tích cực mức thấp (`rst_n`).

## Cách kiểm thử

Testbench `test/tb.v` chạy 8 ca, so sánh thương, số dư, cờ lỗi và `uio_oe[4]` với giá
trị mong đợi tính tay trước:

| Ca | Vì sao chọn |
|---|---|
| 10 ÷ 2 | chia hết, trường hợp cơ bản |
| 17 ÷ 5 | có dư |
| 255 ÷ 15 | giá trị lớn nhất của cả hai đầu vào; thương 17, dư 0 |
| 7 ÷ 2 | có dư, số chia nhỏ |
| 0 ÷ 3 | số bị chia bằng 0 |
| 100 ÷ 1 | chia cho 1, thương bằng số bị chia |
| 3 ÷ 5 | số bị chia nhỏ hơn số chia: thương 0, dư bằng số bị chia |
| 9 ÷ 0 | trường hợp bất thường: chia cho 0, phải bật cờ lỗi |

Các ca chạy liên tiếp trong một lần mô phỏng, nên cũng kiểm tra mạch nạp lại đúng trạng
thái giữa hai phép chia. Mỗi lần push, GitHub Actions biên dịch bằng Icarus Verilog và
chạy lại toàn bộ testbench; có ca sai thì workflow báo lỗi.

## Ánh xạ chân

| Chân | Tín hiệu | Ý nghĩa |
|---|---|---|
| `ui_in[7:0]` | `dividend[7:0]` | Số bị chia, 8 bit |
| `uo_out[7:0]` | `quotient[7:0]` | Thương, 8 bit |
| `uio_in[3:0]` | `divisor[3:0]` | Số chia, 4 bit (đầu vào) |
| `uio_in[4]` | `start` | Bắt đầu phép chia, nhận theo sườn lên (đầu vào) |
| `uio_out[3:0]` | `remainder[3:0]` | Số dư, 4 bit (đầu ra, `uio_oe[3:0]` luôn bằng 1) |
| `uio_out[4]` | `div_by_zero` | Cờ báo chia cho 0 (đầu ra, `uio_oe[4]` chỉ bằng 1 khi đã có kết quả) |
| `uio[7:5]` | không dùng | `uio_out[7:5]` = 0, `uio_oe[7:5]` = 0 |

## Giới hạn

- Đây là thiết kế để học: kết quả mô phỏng và các lần chạy công cụ **không** chứng minh
  thiết kế sẵn sàng sản xuất, và không phải tape-out hay sign-off.
- Chỉ có 8 ca kiểm thử, chưa phủ hết các tổ hợp đầu vào (256 × 16). Kết quả đạt nghĩa là
  8 ca này đúng, chưa phải mọi ca đều đúng. Chưa có kiểm chứng hình thức.
- Chỉ mô phỏng mức RTL; chưa mô phỏng sau tổng hợp (gate-level) và không có phép kiểm tra
  số chu kỳ bằng assertion trong testbench.
- Chỉ chia số nguyên không dấu, số chia tối đa 4 bit; không xử lý số có dấu.
- Không có chân báo "xong" riêng. `uo_out` và `uio_out[3:0]` hiện giá trị trung gian trong
  lúc đang tính, nên người dùng phải chờ đủ 9 chu kỳ (1 chu kỳ với chia cho 0) rồi mới đọc.
- Chân `uio[4]` được dùng cho cả đầu vào (start) và đầu ra (báo lỗi) theo yêu cầu của đề.
  Vì `uio_oe[4]` bằng 1 sau khi có kết quả, trên chip thật chân này do mạch điều khiển,
  nên nhiều khả năng không thể đưa xung start mới từ ngoài vào cho đến khi reset. Mô phỏng
  RTL không thể hiện điều này vì `uio_in` và `uio_out` là hai tín hiệu tách rời.
- Thông tin về thời gian và diện tích chỉ phản ánh điều kiện của công cụ đã dùng (một
  góc công nghệ, chưa qua đặt và đi dây đầy đủ); không nên suy ra tần số hoạt động tối đa
  thật.
