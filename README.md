# Luyện dịch hợp đồng

Trang web một file để ôn thi giữa kì môn **Biên dịch nâng cao**: dịch điều khoản hợp đồng hai chiều
Trung ⇄ Việt, Claude chấm bài và chỉ lỗi.

62 câu từ 7 hợp đồng · 142 thuật ngữ · 26 cấu trúc pháp lý · 3 chế độ luyện.

## Chạy

Mở `index.html` bằng trình duyệt là xong — không build, không cài gì.
Phần **chấm bài tự động** chỉ chạy khi trang được đăng trên claude.ai (cần capability `sample`);
mở bằng `file://` thì vẫn luyện được, chỉ tự đối chiếu bản tham khảo.

Bản đang dùng: https://claude.ai/artifact/UtdA5rZWUkAxgddEhCRAzP

## Kiểm tra

```bash
python tools/check.py
```

```bash
python tools/check.py --render
```

## Tài liệu

| File | Nội dung |
|---|---|
| [CLAUDE.md](CLAUDE.md) | Luật khi sửa — đọc trước |
| [docs/HANDOFF.md](docs/HANDOFF.md) | Bàn giao: nghiệp vụ, dữ liệu, logic chấm, nợ kỹ thuật, cách đăng lại |
| [docs/ONTOLOGY.md](docs/ONTOLOGY.md) | Khái niệm miền, ràng buộc, từ điển code ↔ UI ↔ 中文 |
| [docs/UI.md](docs/UI.md) | Design token, nguyên tắc giao diện |
| [docs/SKILLS.md](docs/SKILLS.md) | Skill nào dùng cho việc nào |
| [source/README.md](source/README.md) | Tài liệu gốc cần bỏ vào |
