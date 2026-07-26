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

## 2026-07-26 输入源发现与诊断进展

- 已完成输入源发现/诊断改进，并按用户最新偏好默认选择 1，将 `feature/input-source-discovery` fast-forward 合并回 `main`；`.worktrees/input-source-discovery` 已删除，本地 feature 分支已删除。
- 新增输入法 icon 资源：`Resources/InputMethod/MacAIInputIcon.pdf`，并在 `Info.plist` 中加入 `tsInputMethodIconFileKey = MacAIInputIcon.pdf`。
- `scripts/build-inputmethod-app.sh` 现在会复制 icon 资源，并对最终 `.build/MacAIInput.app` 做 ad-hoc bundle 签名；签名后 `codesign` 显示 `Identifier=local.macai.inputmethod`、`Info.plist entries=18`、`Sealed Resources version=2`。
- 新增诊断脚本：`scripts/check-inputmethod-install.sh`，可检查 app、可执行文件、plist、bundle id、连接名、控制器类、icon、签名、SQLite 词库、双拼方案、导入报告、AppleEnabledInputSources 和 LaunchServices dump。
- 已重新真实安装：`/Users/HaoQi/Library/Input Methods/MacAIInput.app`，并保留旧版本备份目录。
- 已通过的验证：合并后在 `main` 运行 `swift test --disable-sandbox`，31 个 XCTest、0 失败；`./scripts/build-inputmethod-app.sh` 通过；fake home 安装与诊断通过。
- 当前状态：文件、plist、icon、签名、词库均 OK；`MacAIInput` 仍未出现在 `AppleEnabledInputSources`，LaunchServices dump 也暂未列出 `local.macai.inputmethod`。下一步应注销/重新登录 macOS 后重跑 `./scripts/check-inputmethod-install.sh`，再尝试系统设置中启用输入源。

## 2026-07-26 Haoqi Pinyin 命名进展

- 用户将输入法正式命名为 `Haoqi Pinyin`，图标要求使用单个 `H`。
- 已按默认选择 1 将 `feature/haoqi-pinyin-branding` fast-forward 合并回 `main`；`.worktrees/haoqi-pinyin-branding` 已删除，本地 feature 分支已删除。
- 用户可见名称已改为 `Haoqi Pinyin`：`CFBundleName`、`CFBundleDisplayName`、打包产物 `.build/Haoqi Pinyin.app`、安装目录 `~/Library/Input Methods/Haoqi Pinyin.app`、运行时数据目录 `~/Library/Application Support/Haoqi Pinyin`。
- 内部 bundle id、连接名和控制器类暂保持不变：`local.macai.inputmethod`、`MacAIInputConnection`、`MacAIInputController`，避免系统集成状态发生无必要变化。
- 图标资源 `Resources/InputMethod/MacAIInputIcon.pdf` 已从 `AI` 改为单个 `H`。
- 已执行真实安装：旧 `MacAIInput.app` 被移动到带时间戳的备份目录，新 `Haoqi Pinyin.app` 已安装；词库、双拼方案和导入报告已写入 `~/Library/Application Support/Haoqi Pinyin`。
- 已通过的验证：合并后在 `main` 运行 `swift test --disable-sandbox`，31 个 XCTest、0 失败；`./scripts/build-inputmethod-app.sh` 通过；fake home 安装与诊断通过。

## 2026-07-26 输入模式 metadata 进展

- 针对 `Haoqi Pinyin` 已安装但系统输入源未识别的问题，对比了本机 `/Library/Input Methods/Squirrel.app/Contents/Info.plist`。
- 发现成熟 InputMethodKit app 会声明 `TISInputSourceID` 和 `ComponentInputModeDict/tsInputModeListKey`；此前 `Haoqi Pinyin` 只声明了顶层 `tsInputMethod...` 字段。
- 已按默认选择 1 将 `feature/input-mode-metadata` fast-forward 合并回 `main`；`.worktrees/input-mode-metadata` 已删除，本地 feature 分支已删除。
- `Resources/InputMethod/Info.plist` 已新增：
  - `TISInputSourceID = local.macai.inputmethod`
  - `ComponentInputModeDict`，包含单个可见输入模式 `local.macai.inputmethod.Hans`
  - `TISIntendedLanguage = zh-Hans`
  - menu/palette/alternate icon 均为 `MacAIInputIcon.pdf`
  - `NSPrincipalClass = NSApplication`
  - `LSUIElement = true`
  - `LSBackgroundOnly = false`
- `scripts/check-inputmethod-install.sh` 已扩展检查 app-level TIS id、可见 input mode、Hans mode id 和语言。
- 已重新真实安装：`~/Library/Input Methods/Haoqi Pinyin.app` 以及 `~/Library/Application Support/Haoqi Pinyin`。
- 已通过的验证：合并后在 `main` 运行 `swift test --disable-sandbox`，31 个 XCTest、0 失败；`./scripts/build-inputmethod-app.sh` 通过；fake home 安装与诊断通过；真实安装诊断确认 input-mode metadata 存在。
- 当前状态：诊断仍显示 `Haoqi Pinyin is not enabled in AppleEnabledInputSources`；下一步应注销/重新登录 macOS，重新运行 `./scripts/check-inputmethod-install.sh`，再到系统设置里尝试启用 `Haoqi Pinyin`。

## 2026-07-26 TIS 注册 helper 进展

