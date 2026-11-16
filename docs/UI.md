# Giao diện — token và nguyên tắc

Hướng thiết kế đang có: **giấy chấm bi hồng, thẻ bo tròn nổi khối, con dấu trái tim là điểm nhấn
duy nhất**. Dễ thương nhưng không trẻ con — vì nội dung là hợp đồng, phần chữ Hán và bản dịch phải
đọc được như văn bản nghiêm túc. Giữ hai thứ đó cân nhau là cả bài toán thiết kế của trang này.

## Token màu — `index.html:11–40`

Mọi màu khai ở `:root`, lặp lại hai lần nữa cho dark mode
(`@media (prefers-color-scheme:dark)` có chặn `:root:not([data-theme="light"])`, và `:root[data-theme="dark"]`).
**Sửa màu là sửa token, không viết màu thẳng vào component.**

| Token | Sáng | Tối | Dùng cho |
|---|---|---|---|
| `--paper` | `#fff4f8` | `#2a1822` | nền trang (kèm chấm bi `--dots`) |
| `--card` | `#ffffff` | `#3a2230` | mặt thẻ, ô nhập, nút phụ |
| `--ink` | `#4a2a3a` | `#ffe6f0` | chữ chính |
| `--muted` | `#9a6b80` | `#e0a9c1` | chữ phụ, nhãn |
| `--line` | `#f7cfe0` | `#5c3249` | viền, đổ bóng khối |
| `--seal` | `#ff5c9a` | `#ff7eb0` | **màu nhận diện**: tab đang chọn, nút chính, con dấu, `<mark>` |
| `--seal-soft` | `#ffe3ee` | `#4f2438` | nền câu gốc, chip |
| `--jade` / `--jade-soft` | `#2fa37a` / `#e2f7ee` | `#5fd3a6` / `#1f3a31` | "Đúng" (≥8 điểm), phần sửa đúng |
| `--amber` / `--amber-soft` | `#c27a00` / `#fff2d6` | `#f2b74a` / `#3f2f12` | "Gần đúng" (5–7), banner cảnh báo, `note` |
| `--dots` | `#ffd6e7` | `#2a1822` | chấm bi nền (dark mode tắt hẳn) |

Ba màu trạng thái **mang nghĩa, không phải trang trí**: hồng = sai/điểm nhấn, hổ phách = gần đúng/cảnh báo,
xanh ngọc = đúng. Thêm màu mới thì phải nói được nó mang nghĩa gì.

## Chữ — `index.html:28–32`

| Token | Font | Dùng cho |
|---|---|---|
| `--font-body` | Quicksand → Be Vietnam Pro → system | toàn bộ chữ tiếng Việt |
| `--font-zh`, `--font-zh-sans` | Noto Sans SC → PingFang SC → Microsoft YaHei | **mọi** chữ Hán |
| `--font-cute` | ZCOOL KuaiLe | chỉ hai chữ `合同` ở tiêu đề |

Chữ Hán luôn to hơn và giãn dòng rộng hơn chữ Việt (`.src.zh` 19px/1.9 so với 17px/1.75) — chữ Hán
nhỏ là không đọc nổi nét. Hai token `--font-zh` và `--font-zh-sans` hiện **trùng nội dung**; nếu
muốn tách khối (serif cho văn bản luật, sans cho ví dụ) thì sửa ở đây, đừng thêm token thứ ba.

## Hình khối

- **Thẻ**: `border-radius:24px`, viền `2px` màu `--line`, bóng khối đặc `0 6px 0 var(--line)` —
  không phải bóng mờ. Đó là thứ tạo cảm giác giấy dán.
- **Nút / chip / tab**: `border-radius:999px`. Nút chính có bóng `0 3px 0 #d63d7a` và lún 2px khi bấm.
- **Ô nhập**: viền **đứt** `2px dashed` — ra tín hiệu "chỗ để viết vào".
- **Con dấu điểm**: tròn 72px, viền đứt, nghiêng `-8deg`, số dùng `tabular-nums`. Đây là phần thưởng
  của cả trang — đừng làm nó nhạt đi.

## Quy tắc không được phá

1. Một cột, `max-width:760px`. Trang này chủ yếu mở trên điện thoại.
2. Thanh tab `position:sticky; top:0` — đổi tab không phải cuộn lên.
3. Mọi phần tử bấm được có `:focus-visible` viền `--seal` dày 2px.
4. Có `@media (prefers-reduced-motion:reduce)` tắt animation chấm nhấp nháy. Thêm animation mới thì
   thêm vào đó luôn.
5. `<mark>` chỉ dùng để tô từ/cấu trúc đang học trong câu — không dùng làm highlight trang trí.
6. Mọi chuỗi chữ là **tiếng Việt**. Chữ Hán chỉ nằm trong ngữ liệu.
7. Breakpoint duy nhất `max-width:420px` (thu nhỏ chữ Hán và mặt thẻ). Thêm breakpoint thì cân nhắc kỹ.

## Muốn làm lại giao diện

Đọc `docs/SKILLS.md` trước. Giữ nguyên: cấu trúc 3 tab, tông hồng, chữ Việt, một file.
Chụp ảnh trước/sau bằng `python tools/check.py --render` (ra `tools/_render/`) để so.
