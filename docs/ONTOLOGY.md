# Ontology — Luyện dịch hợp đồng

Hai tầng khái niệm. **Tầng ứng dụng** là thứ có trong code. **Tầng miền** là thứ môn học dạy, nằm
trong nội dung câu chữ chứ không thành biến — nhưng chấm bài sai hay đúng là do nó.

Mỗi khái niệm có neo: `index.html:<dòng>`. Đổi code thì sửa neo ở đây.
Kiểm bằng `python tools/check.py` (phần kiểm dữ liệu chính là ràng buộc trong tài liệu này).

---

## A. Tầng ứng dụng

### A.1 Thực thể

| Khái niệm | Trong code | Neo | Định danh | Ghi chú |
|---|---|---|---|---|
| **Câu luyện** | phần tử `SENTS` | `index.html:204` | `id = "s" + (vị trí+1)` | Đơn vị luyện tập. 62 câu. |
| **Chiều dịch** | `dir` | `index.html:204` | `zh-vi` \| `vi-zh` | Quyết định mặt nào là đề, mặt nào là đáp án. |
| **Điều khoản** | `tag` | `index.html:204` | chuỗi tiếng Việt | 17 giá trị, là phân loại nghiệp vụ. |
| **Văn bản nguồn** | `doc` | `index.html:204` | chuỗi | 7 hợp đồng. Chưa dùng để lọc. |
| **Ghi chú ngữ cảnh** | `note` | `index.html:204` | — | Chỉ dùng cảnh báo vai bên A/bên B. 4 câu có. |
| **Thuật ngữ** | phần tử `VOCAB` | `index.html:269,283` | chuỗi Hán `zh` | Khai 204, dùng 142. |
| **Bộ từ** | khoá của `VOCAB_RAW` | `index.html:269` | tên bộ | 6 bộ. |
| **Biến thể viết** | `v.parts` | `index.html:318` | — | Tách bằng ` / `, ví dụ `出租人 / 出租方`. |
| **Cấu trúc** | phần tử `STRUCTS` | `index.html:286` | `pat` | 26 khuôn câu pháp lý. |
| **Khoá điền** | `ans` | `index.html:286` | — | Vừa là đáp án, vừa là chuỗi để nối về câu. |
| **Lượt chấm** | object JSON trả về | `index.html:454` | — | `diem`, `ket_luan`, `nhan_xet`, `loi[]`, `ban_dich_goi_y`, `tu_can_nho[]`. |
| **Lỗi dịch** | `loi[i]` | `index.html:436` | — | `doan` (trích bài) → `sua`, kèm `van_de`. |
| **Tiến độ dịch** | `store.tr[id]` | `index.html:335` | id câu | `{text, score, result}`. |
| **Từ đã nhớ** | `store.vk[zh]` | `index.html:335` | chuỗi Hán | Có khoá = đã nhớ. |

### A.2 Quan hệ

```
Văn bản nguồn 1 ──< n Câu luyện          (doc)
Điều khoản    1 ──< n Câu luyện          (tag)
Chiều dịch    1 ──< n Câu luyện          (dir)

Thuật ngữ     n >──< n Câu luyện         (v.sents / s.words   — tự sinh, index.html:319,323)
Cấu trúc      n >──< n Câu luyện         (st.sents / s.structs — tự sinh, index.html:322,323)

Câu luyện     1 ──  0..1 Tiến độ dịch    (store.tr[id])
Tiến độ dịch  1 ──  0..1 Lượt chấm       (result)
Lượt chấm     1 ──< 0..5 Lỗi dịch
Lượt chấm     1 ──< 0..4 Thuật ngữ gợi nhớ   (tu_can_nho — chuỗi tự do, KHÔNG nối vào VOCAB)
Thuật ngữ     1 ──  0..1 Từ đã nhớ       (store.vk[zh])
Bộ từ         1 ──< n Thuật ngữ
```

