#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tự kiểm trước khi commit — EEE703128 B2.

    python3 KIEM_TRA_TRUOC_KHI_COMMIT.py

Bắt các lỗi khiến chuỗi công cụ hỏng, TRƯỚC khi tốn 5 phút chạy rồi mới biết.
Không cần cài gì ngoài Python 3.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
loi, canh = [], []
def R(p):
    f = os.path.join(HERE, p)
    return open(f, encoding="utf-8").read() if os.path.exists(f) else None

print("=" * 70); print("KIỂM TRA TRƯỚC KHI COMMIT — EEE703128 B2"); print("=" * 70)

v = R("src/project.v"); y = R("info.yaml"); tb = R("test/tb.v"); md = R("docs/info.md")
for name, txt in [("src/project.v", v), ("info.yaml", y), ("test/tb.v", tb), ("docs/info.md", md)]:
    if txt is None: loi.append(f"thiếu tệp {name}")
if loi:
    for e in loi: print("❌", e)
    sys.exit(1)

# 1 ── còn chỗ chưa điền không
# Bỏ dòng chú thích trước khi quét: chính phần hướng dẫn có nhắc <MSSV>, <...>
# nên nếu quét cả chú thích thì bài làm xong vẫn bị báo là chưa điền.
def bo_chu_thich(name, t):
    if name.endswith((".v", ".sv")):
        t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)      # chú thích khối
        t = re.sub(r"//[^\n]*", "", t)                    # chú thích dòng
    elif name.endswith((".yaml", ".yml")):
        t = re.sub(r"(?m)^\s*#[^\n]*$", "", t)            # dòng chú thích YAML
        t = re.sub(r"(?m)\s+#[^\n]*$", "", t)             # chú thích cuối dòng
    return t

print("\n── 1. Còn chỗ chưa điền ──")
for name, txt in [("src/project.v", v), ("info.yaml", y), ("test/tb.v", tb), ("docs/info.md", md)]:
    txt = bo_chu_thich(name, txt)
    n = len(re.findall(r"<[^<>\n]{2,40}>", txt))
    if n:
        loi.append(f"{name}: còn {n} chỗ dạng <...> chưa điền")
        print(f"   ❌ {name}: còn {n} chỗ <...>")
    else:
        print(f"   ✅ {name}")

# 2 ── tên module
print("\n── 2. Tên module ──")
m = re.search(r"module\s+(tt_um_[\w<>]+)\s*\(", v)
if not m:
    loi.append("src/project.v không có module nào bắt đầu bằng tt_um_ — chuỗi công cụ sẽ không nhận")
    print("   ❌ không thấy module tt_um_...")
elif "<" in m.group(1):
    loi.append(f"chưa đổi tên module: {m.group(1)} — thay <MSSV> bằng mã số của em")
    print(f"   ❌ {m.group(1)} — chưa đổi <MSSV>")
    m = None
else:
    mod = m.group(1)
    ty = re.search(r'top_module:\s*"?([\w<>]+)"?', y or "")
    top = ty.group(1) if ty else None
    print(f"   project.v : {mod}")
    print(f"   info.yaml : {top}")
    if top != mod:
        loi.append(f"top_module trong info.yaml ({top}) KHÁC tên module trong project.v ({mod})")
        print("   ❌ hai chỗ không khớp — đây là lỗi làm hỏng flow hay gặp nhất")
    else:
        print("   ✅ khớp")
    if not re.search(re.escape(mod) + r"\s+\w+\s*\(", tb):
        canh.append(f"test/tb.v chưa gọi module {mod} — testbench sẽ không biên dịch được")
        print(f"   ⚠  test/tb.v chưa gọi {mod}")

# 3 ── danh sách cổng phải nguyên vẹn
print("\n── 3. Danh sách cổng ──")
CHAN = ["ui_in", "uo_out", "uio_in", "uio_out", "uio_oe", "ena", "clk", "rst_n"]
head = v[v.find("module tt_um_"):]
head = head[:head.find(");") + 2] if ");" in head else head
thieu = [c for c in CHAN if not re.search(r"\b" + c + r"\b", head)]
if thieu:
    loi.append(f"thiếu cổng: {thieu} — KHÔNG được bớt cổng, kể cả đề tổ hợp")
    print(f"   ❌ thiếu: {thieu}")
else:
    print(f"   ✅ đủ 8 cổng")

# 4 ── mọi chân ra phải được gán
print("\n── 4. Chân ra đã gán hết chưa ──")
body = v
for out in ["uo_out", "uio_out", "uio_oe"]:
    if re.search(r"(assign\s+" + out + r"\b|" + out + r"\s*(\[[^\]]*\])?\s*<?=)", body):
        print(f"   ✅ {out}")
    else:
        loi.append(f"{out} chưa được gán ở đâu cả — để hở là công cụ báo lỗi")
        print(f"   ❌ {out} chưa gán")

