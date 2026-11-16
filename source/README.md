# source/ — tài liệu gốc

**Thư mục này đang trống, và đó là việc cần làm đầu tiên.**

Luật trong `CLAUDE.md`: mọi câu, từ, cấu trúc trong `index.html` phải truy ra được về một file ở
đây. Chừng nào `source/` còn trống thì luật đó chưa kiểm chứng được — người sửa chỉ còn cách tin
vào dữ liệu đã có.

## Cần bỏ vào đây

| Đặt vào | Là gì |
|---|---|
| `source/hop-dong/` | Bản gốc 7 hợp đồng đã rút câu: `买卖合同`, `租赁合同 (练习 1)`, `房屋租赁合同协议书`, `HĐ mua bán ĐH Tây Nguyên`, `HĐ thuê nhà 2013`, `HĐ thuê nhà Văn Khê 2018`, `HĐ bán hàng cao su (练习 2)` |
| `source/tu-vung/` | Bảng từ giảng viên phát, **giữ nguyên phần tô vàng / tô đỏ** — hai bộ `Từ bôi vàng`, `Từ bôi đỏ` trong app lấy từ đó |
| `source/de-cuong/` | Đề cương ôn tập, đề thi mẫu, đáp án nếu có |

Định dạng nào cũng được (`.docx`, `.pdf`, `.md`, ảnh chụp). Giữ nguyên tên gốc, đừng sửa nội dung.
Nếu là ảnh chụp thì kèm một file `.md` gõ lại phần chữ, để còn tìm kiếm được.

Bản tổng hợp đã có trên claude.ai (doc "Ôn giữa kì Biên dịch nâng cao — Hợp đồng (Trung ⇄ Việt)",
https://claude.ai/artifact/7jJxtBbYkD453sYZZeLXRH) có thể xuất ra Markdown và bỏ vào
`source/de-cuong/` làm bản nền.

## Khi thêm ngữ liệu mới

1. Mở file trong `source/`, chép **nguyên văn** câu gốc và bản dịch của tài liệu.
2. Thêm vào **cuối** `SENTS` (xem `CLAUDE.md`, luật 1).
3. Ghi trong commit: lấy từ file nào, điều khoản nào.
4. `python tools/check.py`.

Không tự dịch lại bản `ref`, không "làm cho câu hay hơn", không ghép câu từ hai hợp đồng khác nhau.
Đề thi ra theo tài liệu, không ra theo bản dịch đẹp.
