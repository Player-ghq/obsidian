# 考研英语外刊精读

本项目用于把英文杂志、报刊、社论、长文和整期 PDF 转化为考研英语能力训练材料。默认使用本地 skill `english-magazine-close-reading`，先按主题筛选文章，再进入泛读与精读。

## 项目目标

- 提升考研英语阅读的信息提取、主旨判断、态度判断和推理能力。
- 积累高价值主题语料，用于作文、翻译和长难句训练。
- 建立整期杂志的筛选机制，避免把时间浪费在低考试价值文章上。

## 日常入口

```text
这期杂志先帮我分类
按外刊精读项目处理这个 PDF
从推荐第一篇开始精读
把这篇文章做泛读和精读
我不知道怎么精读这篇文章
更新外刊阅读记录
```

## 训练闭环

```text
整期 PDF/单篇文章输入
→ 目录与文章边界识别
→ 重点主题匹配
→ 考研价值排序
→ 选 1 篇泛读
→ 提取并清理文章全文，保存到知识库 source text
→ 生成全文中文翻译
→ 选重点段落精读
→ 词汇/长难句/翻译/写作迁移沉淀
→ reading-log.md 记录进度
```

## 当前工具

- Skill：`english-magazine-close-reading`
- Anki 制卡：`anki-excel-card-maker`
- 重点流程：见 [[workflow]]
- 精读操作手册：见 [[how-to-close-read]]
- 完整精读输出需求：见 [[full-deep-reading-requirements]]
- 重点主题：见 [[theme-priority]]
- 阅读记录：见 [[reading-log]]
- 当前状态：见 [[state]]

## 输出约定

- 有用的外刊精读笔记默认写入本知识库，聊天窗口只给简短摘要和文件位置。
- 单篇文章默认使用一个独立文件夹，文件夹名称直接使用文章题目，例如 `articles/Rules for supermodels/`。
- 进入单篇精读前，默认先把文章全文从 PDF/网页/用户文本中提取出来，清理版保存为 `articles/[Article Title]/source-text.md`，再基于该文本做泛读、精读、翻译和制卡。
- 单篇精读必须生成全文中文翻译，保存为 `articles/[Article Title]/full-translation.md`，供对照精读使用。
- 单篇文章产生的词汇、短语、语法和作文表达，默认用 `anki-excel-card-maker` 生成 Anki 可导入 `.tsv`，同时保留 `.xlsx` 编辑版和 `.json` 源数据，统一放入 `articles/[Article Title]/anki/`。
- Anki 标签默认包含 `外刊精读`，并追加文章名标签，方便后续检索。
