#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
DAILY_DIR = PROJECT_DIR / "每日晨测"
QUESTION_DIR = DAILY_DIR / "题目"
SUMMARY_PATH = DAILY_DIR / "每日题目汇总.md"


ROW_RE_LEGACY = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$")
ROW_RE_DETAILED = re.compile(
    r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$"
)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})-题目\.md$")
SUBJECTS = ["解剖", "生理", "康复"]


def clean_cell(value: str) -> str:
    return " ".join(value.strip().split())


def parse_question_file(path: Path) -> list[dict[str, str]]:
    date_match = DATE_RE.search(path.name)
    if not date_match:
        return []
    date = date_match.group(1)
    rows: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        detailed_match = ROW_RE_DETAILED.match(line)
        legacy_match = ROW_RE_LEGACY.match(line)
        if detailed_match:
            no, subject, score, outline_module, knowledge_detail, basis, question = [
                clean_cell(item) for item in detailed_match.groups()
            ]
        elif legacy_match:
            no, subject, score, keywords, basis, question = [clean_cell(item) for item in legacy_match.groups()]
            outline_module = keywords
            knowledge_detail = keywords
        else:
            continue
        if subject not in SUBJECTS:
            continue
        rows.append(
            {
                "date": date,
                "no": no,
                "subject": subject,
                "score": score,
                "outline_module": outline_module,
                "knowledge_detail": knowledge_detail,
                "basis": basis,
                "question": question,
                "source": f"[[题目/{date}-题目|{date} 题目]]",
            }
        )
    return rows


def build_markdown(rows: list[dict[str, str]]) -> str:
    lines: list[str] = [
        "# 每日晨测题目汇总",
        "",
        f"统计范围：{rows[0]['date']} 至 {rows[-1]['date']}；共 {len(rows)} 题。",
        "",
        "更新规则：每日晨测生成后，重新扫描 `题目/YYYY-MM-DD-题目.md` 并按科目汇总；本表只收录题目，不收录答案。",
        "",
    ]
    for subject in SUBJECTS:
        subject_rows = [row for row in rows if row["subject"] == subject]
        lines.extend(
            [
                f"## {subject}",
                "",
                f"共 {len(subject_rows)} 题。",
                "",
        "| 日期 | 原题号 | 分值 | 考纲模块 | 知识点明细 | 依据 | 题目 | 来源 |",
        "|---|---:|---:|---|---|---|---|---|",
            ]
        )
        for row in subject_rows:
            lines.append(
                "| {date} | {no} | {score} | {outline_module} | {knowledge_detail} | {basis} | {question} | {source} |".format(**row)
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    rows: list[dict[str, str]] = []
    for path in sorted(QUESTION_DIR.glob("????-??-??-题目.md")):
        rows.extend(parse_question_file(path))
    if not rows:
        raise SystemExit(f"No question rows found in {QUESTION_DIR}")
    rows.sort(key=lambda row: (SUBJECTS.index(row["subject"]), row["date"], int(row["no"])))
    SUMMARY_PATH.write_text(build_markdown(rows), encoding="utf-8")
    print(f"Wrote {SUMMARY_PATH} ({len(rows)} questions)")


if __name__ == "__main__":
    main()
