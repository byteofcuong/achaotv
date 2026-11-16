# CLAUDE.md — Luyện dịch hợp đồng

Trang web **một file** (`index.html`) để ôn thi giữa kì môn **Biên dịch nâng cao**: dịch điều khoản
hợp đồng hai chiều Trung ⇄ Việt. Chủ dự án là sinh viên, không phải dev — trang phải tự chạy được
trong trình duyệt, không build, không cài gì.

**Đọc `docs/HANDOFF.md` trước khi sửa bất cứ thứ gì.** Ở đó có nghiệp vụ, mô hình dữ liệu, logic
chấm, nợ kỹ thuật và cách đăng lại.

## Bản đồ repo

| Đường dẫn | Là gì |
|---|---|
| `index.html` | Toàn bộ sản phẩm: dữ liệu + CSS + JS trong một file. Nguồn sự thật để sửa. |
| `source/` | Tài liệu gốc (hợp đồng mẫu, đề cương, bảng từ của giảng viên). Mọi dữ liệu trong trang phải truy ra được về đây. |
| `docs/HANDOFF.md` | Bàn giao đầy đủ. |
| `docs/ONTOLOGY.md` | Khái niệm miền + từ điển thuật ngữ code ↔ UI ↔ tiếng Trung. |
| `docs/UI.md` | Design token, nguyên tắc giao diện. |
| `docs/SKILLS.md` | Skill nào dùng cho việc nào. |
| `tools/check.py` | Kiểm tra tĩnh + render. Lệnh nghiệm thu duy nhất. |
| `tools/_render/` | Ảnh chụp do `--render` sinh ra (không commit). |

## Luật cứng — vi phạm là hỏng dữ liệu người dùng

1. **Chỉ thêm câu vào cuối mảng `SENTS`.** id sinh theo vị trí (`id:"s"+(i+1)`), tiến độ đã chấm
   lưu theo id. Chèn hoặc xoá câu giữa mảng = toàn bộ bài đã làm bị gán nhầm sang câu khác.
2. **Không đổi `KEY="ldhd-v1"`.** Đổi khoá localStorage là xoá sạch tiến độ.
3. **Không bịa dữ liệu.** Câu, từ, cấu trúc mới phải lấy từ tài liệu trong `source/`. Khi thêm,
   ghi rõ trong commit lấy từ file nào. Không "dịch lại cho hay" bản `ref` — đó là bản của giáo trình.
4. **Chữ hiển thị bằng tiếng Việt.** Không chen tiếng Anh vào UI. Chữ Hán chỉ xuất hiện trong
   ngữ liệu (câu, từ, cấu trúc), không dùng làm nhãn nút.
5. **Giữ tông hồng.** Màu định nghĩa bằng biến ở `:root` (`--paper`, `--seal`, `--line`…), có
   nhánh dark mode. Sửa màu thì sửa token, không hardcode rải rác. Xem `docs/UI.md`.
6. **Một file, không phụ thuộc ngoài** trừ Google Fonts. Không thêm framework, không `<script src>`,
   không gọi API nào khác ngoài `window.claude.use("sample")`.
7. **Chiều dịch phải đúng:** `zh-vi` → `src` tiếng Trung, `ref` tiếng Việt; `vi-zh` → ngược lại.
   Hợp đồng nào mà bên A **không** theo thông lệ (bên A là bên thuê / bên mua) thì câu đó **bắt buộc**
   có trường `note` giải thích, nếu không sinh viên và bộ chấm đều hiểu sai vai.
8. **Trang phải còn dùng được khi không có `sample()`** (mở bằng `file://`, hoặc người dùng chưa cấp
   quyền). Mọi tính năng gọi Claude đều phải có nhánh dự phòng là bản tham khảo.

## Quy trình mỗi lần sửa

```bash
python tools/check.py
```

```bash
python tools/check.py --render
```

1. Sửa `index.html`.
2. Chạy `python tools/check.py` — phải `OK`, exit 0. Thêm `--render` khi đổi giao diện
   (dùng Chromium/Edge sẵn có, ảnh ra `tools/_render/`).
3. Commit kèm nguồn của dữ liệu mới.
4. **Báo chủ dự án để họ tự đăng lại lên claude.ai.** Claude Code không đăng được artifact này.
   Cách đăng: xem `docs/HANDOFF.md` mục "Đăng lại".

## Không làm

- Không tự đăng, tự publish, tự chia sẻ trang.
- Không đổi schema JSON của bộ chấm (`diem`, `ket_luan`, `nhan_xet`, `loi`, `ban_dich_goi_y`,
  `tu_can_nho`) nếu không sửa `showResult()` tương ứng.
- Không refactor lớn "cho sạch" khi chưa hỏi: mỗi lần sửa file này là một lần chủ dự án phải đăng lại tay.
- Không thêm thư viện, không tách file, không dựng build step.

## Đội agent

Theo CLAUDE.md cá nhân. Ở repo này gần như mọi thay đổi đều nằm trong **một file duy nhất** nên
mặc định **làm inline**. Chỉ bật đội khi có phần tách rời thật sự — ví dụ: một người soạn lô câu
mới từ `source/`, một người làm lại giao diện, rồi ghép. Khi bật thì nói trước một dòng chia việc.
