#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[0]
DAILY = PROJECT / "每日晨测"
QUESTION_DIR = DAILY / "题目"
ANSWER_DIR = DAILY / "答案"
SUPP_DIR = ROOT / "qa" / "背诵稿" / "晨测补充"


SUBJECT_DIR = {
    "解剖": ROOT / "qa" / "背诵稿",
    "生理": ROOT / "运动生理学-王瑞元苏全生",
    "康复": SUPP_DIR,
}


ANATOMY_TARGETS = [
    (("骨盆", "髋"), "qa/背诵稿/09-骨盆与髋关节-完整版.md；qa/背诵稿/09A-骨盆与髋关节主要肌肉高颗粒度专题.md"),
    (("膝", "TKA", "全膝"), "qa/背诵稿/10-膝关节-完整版.md；qa/背诵稿/10A-膝关节主要肌肉高颗粒度专题.md"),
    (("踝", "足", "足弓"), "qa/背诵稿/11-小腿踝足与足弓-完整版.md；qa/背诵稿/11A-小腿踝足主要肌肉高颗粒度专题.md"),
    (("肩", "肩袖", "上肢带"), "qa/背诵稿/07-上肢带与肩关节-完整版.md；qa/背诵稿/07A-上肢带与肩关节主要肌肉专题.md"),
    (("肘", "前臂", "腕", "手"), "qa/背诵稿/08-肘前臂腕手-完整版.md；qa/背诵稿/08A-肘前臂腕手主要肌肉高颗粒度专题.md"),
    (("躯干", "脊柱", "胸廓", "腰"), "qa/背诵稿/06-躯干-完整版.md；qa/背诵稿/06A-躯干主要肌肉高颗粒度专题.md"),
    (("头", "颈", "颅"), "qa/背诵稿/05-头颈-完整版.md；qa/背诵稿/05A-头颈主要肌肉高颗粒度专题.md"),
    (("动作", "深蹲", "跑", "走", "俯卧撑", "仰卧起坐", "引体", "墙球"), "qa/背诵稿/12-动作解剖学分析与其他系统整合-完整版.md；qa/背诵稿/12A-动作分析高颗粒度模板与体表定位专题.md"),
    (("骨骼肌", "肌肉", "肌力"), "qa/背诵稿/04-骨骼肌总论-完整版.md；qa/背诵稿/04A-骨骼肌总论高颗粒度专题.md"),
    (("关节", "骨连结"), "qa/背诵稿/03-骨连结与关节总论-完整版.md；qa/背诵稿/03A-骨连结与关节总论高颗粒度专题.md"),
    (("骨",), "qa/背诵稿/02-骨学总论-完整版.md；qa/背诵稿/02A-骨学总论高颗粒度专题.md"),
]


def split_table_row(line: str) -> list[str]:
    row = line.strip()
    if not row.startswith("|"):
        return []
    parts = [p.strip() for p in row.strip("|").split("|")]
    if any(re.fullmatch(r":?-{2,}:?", p.replace(" ", "")) for p in parts):
        return []
    return parts


def parse_questions(path: Path) -> dict[int, dict[str, str]]:
    questions: dict[int, dict[str, str]] = {}
    header: list[str] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = split_table_row(line)
        if not parts:
            continue
        if "题号" in parts[0] or "No." in parts[0]:
            header = parts
            continue
        if not header or not parts[0].strip().isdigit():
            continue
        no = int(parts[0])
        row = dict(zip(header, parts))
        questions[no] = {
            "subject": row.get("科目", row.get("Subject", "")),
            "points": row.get("分值", row.get("Points", "")),
            "module": row.get("考纲模块") or row.get("模块关键词") or row.get("模块/关键词") or row.get("Outline Module", ""),
            "detail": row.get("知识点明细") or row.get("模块关键词") or row.get("模块/关键词") or row.get("Detailed Knowledge Points", ""),
            "basis": row.get("依据", row.get("Type", "")),
            "question": row.get("题目", row.get("Question", "")),
        }
    return questions


