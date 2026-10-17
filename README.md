# Kho mẫu B2 — EEE703128

> ⚠️ **ĐÂY LÀ GÓI FILE OVERLAY/THAM CHIẾU, KHÔNG PHẢI MỘT REPOSITORY CI HOÀN CHỈNH.**
> Sinh viên phải tạo repo bằng **Use this template** từ kho GitHub chính thức do giảng viên phát trên LMS. Hạ tầng `.github/workflows/` nằm ở kho chính thức. Nếu tab **Actions** trống, báo mentor; không tự cài Docker để chữa repo thiếu workflow.


Kho này là điểm xuất phát cho **Bài kiểm tra số 2**: chọn một đề trong 80 đề, viết Verilog, cho
chạy qua chuỗi RTL-to-GDSII, rồi viết báo cáo giải thích kết quả.

> **Bắt đầu:** bấm **Use this template → Create a new repository**, đặt tên `eee703128-b2-<MSSV>`.
> Đừng bấm *Fork* — fork làm rối lịch sử commit, mà lịch sử commit là bằng chứng em tự làm.

---

## Có gì trong kho này

```text
src/project.v              ← viết thiết kế của em ở đây (đang chứa ví dụ mẫu)
test/tb.v                  ← testbench, thay bằng ca kiểm thử của đề em
info.yaml                  ← tên đề, MSSV, tần số xung nhịp, đặt tên chân
docs/info.md               ← mô tả thiết kế, nộp kèm
HUONG_DAN_CHAY_FLOW.md     ← đọc trước tiên: cách chạy và cách đọc kết quả
```

## Bốn việc phải sửa

| Tệp | Sửa gì |
|---|---|
| `src/project.v` | Đổi `<MSSV>` trong tên module · xoá ví dụ mẫu · viết thiết kế của em |
| `test/tb.v` | Đổi tên module cho khớp · thay ca kiểm thử · tính giá trị mong đợi **bằng tay trước** |
| `info.yaml` | Tên đề, họ tên, MSSV, `top_module` (khớp `project.v`), `clock_hz`, đặt tên chân |
| `docs/info.md` | Điền hết chỗ trong dấu `<>` |

Xong bốn việc đó thì **Commit**. Vào thẻ **Actions**, đợi ~5 phút, tải kết quả ở mục *Artifacts*.

---

## Ví dụ mẫu đang có sẵn

`src/project.v` hiện chứa case `threshold_alarm` của học phần — chính cái đã học ở tuần 8–10:

```verilog
alarm = 1 khi sample >= threshold
```

Nó **không nằm trong 80 đề**, chỉ để em thấy cách nối tín hiệu vào khung chân và cách viết
testbench. Đọc hiểu rồi xoá đi.

Chạy thử ví dụ này trên máy (nếu có Icarus Verilog):

```bash
iverilog -g2012 -o tb.out test/tb.v src/project.v && vvp tb.out
```

Kết quả mong đợi: **7 ca, 0 sai**.

> **Vì sao testbench mẫu có ca `sample = threshold`.** Đổi `>=` thành `>` là lỗi kinh điển và
> mạch vẫn chạy — chỉ sai đúng ở biên. Testbench mẫu bắt được lỗi đó (2/7 ca đỏ). Testbench nào
> không có ca biên thì gần như vô dụng. Rubric tiêu chí 2 chấm chính chỗ này.

---

## Khung chân — dùng chung cho mọi đề

```verilog
module tt_um_eee703128_<MSSV> (
    input  wire [7:0] ui_in,    // 8 chân vào riêng
    output wire [7:0] uo_out,   // 8 chân ra riêng
    input  wire [7:0] uio_in,   // 8 chân hai chiều — chiều vào
    output wire [7:0] uio_out,  // 8 chân hai chiều — chiều ra
    output wire [7:0] uio_oe,   // 1 = chân đó là đầu ra
    input  wire       ena,      // luôn = 1
    input  wire       clk,      // xung nhịp
    input  wire       rst_n     // reset, TÍCH CỰC MỨC THẤP
);
```

Ba quy tắc không được phá:

1. **Không đổi danh sách cổng.** Kể cả đề tổ hợp cũng phải khai báo `clk` và `rst_n`.
2. **Mọi chân ra phải được gán.** Không dùng thì gán `8'b0`. Để hở là lỗi.
3. **`rst_n` tích cực mức thấp** — `rst_n == 0` nghĩa là đang reset.

Cột *Giao diện* của mỗi đề cho biết gán tín hiệu nào vào chân nào.

---

## Nhắc lại điều quan trọng nhất

**58 trên 100 điểm nằm ở việc đọc hiểu kết quả**, không phải ở độ khó của thiết kế. Thiết kế
được giữ đơn giản một cách có chủ ý. Chạy ra GDS mới là nửa đầu; nửa sau — và là nửa nặng điểm hơn —
là giải thích được các con số nghĩa là gì, và chúng **không** chứng minh được điều gì.

**Học phần này không chế tạo chip.** Em thu được một tệp layout dùng để học. Không phải tape-out,
không phải sign-off, không phải sản phẩm sẵn sàng sản xuất. Viết vượt mức bị trừ điểm — xem mục 5
của đề bài.

---

## Ghi chú kỹ thuật

- Chuỗi công cụ: **LibreLane** (bản kế tục OpenLane, do FOSSi Foundation duy trì) trên **PDK
  SkyWater sky130A**, chạy qua GitHub Actions.
- Khung chân và hạ tầng CI dựa trên mẫu `ttsky-verilog-template` của dự án Tiny Tapeout.
- **Không bắt buộc nộp lên shuttle chế tạo.** Lớp chỉ dùng phần chạy tự động, hoàn toàn miễn phí.
