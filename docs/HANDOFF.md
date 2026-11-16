# Bàn giao — Luyện dịch hợp đồng

Tài liệu này mô tả trang đang chạy, đủ để sửa nó mà không phải đọc lại toàn bộ 645 dòng
`index.html`. Số liệu trong đây lấy từ `python tools/check.py --json` ngày 16/11/2026.

---

## 1. Nghiệp vụ

**Người dùng:** một sinh viên, ôn thi giữa kì môn Biên dịch nâng cao (tiếng Trung thương mại).

**Dạng đề thi:** đề cho một đoạn/điều khoản hợp đồng, yêu cầu dịch **hai chiều** Trung ⇄ Việt.
Thi viết tay, không tra từ điển. Nên trang này không phải app dịch — nó là **phòng tập**: gõ bản
dịch của mình, bị chấm, thấy lỗi, nhớ thuật ngữ.

**Trang giải quyết đúng ba việc, đúng ba tab:**

| Tab | Việc | Vì sao cần |
|---|---|---|
| **Dịch câu** | Hiện câu gốc → sinh viên gõ bản dịch → Claude chấm 0–10, chỉ lỗi, sửa lại chính bài của sinh viên, đưa bản tham khảo của giáo trình | Luyện đúng thứ sẽ thi |
| **Từ vựng** | Thẻ ghi nhớ + trắc nghiệm, hai chiều 中→Việt và Việt→中 | Thi không được tra từ; thuật ngữ hợp đồng là phần mất điểm nhiều nhất |
| **Cấu trúc** | Điền khuyết cấu trúc pháp lý / tự đặt câu / bảng tra | Văn phong hợp đồng nằm ở khuôn câu (`未经…不得…`, `…的，视为…`), không nằm ở từ lẻ |

