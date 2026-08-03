# Anki 图片遮挡插件

## 状态

- 2026-08-03：为替代容易崩溃的 Image Occlusion Enhanced，开发了第一版 `Simple Image Occlusion`。
- 2026-08-03：发布 `0.1.1`，修复 Anki 26.05 加载插件时 `mw.col is None` 导致的启动崩溃。
- 第一版定位：稳定优先，只支持矩形遮挡，不做自由形状、箭头、文字、分层、旧卡转换或原地编辑旧卡。
- 工作区：`/Users/HaoQi/Documents/Codex/2026-08-03/new-chat/work/simple-image-occlusion`
- 交付目录：`/Users/HaoQi/Documents/Codex/2026-08-03/new-chat/outputs/simple_image_occlusion`
- 干净安装包：`/Users/HaoQi/Documents/Codex/2026-08-03/new-chat/outputs/simple_image_occlusion_clean.zip`

## 已实现

- 插件内 README 使用文档，包含安装、使用、限制、测试和迭代纪律。
- 启动安全：不在插件导入阶段直接访问 `mw.col.models`，等 profile 打开后再创建笔记类型。
- Anki 编辑器按钮 `SIO`，快捷键 `Ctrl+Shift+I`。
- 本地选择图片。
- HTML/JS 矩形遮挡编辑器，支持绘制、选择、删除、清空矩形。
- 两种模式：`hide_all` 与 `hide_one`。
- 自动创建 `Simple Image Occlusion` 笔记类型。
- 为每个遮挡矩形生成一张卡。
- 背面有 `Toggle Masks` 按钮。
- 纯逻辑测试使用 `python3 -m unittest`，覆盖矩形校验、SVG 生成、note payload。

## 验证

- 2026-08-03：`0.1.1` 在交付目录通过 7 个测试，新增启动回归测试 `tests/test_startup.py`。
- 2026-08-03：`python3 -m unittest discover -s tests -v` 在交付目录通过 6 个测试。
- 2026-08-03：`python3 -m compileall -q outputs/simple_image_occlusion` 通过。
- 尚未在真实 Anki/AQT 运行时手测。

## 维护纪律

- 每次更新迭代必须同步修改插件内 `README.md`。
- 涉及功能、安装方式、快捷键、字段、使用流程、限制范围或测试方式的变化，都必须更新 README 后再重新打包。