def parse_answer_sections(text: str) -> dict[int, str]:
    matches = list(re.finditer(
        r"(?m)^(?:###\s*第\s*(\d+)\s*题.*|##\s*题\s*(\d+)\b.*|##\s*(\d+)\.\s+.*)$",
        text,
    ))
    sections: dict[int, str] = {}
    for i, m in enumerate(matches):
        no = int(next(g for g in m.groups() if g))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if 1 <= no <= 9:
            sections[no] = body
    return sections


def extract_label(section: str, label: str) -> str:
    patterns = [
        rf"\*\*{re.escape(label)}\*\*[:：]\s*(.*?)(?=\n\*\*|\n##|\n###|\Z)",
        rf"{re.escape(label)}[:：]\s*(.*?)(?=\n\n[A-Za-z\u4e00-\u9fff]+[:：]|\n##|\n###|\Z)",
    ]
    for pat in patterns:
        m = re.search(pat, section, flags=re.S)
        if m:
            return clean(m.group(1))
    return ""


def clean(s: str) -> str:
    s = re.sub(r"\n{3,}", "\n\n", s.strip())
    return s


def uniq_parts(text: str) -> str:
    seen: set[str] = set()
    parts: list[str] = []
    for part in re.split(r"[；;]", text):
        p = part.strip()
        if p and p not in seen:
            seen.add(p)
            parts.append(p)
    return "；".join(parts)


def bullets_to_sentence(scoring: str) -> str:
    lines = []
    for line in scoring.splitlines():
        line = line.strip().lstrip("-").strip()
        if not line:
            continue
        line = re.sub(r"[，,]?\s*\d+\s*分。?$", "", line)
        line = re.sub(r"（\d+分）", "", line)
        lines.append(line.rstrip("。"))
    return "；".join(lines[:7])


def strip_generated_appendix(text: str) -> str:
    markers = [
        "\n## 答案优化版",
        "\n## 背诵稿对照与补充",
    ]
    cut = len(text)
    for marker in markers:
        idx = text.find(marker)
        if idx != -1:
            cut = min(cut, idx)
    return text[:cut].rstrip()


def extract_bullet_points(block: str) -> list[str]:
    points: list[str] = []
    for raw in block.splitlines():
        line = raw.strip()
        if not line:
            continue
        line = line.lstrip("-").strip()
        line = re.sub(r"[，,。；;]?\s*\d+\s*分。?$", "", line)
        line = re.sub(r"（\d+\s*分）", "", line)
        line = re.sub(r"\(\d+\s*分\)", "", line)
        line = line.rstrip("。；;")
        if line:
            points.append(line)
    return points


def prose_from_points(points: list[str]) -> str:
    if not points:
        return ""
    sentences = []
    for point in points:
        if "：" in point:
            head, body = point.split("：", 1)
            sentences.append(f"{head}方面，应说明{body}。")
        elif ":" in point:
            head, body = point.split(":", 1)
            sentences.append(f"{head}方面，应说明{body.strip()}。")
        else:
            if any(word in point for word in ("意义", "联系", "应用", "风险", "控制", "预防")):
                sentences.append(f"还应联系{point.rstrip('。')}。")
            else:
                sentences.append(f"还应说明{point.rstrip('。')}。")
    return "".join(sentences)


def missing_note(question: dict[str, str]) -> str:
    subject = question["subject"]
    detail = uniq_parts(question["detail"])
    if subject == "康复":
        return f"需补成“机制/问题分析-评定指标-治疗训练-分期进阶-风险控制”的方案化表达，重点补 {detail} 的评定、进阶和回归标准。"
    if subject == "生理":
        return f"需补成“概念-机制-运动反应/训练适应-评定或处方应用”的机制链，重点补 {detail} 与运动表现、康复安全之间的联系。"
    if "动作" in detail or "动作分析" in detail:
        return f"需补成“动作分期-关节运动-肌肉工作-稳定控制-常见代偿-训练康复意义”的动作分析模板，重点补 {detail} 的应用表达。"
    return f"需补成“结构-功能-运动/训练影响-康复意义”的大题表达链，重点补 {detail} 的机制和应用。"