**Nguyên tắc sư phạm đã cài vào dữ liệu — giữ nguyên khi mở rộng:** từ vựng và cấu trúc **không rời
khỏi câu**. Mỗi từ, mỗi cấu trúc đều được tự động nối ngược về những câu dịch chứa nó; thẻ ghi nhớ
và câu điền khuyết đều trích từ câu thật trong bài. Từ nào không xuất hiện trong câu nào thì bị
loại khỏi app lúc chạy (xem §7, nợ kỹ thuật #2).

---

## 2. Nguồn ngữ liệu

62 câu trong `SENTS` rút từ **7 văn bản**:

| Văn bản (`doc`) | Loại | Chiều |
|---|---|---|
| `买卖合同` | HĐ mua bán (bản tiếng Trung) | zh-vi |
| `租赁合同 (练习 1)` | HĐ thuê nhà, bài tập 1 | zh-vi |
| `房屋租赁合同协议书` | HĐ thuê nhà | zh-vi |
| `HĐ mua bán ĐH Tây Nguyên` | HĐ mua bán thiết bị (bản tiếng Việt) | vi-zh |
| `HĐ thuê nhà 2013` | HĐ thuê nhà | vi-zh |
| `HĐ thuê nhà Văn Khê 2018` | HĐ thuê nhà | vi-zh |
| `HĐ bán hàng cao su (练习 2)` | HĐ ngoại thương, bài tập 2 | vi-zh |

Hai bộ từ `Từ bôi vàng` / `Từ bôi đỏ` là từ giảng viên tô màu trong tài liệu phát tay — đó là chỉ
dấu trọng tâm thi, **ưu tiên giữ**.

> **Khoảng trống cần chủ dự án lấp:** thư mục `source/` hiện **chưa có file gốc**. Quy tắc "câu mới
> phải lấy từ `source/`" vì thế chưa kiểm chứng được. Xem `source/README.md` để biết cần bỏ gì vào.
> Bản tổng hợp trên claude.ai: doc **"Ôn giữa kì Biên dịch nâng cao — Hợp đồng (Trung ⇄ Việt)"**
> (https://claude.ai/artifact/7jJxtBbYkD453sYZZeLXRH).

---

## 3. Bản đồ `index.html` (645 dòng)

| Dòng | Nội dung |
|---|---|
| 1–9 | `<head>`, `lang="vi"`, Google Fonts (Quicksand, Be Vietnam Pro, Noto Sans SC, ZCOOL KuaiLe) |
| 10–143 | `<style>` — token màu, dark mode, toàn bộ component |
| 145–200 | HTML: header + thống kê, `<nav class="tabs">`, ba `<section class="view">` rỗng (nội dung do JS đổ vào) |
| 203–314 | **DATA** — `SENTS` (204), `VOCAB_RAW` (269), `STRUCTS` (286) |
| 315–333 | **LINK TO SENTENCES** — nối từ/cấu trúc ngược về câu, hàm `hl()` tô vàng |
| 334–352 | **STATE** — localStorage, `renderStats()` |
| 353–361 | **ROUTING** — hash `#dich` / `#tu-vung` / `#cau-truc` |
| 362–383 | **AI** — `sample()`, `parseJSON()`, thông báo lỗi tiếng Việt |
| 384–502 | **DỊCH CÂU** — lọc, `renderSentence()`, `grade()`, `followUp()` |
| 503–574 | **TỪ VỰNG** — thẻ ghi nhớ, trắc nghiệm |
| 575–635 | **CẤU TRÚC** — điền khuyết, tự đặt câu, bảng tra |
| 636–643 | **INIT** — render lần đầu + xin quyền `sample` |

---

## 4. Mô hình dữ liệu

### 4.1 `SENTS` — 62 câu (Trung→Việt 35, Việt→Trung 27)

```js
{
  dir:  "zh-vi" | "vi-zh",   // chiều dịch
  tag:  "Thanh toán",        // điều khoản — 17 giá trị, đổ vào ô lọc
  doc:  "买卖合同",           // văn bản gốc
  src:  "...",               // câu đề bài
  ref:  "...",               // bản dịch tham khảo của giáo trình
  note: "..."                // tuỳ chọn — cảnh báo ngữ cảnh, 4 câu đang có
}
```

Sau đó `.map((s,i)=>({...s,id:"s"+(i+1)}))` gắn id **theo vị trí**. Đây là lý do của luật
"chỉ thêm vào cuối" trong `CLAUDE.md`.

`note` hiện chỉ dùng cho một việc, và là việc quan trọng nhất của hợp đồng: **ai là bên A**.
Trong `HĐ mua bán ĐH Tây Nguyên` bên A là bên **mua**; trong `HĐ thuê nhà Văn Khê 2018` bên A là
bên **thuê** — ngược thông lệ 甲方 = bên bán/bên cho thuê. Dịch sai vai là sai cả điều khoản.

17 điều khoản: Mở đầu · Hàng hóa – giá · Giá – chi phí · Thanh toán · Giao hàng – rủi ro ·
Chất lượng – khiếu nại · Quyền và nghĩa vụ · Tiền thuê – đặt cọc · Thời hạn – gia hạn ·
Chấm dứt hợp đồng · Thanh lý hợp đồng · Vi phạm – bồi thường · Bất khả kháng · Bảo mật ·
Tranh chấp · Hiệu lực – số bản · Điều khoản khác.

### 4.2 `VOCAB_RAW` — 204 mục khai báo, 142 thực dùng

Object: tên bộ → mảng chuỗi `"中文|tiếng Việt"` hoặc `"中文|tiếng Việt|giải thích bằng tiếng Trung"`.

6 bộ: `Khung & các bên` (25) · `Mua bán` (55) · `Thuê nhà` (35) · `Bổ sung từ câu dịch` (49) ·
`Từ bôi vàng` (20) · `Từ bôi đỏ` (20).

- `出租人 / 出租方` — dấu ` / ` tách **biến thể viết**, cả hai đều được dò trong câu.
- Phần giải thích (ô thứ 3) chỉ bộ `Từ bôi vàng` có — hiện ở mặt sau thẻ: "Giải thích bằng từ khác".

### 4.3 `STRUCTS` — 26 cấu trúc, cả 26 đều dùng được

```js
{ pat:"未经…书面同意，…不得…", vi:"Chưa được … đồng ý bằng văn bản thì không được…",
  ex:"…", exvi:"…", ans:"未经", opts:["未经","经过","除非","无论"] }
```

`ans` là chuỗi dùng để (a) nối cấu trúc về câu, (b) khoét trống trong bài điền. `opts` phải chứa
`ans`. `ex`/`exvi` là ví dụ minh hoạ, chỉ hiện ở chế độ "Tự đặt câu".

### 4.4 Liên kết tự sinh (dòng 315–332)

```
zhOf(s)  → mặt tiếng Trung của câu (src nếu zh-vi, ref nếu vi-zh)
viOf(s)  → mặt tiếng Việt
v.sents  → các câu chứa từ v      → từ không có câu nào thì BỊ XOÁ khỏi VOCAB
st.sents → các câu chứa cấu trúc  → cấu trúc không có câu nào thì BỊ XOÁ khỏi STRUCTS
s.words / s.structs → chiều ngược lại, dùng cho ô "Từ mới & cấu trúc trong câu này"
```

Khử trùng từ chạy **ngược mảng**, nên khi một chữ Hán xuất hiện ở hai bộ, **bản khai sau thắng**
và nghĩa tiếng Việt của bản trước bị bỏ.

---

## 5. Logic chấm

### 5.1 Chấm bản dịch — `grade()` (dòng 454)

Gọi `sample(prompt, {modelTier:"default"})`. Prompt đóng vai **giảng viên Biên dịch nâng cao**, được
đưa: chiều dịch, tên văn bản, điều khoản, `note` nếu có, câu gốc, bản tham khảo (kèm câu
"KHÔNG bắt sinh viên dịch giống hệt"), bản của sinh viên.

Bốn tiêu chí chấm: (1) đúng và đủ nghĩa; (2) thuật ngữ pháp lý chuẩn; (3) văn phong trang trọng,
không khẩu ngữ; (4) ngữ pháp, chính tả, số liệu, ngày tháng, **đúng vai bên A / bên B**.

Trả về **một** object JSON:

```json
{ "diem": 0-10, "ket_luan": "Đúng|Gần đúng|Sai", "nhan_xet": "1–2 câu",
  "loi": [{"doan":"trích bài sinh viên","van_de":"vì sao sai","sua":"cách viết đúng"}],
  "ban_dich_goi_y": "bản sửa, giữ tối đa cách diễn đạt của sinh viên",
  "tu_can_nho": [{"tu":"中文","nghia":"tiếng Việt"}] }
```

Ngưỡng: **8–10 Đúng · 5–7 Gần đúng · 0–4 Sai** (tối đa 5 lỗi, 4 từ). `parseJSON()` cắt từ `{` đầu
đến `}` cuối nên model lỡ bọc markdown vẫn đọc được. `diem` bị kẹp về 0–10 rồi mới lưu.
`cls()` quyết màu con dấu: xanh ngọc ≥8, hổ phách ≥5, hồng còn lại.

Sau khi chấm: lưu điểm + nguyên object kết quả, cập nhật thống kê, hiện con dấu, danh sách lỗi
(gạch ngang phần sai → phần sửa), bản sửa, bản tham khảo, từ nên nhớ, và ô **hỏi thêm** —
`followUp()` gọi `sample` lần nữa, giới hạn 120 từ, có stream từng đoạn.

### 5.2 Chấm câu tự đặt — `gradeMake()` (dòng 617)

JSON gọn hơn: `{diem, ket_luan, nhan_xet, cau_sua, nghia}`. **Không lưu** vào localStorage.

### 5.3 Khi không có `sample()`

`window.claude.use("sample")` chỉ có trên claude.ai và chỉ sau khi người dùng bấm cho phép. Mở file
bằng `file://` thì không có. Khi đó: hiện banner vàng tiếng Việt và **tự mở bản tham khảo** để
sinh viên tự đối chiếu. Hai mã lỗi được nói riêng bằng tiếng Việt: `not_granted` (chưa cấp quyền),
`rate_limited` (hỏi quá nhanh).

---

## 6. Trạng thái & tiến độ

```js
localStorage["ldhd-v1"] = {
  tr: { "s12": { text:"bản dịch đang gõ", score:8, result:{…JSON chấm…} } },
  vk: { "违约金": 1 }     // từ đã nhớ
}
```

- Bản nháp lưu **theo từng ký tự gõ**, nên đóng tab không mất bài.
- Thống kê đầu trang: số câu đã chấm / 62, điểm trung bình, số từ đã nhớ / 142.
- Không có nút xoá tiến độ, không có export/import. Xoá dữ liệu trình duyệt là mất sạch.
- Mỗi URL artifact là một origin riêng → đăng ở link khác là tiến độ không theo sang.

---

## 7. Nợ kỹ thuật & chỗ cần quyết

Đánh dấu ✱ = nên xử lý trước kì thi; còn lại là ghi để biết.

1. ✱ **`source/` trống.** Luật "không bịa dữ liệu" chưa có gì để đối chiếu.
2. ✱ **62/204 từ bị loại lúc chạy** vì không nằm trong câu dịch nào (`出卖人`, `买受人`,
   `法定代表人`, `税号`, `开户行`, `检验证书`…). Đây toàn là từ khung hợp đồng, rất dễ ra thi.
   Ba hướng: (a) thêm câu từ `source/` chứa chúng; (b) bỏ bộ lọc, cho phép từ không gắn câu;
   (c) xoá khỏi `VOCAB_RAW`. **Chưa chọn.** `tools/check.py` đang chốt ngưỡng ở 62 — vượt là báo lỗi.
3. ✱ **id theo vị trí** (`s1…s62`): chèn/xoá câu giữa mảng làm lệch toàn bộ tiến độ, không có
   migration. Muốn an toàn lâu dài thì chuyển sang id cố định + script chuyển đổi.
4. **Không lọc được theo văn bản.** Có 7 hợp đồng nhưng chỉ lọc theo chiều và điều khoản.
5. **17 tag cho 62 câu**, trong đó `Hàng hóa – giá` và `Giá – chi phí` gần trùng nhau — taxonomy
   nên gom lại (xem `docs/ONTOLOGY.md`).
6. **Điền khuyết chỉ khoét lần xuất hiện đầu** (`zt.replace(ans, …)`); câu nào chứa cấu trúc hai
   lần thì lần thứ hai lộ đáp án.
7. **Trắc nghiệm bộ nhỏ (<8 từ) lấy phương án nhiễu từ toàn bộ từ vựng**, khác chủ đề nên dễ đoán.
8. **"Tự đặt câu" không lưu kết quả** — làm xong là mất.
9. **Mã chết:** `lastResult` (dòng 389) và `isZh` (dòng 344) không ai dùng; `VOCAB.reverse();
   VOCAB.reverse();` (cuối dòng 321) là no-op; `--font-zh` và `--font-zh-sans` khai báo y hệt nhau.
10. **Không có nút đặt lại toàn bộ tiến độ** (chỉ đặt lại được từng bộ từ).

---

## 8. Nghiệm thu

```bash
python tools/check.py
```

```bash
python tools/check.py --render
```

`check.py` tự rút `SENTS` / `VOCAB_RAW` / `STRUCTS` ra khỏi HTML và kiểm:

- khung trang: `lang="vi"`, một `<script>` nội tuyến duy nhất, không tài nguyên ngoài ngoài Google Fonts;
- token màu hồng + dark mode còn đủ;
- 18 chuỗi chữ tiếng Việt trên UI còn nguyên, không có chữ Anh lọt vào;
- hợp đồng runtime: khoá `ldhd-v1`, cách sinh id, xin quyền `sample`, nhánh dự phòng, 6 trường JSON chấm bài, kẹp điểm 0–10;
- dữ liệu: đủ trường, đúng chiều (zh-vi phải có chữ Hán ở `src` và không có ở `ref`, vi-zh ngược lại), không trùng câu, dòng từ vựng đúng dạng `中文|Việt[|giải thích]`, không khai trùng từ, `opts` chứa `ans`, cấu trúc nào cũng có câu chứa nó.

`--render` mở trang bằng Chromium/Edge sẵn có (không cần tải trình duyệt riêng), đi qua cả ba tab,
bắt lỗi console và chụp `tools/_render/*.png`. Không có Playwright thì chỉ cảnh báo, không fail.

Kết quả hiện tại: **OK — không lỗi, 1 cảnh báo** (chính là nợ #2).

---

## 9. Đăng lại lên claude.ai

Claude Code **không đăng được** artifact này. Quy trình:

1. Chạy `python tools/check.py` cho sạch, commit.
2. Chủ dự án mở chat claude.ai, gửi kèm `index.html` và bảo: *"Cập nhật artifact Luyện dịch hợp đồng
   bằng file này, giữ nguyên capability `sample`."*
   Artifact: **Luyện dịch hợp đồng** — https://claude.ai/artifact/UtdA5rZWUkAxgddEhCRAzP
3. ⚠️ **Phải giữ khai báo capability `{"sample":{}}`.** Mất nó là mất toàn bộ chức năng chấm bài,
   trang tụt xuống chỉ còn đối chiếu bản tham khảo.
4. Đăng **đè lên đúng link cũ**. Link mới = origin mới = mất sạch tiến độ đã học.
5. Mở lại trang, bấm cho phép khi Claude hỏi quyền, chấm thử một câu để chắc chắn.
