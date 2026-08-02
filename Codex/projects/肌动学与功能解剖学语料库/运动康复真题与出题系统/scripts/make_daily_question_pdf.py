from __future__ import annotations

import argparse
from pathlib import Path
import re
import textwrap

from PIL import Image, ImageDraw, ImageFont


DEFAULT_BASE = Path(
    "/Users/HaoQi/Documents/Codex/obsidian-vault-codex-codex-codex-todo-2/"
    "Codex/projects/运动康复真题与出题系统/每日晨测"
)
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"


def wrap_by_chars(text: str, chars: int) -> str:
    return "\n".join(
        textwrap.wrap(text, width=chars, break_long_words=True, replace_whitespace=False)
    )


def draw_multiline(draw: ImageDraw.ImageDraw, xy, text: str, font, fill: str, line_gap=6):
    x, y = xy
    for line in text.splitlines():
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap


def parse_question_md(path: Path) -> tuple[str, str, list[tuple[str, str, str, str, str, str]]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = next((line.lstrip("# ").strip() for line in lines if line.startswith("# ")), path.stem)
    meta = next((line.strip() for line in lines if line.startswith("结构：")), "")

    rows: list[tuple[str, str, str, str, str, str]] = []
    for line in lines:
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            continue
        if cells[0] in {"题号", "---"} or set(cells[0]) <= {"-", ":"}:
            continue
        if cells[0].isdigit():
            rows.append(tuple(cells))  # type: ignore[arg-type]

    if len(rows) != 9:
        raise ValueError(f"Expected 9 question rows, found {len(rows)} in {path}")
    return title, meta, rows


def default_paths(date: str, base: Path) -> tuple[Path, Path, Path]:
    question_md = base / "题目" / f"{date}-题目.md"
    question_pdf = base / "题目" / f"{date}-题目.pdf"
    render_source = Path("work/pdf-render") / f"{date}-question-source.png"
    return question_md, question_pdf, render_source


def make_pdf(
    title: str,
    meta: str,
    rows: list[tuple[str, str, str, str, str, str]],
    out_pdf: Path,
    out_png: Path,
):
    # A4 landscape at 200 dpi.
    width, height = 2339, 1654
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(FONT, 44)
    meta_font = ImageFont.truetype(FONT, 24)
    head_font = ImageFont.truetype(FONT, 23)
    cell_font = ImageFont.truetype(FONT, 22)

    margin = 58
    y = 42
    title = re.sub(r"\s+", " ", title)
    tw = draw.textbbox((0, 0), title, font=title_font)[2]
    draw.text(((width - tw) / 2, y), title, font=title_font, fill="#111111")
    y += 56
    meta = meta.replace("结构：", "").strip()
    mw = draw.textbbox((0, 0), meta, font=meta_font)[2]
    draw.text(((width - mw) / 2, y), meta, font=meta_font, fill="#333333")
    y += 45

    col_w = [80, 105, 88, 255, 150, width - 2 * margin - 80 - 105 - 88 - 255 - 150]
    row_h = 142
    header_h = 48
    table_w = sum(col_w)
    header = ["题号", "科目", "分值", "模块/关键词", "依据", "题目"]

    draw.rectangle((margin, y, margin + table_w, y + header_h), fill="#1F4E79")
    x = margin
    for i, h in enumerate(header):
        bbox = draw.textbbox((0, 0), h, font=head_font)
        draw.text(
            (x + (col_w[i] - (bbox[2] - bbox[0])) / 2, y + 11),
            h,
            font=head_font,
            fill="white",
        )
        x += col_w[i]

    y0 = y + header_h
    for r, row in enumerate(rows):
        top = y0 + r * row_h
        bottom = top + row_h
        fill = "#F7FAFC" if r % 2 else "white"
        draw.rectangle((margin, top, margin + table_w, bottom), fill=fill)
        x = margin
        for i, text in enumerate(row):
            if i == 5:
                wrapped = wrap_by_chars(text, 43)
            elif i == 3:
                wrapped = wrap_by_chars(text, 10)
            elif i == 4:
                wrapped = wrap_by_chars(text, 5)
            else:
                wrapped = text
            if i <= 2:
                bbox = draw.textbbox((0, 0), wrapped, font=cell_font)
                draw.text(
                    (x + (col_w[i] - (bbox[2] - bbox[0])) / 2, top + 55),
                    wrapped,
                    font=cell_font,
                    fill="#111111",
                )
            else:
                draw_multiline(draw, (x + 12, top + 22), wrapped, cell_font, "#111111")
            x += col_w[i]

    table_bottom = y0 + len(rows) * row_h
    x = margin
    for w in col_w:
        draw.line((x, y, x, table_bottom), fill="#9EB6CB", width=2)
        x += w
    draw.line((margin + table_w, y, margin + table_w, table_bottom), fill="#9EB6CB", width=2)
    for i in range(len(rows) + 2):
        yy = y if i == 0 else y + header_h + (i - 1) * row_h
        draw.line((margin, yy, margin + table_w, yy), fill="#9EB6CB", width=2)

    out_png.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_png)
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_pdf, "PDF", resolution=200.0)


def main():
    parser = argparse.ArgumentParser(description="Generate one-page A4 daily exam PDF from question MD.")
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format.")
    parser.add_argument("--base", type=Path, default=DEFAULT_BASE, help="每日晨测 base directory.")
    parser.add_argument("--question-md", type=Path, help="Override question markdown path.")
    parser.add_argument("--out-pdf", type=Path, help="Override output PDF path.")
    parser.add_argument("--out-png", type=Path, help="Override rendered source PNG path.")
    args = parser.parse_args()

    question_md, question_pdf, render_source = default_paths(args.date, args.base)
    question_md = args.question_md or question_md
    question_pdf = args.out_pdf or question_pdf
    render_source = args.out_png or render_source

    title, meta, rows = parse_question_md(question_md)
    make_pdf(title, meta, rows, question_pdf, render_source)
    print(question_pdf)


if __name__ == "__main__":
    main()
