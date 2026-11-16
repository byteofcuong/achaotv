# Tin bàn giao — dán vào phiên Claude Code mới

Mở Claude Code tại `D:\Direc of code\pet_project\achaotv` rồi dán nguyên khối dưới đây.

---

Mình chuyển dự án "Luyện dịch hợp đồng" từ claude.ai sang repo này để làm tiếp. Đây là trang web
một file (`index.html`) giúp mình ôn thi giữa kì môn Biên dịch nâng cao. Đề ra điều khoản hợp đồng,
dịch hai chiều Trung ⇄ Việt. Repo đã có sẵn tài liệu bàn giao, bạn đừng dựng lại từ đầu.

**Trước khi sửa gì, làm giúp mình:**

1. Đọc `CLAUDE.md`, `docs/HANDOFF.md`, `docs/ONTOLOGY.md`, `docs/UI.md`. Bốn file này ghi nghiệp vụ,
   mô hình dữ liệu, logic chấm, design token và nợ kỹ thuật.
2. Chạy `python tools/check.py` (thêm `--render` nếu muốn chụp ảnh ba tab). Hiện phải ra
   `OK — không lỗi, 1 cảnh báo`; cảnh báo đó là nợ kỹ thuật #2 đã ghi trong HANDOFF.
3. Tóm tắt lại cho mình 5–7 dòng: trang làm gì, dữ liệu gồm gì, chấm bài ra sao. Kèm những chỗ
   trong tài liệu bạn thấy chưa rõ hoặc không khớp với code — nói thẳng, đừng gật.

**Quy tắc khi làm:**

- Câu, từ, cấu trúc mới phải lấy từ `source/`, không tự bịa. Câu mới **chỉ thêm vào cuối mảng
  `SENTS`** (id gắn theo vị trí, chèn giữa là lệch hết tiến độ đã học).
- Không đổi khoá localStorage `ldhd-v1`.
- Giữ tông hồng, giữ chữ hiển thị bằng tiếng Việt, giữ một file duy nhất.
- Sau mỗi lần sửa, chạy lại `python tools/check.py`.
- Bạn **không đăng lên claude.ai được**. Sửa xong thì báo mình, mình tự gửi `index.html` lên đăng lại
  (nhớ nhắc mình giữ capability `sample`).

**Việc đầu tiên mình muốn làm — theo thứ tự này:**

1. Chốt hai thứ đang treo trong `docs/HANDOFF.md` §7: (a) `source/` đang trống, mình sẽ bỏ file gốc
   vào, bạn nói rõ cần đúng những file nào; (b) 62/204 từ bị loại lúc chạy vì không nằm trong câu
   dịch nào — toàn từ khung hợp đồng dễ ra thi. Bạn phân tích ba hướng xử lý và khuyên mình chọn
   hướng nào, đừng tự sửa trước khi mình đồng ý.
2. Soát lại `docs/ONTOLOGY.md`: nó đang là bản nháp viết tay. Dùng skill `ontology` để kiểm các neo
   `index.html:<dòng>` còn đúng không và bổ sung chỗ thiếu.
3. Xem `docs/SKILLS.md`. Các skill đó đã có sẵn trong máy rồi, bạn xác nhận giúp mình cái nào thật
   sự hợp với trang một file này, cái nào bỏ qua.
4. Sau đó mình muốn nâng giao diện lên mức thật đẹp: đọc `docs/UI.md` trước, dùng `frontend-design`
   + `ui-ux-pro-max`, đề xuất hướng cho mình duyệt **trước khi** sửa `index.html`. Chụp trước/sau
   bằng `python tools/check.py --render`.
