# TODO

- [x] Mac AI 自研输入法：在 macOS Terminal 中处理 Apple 开发者工具 license gate：`sudo xcodebuild -license`；随后回到 `/Users/HaoQi/Documents/Codex/2026-07-25/mac-ai/.worktrees/dictionary-toolchain` 复跑 `swift test --disable-sandbox` 和词库 CLI 烟测。
- [ ] Haoqi Pinyin：注销并重新登录 macOS 后，在 `/Users/HaoQi/Documents/Codex/2026-07-25/mac-ai` 运行 `./scripts/check-inputmethod-install.sh`；若仍未启用，到 System Settings -> Keyboard -> Text Input -> Input Sources 手动添加 `Haoqi Pinyin`，再测试真实输入框里的 `gu`、Backspace、Return/Tab 和候选显示。
