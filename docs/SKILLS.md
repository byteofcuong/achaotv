# Skill dùng cho dự án này

Các skill dưới đây **đã có sẵn** trong Claude Code của máy này, không phải tải gì thêm. Vấn đề chỉ
là dùng đúng cái, đúng lúc. Gọi bằng `/<tên>` hoặc để Claude tự nạp.

## Thiết kế giao diện

| Skill | Dùng khi | Không dùng khi |
|---|---|---|
| `frontend-design` | Cần hướng thẩm mỹ cho một màn mới, chọn typography, tránh giao diện "AI mặc định" | Chỉ sửa vài px |
| `ui-ux-pro-max` | Cần tra cụ thể: bảng màu sản phẩm, cặp font, guideline UX, biểu đồ. Có dữ liệu tra tại chỗ (79 style, 192 palette, 74 cặp font, 119 guideline UX) | Cần ý tưởng tổng thể — dùng `frontend-design` |
| `redesign-skill` | Làm lại toàn bộ trang mà **không được vỡ chức năng** — có bước audit trước | Trang mới tinh |
| `taste-skill-design` | Trang đích/portfolio, chống giao diện rập khuôn | Trang công cụ như trang này (ít hợp) |
| `design-system` | Muốn chuẩn hoá token ba lớp (primitive → semantic → component) | Dự án một file như hiện tại — hơi nặng |
| `ui-styling` | Khi dự án dùng Tailwind/shadcn | **Không hợp ở đây** — trang này là CSS thuần, một file |
| `artifact-design` | Trước khi viết/đăng artifact trên claude.ai | Sửa file local |

**Cho trang này:** `frontend-design` để quyết hướng → `ui-ux-pro-max` để tra chi tiết →
`redesign-skill` nếu làm lại lớn. Luôn đọc `docs/UI.md` trước, vì nó mới là ràng buộc.

## Phát triển sản phẩm

| Skill | Dùng khi |
|---|---|
| `agent-skills:spec` / `spec-driven-development` | Thêm tính năng đáng kể (ví dụ: xuất/nhập tiến độ, chế độ thi thử) — viết đặc tả trước khi code |
| `agent-skills:plan` / `planning-and-task-breakdown` | Chia việc lớn thành bước có tiêu chí nghiệm thu |
| `agent-skills:build` / `incremental-implementation` | Làm từng lát mỏng, chạy `check.py` sau mỗi lát |
| `agent-skills:test` / `test-driven-development` | Mở rộng `tools/check.py` — viết kiểm tra hỏng trước |
| `agent-skills:review` / `code-review-and-quality` | Trước khi chủ dự án đăng lại |
| `agent-skills:constraints` | Muốn chốt chuẩn chất lượng thành file `CONSTRAINTS.md` |
| `ontology` | Cập nhật `docs/ONTOLOGY.md` khi mô hình dữ liệu đổi; skill này neo khái niệm vào file và sinh script kiểm |
| `webapp-testing` | Kiểm tra tương tác thật bằng Playwright, ngoài `check.py --render` |
| `team` | Chia việc cho nhiều agent — xem mục cuối `CLAUDE.md`, phần lớn task ở đây nên làm inline |
| `agent-skills:source-driven-development` | Khi thêm ngữ liệu mới và cần bám sát `source/` |

## Thứ tự mặc định cho một việc mới

1. Đọc `CLAUDE.md` → `docs/HANDOFF.md`.
2. Việc nhỏ (sửa chữ, thêm vài câu): làm thẳng, rồi `python tools/check.py`.
3. Việc vừa (một tính năng): `agent-skills:plan` → làm → `check.py` → báo chủ dự án.
4. Việc lớn (đổi giao diện, đổi mô hình dữ liệu): `agent-skills:spec` → `frontend-design`
   hoặc `redesign-skill` → `check.py --render` → `agent-skills:review`.
