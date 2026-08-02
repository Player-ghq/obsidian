import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/Users/HaoQi/Documents/Codex/2026-07-27/vg")
INPUT = ROOT / "outputs" / "运动康复考研真题分类表.csv"
OUTPUT_CSV = ROOT / "outputs" / "运动康复考研真题知识点关键词表.csv"
OUTPUT_JSON = ROOT / "work" / "xlsx-builder" / "questions_with_keywords.json"
OUTPUT_MD = ROOT / "outputs" / "运动康复考研真题知识点关键词整理.md"


KEYWORD_RULES = [
    ("解剖", "骨结构与骨适应", r"骨骼|骨结构|骨的|骨组织|骨密度|骨杠杆|骨形态|骨生长|骨折分型|骨小梁|骨膜"),
    ("解剖", "关节结构与关节运动", r"关节(?!置换)|关节结构|关节运动|关节唇|滑膜|关节软骨|关节内软骨|关节囊|运动幅度|活动度|ROM"),
    ("解剖", "膝关节", r"膝关节|半月板|交叉韧带|股四头肌|髌骨|伸膝|屈膝|Q角"),
    ("解剖", "肩关节与肩复合体", r"肩关节|肩袖|肩胛|肩峰|盂肱|肩部|Dugas|肱骨外上髁|网球肘"),
    ("解剖", "髋关节与骨盆", r"髋关节|骨盆|骨盆前倾|臀大肌|髂腰肌"),
    ("解剖", "踝足结构", r"踝关节|踝扭伤|踝.*韧带|足弓|足背|距小腿|胫骨|腓骨|小腿骨"),
    ("解剖", "脊柱与躯干", r"脊柱|椎间盘|颈椎|胸廓|腰椎|腰部|腰突|核心稳定|躯干|俯卧撑|仰卧起坐|燕式平衡"),
    ("解剖", "骨骼肌结构与肌肉工作", r"肌组织|骨骼肌|肌肉工作|向心|离心|等长|等张|等速|多关节肌|主动不足|被动不足|肌力|肌腱|腱鞘|肌腱袖|背阔肌|三角肌|绳肌|腓肠肌"),
    ("解剖", "神经解剖与传导通路", r"内囊|神经束|神经通路|传导通路|臂丛|中枢神经系统|大脑皮质|基底神经节|小脑|神经核|自主神经|位觉感受器|内耳|视器"),
    ("解剖", "运动动作解剖学分析", r"动作分析|解剖学分析|正足背踢|卧推|引体向上|站立|跑步|步态|俯卧撑|仰卧起坐|燕式平衡"),
    ("生理", "内环境稳态", r"内环境|稳态|酸碱平衡|碱储备|体液调节"),
    ("生理", "细胞兴奋与肌肉收缩", r"静息电位|动作电位|兴奋-收缩偶联|钠钾泵|细胞膜|心肌|骨骼肌收缩|肌紧张|腱反射"),
    ("生理", "血液与心血管", r"血液|运动员血液|心血管|血压|心传导|心电图|心纤维支架|静脉回心|心输出量|循环|体循环"),
    ("生理", "呼吸与肺功能", r"呼吸|肺通气|肺活量|时间肺活量|氧离曲线|氧解离|呼吸困难|体位引流|吹笛式呼吸"),
    ("生理", "供能系统与能量代谢", r"能量|能源|供能|ATP|CP|糖酵解|有氧氧化|乳酸|三大.*系统|基础代谢|物质代谢"),
    ("生理", "运动强度与生理评定", r"最大摄氧量|摄氧量|乳酸阈|通气无氧阈|靶心率|CPET|心肺运动|运动试验|机能评定|运动负荷"),
    ("生理", "内分泌与血糖调节", r"激素|内分泌|血糖|胰岛素|胰高血糖素|应急反应|信息传递|细胞信号"),
    ("生理", "体温调节", r"体温|散热|产热|体温调节"),
    ("生理", "运动疲劳与恢复", r"疲劳|恢复|极点|第二次呼吸|酸痛|延迟性肌肉酸痛"),
    ("生理", "运动技能与神经调控", r"运动技能|技能形成|神经调控|本体感觉|平衡生理机制|反射"),
    ("生理", "运动处方与特殊人群", r"运动处方|老年|儿童|青少年|女子|肥胖|体重控制|糖尿病|冠心病|新冠"),
    ("康复", "康复评定", r"康复评定|评定方法|评估|测量|量表|SOAP|ADL|IADL|生活质量|ASIA|Brunnstrom|肌力评定|平衡评定|步态分析|感觉评定"),
    ("康复", "运动治疗与训练方案", r"运动治疗|治疗方案|康复方案|训练方案|功能训练|负荷|抗阻|有氧耐力|悬吊训练|PNF|FES|物理治疗|麦肯基|3M原则"),
    ("康复", "运动损伤康复", r"运动损伤|肌肉损伤|挫伤|拉伤|扭伤|韧带损伤|骨折|脱位|半脱位|炎|疼痛|网球肘|肱骨外上髁炎|胫骨骨膜炎"),
    ("康复", "神经康复", r"脊髓损伤|中枢神经损伤|脑损伤|脑瘫|偏瘫|缺血缺氧性脑病|迟缓期|共同运动|联合反应|痉挛|共济失调"),
    ("康复", "术后康复", r"置换术|全膝关节置换|髋关节置换|术后|手术后"),
    ("康复", "疼痛与慢病康复", r"疼痛|神经病理性疼痛|腰痛|冠心病|糖尿病|肥胖|慢性|社区康复"),
    ("康复", "平衡步态与功能恢复", r"平衡|步态|跌倒|单足站立|稳定极限|跨步调节|反应性平衡|功能恢复|日常生活"),
    ("康复", "病例分析与方案设计", r"病例|患者|主诉|病因|查体|方案设计|分期治疗|禁忌|返回运动"),
    ("体育教育/训练", "学校体育与课程教学", r"学校体育|体育教学|说课|课程标准|核心素养|体育课|教案|教学目标|教学方法"),
    ("体育教育/训练", "训练学与体能训练", r"训练原则|周期安排|系统持续|力量训练|快速力量|最大肌力|法特莱克|运动训练"),
]


