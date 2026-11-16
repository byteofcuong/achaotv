#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiem tra tinh cho index.html cua "Luyen dich hop dong".

Chay:
    python tools/check.py
    python tools/check.py --render       # them kiem tra render bang Playwright (neu co)
    python tools/check.py --json         # in them ban tom tat dang JSON

Khong can mang, khong can cai them goi nao cho phan kiem tra tinh.
Exit code 0 = dat, 1 = co loi.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # de terminal Windows in duoc tieng Viet
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

HAN = re.compile(r"[㐀-䶿一-鿿豈-﫿]")
ALLOWED_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com"}

# No ky thuat da biet (xem docs/HANDOFF.md muc "Nợ kỹ thuật"): 62 tu trong VOCAB_RAW
# khong xuat hien trong cau dich nao nen bi loai luc chay. Day la nguong chot: them tu
# mo nua se thanh LOI, giam xuong thi ha nguong nay.
BASELINE_ORPHAN_VOCAB = 62

ERRORS: list[str] = []
WARNS: list[str] = []
INFO: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNS.append(msg)


def info(msg: str) -> None:
    INFO.append(msg)


# ---------------------------------------------------------------- doc trich


def slice_between(html: str, start: str, end: str, name: str) -> str | None:
    i = html.find(start)
    if i < 0:
        err(f"Khong tim thay `{start.strip()}` trong index.html ({name}).")
        return None
    j = html.find(end, i)
    if j < 0:
        err(f"Khong tim thay doan ket `{end.strip()}` cua {name}.")
        return None
    # `end` bat dau bang "\n]" hoac "\n}" — lay ca dau dong bao de JSON hop le
    return html[i + len(start) - 1 : j + 2]


BARE_KEYS = ("dir", "tag", "doc", "src", "ref", "note", "pat", "vi", "ex", "exvi", "ans", "opts")
KEY_RE = re.compile(r"([{,]\s*)(" + "|".join(BARE_KEYS) + r")\s*:")


def js_to_json(block: str, name: str):
    """Doi literal JS (key khong co nhay) sang JSON roi parse."""
    fixed = KEY_RE.sub(lambda m: f'{m.group(1)}"{m.group(2)}":', block)
    try:
        return json.loads(fixed)
    except json.JSONDecodeError as e:
        err(f"Khong parse duoc {name}: {e}. Co the da them key moi hoac dung dau nhay la.")
        return None


# ---------------------------------------------------------------- kiem tra


def check_shell(html: str) -> None:
    if '<html lang="vi"' not in html:
        err('Thieu lang="vi" tren the <html>.')
    if "<!DOCTYPE html>" not in html:
        err("Thieu <!DOCTYPE html>.")
    if not html.rstrip().endswith("</html>"):
        err("File khong ket thuc bang </html>.")
    if "<title>Luyện dịch hợp đồng</title>" not in html:
        err("Thieu hoac doi <title>Luyện dịch hợp đồng</title>.")
    if 'name="viewport"' not in html:
        err("Thieu meta viewport (trang phai dung duoc tren dien thoai).")

    scripts = re.findall(r"<script\b([^>]*)>", html)
    if len(scripts) != 1:
        err(f"Trang phai co dung 1 the <script> noi tuyen, dang co {len(scripts)}.")
    for attrs in scripts:
        if "src=" in attrs:
            err("Co <script src=...>: trang phai la mot file, khong tai script ngoai.")

    urls = re.findall(r'(?:href|src)="(https?://[^"]+)"', html)
    for u in urls:
        host = u.split("/")[2]
        if host not in ALLOWED_HOSTS:
            err(f"Tai nguyen ngoai khong cho phep: {u} (chi cho {', '.join(sorted(ALLOWED_HOSTS))}).")

    if 'rel="stylesheet"' not in html:
        warn("Khong thay link stylesheet Google Fonts.")


def check_theme(html: str) -> None:
    for token in ("--paper:", "--seal:", "--seal-soft:", "--jade:", "--amber:", "--line:", "--ink:"):
        if token not in html:
            err(f"Thieu bien mau {token} (phai giu he token tong hong).")
    if "#ff5c9a" not in html:
        err("Mat mau nhan hong --seal:#ff5c9a.")
    if "prefers-color-scheme:dark" not in html:
        err("Mat khoi dark mode (@media prefers-color-scheme:dark).")
    if '[data-theme="dark"]' not in html:
        warn("Khong thay nhanh :root[data-theme=\"dark\"].")
    if "prefers-reduced-motion" not in html:
        warn("Khong thay @media prefers-reduced-motion.")


