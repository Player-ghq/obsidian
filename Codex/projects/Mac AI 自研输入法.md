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

## 2026-07-26 InputMethodKit 外壳进展

- 已完成最小 macOS InputMethodKit 输入法外壳，并按用户选择将 `feature/inputmethodkit-shell` fast-forward 合并回 `main`；`.worktrees/inputmethodkit-shell` 已删除，本地 feature 分支已删除。
- 新增 `macai-inputmethod` Swift executable，包含 `MacAIInputController`、本地 `InputEngine` 加载、基本字母 buffer、Backspace、Return/Tab 提交，以及候选查询桥接。
- 新增 `.app` 打包脚本：`scripts/build-inputmethod-app.sh`，产物为 `.build/MacAIInput.app`。
- 新增 InputMethodKit `Info.plist`：`Resources/InputMethod/Info.plist`，关键字段为 `InputMethodConnectionName = MacAIInputConnection`、`InputMethodServerControllerClass = MacAIInputController`。
- 新增用户文档：`docs/user/inputmethodkit-shell.md`，说明构建、本地词库路径、手动安装和当前限制。
- 已通过的验证：合并后在 `main` 运行 `swift test --disable-sandbox`，31 个 XCTest、0 失败；运行 `./scripts/build-inputmethod-app.sh` 成功；`plutil -lint .build/MacAIInput.app/Contents/Info.plist` 通过。
- 未验证项：尚未在 macOS 系统输入源中手动安装和真实输入测试；下一步应做本机安装、候选窗口行为检查和输入体验修正。

## 2026-07-26 本机安装验证进展

- 已完成本机安装辅助脚本，并按用户选择将 `feature/local-install-validation` fast-forward 合并回 `main`；`.worktrees/local-install-validation` 已删除，本地 feature 分支已删除。
- 新增脚本：`scripts/install-local-inputmethod.sh`，可构建 `.build/MacAIInput.app`、编译样例 TSV 为 SQLite、复制双拼方案、安装到 `~/Library/Input Methods/MacAIInput.app`，并输出安装位置、词库路径、方案路径和导入报告路径。
- 脚本支持 `MACAI_REAL_HOME` fake home smoke test；fake home 下会跳过刷新 `TextInputMenuAgent`，真实 `HOME` 安装时会刷新。
- 已更新文档：`docs/user/inputmethodkit-shell.md` 和 `docs/user/dictionary-toolchain.md`，补充自动安装、本机验证清单和导入报告说明。
- 已执行真实本机安装：`/Users/HaoQi/Library/Input Methods/MacAIInput.app`、`/Users/HaoQi/Library/Application Support/MacAIInput/Dictionary.sqlite`、`DoublePinyin.tsv`、`LastImportReport.json` 均已生成，`InputMethodConnectionName = MacAIInputConnection`。
- 已通过的验证：合并后在 `main` 运行 `swift test --disable-sandbox`，31 个 XCTest、0 失败；`./scripts/build-inputmethod-app.sh` 通过；fake home 安装 smoke test 通过。
- 未验证项：还需要用户在 macOS 系统设置中启用 `MacAIInput` 输入源，并在真实文本输入框中检查 `gu`、Return/Tab、Backspace 和候选显示行为。
