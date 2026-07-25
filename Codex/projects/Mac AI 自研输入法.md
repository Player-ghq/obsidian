# Mac AI 自研输入法

## 项目背景

- 用户希望做一个 macOS 版本自研 AI 输入法。
- 用户是双拼输入法用户。
- 核心诉求：词库可配置，可放入专业词汇、日常用语和频繁使用的英语表达。

## 初步产品方向

- 第一阶段优先做可用的双拼输入与可配置词库，而不是先做复杂 AI。
- AI 的主要价值应体现在候选词排序、上下文联想、个人用语学习、专业词汇召回和中英混输优化。

## 2026-07-25 需求收敛

- 第一版只给用户自己使用。
- 双拼方案需要可配置，不要求第一版内置完整方案库。
- AI 暂不进入 MVP，后续作为扩展；若以后加入，优先本地、低占用、可关闭。
- 词库采用“文本源文件 + 本地编译索引”的方向：用户直接编辑文本，输入法使用编译后的索引保证速度。
- 词库必须支持导入、导出、手动修改，并在编辑后给出明确的成功/失败反馈。
- MVP 重点同时满足专业词命中率和日常输入流畅度。

## 产物

- 需求整理文档：`/Users/HaoQi/Documents/Codex/2026-07-25/mac-ai/docs/superpowers/specs/2026-07-25-mac-ai-input-method-requirements.md`

## 2026-07-25 开发进展

- 已在 `/Users/HaoQi/Documents/Codex/2026-07-25/mac-ai` 初始化 git 仓库。
- 已创建隔离 worktree：`/Users/HaoQi/Documents/Codex/2026-07-25/mac-ai/.worktrees/dictionary-toolchain`，分支 `feature/dictionary-toolchain`。
- 已完成词库工具链主体：
  - Swift Package 脚手架。
  - TSV 词库解析器。
  - 词库校验器与 JSON 导入报告。
  - SQLite 编译索引。
  - 候选词规则排序。
  - CLI：`validate`、`compile`、`query`、`export`。
  - 用户文档：`docs/user/dictionary-format.md`、`docs/user/dictionary-toolchain.md`。
- 已通过的验证：完整 `swift test --disable-sandbox` 通过，17 个 XCTest、0 失败；样例 TSV 可校验、编译为 SQLite、查询 `gu` 返回「股四头肌」、导出回 TSV。
- Apple 开发者工具 license gate 已由用户处理完成。
- 已按用户选择将 `feature/dictionary-toolchain` fast-forward 合并回 `main`；合并后在 `main` 再次通过完整测试与 CLI 烟测；`.worktrees/dictionary-toolchain` 已删除，本地 feature 分支已删除。

## 2026-07-26 开发进展

- 已创建第二阶段 worktree：`/Users/HaoQi/Documents/Codex/2026-07-25/mac-ai/.worktrees/double-pinyin-engine`，分支 `feature/double-pinyin-engine`。
- 已完成双拼配置与输入引擎核心：
  - `DoublePinyin.sample.tsv` 样例配置。
  - 双拼方案 TSV 解析与行号错误。
  - 双拼 raw buffer 到词库查询前缀的转换。
  - `InputEngine`：维护 raw buffer、翻译 lookup prefix、查询 SQLite、输出排序候选。
  - CLI：`scheme-validate`、`suggest`。
  - 用户文档：`docs/user/double-pinyin-scheme.md`，并更新 `docs/user/dictionary-toolchain.md`。
- 已通过的验证：完整 `swift test --disable-sandbox` 通过，31 个 XCTest、0 失败；样例词库编译后，`suggest --keys "gu"` 返回「股四头肌」。
- 已按用户选择将 `feature/double-pinyin-engine` fast-forward 合并回 `main`；合并后在 `main` 再次通过完整测试与 CLI 烟测；`.worktrees/double-pinyin-engine` 已删除，本地 feature 分支已删除。