UI_STRINGS = [
    "Dịch câu", "Từ vựng", "Cấu trúc",
    "Chấm bài", "Xem bản tham khảo", "Bản tham khảo (theo tài liệu)",
    "Thẻ ghi nhớ", "Trắc nghiệm", "Đã nhớ", "Chưa nhớ",
    "Điền cấu trúc", "Tự đặt câu", "Bảng tra",
    "Trung → Việt", "Việt → Trung",
    "Lỗi cần sửa", "Từ nên nhớ", "Hỏi thêm về câu này",
]


def check_vietnamese_ui(html: str) -> None:
    for s in UI_STRINGS:
        if s not in html:
            err(f"Mat chu hien thi tieng Viet: “{s}”.")
    for bad in ("Submit", "Next question", "Score:", "Loading...", "Check answer"):
        if bad in html:
            err(f"Co chu hien thi tieng Anh: “{bad}”.")


def check_runtime_contract(html: str) -> None:
    if 'const KEY="ldhd-v1"' not in html:
        err('Khoa localStorage phai la "ldhd-v1" — doi khoa la xoa sach tien do cua nguoi dung.')
    if 'id:"s"+(i+1)' not in html:
        err("Mat cach sinh id `s<N>` theo vi tri trong SENTS (quy tac chi them cau vao cuoi mang).")
    if 'window.claude.use("sample")' not in html:
        err("Mat phan xin quyen sample() cua Claude.")
    if html.count("if(!sample)") < 2:
        err("Mat nhanh du phong khi khong co sample() (phai con doc duoc ban tham khao).")
    for code in ("not_granted", "rate_limited"):
        if code not in html:
            warn(f"Khong xu ly rieng loi sample `{code}`.")
    for key in ("diem", "ket_luan", "nhan_xet", "loi", "ban_dich_goi_y", "tu_can_nho"):
        if f'"{key}"' not in html:
            err(f"Prompt cham bai mat truong JSON `{key}`.")
    if "Math.max(0,Math.min(10" not in html:
        err("Mat phan kep diem ve khoang 0-10.")
    if "Đúng" not in html or "Gần đúng" not in html:
        err("Mat nhan ket luan Đúng / Gần đúng / Sai.")


def zh_of(s: dict) -> str:
    return s["src"] if s["dir"] == "zh-vi" else s["ref"]


def vi_of(s: dict) -> str:
    return s["ref"] if s["dir"] == "zh-vi" else s["src"]


def check_sents(sents: list[dict]) -> None:
    allowed = {"dir", "tag", "doc", "src", "ref", "note"}
    seen_src: dict[str, int] = {}
    for n, s in enumerate(sents, 1):
        extra = set(s) - allowed
        if extra:
            err(f"Cau {n}: key la {sorted(extra)} (chi dung {sorted(allowed)}).")
        for k in ("dir", "tag", "doc", "src", "ref"):
            if not str(s.get(k, "")).strip():
                err(f"Cau {n}: thieu `{k}`.")
        if s.get("dir") not in ("zh-vi", "vi-zh"):
            err(f"Cau {n}: dir = {s.get('dir')!r}, phai la 'zh-vi' hoac 'vi-zh'.")
            continue
        src, ref = s.get("src", ""), s.get("ref", "")
        if s["dir"] == "zh-vi":
            if not HAN.search(src):
                err(f"Cau {n} (zh-vi): `src` khong co chu Han.")
            if HAN.search(ref):
                err(f"Cau {n} (zh-vi): `ref` co chu Han — ban tham khao phai la tieng Viet.")
        else:
            if HAN.search(src):
                err(f"Cau {n} (vi-zh): `src` co chu Han — cau goc phai la tieng Viet.")
            if not HAN.search(ref):
                err(f"Cau {n} (vi-zh): `ref` khong co chu Han.")
        if src in seen_src:
            err(f"Cau {n}: trung `src` voi cau {seen_src[src]}.")
        else:
            seen_src[src] = n