Hai quan hệ n–n đều **tự sinh bằng cách dò chuỗi con**, không khai tay: một từ thuộc về một câu
khi mặt tiếng Trung của câu chứa chuỗi đó.

### A.3 Vòng đời

**Câu luyện** (theo `store.tr[id]`):

```
chưa đụng → đang gõ (có text, chưa score) → đã chấm (có score 0–10)
                                   ↑___________________|   chấm lại ghi đè
```
Không có trạng thái "đã xong"; bộ lọc *Chỉ câu chưa chấm* dựa vào `typeof score === "number"`.

**Thuật ngữ**: `chưa nhớ → đã nhớ`. Lên "đã nhớ" bằng hai đường: bấm **Đã nhớ** trên thẻ, hoặc
chọn đúng trong trắc nghiệm. Bấm **Chưa nhớ** thì xoá cờ **và đẩy thẻ xuống cuối lượt**.

**Lượt thẻ / lượt trắc nghiệm / lượt điền khuyết** là trạng thái tạm, **không lưu** — tải lại trang
là mất. Chỉ `tr` và `vk` được lưu.

### A.4 Ràng buộc nghiệp vụ

| # | Ràng buộc | Vì sao | Kiểm bởi |
|---|---|---|---|
| R1 | Câu mới chỉ thêm vào **cuối** `SENTS` | id theo vị trí, tiến độ gắn theo id | luật trong `CLAUDE.md`; `check.py` kiểm cách sinh id |
| R2 | `dir=zh-vi` ⇒ `src` có chữ Hán, `ref` không; `vi-zh` ⇒ ngược lại | sai là đề bài hiện nhầm mặt | `check.py` |
| R3 | `src` không được trùng nhau | tránh luyện lặp | `check.py` |
| R4 | Dòng từ vựng đúng dạng `中文\|Việt[\|giải thích]`, không ô trống | tách sai thì thẻ hỏng | `check.py` |
| R5 | Không khai trùng một chữ Hán ở hai bộ | bản khai sau thắng, nghĩa trước bị nuốt | `check.py` |
| R6 | `opts` phải chứa `ans`, không có phương án trùng | bài điền không có đáp án đúng | `check.py` |
| R7 | Mỗi cấu trúc phải có ít nhất 1 câu chứa `ans` | nếu không, bị xoá lúc chạy | `check.py` |
| R8 | Từ phải có ít nhất 1 câu chứa nó | nguyên tắc "từ không rời khỏi câu" | `check.py` (cảnh báo, ngưỡng 62 — xem nợ #2) |
| R9 | Câu có vai bên A ngược thông lệ **phải** có `note` | dịch sai vai là sai điều khoản | **chưa tự động kiểm** |
| R10 | Điểm luôn nằm trong 0–10, nhãn khớp ngưỡng 8/5 | ổn định con dấu và thống kê | `check.py` kiểm phần kẹp điểm |

---

## B. Tầng miền — hợp đồng Trung ⇄ Việt

Đây là thứ bộ chấm đang đánh giá và là thứ sinh viên phải thuộc.

### B.1 Vai

| 中文 | Tiếng Việt | Thông lệ | Bẫy |
|---|---|---|---|
| 甲方 | bên A | bên bán / bên cho thuê | **Không phải lúc nào cũng vậy** — xem `note` của câu |
| 乙方 | bên B | bên mua / bên thuê | |
| 出卖人 / 买受人 | bên bán / bên mua | | chỉ có trong bảng từ, chưa có câu |
| 出租人(方) / 承租人(方) | bên cho thuê / bên thuê | | |
| 违约方 / 守约方 | bên vi phạm / bên tuân thủ | | |
| 承运人 / 保险人 | người vận tải / người bảo hiểm | | |
| 法定代表人 / 委托代理人 | người đại diện theo pháp luật / người được uỷ quyền | | |

### B.2 Điều khoản (= `tag`) ↔ tên tiếng Trung

| `tag` | 中文 |
|---|---|
| Mở đầu | 鉴于条款 / 合同前言 |
| Hàng hóa – giá *(nên gộp vào Giá – chi phí)* | 标的与价格 |
| Giá – chi phí | 价格与费用 |
| Thanh toán | 付款方式 |
| Giao hàng – rủi ro | 交付与风险 |
| Chất lượng – khiếu nại | 质量与异议 |
| Quyền và nghĩa vụ | 双方权利义务 |
| Tiền thuê – đặt cọc | 租金与押金 |
| Thời hạn – gia hạn | 租期与续租 |
| Chấm dứt hợp đồng | 合同的解除与终止 |
| Thanh lý hợp đồng | 合同清算 |
| Vi phạm – bồi thường | 违约与赔偿 |
| Bất khả kháng | 不可抗力 |
| Bảo mật | 保密条款 |
| Tranh chấp | 争议解决 |
| Hiệu lực – số bản | 生效与份数 |
| Điều khoản khác | 其他条款 |

### B.3 Ba cặp dễ mất điểm nhất

| 中文 | Tiếng Việt | Khác nhau ở đâu |
|---|---|---|
| 解除 / 终止 / 中止 | huỷ bỏ / chấm dứt / tạm dừng | 解除 làm hợp đồng mất hiệu lực từ đầu; 终止 dừng từ nay; 中止 chỉ tạm ngưng |
| 违约金 / 赔偿 / 滞纳金 | tiền phạt vi phạm / bồi thường / tiền phạt chậm nộp | phạt theo thoả thuận ≠ bồi thường thiệt hại thực tế ≠ phạt chậm trả |
| 应当 / 有权 / 不得 | phải / có quyền / không được | nghĩa vụ ≠ quyền ≠ điều cấm — dịch lệch là lệch trách nhiệm pháp lý |

Thêm: 视为 / 视同 "được coi là" (suy đoán pháp lý), 逾期 "quá hạn", 未经…不得… "chưa được… thì không được…".

---

## C. Từ điển — một khái niệm, ba cách gọi

| Khái niệm | Code | Chữ trên UI | 中文 |
|---|---|---|---|
| Câu luyện | `SENTS[i]` / `s` | "câu" | 句子 |
| Chiều dịch | `dir`, `dirF` | "Trung → Việt" / "Việt → Trung" | 翻译方向 |
| Điều khoản | `tag`, `tagF` | "Mọi điều khoản" | 条款 |
| Bản tham khảo | `ref` | "Bản tham khảo (theo tài liệu)" | 参考译文 |
| Bản dịch của sinh viên | `store.tr[id].text` | "Bản dịch của bạn" | 学生译文 |
| Bản sửa | `ban_dich_goi_y` | "Bản sửa từ bài của bạn" | 修改稿 |
| Chấm | `grade()` | "Chấm bài" | 批改 |
| Điểm | `diem`, `score` | con dấu `n/10` | 分数 |
| Kết luận | `ket_luan` | "Đúng / Gần đúng / Sai" | 评定 |
| Thuật ngữ | `VOCAB`, `v` | "Từ vựng", "Từ nên nhớ" | 词汇 |
| Thẻ ghi nhớ | `deck`, `renderFlash` | "Thẻ ghi nhớ" | 记忆卡 |
| Đã nhớ | `store.vk` | "Đã nhớ" | 已记住 |
| Cấu trúc | `STRUCTS`, `st` | "Cấu trúc" | 句型 |
| Điền khuyết | `cloze`, `cz` | "Điền cấu trúc" | 填空 |
| Tự đặt câu | `gradeMake()` | "Tự đặt câu" | 造句 |
| Bảng tra | `sMode="list"` | "Bảng tra" | 一览表 |

**Lệch tên đang tồn tại** (ghi để đừng lệch thêm):
`tag` trên UI gọi là "điều khoản"; `doc` không có chữ nào trên UI (chỉ hiện giá trị trần);
`vk` = *vocabulary known*; `tr` = *translation*; `pat` = *pattern* nhưng UI gọi là "cấu trúc".
