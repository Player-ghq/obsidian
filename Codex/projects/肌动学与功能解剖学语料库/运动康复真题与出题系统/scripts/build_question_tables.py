import csv
import re
from pathlib import Path


ROOT = Path("work/ocr")
OUT = Path("outputs")
OUT.mkdir(exist_ok=True)


SUBJECT_ALIASES = {
    "解剖": "解剖",
    "解": "解剖",
    "人体及运动解剖学": "解剖",
    "运动解剖学": "解剖",
    "人体运动学": "康复",
    "生理": "生理",
    "人体生理学": "生理",
    "运动生理学": "生理",
    "康复": "康复",
    "运动康复评定与运动治疗": "康复",
    "肌肉骨骼康复学": "康复",
    "神经康复学": "康复",
}

TYPE_RE = re.compile(r"(名词解释|简答题?|论述题?|病例分析题|单选题|多选题)")
QUESTION_RE = re.compile(r"^\s*([一二三四五六七八九十]+|[0-9]+|[（(][0-9]+[）)])[\.\、．)]\s*(.+)")
HEADER_RE = re.compile(r"^(20)?2[345]考研专业课真题|^2[345]考研专业课真题")
SCHOOL_HINT_RE = re.compile(r"(大学|学院|研究院|研究生).*?(运动康复|康复|医学技术|运动训练|运动人体科学)?")
POINT_RE = re.compile(r"[（(]?\s*(\d{1,3})\s*分\s*[）)]?")
BARE_TRAILING_POINT_RE = re.compile(r"(?<!\d)(\d{1,3})\s*$")


def clean_line(line: str) -> str:
    line = line.strip()
    exact_noise = {
        "南烛考研", "南烛康复考研", "南烛运动人体科学考研", "南烛", "烛考研",
        "康复考研", "考研", "南烟", "南烛扇", "商烛考研", "南烛考矿",
        "（更多康复考研院校专业课真题，请关注公众号：南烛康复考研）",
        "（更多康复考研院校专业课真题，请关注公众号：南烛考研）",
        "（更多运动人体科学考研真题，请关注公众号：南烛运动人体科学考研）",
    }
    if line in exact_noise:
        return ""
    return re.sub(r"\s+", " ", line).strip()


def infer_subject(line: str, current: str) -> str:
    if re.search(r"(大学|学院|研究院|真题|考研|公众号)", line):
        return current
    normalized = line.replace("：", "").replace(":", "").strip()
    for key, value in SUBJECT_ALIASES.items():
        if normalized == key or normalized.startswith(key + "（") or normalized.startswith(key + "("):
            return value
    if "解剖" in line and len(line) <= 35:
        return "解剖"
    if "生理" in line and len(line) <= 35:
        return "生理"
    if "康复" in line and len(line) <= 35:
        return "康复"
    return current


def classify_subject(question: str, current: str) -> str:
    if "动作分析" in question or "解剖学分析" in question:
        return "解剖"
    if re.search(r"内囊|神经束", question):
        return "解剖"
    if current:
        return current
    q = question
    anatomy_kw = "关节|骨|肌|韧带|半月板|解剖|脊柱|肩|髋|膝|踝|足弓|颅|内囊|神经束|内耳|体表|动脉|静脉|肝|肺|肾"
    phys_kw = "稳态|血液|心血管|体温|静息电位|动作电位|激素|血糖|呼吸|血压|摄氧量|乳酸阈|能量|内环境|氧解离|肝脏.*生理|应急反应|细胞膜|钠钾泵"
    rehab_kw = "康复|评定|治疗|方案|损伤|疼痛|脊髓损伤|脑病|脑损伤|骨折|肩袖|颈椎病|置换术|偏瘫|ASIA|Brunnstrom|训练"
    if re.search(rehab_kw, q):
        return "康复"
    if re.search(phys_kw, q):
        return "生理"
    if re.search(anatomy_kw, q):
        return "解剖"
    return "待判定"


def infer_question_type(line: str, current: str) -> str:
    m = TYPE_RE.search(line)
    if not m:
        return current
    t = m.group(1)
    if t.startswith("简答"):
        return "简答"
    if t.startswith("论述"):
        return "论述"
    if t == "名词解释":
        return "名词解释"
    if t == "病例分析题":
        return "病例分析"
    if t == "单选题":
        return "单选"
    if t == "多选题":
        return "多选"
    return t


def infer_section_score(line: str, current: str) -> str:
    if not TYPE_RE.search(line):
        return current
    for pattern in [
        r"[*x×]\s*(\d{1,3})\s*分",
        r"每题\s*(\d{1,3})\s*[～~-]?\s*(?:\d{1,3})?\s*分",
        r"一题\s*(\d{1,3})\s*分",
    ]:
        m = re.search(pattern, line)
        if m:
            return m.group(1)
    return current


def extract_score(question: str, fallback: str) -> str:
    m = POINT_RE.search(question)
    if m:
        return m.group(1)
    m = BARE_TRAILING_POINT_RE.search(question)
    if m:
        return m.group(1)
    return fallback


def strip_score(question: str) -> str:
    question = POINT_RE.sub("", question).strip()
    question = BARE_TRAILING_POINT_RE.sub("", question).strip()
    return question


