# Hướng dẫn chạy RTL-to-GDSII — không cần cài gì trên máy

**EEE703128 · Bài kiểm tra số 2** — phụ lục phát ở tuần 10

Tài liệu này dạy đúng một việc: đưa mã Verilog của em qua chuỗi công cụ nguồn mở để ra được
bản vẽ mặt nạ và các báo cáo. Việc **đọc** những báo cáo đó — phần chiếm 58/100 điểm — đã được
dạy ở tuần 8, 9, 10; ở đây chỉ nói cách tạo ra chúng.

---

## 0. Trước khi bắt đầu — hiểu mình đang làm gì

Chuỗi công cụ biến mã Verilog thành hình vẽ các lớp vật liệu trên đế silicon. Nó đi qua sáu bước,
và **mỗi bước sinh ra một báo cáo mà báo cáo của em phải đọc**:

| Bước | Tên | Làm gì | Sinh ra báo cáo gì | Mục nào của báo cáo |
|---|---|---|---|---|
| 1 | Synthesis | Dịch Verilog thành các cổng logic có sẵn trong thư viện | số cell, loại cell, diện tích | Mục 4 |
| 2 | Floorplan | Định hình chữ nhật của ô, chừa chỗ cho hàng cell | hệ số sử dụng (utilization) | Mục 4 |
| 3 | Placement | Đặt từng cell vào vị trí cụ thể | mật độ đặt, độ chật | Mục 7 |
| 4 | CTS | Dựng cây phân phối xung nhịp | số buffer xung nhịp, độ lệch | Mục 5 |
| 5 | Routing | Nối dây giữa các cell bằng các lớp kim loại | chiều dài dây, số via | Mục 7 |
| 6 | Sign-off checks | Kiểm luật vẽ (DRC) và đối chiếu sơ đồ (LVS), phân tích thời gian (STA) | slack, DRC, LVS, công suất | Mục 5, 6 |

> **Chữ "sign-off" ở bước 6 là tên kỹ thuật của bước kiểm, không có nghĩa thiết kế của em đã được
> sign off.** Sign-off thật của một con chip là quy trình phê duyệt của nhà máy, cần nhiều thứ mà
> học phần này không có. Viết "em đã sign-off" trong báo cáo là sai và bị trừ điểm.

---

## 1. Bảy bước làm

### Bước 1 — Có tài khoản GitHub
Miễn phí, đăng ký tại github.com. Dùng email trường cho tiện.

### Bước 2 — Tạo kho riêng từ kho mẫu của lớp
Mở kho mẫu (đường dẫn thầy phát), bấm nút xanh **Use this template → Create a new repository**.
Đặt tên dạng `eee703128-b2-<MSSV>`. Để **Public** thì Actions chạy miễn phí không giới hạn.

> Đừng bấm **Fork**. Fork giữ liên hệ với kho gốc và làm rối lịch sử commit — mà lịch sử commit
> chính là bằng chứng em tự làm (cổng A của rubric).

### Bước 3 — Sửa `src/project.v`
Bấm vào tệp, bấm biểu tượng bút chì để sửa ngay trên trình duyệt.

1. Đổi `<MSSV>` trong tên module thành mã số của em.
2. **Giữ nguyên danh sách cổng** — không thêm, không bớt, không đổi tên. Kể cả đề tổ hợp cũng
   phải khai báo `clk` và `rst_n`.
3. Xoá phần ví dụ mẫu, viết thiết kế của em vào giữa hai dòng đánh dấu `PHẦN CỦA EM`.
4. **Mọi chân ra phải được gán giá trị.** Không dùng thì gán `8'b0`. Để hở là công cụ báo lỗi.

### Bước 4 — Sửa `test/tb.v`
Thay các ca kiểm thử bằng ca của đề em (cột *Ca kiểm thử tối thiểu*), cộng **ít nhất hai ca tự
nghĩ thêm**.

**Tính giá trị mong đợi bằng tay TRƯỚC, rồi mới chạy.** Nếu em chạy trước rồi chép kết quả vào ô
mong đợi thì testbench chỉ xác nhận mạch làm đúng cái nó đang làm — vô nghĩa.

### Bước 5 — Sửa `info.yaml` và `docs/info.md`
`info.yaml`: tên đề, họ tên, MSSV, `top_module` phải khớp đúng tên module trong `project.v`,
`clock_hz` để `0` nếu đề tổ hợp. `docs/info.md`: mô tả thiết kế theo mẫu có sẵn.

### Bước 6 — Commit và xem kết quả
Mỗi lần bấm **Commit changes** là chuỗi công cụ tự chạy. Vào thẻ **Actions** xem tiến trình,
khoảng 5 phút.

- **Dấu ✓ xanh** — chạy xong. Kéo xuống cuối trang, mục **Artifacts**, tải tệp `.zip` về.
- **Dấu ✗ đỏ** — có lỗi. Bấm vào để đọc, xem mục 3 dưới đây.

### Bước 7 — Đọc kết quả
Trong tệp tải về có: bản vẽ `.gds`, ảnh layout 2D và 3D, và thư mục báo cáo. Đây là nguyên liệu
cho mục 4 đến mục 8 của báo cáo.

> **Đừng đợi đến sát hạn mới chạy lần đầu.** Hãy commit một lần ngay khi mới sửa vài dòng, chỉ để
> chắc chắn chuỗi công cụ chạy được với tài khoản của em. Tuần 11–12 sẽ có mốc nộp ảnh chụp một
> lần chạy xanh — coi như bài tập bắt buộc, không tính điểm.

---

## 2. Tìm số liệu ở đâu trong đống báo cáo