# 5 ── quy ước bắt buộc
print("\n── 5. Quy ước bắt buộc ──")
for pat, msg, bat in [(r"`default_nettype\s+none", "`default_nettype none ở đầu", True),
                      (r"`default_nettype\s+wire", "`default_nettype wire ở cuối", True),
                      (r"\bendmodule\b", "endmodule", True)]:
    if re.search(pat, v): print(f"   ✅ {msg}")
    elif bat: loi.append(f"thiếu {msg}"); print(f"   ❌ thiếu {msg}")

# 6 ── clock_hz khớp loại mạch
print("\n── 6. clock_hz và loại mạch ──")
ch = re.search(r"clock_hz:\s*(\d+)", y or "")
hz = int(ch.group(1)) if ch else None
tuantu = bool(re.search(r"always\s*@\s*\(\s*posedge|always_ff", v))
print(f"   thiết kế: {'TUẦN TỰ (có always @(posedge))' if tuantu else 'TỔ HỢP'} · clock_hz = {hz}")
if tuantu and hz == 0:
    canh.append("thiết kế tuần tự mà clock_hz = 0 — nên ghi tần số thật, ví dụ 10000000")
    print("   ⚠  tuần tự nhưng clock_hz = 0")
elif (not tuantu) and hz and hz > 0:
    canh.append("thiết kế tổ hợp mà clock_hz > 0 — không sai, nhưng nên để 0 cho đúng")
    print("   ⚠  tổ hợp nhưng clock_hz > 0")
else:
    print("   ✅ hợp lý")

# 7 ── testbench có ca biên không
print("\n── 7. Testbench ──")
n_ca = len(re.findall(r"\bkiem\s*\(", tb))
print(f"   số ca kiểm thử: {n_ca}")
if n_ca < 5:
    canh.append(f"mới có {n_ca} ca kiểm thử — đề nào cũng nên có ít nhất 5, cộng 2 ca tự nghĩ")
    print("   ⚠  ít hơn 5 ca")
else:
    print("   ✅ đủ số lượng tối thiểu")

# 8 ── phát biểu vượt mức
print("\n── 8. Phát biểu vượt mức ──")
CAM = [r"tape[- ]?out", r"sign[- ]?off", r"đã (được )?sản xuất", r"sẵn sàng sản xuất",
       r"kiểm chứng trên silicon"]
# Câu PHỦ ĐỊNH hoặc câu HƯỚNG DẪN nhắc tới từ cấm thì không tính là vi phạm.
# Không có phần này, kịch bản bắt nhầm chính dòng dặn sinh viên đừng viết như vậy.
MIEN = re.compile(r"không|chưa|tránh|cấm|trừ điểm|vượt mức|đừng|sai sự thật|"
                  r"không phải|rubric|mục 5|bị trừ", re.I)
hit = []
for f, t in [("docs/info.md", md), ("info.yaml", y)]:
    for p in CAM:
        for mm in re.finditer(p, t, re.I):
            ctx = t[max(0, mm.start() - 220):mm.end() + 220]   # cửa sổ rộng, câu tiếng Việt dài
            if MIEN.search(ctx): continue
            hit.append((f, mm.group(0)))
if hit:
    loi.append(f"phát biểu vượt mức: {hit[:4]} — bị trừ điểm theo mục 5 của đề bài")
    print(f"   ❌ {hit[:4]}")
else:
    print("   ✅ không có")

print("\n" + "=" * 70)
if loi:
    print(f"❌ {len(loi)} LỖI — sửa xong hãy commit:")
    for e in loi: print("   •", e)
if canh:
    print(f"\n⚠  {len(canh)} cảnh báo (không chặn):")
    for c in canh: print("   •", c)
if not loi:
    print("✅ SẴN SÀNG COMMIT" + ("  (đọc kỹ cảnh báo ở trên)" if canh else ""))
print("=" * 70)
sys.exit(1 if loi else 0)

# ── v2.2 ────────────────────────────────────────────────────────────────
#  1) Kiem kho co CI khong — README hua "vao tab Actions", phai co that.
#  2) THOAT VOI MA 1 khi co loi. Truoc v2.2 file nay in "X LOI" roi thoat 0,
#     nen moi pre-commit hook hay buoc CI doc no deu thay XANH.
import os as _os, sys as _sys
if not _os.path.isdir(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                                    ".github", "workflows")):
    print()
    print("  (!) Kho nay KHONG co .github/workflows/ — day KHONG phai loi cua em.")
    print("      Kho mau phai duoc dung tu 'ttsky-verilog-template'. Neu tab Actions")
    print("      trong tron, bao giang vien truoc khi lam tiep.")
    print()
try:    _loi = loi
except NameError: _loi = []
_sys.exit(1 if _loi else 0)
