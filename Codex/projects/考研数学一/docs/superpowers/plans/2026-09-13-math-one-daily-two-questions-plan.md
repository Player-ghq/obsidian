# 数学一每日两题 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立每天北京时间 07:00 自动生成一道极限题和一道积分题的 Obsidian 学习项目，并把考研最高优先级完全切换为数学一。

**Architecture:** 题目、分类索引和复盘记录统一存放在 `Codex/projects/考研数学一/`。Codex 定时任务每天读取索引与历史题目，创建当日笔记并更新覆盖记录；持久记忆文件同步保存科目变更。

**Tech Stack:** Obsidian Markdown、Codex 本地定时任务、Git

**Spec:** `Codex/projects/考研数学一/docs/superpowers/specs/2026-09-13-math-one-daily-two-questions-design.md`

## Global Constraints

- 每天北京时间 07:00 生成。
- 每日固定极限 1 题、积分 1 题。
- 每题必须包含一级题型、二级题型、核心方法、难度、预计用时、折叠解析与复盘字段。
- 重复运行不得覆盖已经存在的当日文件。
- 运动生理学和人体解剖学不再作为默认考研科目；历史资料保留。

---

### Task 1: 建立项目与每日模板

**Files:**
- Create: `Codex/projects/考研数学一/README.md`
- Create: `Codex/projects/考研数学一/templates/每日两题模板.md`
- Create directory: `Codex/projects/考研数学一/每日两题/`

- [x] **Step 1:** 写入项目目标、限时作答—核对解析—记录错误的使用流程。
- [x] **Step 2:** 写入包含两道题及折叠解析、结果、实际用时、错误原因字段的模板。
- [x] **Step 3:** 检查模板中恰好包含一节“极限”和一节“积分”，且包含全部必填元数据。

### Task 2: 建立题型索引

**Files:**
- Create: `Codex/projects/考研数学一/题型索引.md`

- [x] **Step 1:** 建立极限的一级、二级分类表与覆盖计数列。
- [x] **Step 2:** 建立积分的一级、二级分类表与覆盖计数列。
- [x] **Step 3:** 写明轮换规则：优先未覆盖和薄弱题型，禁止仅更换数字的连续重复。
- [x] **Step 4:** 检查设计文件列出的全部子题型均在索引中出现。

### Task 3: 替换持久备考目标

**Files:**
- Modify: `Codex/AGENTS.md`
- Modify: `Codex/projects/长期目标.md`
- Modify: `Codex/people/用户.md`

- [x] **Step 1:** 将最高优先级改为 2026-12-19 考研数学一。
- [x] **Step 2:** 删除运动生理学、人体解剖学作为默认考纲边界的指令，保留历史项目与资料。
- [x] **Step 3:** 添加每日极限、积分各 1 题和 07:00 生成的长期工作约定。
- [x] **Step 4:** 全文检索三个文件，确认不存在“运动康复专业考研仍为最高优先级”的冲突表述。

### Task 4: 创建并验证自动任务

**Files:**
- Runtime configuration: Codex automation

- [x] **Step 1:** 查询可用本地项目，选择承载 Obsidian Vault 的项目 ID。
- [x] **Step 2:** 创建每天 07:00 运行的本地定时任务，提示词写明读取路径、生成格式、题型轮换、幂等和索引更新规则。
- [x] **Step 3:** 查看任务配置，确认名称、启用状态、北京时间计划、项目 ID 与提示词均正确。
- [x] **Step 4:** 检查所有新增与修改文件，并仅提交本次变更，不包含 `.obsidian/workspace.json` 等既有改动。
