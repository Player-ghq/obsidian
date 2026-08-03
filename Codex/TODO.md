# TODO

- [ ] Anki 图片遮挡插件：在真实 Anki 26.05 profile 安装 `/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/dist/universal_image_occlusion.ankiaddon`，验收 Config 快捷键、Add Cards/Browser/Edit Current 入口、默认锁定与解锁编辑、仅 `OcclusionData` 保存、无重复媒体/卡片，以及调度和复习历史保持不变。
- [x] Mac AI 自研输入法：在 macOS Terminal 中处理 Apple 开发者工具 license gate：`sudo xcodebuild -license`；随后回到 `/Users/HaoQi/Documents/Codex/2026-07-25/mac-ai/.worktrees/dictionary-toolchain` 复跑 `swift test --disable-sandbox` 和词库 CLI 烟测。
- [ ] Haoqi Pinyin：用户在终端运行 `/Users/HaoQi/Documents/Codex/2026-07-25/mac-ai/scripts/install-local-inputmethod.sh` 安装 Space 选首候选新版；切换到 `Haoqi Pinyin` 后，在真实输入框测试 `gu` + Space 是否提交「股四头肌」，并测试 Backspace、Return/Tab。若 Space 后仍输出 `gu` 或空格，继续调试 InputMethodKit 事件拦截层。
- [x] 运动康复真题库：用户提供 2023、2024、2025 微信真题文章的截图长图、复制文本、PDF 或原图后，按年份、学校、方向、生理/解剖/康复、题型、题干、分值、置信度、OCR 来源和复核原图入库，并补全上海体育大学/上海体育学院 2023-2025 运动康复重点。
- [ ] 运动康复真题库：人工复核 `23年.zip` 中上海体育学院运动康复源图 `qq370571-11.png`，确认 OCR 原文题号从 6 跳到 8 是否确实缺第 7 题。
