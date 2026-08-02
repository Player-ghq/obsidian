import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path("work/pydeps").resolve()))

from PIL import Image
from rapidocr_onnxruntime import RapidOCR


def natural_key(path: Path):
    return [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", str(path))]


def main():
    if len(sys.argv) != 4:
        raise SystemExit("usage: batch_ocr.py <input-dir> <output-dir> <manifest.jsonl>")
    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    manifest_path = Path(sys.argv[3])
    output_dir.mkdir(parents=True, exist_ok=True)
    ocr = RapidOCR()
    records = []
    for path in sorted(input_dir.rglob("*"), key=natural_key):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".gif", ".svg"}:
            continue
        try:
            im = Image.open(path)
            w, h = im.width, im.height
        except Exception as exc:
            records.append({"file": str(path), "status": "image-open-failed", "error": str(exc)})
            continue
        area = w * h
        if area < 250_000:
            records.append({"file": str(path), "status": "skipped-small", "width": w, "height": h})
            continue
        out = output_dir / (path.stem + ".txt")
        if out.exists() and out.stat().st_size > 0:
            text = out.read_text(encoding="utf-8", errors="ignore")
            records.append({"file": str(path), "status": "cached", "width": w, "height": h, "chars": len(text), "out": str(out)})
            continue
        try:
            result, elapse = ocr(str(path))
            lines = []
            if result:
                for row in result:
                    if len(row) >= 2 and row[1]:
                        lines.append(str(row[1]).strip())
            text = "\n".join([x for x in lines if x])
            out.write_text(text, encoding="utf-8")
            records.append({"file": str(path), "status": "ok", "width": w, "height": h, "chars": len(text), "lines": len(lines), "out": str(out), "elapsed": elapse})
            print(f"OK {path.name} {w}x{h} chars={len(text)}")
        except Exception as exc:
            records.append({"file": str(path), "status": "ocr-failed", "width": w, "height": h, "error": str(exc)})
            print(f"FAIL {path.name}: {exc}")
    with manifest_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
