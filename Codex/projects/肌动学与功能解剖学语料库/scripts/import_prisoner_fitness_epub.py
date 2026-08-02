#!/usr/bin/env python3
"""Import the Convict Conditioning EPUB into this Obsidian corpus project."""

from __future__ import annotations

import argparse
import html
import posixpath
import re
import textwrap
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "container": "urn:oasis:names:tc:opendocument:xmlns:container",
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "ncx": "http://www.daisy.org/z3986/2005/ncx/",
}

BOOK_SLUG = "囚徒健身全集-共4册"


class XHTMLTextParser(HTMLParser):
    block_tags = {
        "address",
        "article",
        "aside",
        "blockquote",
        "br",
        "div",
        "dl",
        "dt",
        "dd",
        "figcaption",
        "figure",
        "footer",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hr",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "pre",
        "section",
        "table",
        "td",
        "th",
        "tr",
        "ul",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style"}:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in self.block_tags:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag in self.block_tags:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        raw = html.unescape(raw)
        lines = []
        for line in raw.splitlines():
            line = re.sub(r"[ \t\u3000]+", " ", line).strip()
            if line:
                lines.append(line)
            elif lines and lines[-1] != "":
                lines.append("")
        return "\n\n".join(line for line in lines if line).strip()


def parse_xml(data: bytes) -> ET.Element:
    return ET.fromstring(data)


def safe_stem(text: str, fallback: str) -> str:
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"[\\/:*?\"<>|#]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:80] or fallback


def read_epub_package(epub: zipfile.ZipFile) -> tuple[str, ET.Element]:
    container = parse_xml(epub.read("META-INF/container.xml"))
    rootfile = container.find(".//container:rootfile", NS)
    if rootfile is None:
        raise RuntimeError("EPUB container does not contain a rootfile entry.")
    opf_path = rootfile.attrib["full-path"]
    return opf_path, parse_xml(epub.read(opf_path))


def metadata(opf: ET.Element) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, tag in {
        "title": "dc:title",
        "creator": "dc:creator",
        "language": "dc:language",
        "identifier": "dc:identifier",
        "publisher": "dc:publisher",
        "date": "dc:date",
    }.items():
        node = opf.find(f".//{tag}", NS)
        if node is not None and node.text:
            result[key] = node.text.strip()
    return result


def manifest(opf: ET.Element, opf_dir: str) -> dict[str, dict[str, str]]:
    items: dict[str, dict[str, str]] = {}
    for item in opf.findall(".//opf:manifest/opf:item", NS):
        item_id = item.attrib["id"]
        href = item.attrib["href"]
        full_path = posixpath.normpath(posixpath.join(opf_dir, href))
        items[item_id] = {
            "href": href,
            "path": full_path,
            "media_type": item.attrib.get("media-type", ""),
            "properties": item.attrib.get("properties", ""),
        }
    return items


def spine(opf: ET.Element, items: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for itemref in opf.findall(".//opf:spine/opf:itemref", NS):
        item_id = itemref.attrib["idref"]
        if item_id in items:
            entries.append({"id": item_id, **items[item_id]})
    return entries


def title_from_text(text: str, path: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line and line not in {"未知", "封面页", "目录", "Contents"}:
            return line[:80]
    return posixpath.basename(path)


def infer_volume(path: str, title: str) -> str:
    match = re.search(r"part(\d{4})", path)
    part_num = int(match.group(1)) if match else -1
    if 1 <= part_num <= 24:
        return "囚徒健身"
    if 25 <= part_num <= 59:
        return "囚徒健身2"
    if 60 <= part_num <= 82:
        return "囚徒爆发力"
    if 83 <= part_num <= 143:
        return "囚徒增肌"
    if "囚徒健身2" in title:
        return "囚徒健身2"
    if "囚徒爆发力" in title:
        return "囚徒爆发力"
    if "囚徒增肌" in title:
        return "囚徒增肌"
    if "囚徒健身" in title:
        return "囚徒健身"
    return "总目录与附属页"


def wrap_markdown(title: str, frontmatter: dict[str, str], body: str) -> str:
    fm = ["---"]
    for key, value in frontmatter.items():
        fm.append(f"{key}: {value}")
    fm.append("---")
    fm.append("")
    fm.append(f"# {title}")
    fm.append("")
    fm.append(body.strip())
    fm.append("")
    return "\n".join(fm)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("epub", type=Path)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    args = parser.parse_args()

    epub_path = args.epub.expanduser().resolve()
    project = args.project.resolve()

    with zipfile.ZipFile(epub_path) as epub:
        opf_path, opf = read_epub_package(epub)
        opf_dir = posixpath.dirname(opf_path)
        meta = metadata(opf)
        items = manifest(opf, opf_dir)
        entries = spine(opf, items)

        imported = []
        for idx, entry in enumerate(entries, start=1):
            if entry["media_type"] not in {
                "application/xhtml+xml",
                "text/html",
                "application/x-dtbncx+xml",
            }:
                continue
            data = epub.read(entry["path"])
            parser_obj = XHTMLTextParser()
            parser_obj.feed(data.decode("utf-8", errors="replace"))
            text = parser_obj.text()
            if not text:
                continue
            title = title_from_text(text, entry["path"])
            volume = infer_volume(entry["path"], title)
            stem = f"{idx:04d}-{safe_stem(title, entry['id'])}"
            frontmatter = {
                "type": "epub-extract",
                "book": "囚徒健身全集（共4册）",
                "volume": volume,
                "source_path": entry["path"],
                "spine_index": str(idx),
            }
            markdown = wrap_markdown(title, frontmatter, text)
            extracted_path = project / "extracted" / BOOK_SLUG / f"{stem}.md"
            chunk_path = project / "chunks" / "by-book" / BOOK_SLUG / f"prisoner-fitness-{stem}.md"
            cleaned_path = project / "cleaned" / "by-book" / BOOK_SLUG / f"prisoner-fitness-{stem}.md"
            write_text(extracted_path, markdown)
            write_text(chunk_path, markdown)
            write_text(cleaned_path, markdown)
            imported.append(
                {
                    "idx": idx,
                    "title": title,
                    "volume": volume,
                    "source": entry["path"],
                    "extracted": extracted_path.relative_to(project).as_posix(),
                    "chunk": chunk_path.relative_to(project).as_posix(),
                    "cleaned": cleaned_path.relative_to(project).as_posix(),
                }
            )

    toc_lines = [
        "# 囚徒健身全集（共4册）EPUB 目录",
        "",
        f"- EPUB 原件: `{epub_path}`",
        f"- EPUB 标题: {meta.get('title', '未知')}",
        f"- 作者: {meta.get('creator', '未知')}",
        f"- 语言: {meta.get('language', '未知')}",
        f"- 导入条目数: {len(imported)}",
        "",
    ]
    current_volume = None
    for item in imported:
        if item["volume"] != current_volume:
            current_volume = item["volume"]
            toc_lines.extend(["", f"## {current_volume}", ""])
        toc_lines.append(
            f"- {item['idx']:04d}. {item['title']} | `{item['source']}` | `{item['cleaned']}`"
        )
    write_text(project / "index" / "prisoner-fitness-toc.md", "\n".join(toc_lines) + "\n")

    retrieval_lines = []
    for item in imported:
        retrieval_lines.append(
            (
                '{{"book":"囚徒健身全集（共4册）","volume":"{volume}",'
                '"title":"{title}","source_path":"{source}",'
                '"cleaned_path":"{cleaned}","chunk_path":"{chunk}"}}'
            ).format(
                volume=item["volume"],
                title=item["title"].replace('"', '\\"'),
                source=item["source"].replace('"', '\\"'),
                cleaned=item["cleaned"],
                chunk=item["chunk"],
            )
        )
    write_text(project / "index" / "prisoner-fitness-retrieval-map.jsonl", "\n".join(retrieval_lines) + "\n")

    summary = textwrap.dedent(
        f"""
        Imported {len(imported)} EPUB spine entries from:
        {epub_path}

        Wrote:
        - extracted/{BOOK_SLUG}/
        - chunks/by-book/{BOOK_SLUG}/
        - cleaned/by-book/{BOOK_SLUG}/
        - index/prisoner-fitness-toc.md
        - index/prisoner-fitness-retrieval-map.jsonl
        """
    ).strip()
    print(summary)


if __name__ == "__main__":
    main()
