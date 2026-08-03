# 外刊精读工作流

## 整期 PDF 模式

用于用户提供一整期杂志 PDF 时。

1. 读取 PDF 基本信息：期刊名、日期、页数、文本层质量。
2. 优先读取目录页；若无目录，则根据标题、栏目、页眉和版式推断文章边界。
3. 建立文章表：栏目、标题、作者、页码、体裁、可信度、备注。
4. 按 [[theme-priority]] 匹配重点主题。
5. 按以下维度排序：
   - 阅读理解价值
   - 词汇与词块价值
   - 长难句与翻译价值
   - 写作迁移价值
   - 重点主题匹配度
6. 输出阅读计划：
   - Intensive Reading First
   - Extensive Reading
   - Skim or Skip
7. 推荐下一篇精读文章，等待用户确认后进入单篇流程。

## 单篇文章模式

用于用户提供单篇文章，或从整期 PDF 中选定一篇文章时。

如果用户无从下手，先使用 [[how-to-close-read]] 的 6 步法带读，不要一次性把全文讲完。

如果用户要求完整精读、全文翻译、段落分片、长难句语法、作文金句或 Anki 卡片，使用 [[full-deep-reading-requirements]]。

### Extensive Reading

快速提取：

- Title and Prediction
- One-Sentence Gist
- Key Information
- Author's Position
- Paragraph Map
- Reading Strategy

### Intensive Reading

逐层拆解：

- Title
- Main Idea
- Structure
- Paragraph Close Reading
- Language Upgrade
- Kaoyan English Transfer

### Anki 制卡协作流程

单篇文章精读结束后，默认直接生成最终 Anki 卡片，除非用户明确说“先别制卡”。

1. 制卡内容分为三类：
   - `单词`：阅读卡壳词、考研核心词、熟词辟义、一词多义、态度词、抽象名词。
   - `词组/句块`：外刊高频搭配、动词短语、固定搭配、长难句结构、可背诵句块。
   - `作文复用`：可直接迁移到考研作文的句型、论证动作和话题表达。
2. 单词和词组部分由用户与 Codex 共同完成：
   - 用户可以给自己的词表。
   - Codex 必须主动从文章中补充值得背诵的表达。
   - 明显有考研价值的表达不需要再次征求用户同意，直接加入最终制卡清单。
3. 作文复用部分全部由 Codex 负责：
   - 从文章中挑选可迁移表达。
   - 判断适配话题和作文功能。
   - 按 [[anki-writing-transfer-card-template]] 制作生产型作文卡。
4. 合并双方词表：去重、还原原型、合并变体、删掉不符合考研英语一价值的项目。
5. 每个最终候选项至少标明：
   - 原型/归一化后的制卡 front
   - 原文位置或原句
   - 建议原因：阅读理解、熟词僻义、长难句、翻译、完形搭配、作文迁移等
   - 类型：单词 / 词组句块 / 作文复用
6. 正式生成 `cards.json`、`anki.tsv`、`anki.xlsx`，统一放入该文章文件夹的 `anki/`。

## 沉淀规则

- 每期杂志的目录、分类和排序结果放入 `readings/`。
- 每次完成整期整理或单篇精读后，更新 [[reading-log]]。
- 当前下一步与未完成事项写入 [[state]]。
- 不保存整篇版权正文；只保存学习分析、页码、标题、主题、短摘录和训练结论。
