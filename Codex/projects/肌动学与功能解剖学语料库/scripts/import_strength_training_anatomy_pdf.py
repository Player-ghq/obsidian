#!/usr/bin/env python3
"""Import Strength Training Anatomy into the local Obsidian corpus."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    import pdfplumber
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: pdfplumber") from exc


BOOK = "力量训练解剖全书"
BOOK_FULL = "力量训练解剖全书：肌肉与力量的解剖学认知及科学训练方案"


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t\u3000]+", " ", text)
    lines = [line.strip() for line in text.splitlines()]
    collapsed: list[str] = []
    blank = False
    for line in lines:
        if line:
            collapsed.append(line)
            blank = False
        elif not blank:
            collapsed.append("")
            blank = True
    return "\n".join(collapsed).strip()


def safe_text(text: str) -> str:
    return text.replace('"', '\\"').replace("\n", "\\n")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def guess_heading(text: str, page_no: int) -> str:
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if len(line) <= 2:
            continue
        if re.fullmatch(r"\d+", line):
            continue
        return line[:80]
    return f"page-{page_no:04d}"


def page_markdown(page_no: int, heading: str, text: str, source_pdf: Path) -> str:
    return "\n".join(
        [
            "---",
            "type: pdf-page-extract",
            f"book: {BOOK}",
            f"full_title: {BOOK_FULL}",
            f"page: {page_no}",
            f"source_pdf: {source_pdf}",
            "---",
            "",
            f"# {BOOK} page-{page_no:04d}",
            "",
            f"## 识别标题",
            "",
            heading,
            "",
            "## 页文本",
            "",
            text or "OCR 未抽取到文字。",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--chunk-pages", type=int, default=4)
    args = parser.parse_args()

    pdf_path = args.pdf.expanduser().resolve()
    project = args.project.resolve()

    extracted_dir = project / "extracted" / BOOK
    chunk_dir = project / "chunks" / "by-book" / BOOK
    cleaned_dir = project / "cleaned" / "by-book" / BOOK
    index_dir = project / "index"

    page_records = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for idx, page in enumerate(pdf.pages, start=1):
            raw = page.extract_text(x_tolerance=1.5, y_tolerance=3) or ""
            text = normalize_text(raw)
            heading = guess_heading(text, idx)
            md = page_markdown(idx, heading, text, pdf_path)
            page_path = extracted_dir / f"page-{idx:04d}.md"
            write(page_path, md)
            page_records.append(
                {
                    "page": idx,
                    "heading": heading,
                    "chars": len(text),
                    "empty": not bool(text),
                    "path": page_path.relative_to(project).as_posix(),
                    "text": text,
                }
            )

    chunk_records = []
    for chunk_no, start in enumerate(range(1, len(page_records) + 1, args.chunk_pages), start=1):
        records = page_records[start - 1 : start - 1 + args.chunk_pages]
        end_page = records[-1]["page"]
        body = []
        for record in records:
            body.extend(
                [
                    f"## PDF p.{record['page']} | {record['heading']}",
                    "",
                    record["text"] or "OCR 未抽取到文字。",
                    "",
                ]
            )
        md = "\n".join(
            [
                "---",
                "type: pdf-chunk",
                f"book: {BOOK}",
                f"full_title: {BOOK_FULL}",
                f"page_start: {start}",
                f"page_end: {end_page}",
                f"source_pdf: {pdf_path}",
                "---",
                "",
                f"# {BOOK} p.{start}-{end_page}",
                "",
                *body,
            ]
        )
        chunk_path = chunk_dir / f"strength-training-anatomy-{chunk_no:04d}-p{start:04d}-{end_page:04d}.md"
        cleaned_path = cleaned_dir / f"strength-training-anatomy-{chunk_no:04d}-p{start:04d}-{end_page:04d}.md"
        write(chunk_path, md)
        write(cleaned_path, md)
        chunk_records.append(
            {
                "chunk": chunk_no,
                "page_start": start,
                "page_end": end_page,
                "path": cleaned_path.relative_to(project).as_posix(),
            }
        )

    toc_lines = [
        f"# {BOOK} 抽取索引",
        "",
        f"- 书名: {BOOK_FULL}",
        f"- PDF: `{pdf_path}`",
        f"- PDF 页数: {len(page_records)}",
        f"- 页级语料: `extracted/{BOOK}/`",
        f"- 清洗语料: `cleaned/by-book/{BOOK}/`",
        f"- 知识块: `chunks/by-book/{BOOK}/`",
        f"- 空文本页数: {sum(1 for r in page_records if r['empty'])}",
        "",
        "## 页级标题抽样",
        "",
    ]
    for record in page_records:
        toc_lines.append(f"- p.{record['page']:04d}: {record['heading']} | chars={record['chars']} | `{record['path']}`")
    write(index_dir / "strength-training-anatomy-page-index.md", "\n".join(toc_lines) + "\n")

    retrieval_lines = []
    for record in page_records:
        retrieval_lines.append(
            json.dumps(
                {
                    "book": BOOK,
                    "full_title": BOOK_FULL,
                    "page": record["page"],
                    "heading": record["heading"],
                    "chars": record["chars"],
                    "empty": record["empty"],
                    "path": record["path"],
                },
                ensure_ascii=False,
            )
        )
    write(index_dir / "strength-training-anatomy-retrieval-map.jsonl", "\n".join(retrieval_lines) + "\n")

    print(
        "\n".join(
            [
                f"Imported {len(page_records)} pages from {pdf_path}",
                f"Empty text pages: {sum(1 for r in page_records if r['empty'])}",
                f"Chunks: {len(chunk_records)}",
                f"Wrote extracted/{BOOK}/",
                f"Wrote chunks/by-book/{BOOK}/",
                f"Wrote cleaned/by-book/{BOOK}/",
                "Wrote index/strength-training-anatomy-page-index.md",
                "Wrote index/strength-training-anatomy-retrieval-map.jsonl",
            ]
        )
    )


if __name__ == "__main__":
    main()