def check_vocab(vocab_raw: dict, sents: list[dict]) -> list[dict]:
    flat: list[dict] = []
    for setname, lines in vocab_raw.items():
        if not isinstance(lines, list) or not lines:
            err(f"Bo tu “{setname}” rong hoac khong phai mang.")
            continue
        for line in lines:
            parts = str(line).split("|")
            if len(parts) not in (2, 3):
                err(f"Bo tu “{setname}”: dong {line!r} phai co dang zh|vi hoac zh|vi|giai-thich.")
                continue
            if any(not p.strip() for p in parts):
                err(f"Bo tu “{setname}”: dong {line!r} co o trong.")
                continue
            zh, vi = parts[0], parts[1]
            alt = parts[2] if len(parts) == 3 else ""
            flat.append({"set": setname, "zh": zh, "vi": vi, "alt": alt})

    zh_texts = [zh_of(s) for s in sents]
    orphan, dupes = [], []
    seen: set[str] = set()
    for v in flat:
        v["parts"] = [p.strip() for p in v["zh"].split(" / ") if p.strip()]
        v["hits"] = sum(1 for t in zh_texts if any(p in t for p in v["parts"]))
        if v["hits"] == 0:
            orphan.append(v["zh"])
        if v["zh"] in seen:
            dupes.append(v["zh"])
        seen.add(v["zh"])

    if orphan:
        msg = (
            f"{len(orphan)}/{len(flat)} tu khong xuat hien trong cau dich nao nen bi loai luc chay "
            f"(nguong chot {BASELINE_ORPHAN_VOCAB}): {', '.join(orphan[:8])}"
            + (" …" if len(orphan) > 8 else "")
        )
        if len(orphan) > BASELINE_ORPHAN_VOCAB:
            err(msg + " — them tu khong co trong cau dich la lam no xau them.")
        else:
            warn(msg)
    if dupes:
        err(f"{len(dupes)} tu bi khai trung trong VOCAB_RAW: {', '.join(sorted(set(dupes))[:12])}")
    return [v for v in flat if v["hits"]]


def check_structs(structs: list[dict], sents: list[dict]) -> list[dict]:
    zh_texts = [zh_of(s) for s in sents]
    kept = []
    for n, st in enumerate(structs, 1):
        for k in ("pat", "vi", "ex", "exvi", "ans", "opts"):
            if not st.get(k):
                err(f"Cau truc {n}: thieu `{k}`.")
        opts = st.get("opts") or []
        if len(opts) < 2:
            err(f"Cau truc {n} ({st.get('pat')}): can it nhat 2 phuong an.")
        if st.get("ans") and st["ans"] not in opts:
            err(f"Cau truc {n} ({st.get('pat')}): `ans` khong nam trong `opts`.")
        if len(set(opts)) != len(opts):
            err(f"Cau truc {n} ({st.get('pat')}): `opts` co phuong an trung nhau.")
        if st.get("ans") and not HAN.search(st["ans"]):
            warn(f"Cau truc {n}: `ans` khong co chu Han ({st['ans']!r}).")
        hits = sum(1 for t in zh_texts if st.get("ans") and st["ans"] in t)
        if hits == 0:
            err(
                f"Cau truc {n} ({st.get('pat')}): `ans` = {st.get('ans')!r} khong co trong cau dich nao "
                "nen bi loai luc chay."
            )
        else:
            st["hits"] = hits
            kept.append(st)
        if st.get("ex") and not HAN.search(st["ex"]):
            err(f"Cau truc {n}: vi du `ex` phai la tieng Trung.")
    return kept


# ---------------------------------------------------------------- render


def check_render() -> None:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception:
        warn("Khong co Playwright nen bo qua --render (pip install playwright && playwright install chromium).")
        return

    outdir = ROOT / "tools" / "_render"
    outdir.mkdir(exist_ok=True)
    logs: list[str] = []
    with sync_playwright() as p:
        b = None
        tried = []
        for kw in ({}, {"channel": "msedge"}, {"channel": "chrome"}):
            try:
                b = p.chromium.launch(**kw)
                info(f"Render bang chromium{(' ' + kw['channel']) if kw else ' (ban kem Playwright)'}.")
                break
            except Exception as e:  # noqa: BLE001
                tried.append(f"{kw or 'bundled'}: {str(e).splitlines()[0]}")
        if b is None:
            warn(
                "Playwright khong mo duoc trinh duyet nen bo qua --render. "
                "Chay `playwright install chromium` roi thu lai. Chi tiet: " + " | ".join(tried)
            )
            return
        pg = b.new_page(viewport={"width": 420, "height": 900})
        pg.on("console", lambda m: logs.append(f"{m.type}: {m.text}") if m.type == "error" else None)
        pg.on("pageerror", lambda e: logs.append(f"pageerror: {e}"))
        pg.goto(INDEX.as_uri())
        pg.wait_for_timeout(800)
        for view, must in (
            ("dich", "Chấm bài"),
            ("tu-vung", "Đã nhớ"),
            ("cau-truc", "Điền cấu trúc"),
        ):
            pg.goto(INDEX.as_uri() + "#" + view)
            pg.wait_for_timeout(400)
            body = pg.inner_text("body")
            if must not in body:
                err(f"Render tab #{view}: khong thay “{must}” tren trang.")
            pg.screenshot(path=str(outdir / f"{view}.png"), full_page=True)
        stats = pg.inner_text("#stats")
        if "Đã chấm" not in stats:
            err("Render: thanh thong ke khong hien thi.")
        else:
            info(f"Render thong ke: {' | '.join(stats.split(chr(10)))}")
        b.close()
    for l in logs:
        err(f"Console loi khi render: {l}")
    info(f"Anh chup luu o {outdir}")