| Báo cáo cần | Tìm trong | Con số cần lấy |
|---|---|---|
| Mục 4 — tổng hợp | báo cáo thống kê sau bước synthesis | tổng số cell · số flip-flop · diện tích (µm²) |
| Mục 4 — hệ số sử dụng | báo cáo floorplan | utilization (%) |
| Mục 5 — thời gian | báo cáo STA cuối cùng | worst slack setup · worst slack hold · đường tới hạn |
| Mục 6 — công suất | báo cáo ước lượng công suất | công suất động · công suất tĩnh (rò) |
| Mục 6 — kiểm vật lý | báo cáo DRC và LVS | số vi phạm (phải bằng 0) |
| Mục 7 — layout | ảnh 2D và 3D | mô tả những gì nhìn thấy |

**Tên tệp cụ thể thay đổi theo phiên bản công cụ.** Cách chắc ăn: giải nén rồi tìm theo từ khoá
`slack`, `area`, `power`, `drc`, `utilization` trong tên tệp và trong nội dung.

### Hai chỗ hay hiểu sai

**Slack** là thời gian *còn dư*. Slack **dương** = đạt. Slack **âm** = vi phạm, tín hiệu đến muộn hơn
hạn. Không phải "âm là tốt vì nhanh hơn".

**DRC sạch không có nghĩa mạch chạy đúng.** DRC chỉ kiểm hình vẽ có phạm luật của nhà máy không.
Một mạch sai chức năng hoàn toàn vẫn có thể DRC sạch. Rubric tiêu chí 5 chấm đúng chỗ này —
phải nói được cái kiểm này **không** khẳng định điều gì.

---

## 3. Lỗi thường gặp

| Triệu chứng | Nguyên nhân hay gặp | Cách sửa |
|---|---|---|
| `module not found` | `top_module` trong `info.yaml` khác tên module trong `project.v` | Cho hai chỗ giống hệt nhau, kể cả chữ hoa chữ thường |
| `syntax error near ...` | Thiếu `;`, thiếu `end`, thiếu `endmodule` | Đọc số dòng trong thông báo lỗi, sửa đúng dòng đó |
| `port ... not driven` | Có chân ra chưa được gán | Gán `8'b0` cho những chân không dùng |
| `multiple drivers` | Cùng một tín hiệu bị gán ở hai chỗ | Mỗi tín hiệu chỉ được gán ở đúng một chỗ |
| Chạy rất lâu rồi hỏng | Thiết kế quá lớn so với ô 1×1 | Đổi `tiles` sang `2x1` trong `info.yaml`, hoặc thu nhỏ thiết kế |
| Vi phạm timing (slack âm) | Đường tổ hợp quá dài giữa hai thanh ghi | Hạ `clock_hz` trong `info.yaml`. **Ghi lại việc này vào báo cáo** — đó là số liệu tốt cho mục 5 |
| `latch inferred` | Trong khối `always` tổ hợp có nhánh không gán giá trị | Gán giá trị mặc định ở đầu khối, hoặc dùng `else` đầy đủ |

> **Lỗi là dữ liệu, không phải thất bại.** Chụp lại thông báo lỗi, ghi lại đã thử gì và vì sao.
> Rubric có đường chấm riêng cho báo cáo thất bại trung thực — chẩn đoán đúng một lỗi khó được
> điểm cao hơn hẳn việc chép số liệu của bạn khác.

---

## 4. Muốn chạy trên máy mình (không bắt buộc — điểm cộng +2)

Không cần thiết để hoàn thành bài. Nhưng nếu em muốn xem bên trong công cụ, và có máy đủ khoẻ:

- **LibreLane** là bản kế tục của OpenLane, do FOSSi Foundation duy trì (Efabless — nơi phát triển
  OpenLane — đã đóng cửa đầu năm 2025, nên tài liệu nào còn ghi "OpenLane của Efabless" là đã cũ).
- Ba cách cài: **Nix** (tái lập tốt nhất), **AppImage** (dễ nhất trên Linux/WSL), **Docker**
  (chạy được cả Windows/macOS/Linux). Trên Windows cần WSL2.
- Tài liệu: `librelane.readthedocs.io` → mục Installation.

Muốn lấy điểm cộng thì kèm ảnh chụp quá trình chạy trên máy mình **và** nêu một khác biệt quan sát
được so với chạy trên máy chủ. Chỉ dán ảnh không có nhận xét thì không được cộng.

---

## 5. Tự kiểm trước khi nộp

- [ ] Kho GitHub là của riêng em, có nhiều commit rải theo thời gian (không phải một lần đẩy duy nhất)
- [ ] Actions có ít nhất một lần chạy ✓ xanh, và em đã tải tệp kết quả về
- [ ] Tên module trong `project.v` khớp `top_module` trong `info.yaml`
- [ ] `docs/info.md` mô tả đúng thiết kế của em, không còn chữ trong dấu `<>`
- [ ] Testbench có đủ ca của đề **cộng ít nhất hai ca tự nghĩ**, và giá trị mong đợi được tính tay trước
- [ ] Báo cáo có đủ 9 mục theo cấu trúc trong đề bài
- [ ] Đã trả lời **câu phân tích riêng của đề mình** ở mục 8 — bằng số liệu của chính mình
- [ ] Mọi con số trong báo cáo lấy từ lần chạy của em, đối chiếu được với tệp kết quả trên kho
- [ ] Đã ghi: đường dẫn kho, mã commit, số hiệu lần chạy, phiên bản công cụ, phiên bản PDK, ngày chạy
- [ ] **Không có câu nào nói tape-out, sign-off, chip đã sản xuất, sẵn sàng sản xuất**
- [ ] Đã ghi rõ ở cuối báo cáo nếu có dùng công cụ AI, và dùng vào việc gì
