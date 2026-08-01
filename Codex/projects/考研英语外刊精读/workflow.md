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

## 沉淀规则

- 每期杂志的目录、分类和排序结果放入 `readings/`。
- 每次完成整期整理或单篇精读后，更新 [[reading-log]]。
- 当前下一步与未完成事项写入 [[state]]。
- 不保存整篇版权正文；只保存学习分析、页码、标题、主题、短摘录和训练结论。