TYPE_KEYWORDS = {
    "名词解释": "概念辨析",
    "简答": "基础问答",
    "论述": "综合论述",
    "病例分析": "病例分析",
    "动作分析": "动作分析",
}


def compact_school(raw: str) -> str:
    if not raw:
        return ""
    text = raw.replace("（回忆版）", "").replace("(回忆版)", "").strip()
    text = re.sub(r"^20\d{2}级?", "", text)
    text = re.sub(r"^\d{2}级?", "", text)
    text = text.replace("真题", "").strip()
    return text or raw


def infer_keywords(row: dict) -> tuple[str, str]:
    question = row.get("question_text", "")
    subject = row.get("subject", "")
    qtype = row.get("question_type", "")
    matched = []
    modules = []
    for module, keyword, pattern in KEYWORD_RULES:
        if re.search(pattern, question, flags=re.I):
            matched.append(keyword)
            modules.append(module)
    if qtype in TYPE_KEYWORDS:
        matched.append(TYPE_KEYWORDS[qtype])
        if not modules:
            modules.append(subject if subject and subject != "待判定" else "待判定")
    if not matched and subject and subject != "待判定":
        matched.append(subject)
        modules.append(subject)
    if not matched:
        matched.append("待人工标注")
        modules.append("待判定")
    dedup_keywords = list(dict.fromkeys(matched))[:6]
    dedup_modules = list(dict.fromkeys(modules))[:3]
    return "；".join(dedup_keywords), "；".join(dedup_modules)


def chinese_row(row: dict) -> dict:
    keywords, modules = infer_keywords(row)
    return {
        "年份": row.get("year", ""),
        "学校/方向": compact_school(row.get("school_track", "")),
        "原始学校/方向": row.get("school_track", ""),
        "考试科目/代码": row.get("exam_code", ""),
        "分类": row.get("subject", ""),
        "知识模块": modules,
        "知识点关键词": keywords,
        "题型": row.get("question_type", ""),
        "分值": row.get("score", ""),
        "题干": row.get("question_text", ""),
        "置信度": row.get("confidence", ""),
        "OCR文本": row.get("source_ocr", ""),
        "复核原图": row.get("source_image", ""),
    }


def main():
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8-sig")))
    output_rows = [chinese_row(r) for r in rows]
    headers = list(output_rows[0].keys())

    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(output_rows)

    OUTPUT_JSON.write_text(json.dumps(output_rows, ensure_ascii=False, indent=2), encoding="utf-8")

    year_counts = Counter(r["年份"] for r in output_rows)
    subject_counts = Counter(r["分类"] for r in output_rows)
    module_counts = Counter()
    for r in output_rows:
        for module in r["知识模块"].split("；"):
            if module:
                module_counts[module] += 1

    with OUTPUT_MD.open("w", encoding="utf-8") as f:
        f.write("# 运动康复考研真题知识点关键词整理\n\n")
        f.write("来源：`23年.zip`、`24年.zip`、`25年.zip` OCR 结构化表。所有记录保留分值、OCR 文本路径和复核原图路径；`知识点关键词` 由题干关键词规则自动标注，仍建议结合原图复核。\n\n")
        f.write("## 汇总\n\n")
        f.write(f"- 总题目记录：{len(output_rows)}\n")
        f.write(f"- 已标注分值记录：{sum(1 for r in output_rows if r['分值'])}\n")
        f.write(f"- 有复核原图记录：{sum(1 for r in output_rows if r['复核原图'])}\n")
        f.write(f"- webp 原图记录：{sum(1 for r in output_rows if r['复核原图'].endswith('.webp'))}\n")
        f.write("- 年份分布：" + "；".join(f"{k}年 {v}条" for k, v in sorted(year_counts.items())) + "\n\n")
        f.write("## 知识模块分布\n\n")
        f.write("| 知识模块 | 题目数 |\n|---|---:|\n")
        for k, v in module_counts.most_common():
            f.write(f"| {k} | {v} |\n")
        f.write("\n## 全量题目表\n\n")
        f.write("| 年份 | 学校/方向 | 分类 | 知识点关键词 | 题型 | 分值 | 题干 | 复核原图 |\n")
        f.write("|---|---|---|---|---|---:|---|---|\n")
        for r in output_rows:
            values = [
                r["年份"],
                r["学校/方向"],
                r["分类"],
                r["知识点关键词"],
                r["题型"],
                r["分值"],
                r["题干"],
                f"`{r['复核原图']}`",
            ]
            values = [str(v).replace("|", "｜") for v in values]
            f.write("| " + " | ".join(values) + " |\n")

    print(f"records={len(output_rows)}")
    print(OUTPUT_CSV)
    print(OUTPUT_JSON)
    print(OUTPUT_MD)


if __name__ == "__main__":
    main()
