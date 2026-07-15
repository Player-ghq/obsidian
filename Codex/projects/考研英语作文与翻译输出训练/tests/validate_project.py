from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "AGENTS.md",
    "README.md",
    "profile.md",
    "plan.md",
    "state.md",
    ".agents/skills/kaoyan-english-writing-coach/SKILL.md",
    ".agents/skills/kaoyan-english-writing-coach/agents/openai.yaml",
    ".agents/skills/kaoyan-english-writing-coach/references/rubric.md",
    "knowledge/errors.md",
    "knowledge/expressions.md",
    "knowledge/mastery.md",
    "templates/daily-session.md",
    "templates/daily-study.md",
    "templates/weekly-review.md",
    "daily-study/README.md",
    "reviews/README.md",
]

missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
assert not missing, f"missing required files: {missing}"

skill = (
    ROOT / ".agents/skills/kaoyan-english-writing-coach/SKILL.md"
).read_text(encoding="utf-8")
assert re.search(r"^name: kaoyan-english-writing-coach$", skill, re.MULTILINE)
for phrase in ["保留原稿", "不提供完整范文", "七天后复写", "更新 state.md"]:
    assert phrase in skill, f"skill misses behavior: {phrase}"

agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
for phrase in [
    "profile.md",
    "state.md",
    "knowledge/errors.md",
    "kaoyan-english-writing-coach",
]:
    assert phrase in agents, f"AGENTS.md misses bootstrap rule: {phrase}"

for phrase in ["knowledge/mastery.md", "daily-study", "不会", "模糊", "熟练"]:
    assert phrase in agents or phrase in skill, f"expanded contract misses: {phrase}"

mastery = (ROOT / "knowledge/mastery.md").read_text(encoding="utf-8")
for phrase in ["下次复习", "连续成功", "待确认", "稳定掌握"]:
    assert phrase in mastery, f"mastery ledger misses field or rule: {phrase}"

daily_template = (ROOT / "templates/daily-study.md").read_text(encoding="utf-8")
for phrase in ["作文专项", "高频词汇", "长难句拆解", "每日精译", "功能句", "掌握度反馈"]:
    assert phrase in daily_template, f"daily template misses writing-focused contract: {phrase}"

state = (ROOT / "state.md").read_text(encoding="utf-8")
plan = (ROOT / "plan.md").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
for phrase in ["下一篇作文类型", "小作文", "今日作文任务"]:
    assert phrase in state, f"state misses essay rotation field: {phrase}"
for phrase in ["隔日轮换", "小作文日", "大作文日", "到期重写或复写", "暂停独立安排"]:
    assert phrase in plan, f"plan misses rotation rule: {phrase}"
for phrase in ["今日作文训练", "作文模式", "唯一交付物", "下一篇作文类型"]:
    assert phrase in daily_template, f"daily template misses essay field: {phrase}"
for phrase in ["作文专项训练项目", "近两个月全力只专注作文", "小作文", "大作文"]:
    assert phrase in readme, f"README misses unified purpose: {phrase}"

assert (ROOT / "journal").is_dir()
assert (ROOT / "weekly").is_dir()
assert (ROOT / "daily-study").is_dir()
assert (ROOT / "reviews").is_dir()
print("PASS: project structure and core coaching contract are valid")
