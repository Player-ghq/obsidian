# 肌动学与功能解剖学语料库

这是一个与其他项目隔离的本地知识库，用于以后回答《基础肌动学 第3版》《骨骼肌肉功能解剖学 第2版》以及北体《运动解剖学》运动系统相关问题。

## 内容范围

- 来源书籍: 3 本，其中北体《运动解剖学》仅整理第4-9章运动系统
- 抽取页数: 1339
- 知识块数: 241
- 未抽取到文字的页数: 2
- 清洗层知识块数: 450
- 章节汇编层: 覆盖前两本全书清洗语料，并覆盖北体《运动解剖学》第4-9章 OCR 清洗语料
- 结构化章节样板: 《骨骼肌肉功能解剖学 第2版》第5章 肩复合体
- 高效问答入口: 问题路由图、部位章节速查表、考研答题模板

## 使用方式

以后提问这些教材相关内容时，优先检索本目录：

1. 先看 `index/answer-routing-map.md` 判断问题类型。
2. 再看 `index/body-region-quick-map.md` 定位身体部位和章节页码。
3. 考研简答/论述先套 `index/exam-answer-templates.md`。
4. 北体《运动解剖学》运动系统问题先查 `index/beiti-motion-system-index.md`。
5. 具体内容优先查 `structured/` 与 `concepts/`。
6. 需要顺读整章时打开 `index/compiled-chapter-index.md` 与 `structured/compiled-chapters/`。
7. 需要核对原文时打开 `cleaned/by-book/`。
8. OCR 疑似错误时再查看 `chunks/by-book/` 或 `extracted/`。
9. 回答时说明依据的书名和页码范围。

## 目录说明

- `sources/`: 来源文件与元数据。
- `extracted/`: 按页抽取的 Markdown。
- `chunks/by-book/`: 可检索知识块，按书籍保存。
- `chunks/by-topic/`: 按主题聚合的入口页。
- `cleaned/`: 去除多余换行后的清洗语料层。
- `structured/`: 按章节整理后的高效率读取层。
- `structured/compiled-chapters/`: 两本书按章节自动汇编的清洗语料。
- `concepts/`: 按知识点整理的概念卡。
- `index/`: 问答路由、部位速查、答题模板、关键词、考纲主题索引与 JSONL 检索映射。
- `qa/`: 基于本知识库整理的学习问题答案与复习稿。
- `QA使用说明.md`: 后续问答检索规则。