- 已完成 TIS 注册辅助命令，并按用户默认选择 1 将 `feature/tis-registration-helper` fast-forward 合并回 `main`；`.worktrees/tis-registration-helper` 已删除，本地 feature 分支已删除。
- 新增 Swift executable：`haoqi-pinyinctl`，支持 `register [--app <Haoqi Pinyin.app>] [--source-id <id>] [--mode-id <id>] [--no-select]`。
- 将系统识别 id 从 `local.macai.inputmethod` 调整为更标准的 `local.haoqi.inputmethod.HaoqiPinyin`；Hans input mode id 为 `local.haoqi.inputmethod.HaoqiPinyin.Hans`。
- `Resources/InputMethod/Info.plist` 已补齐 `CFBundleSupportedPlatforms`、`CFBundleSignature`、`CFBundleIconFile`、`InputMethodServerDelegateClass`、`TISIntendedLanguage`，并将 `tsInputMethodCharacterRepertoireKey` 改为 array。
- `scripts/build-inputmethod-app.sh` 现在会生成 `Contents/PkgInfo`；`scripts/install-local-inputmethod.sh` 真实 HOME 安装时会调用 `haoqi-pinyinctl register`，fake home smoke test 会跳过注册。
- code review 后已修正：
  - helper 选择输入模式后会重新检查 `kTISPropertyInputSourceIsSelected`，避免假报 selected。
  - 安装脚本不再吞掉 helper 的硬失败；非致命的会话同步/选择 warning 仍由 helper 以 exit 0 表达。
  - 文档中的手动注册命令显式传入 `--app "$HOME/Library/Input Methods/Haoqi Pinyin.app"`。
- 已执行真实安装：`/Users/HaoQi/Library/Input Methods/Haoqi Pinyin.app` 为新 bundle id 版本，词库和双拼方案仍在 `/Users/HaoQi/Library/Application Support/Haoqi Pinyin`。
- 已通过的验证：合并后在 `main` 运行 `swift test --disable-sandbox`，38 个 XCTest、0 失败；`./scripts/build-inputmethod-app.sh` 通过；fake home 安装与诊断通过；真实安装诊断确认 plist、PkgInfo、签名、词库、双拼方案均 OK。
- 当前状态：`haoqi-pinyinctl register` 已能找到并注册 `local.haoqi.inputmethod.HaoqiPinyin` 与 `local.haoqi.inputmethod.HaoqiPinyin.Hans`，但当前 Codex/macOS 会话中父级 input source 的 enabled 状态未反映，`AppleEnabledInputSources` 和 LaunchServices dump 仍为 warning。下一步需要注销/重新登录 macOS 后重跑诊断，或在系统设置中手动添加 `Haoqi Pinyin`。

## 2026-07-26 用户安装后输入仍为英文的诊断

- 用户反馈已安装但输入仍是英文。
- 重新运行 `./scripts/check-inputmethod-install.sh`：app、plist、签名、词库、双拼方案均 OK，但 `Haoqi Pinyin is not enabled in AppleEnabledInputSources` 仍存在。
- `defaults read com.apple.HIToolbox AppleEnabledInputSources` 未包含 `local.haoqi.inputmethod.HaoqiPinyin`；当前选中项也不是 Haoqi Pinyin。
- 词库和引擎本身可用：`macai-dict suggest --index ~/Library/Application\ Support/Haoqi\ Pinyin/Dictionary.sqlite --scheme ~/Library/Application\ Support/Haoqi\ Pinyin/DoublePinyin.tsv --keys gu` 返回「股四头肌」。
- 当前判断：问题优先定位为 macOS 输入源未启用/未切换到 Haoqi Pinyin，而不是词库或双拼引擎失效。下一步让用户在系统设置中手动添加并切换到 Haoqi Pinyin；若菜单栏已显示 Haoqi Pinyin 但仍输出英文，再进入 InputMethodKit 事件拦截层调试。

## 2026-07-26 Space 选首候选修正

- 用户截图证明 `Haoqi Pinyin` 已出现在 macOS 输入源设置中；之前只根据 `defaults` 判断未启用不够准确。
- 发现当前输入外壳只实现了字母 buffer、Backspace、Return/Tab 提交；未实现中文输入法最常见的 Space 选首候选。用户只打 `gu` 时看到英文，很可能是 composing buffer 尚未提交，或空格未被输入法消费。
- 新增 `CompositionSession` 核心状态机，统一管理字母输入、删除、首候选/原始 buffer 提交。
- `MacAIInputController` 已改为：字母进入 `CompositionSession`；Space、Return、Tab 提交首候选或 raw buffer；Backspace 删除 buffer。
- 新增 `CompositionSessionTests`：覆盖 `gu` 提交「股四头肌」、无候选回退 raw buffer、空 buffer 不提交。
- 验证：新增测试先因 `CompositionSession` 缺失失败；实现后 `CompositionSessionTests` 3 个测试通过；完整 `swift test --disable-sandbox` 41 个 XCTest、0 失败；`./scripts/build-inputmethod-app.sh` 成功生成 `.build/Haoqi Pinyin.app`。
- 当前限制：Codex 沙箱不能写入 `~/Library/Application Support/Haoqi Pinyin`，所以本轮未能替用户完成真实 HOME 重新安装。用户需在终端运行 `/Users/HaoQi/Documents/Codex/2026-07-25/mac-ai/scripts/install-local-inputmethod.sh`，再切换到 Haoqi Pinyin 测试 `gu` + Space。