def complete_answer(section: str, question: dict[str, str]) -> str:
    existing = extract_label(section, "完整参考答案")
    if existing:
        return existing
    framework = extract_label(section, "标准答题框架")
    scoring = extract_label(section, "评分点")
    keywords = extract_label(section, "答案关键词")
    points = extract_bullet_points(scoring)
    core = prose_from_points(points)
    if not core:
        core = "答题时应覆盖以下关键词并展开其逻辑关系：" + keywords.replace("；", "、").replace("，", "、") + "。"
    if framework:
        return f"本题应按“{framework}”组织。先点明{uniq_parts(question['module'])}的核心概念，再围绕{uniq_parts(question['detail'])}展开机制、结构或功能分析。{core}结尾要把上述内容落到运动训练、康复评定、动作控制或风险管理，体现“基础知识到运动康复应用”的完整链条。"
    return f"本题作答应围绕{uniq_parts(question['module'])}展开，核心知识点为{uniq_parts(question['detail'])}。先解释基本概念和结构或机制，再说明运动、训练或康复情境中的作用。{core}结尾应补充训练或康复应用，避免只罗列名词。"


def target_draft(subject: str, text: str) -> str:
    if subject == "解剖":
        for keys, target in ANATOMY_TARGETS:
            if any(k in text for k in keys):
                return target
        return "qa/背诵稿/01-解剖学总论-完整版.md；qa/背诵稿/01A-解剖学总论高颗粒度专题.md"
    if subject == "生理":
        return "运动生理学-王瑞元苏全生/背诵稿-*.md；待归档到对应运动生理学专题主稿"
    return "暂无康复主稿，先归档到 qa/背诵稿/晨测补充/；后续可并入康复评定、运动治疗、运动损伤或术后分期专题"


def sufficiency(subject: str, detail: str, question: str) -> str:
    combined = detail + question
    if subject == "康复":
        return "不够用"
    if subject == "生理":
        return "基本够用但需补充"
    if any(k in combined for k in ("动作分析", "康复", "损伤", "术后", "案例", "方案", "评定")):
        return "基本够用但需补充"
    return "基本够用但需补充"


def supplement_text(section: str, question: dict[str, str]) -> str:
    existing = extract_label(section, "可直接加入背诵稿")
    if existing and existing != "无。":
        return existing
    ans = complete_answer(section, question)
    keywords = extract_label(section, "答案关键词")
    prefix = f"{uniq_parts(question['module'])}相关题要按“概念/结构或机制-运动表现-训练康复意义”组织。"
    if keywords:
        prefix += f" 必背关键词包括：{keywords.rstrip('。')}。"
    return (prefix + ans).replace("。。", "。")


def review_task(question: dict[str, str]) -> str:
    subject = question["subject"]
    detail = uniq_parts(question["detail"])
    if subject == "解剖":
        return f"用“结构-运动-肌肉工作-训练/康复意义”四步口述 {detail}，再默写 1 遍关键结构和易错点。"
    if subject == "生理":
        return f"用“概念-机制-运动反应-训练/康复应用”四步复述 {detail}，补画 1 条机制链。"
    return f"按“问题评定-目标-分期训练-进阶标准-风险控制”重写 {detail} 的 5 步方案。"


def answer_keywords(section: str, question: dict[str, str]) -> str:
    existing = extract_label(section, "答案关键词")
    if existing:
        return existing.rstrip("。")
    return uniq_parts(question["detail"]).replace("；", "；")


def scoring_points(section: str, question: dict[str, str]) -> str:
    existing = extract_label(section, "评分点")
    if existing:
        return existing
    points = question["points"] or "25"
    return f"- 围绕考纲模块和核心概念作答，约 {points} 分\n- 写出知识点之间的机制链或结构-功能关系\n- 联系运动训练、康复评定或风险控制"


def traps(section: str) -> str:
    existing = extract_label(section, "易丢分点")
    if existing:
        return existing.rstrip("。") + "。"
    return "只罗列关键词，不解释机制；只写理论，不联系运动或康复应用；50 分题未分层作答。"


def outline_location(question: dict[str, str]) -> str:
    subject = question["subject"]
    module = uniq_parts(question["module"])
    detail = uniq_parts(question["detail"])
    if detail == module:
        return f"{subject}；{module}"
    if subject in ("解剖", "生理"):
        return f"{subject}；{module}；{detail}"
    return f"康复；{module}；{detail}"