def source_image_for_ocr(path: Path, year: str, workspace_root: Path) -> str:
    candidates = []
    pics_dir = workspace_root / "work" / "extracted" / year / "pics"
    for suffix in [".webp", ".png", ".jpeg", ".jpg", ".gif", ".svg"]:
        candidates.append(pics_dir / f"{path.stem}{suffix}")
    for candidate in candidates:
        if candidate.exists():
            return str(candidate.resolve())
    return ""


def parse_file(path: Path, year: str, workspace_root: Path = Path(".")):
    raw_lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    raw_header = "\n".join(x.strip() for x in raw_lines[:10])
    lines = [clean_line(x) for x in raw_lines]
    lines = [x for x in lines if x]
    joined = "\n".join(lines)
    year_header_ok = False
    short_year = year[-2:]
    year_header_ok = (
        f"{year}考研专业课真题" in raw_header
        or f"{short_year}考研专业课真题" in raw_header
        or re.search(rf"{year}级?.*真题", raw_header)
        or f"{year}考研专业课真题" in joined[:260]
        or f"{short_year}考研专业课真题" in joined[:260]
        or re.search(rf"{year}级?.*真题", joined[:260])
    )
    if not year_header_ok:
        return []

    school = ""
    code = ""
    for i, line in enumerate(lines[:12]):
        if re.search(r"(大学|学院|研究院|体育总局).*?(运动康复|医学技术|康复|运动人体科学|运动训练)", line):
            school = line
            if i + 1 < len(lines):
                code = lines[i + 1] if re.search(r"\d{3}|综合|基础", lines[i + 1]) else ""
            break
    if not school:
        for line in lines[:12]:
            if "大学" in line or "学院" in line:
                school = line
                break

    current_subject = ""
    current_type = ""
    current_score = ""
    records = []
    last_question = None
    for line in lines:
        current_subject = infer_subject(line, current_subject)
        current_type = infer_question_type(line, current_type)
        current_score = infer_section_score(line, current_score)
        m = QUESTION_RE.match(line)
        implicit_first = None
        if not m and line.startswith(("、", "，", ",")) and current_type:
            implicit_first = line.lstrip("、，, ").strip()
        if not m:
            if implicit_first:
                text = implicit_first
            elif last_question and len(line) > 8 and not TYPE_RE.search(line) and "考研专业课真题" not in line:
                last_question["question_text"] += line
                for marker in ["解剖：", "生理：", "康复：", "运动解剖学：", "运动生理学："]:
                    if marker in last_question["question_text"]:
                        last_question["question_text"] = last_question["question_text"].split(marker)[0].strip()
                continue
            else:
                continue
        else:
            text = m.group(2).strip()
        for marker in ["解剖：", "生理：", "康复：", "运动解剖学：", "运动生理学："]:
            if marker in text:
                text = text.split(marker)[0].strip()
        if not text or text in {"略"}:
            continue
        if re.search(r"^\d+题[*x×]", text):
            continue
        score = extract_score(text, current_score)
        text = strip_score(text)
        rec = {
            "year": year,
            "school_track": school,
            "exam_code": code,
            "subject": classify_subject(text, current_subject),
            "question_type": current_type or "待判定",
            "score": score,
            "question_text": text,
            "confidence": "OCR待复核",
            "source_ocr": str(path.resolve()),
            "source_image": source_image_for_ocr(path, year, workspace_root),
        }
        records.append(rec)
        last_question = rec
    return records


def main():
    all_records = []
    for year in ["2023", "2024", "2025"]:
        for path in sorted((ROOT / year).glob("*.txt")):
            all_records.extend(parse_file(path, year, Path(".")))

    csv_path = OUT / "运动康复考研真题分类表.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["year", "school_track", "exam_code", "subject", "question_type", "score", "question_text", "confidence", "source_ocr", "source_image"])
        writer.writeheader()
        writer.writerows(all_records)

    md_path = OUT / "运动康复考研真题分类整理.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# 运动康复考研真题分类整理\n\n")
        f.write("来源：用户提供的 `23年.zip`、`24年.zip`、`25年.zip` 图片包，经 RapidOCR 识别。OCR 错字未逐字人工校对，题干按可读主体整理，置信度统一标为 `OCR待复核`。\n\n")
        current = None
        for rec in all_records:
            key = (rec["year"], rec["school_track"], rec["exam_code"])
            if key != current:
                current = key
                f.write(f"\n## {rec['year']} {rec['school_track']}\n\n")
                if rec["exam_code"]:
                    f.write(f"- 科目/代码：{rec['exam_code']}\n")
                f.write(f"- OCR 来源：`{rec['source_ocr']}`\n")
                if rec["source_image"]:
                    f.write(f"- 复核原图：`{rec['source_image']}`\n")
                f.write("\n")
                f.write("| 分类 | 题型 | 分值 | 题干 | 复核原图 |\n|---|---|---:|---|---|\n")
            q = rec["question_text"].replace("|", "｜")
            image = rec["source_image"].replace("|", "｜")
            f.write(f"| {rec['subject']} | {rec['question_type']} | {rec['score']} | {q} | `{image}` |\n")

    print(f"records={len(all_records)}")
    print(csv_path)
    print(md_path)


if __name__ == "__main__":
    main()