# ---------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", action="store_true", help="mo trang bang Playwright de kiem tra")
    ap.add_argument("--json", action="store_true", help="in them ban tom tat dang JSON")
    args = ap.parse_args()

    if not INDEX.exists():
        print(f"FAIL: khong thay {INDEX}")
        return 1

    html = INDEX.read_text(encoding="utf-8")
    check_shell(html)
    check_theme(html)
    check_vietnamese_ui(html)
    check_runtime_contract(html)

    sents = vocab = structs = None
    b = slice_between(html, "const SENTS = [", "\n].map(", "SENTS")
    if b:
        sents = js_to_json(b, "SENTS")
    b = slice_between(html, "const VOCAB_RAW = {", "\n};", "VOCAB_RAW")
    if b:
        vocab = js_to_json(b, "VOCAB_RAW")
    b = slice_between(html, "const STRUCTS = [", "\n];", "STRUCTS")
    if b:
        structs = js_to_json(b, "STRUCTS")

    summary: dict = {}
    if isinstance(sents, list):
        check_sents(sents)
        dirs = {"zh-vi": 0, "vi-zh": 0}
        for s in sents:
            if s.get("dir") in dirs:
                dirs[s["dir"]] += 1
        summary["cau"] = len(sents)
        summary["chieu"] = dirs
        summary["dieu_khoan"] = sorted({s.get("tag", "") for s in sents})
        summary["van_ban"] = sorted({s.get("doc", "") for s in sents})
        summary["cau_co_note"] = sum(1 for s in sents if s.get("note"))
    if isinstance(vocab, dict) and isinstance(sents, list):
        kept = check_vocab(vocab, sents)
        summary["tu_vung_khai"] = sum(len(v) for v in vocab.values())
        summary["tu_vung_dung"] = len(kept)
        summary["bo_tu"] = {k: len(v) for k, v in vocab.items()}
    if isinstance(structs, list) and isinstance(sents, list):
        kept_s = check_structs(structs, sents)
        summary["cau_truc_khai"] = len(structs)
        summary["cau_truc_dung"] = len(kept_s)

    if args.render:
        check_render()

    print("=" * 62)
    print("KIEM TRA index.html — Luyen dich hop dong")
    print("=" * 62)
    if summary:
        print(f"  Cau dich        : {summary.get('cau')} "
              f"(Trung→Viet {summary.get('chieu', {}).get('zh-vi')}, "
              f"Viet→Trung {summary.get('chieu', {}).get('vi-zh')}; "
              f"{summary.get('cau_co_note')} cau co ghi chu vai ben A/B)")
        print(f"  Van ban nguon   : {len(summary.get('van_ban', []))}")
        print(f"  Dieu khoan (tag): {len(summary.get('dieu_khoan', []))}")
        print(f"  Tu vung         : {summary.get('tu_vung_dung')}/{summary.get('tu_vung_khai')} dung duoc")
        print(f"  Cau truc        : {summary.get('cau_truc_dung')}/{summary.get('cau_truc_khai')} dung duoc")
    for m in INFO:
        print(f"  i  {m}")
    for m in WARNS:
        print(f"  !  {m}")
    for m in ERRORS:
        print(f"  X  {m}")
    print("-" * 62)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print("-" * 62)
    if ERRORS:
        print(f"FAIL — {len(ERRORS)} loi, {len(WARNS)} canh bao.")
        return 1
    print(f"OK — khong loi, {len(WARNS)} canh bao.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