def build_appendix(date: str, questions: dict[int, dict[str, str]], sections: dict[int, str]) -> str:
    out = ["\n## 答案优化版（按当前背诵稿规则补做）\n", "说明：本节按当前要求统一补做。每题包含考纲定位、知识点明细、答案关键词、评分点、完整参考答案、易丢分点、背诵稿够用性、需要补充、可并入背诵稿内容和当日复习任务；补充内容同步沉淀到对应日期的晨测补充稿。\n"]
    for no in range(1, 10):
        q = questions.get(no)
        if not q:
            continue
        sec = sections.get(no, "")
        text = q["module"] + q["detail"] + q["question"]
        out.extend([
            f"\n### 第 {no} 题｜{q['subject']}｜{q['points']} 分\n",
            f"**考纲定位**：{outline_location(q)}  \n",
            f"**知识点明细**：{q['detail']}  \n",
            f"**答案关键词**：{answer_keywords(sec, q)}  \n",
            f"**评分点**：\n{scoring_points(sec, q)}\n\n",
            f"**完整参考答案**：{complete_answer(sec, q)}  \n",
            f"**易丢分点**：{traps(sec)}  \n",
            f"**背诵稿够用性**：{sufficiency(q['subject'], q['detail'], q['question'])}。  \n",
            f"**需要补充**：{missing_note(q)}  \n",
            f"**目标背诵稿**：{target_draft(q['subject'], text)}  \n",
            f"**可直接加入背诵稿**：{supplement_text(sec, q)}  \n",
            f"**当日复习任务**：{review_task(q)}\n",
        ])
    return "".join(out).rstrip() + "\n"


def build_supplement(date: str, questions: dict[int, dict[str, str]], sections: dict[int, str]) -> str:
    out = [f"# {date} 晨测背诵稿补充\n", "\n本文件由历史晨测答案反向补做，用于后续并入解剖、生理、康复主背诵稿。\n"]
    for subject in ("解剖", "生理", "康复"):
        out.append(f"\n## {subject}\n")
        for no in range(1, 10):
            q = questions.get(no)
            if not q or q["subject"] != subject:
                continue
            sec = sections.get(no, "")
            text = q["module"] + q["detail"] + q["question"]
            out.extend([
                f"\n### 题 {no}：{q['question']}\n",
                f"- 考纲定位：{outline_location(q)}。\n",
                f"- 知识点明细：{q['detail']}。\n",
                f"- 背诵稿够用性：{sufficiency(subject, q['detail'], q['question'])}。\n",
                f"- 目标背诵稿：{target_draft(subject, text)}。\n\n",
                f"{supplement_text(sec, q)}\n",
            ])
    return "".join(out).rstrip() + "\n"


def main() -> None:
    SUPP_DIR.mkdir(parents=True, exist_ok=True)
    written_supp = 0
    updated_answers = 0
    processed_questions = 0
    for qpath in sorted(QUESTION_DIR.glob("2026-*-题目.md")):
        date = qpath.name[:10]
        apath = ANSWER_DIR / f"{date}-答案.md"
        if not apath.exists():
            continue
        questions = parse_questions(qpath)
        answer_text = apath.read_text(encoding="utf-8")
        base_answer_text = strip_generated_appendix(answer_text)
        sections = parse_answer_sections(base_answer_text)
        if len(questions) < 9:
            print(f"warning: {date} parsed {len(questions)} questions")
        supplement = build_supplement(date, questions, sections)
        spath = SUPP_DIR / f"{date}-晨测补充.md"
        spath.write_text(supplement, encoding="utf-8")
        written_supp += 1
        appendix = build_appendix(date, questions, sections)
        apath.write_text(base_answer_text.rstrip() + "\n" + appendix, encoding="utf-8")
        updated_answers += 1
        processed_questions += len(questions)
    print(f"processed_questions={processed_questions}")
    print(f"written_supplement_files={written_supp}")
    print(f"updated_answer_files={updated_answers}")


if __name__ == "__main__":
    main()
