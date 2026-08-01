# Kinesiology Knowledge Base Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an isolated local Markdown knowledge base from two kinesiology/function-anatomy PDFs so future Q&A can use local extracted corpus files instead of rereading PDFs.

**Architecture:** A single repeatable Python builder extracts page text, writes page-level Markdown, groups pages into retrieval chunks, tags chunks by book/topic/region/exam topic, and generates Markdown plus JSONL indexes. The generated knowledge base lives under the user's Obsidian Codex projects directory and is isolated from other knowledge projects.

**Tech Stack:** Codex bundled Python 3, `pdfplumber`, `pypdf`, Markdown, JSONL.

## Global Constraints

- Knowledge base root: `/Users/HaoQi/Documents/Codex/obsidian-vault-codex-codex-codex-todo-2/Codex/projects/肌动学与功能解剖学语料库`.
- Source PDFs remain in `/Users/HaoQi/Documents/考研/教材/`; do not move, modify, or duplicate them.
- Preserve source book and page metadata on every page file and retrieval chunk.
- Future Q&A should prefer this local knowledge base before reading source PDFs again.

---

### Task 1: Build Generator

**Files:**
- Create: `work/build_kinesiology_kb.py`
- Create: `/Users/HaoQi/Documents/Codex/obsidian-vault-codex-codex-codex-todo-2/Codex/projects/肌动学与功能解剖学语料库/docs/superpowers/plans/2026-08-01-kinesiology-kb.md`

**Interfaces:**
- Consumes: two fixed PDF paths from the user request.
- Produces: CLI `python build_kinesiology_kb.py --root <knowledge-base-root>`.

- [x] **Step 1: Define source metadata**

The script stores book id, title, slug, short title, and absolute PDF path.

- [x] **Step 2: Implement extraction**

Use `pdfplumber.open(path)` and `page.extract_text()` to create one `PageText` record per page.

- [x] **Step 3: Implement chunking and indexing**

Group text into approximately 4500-character chunks, then tag each chunk by keyword maps for broad topics, anatomical regions, and exam topics.

- [x] **Step 4: Implement generated files**

Write `README.md`, `QA使用说明.md`, `sources/source-index.md`, `extracted/`, `chunks/by-book/`, `chunks/by-topic/`, and `index/retrieval-map.jsonl`.

### Task 2: Generate Knowledge Base

**Files:**
- Generate under: `/Users/HaoQi/Documents/Codex/obsidian-vault-codex-codex-codex-todo-2/Codex/projects/肌动学与功能解剖学语料库`

**Interfaces:**
- Consumes: `work/build_kinesiology_kb.py`.
- Produces: isolated Markdown and JSONL knowledge base.

- [x] **Step 1: Run builder**

Run:

```bash
/Users/HaoQi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 work/build_kinesiology_kb.py --root /Users/HaoQi/Documents/Codex/obsidian-vault-codex-codex-codex-todo-2/Codex/projects/肌动学与功能解剖学语料库
```

Expected: exits 0 and creates the full directory tree.

- [x] **Step 2: Count outputs**

Run `find <root> -type f | wc -l` and inspect key subdirectories.

Expected: page files for both books, chunk files, topic indexes, and root documentation exist.

### Task 3: Verify Corpus Quality

**Files:**
- Read: generated `README.md`
- Read: generated `index/retrieval-map.jsonl`
- Read: representative chunk files

**Interfaces:**
- Consumes: generated corpus.
- Produces: quality report in final response.

- [x] **Step 1: Verify counts**

Check total pages are 410 and 720 respectively, and total extracted pages are 1130.

- [x] **Step 2: Verify retrievability**

Search for representative terms: `肩关节`, `膝关节`, `足弓`, `肌力`, `动作分析`.

Expected: at least one generated chunk or page file contains each term.

- [x] **Step 3: Verify future-use instructions**

Confirm `QA使用说明.md` says to use this knowledge base before reopening PDFs.

### Task 4: Update Long-Term Memory

**Files:**
- Modify: `/Users/HaoQi/Documents/Codex/obsidian-vault-codex-codex-codex-todo-2/Codex/agent/工作流约定.md` if relevant
- Modify: `/Users/HaoQi/Documents/Codex/obsidian-vault-codex-codex-codex-todo-2/Codex/TODO.md` only if unresolved follow-up remains

**Interfaces:**
- Consumes: final generated knowledge base path.
- Produces: concise memory note so future sessions know the corpus exists.

- [x] **Step 1: Record reusable path**

Add a concise note pointing future Codex sessions to the new knowledge base for these two books.

- [x] **Step 2: Record unresolved issues only if needed**

If OCR quality is poor or some verification fails, write the next step to `TODO.md`.
