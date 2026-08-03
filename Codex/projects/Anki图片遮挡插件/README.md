# Anki 图片遮挡插件

## 状态

- 2026-08-03：旧版 `Simple Image Occlusion` 已明确废弃，不再作为基线，不继续扩展，不再使用旧工作区或旧输出目录。
- 2026-08-03：现在要求重新开发通用图片遮挡制卡增强插件，设计文档位于 `/Users/HaoQi/Documents/Codex/anki_modules/docs/superpowers/specs/2026-08-03-universal-image-occlusion-design.md`。
- 新版定位：嵌入 Anki 原生 Add Cards 流程，使用专用笔记类型 `Universal Image Occlusion`，支持单图导入、矩形/多边形遮挡、每个遮挡区域生成一张卡，并为每张卡保存 `Question`、`Hint`、`Answer`、`Extra`、`Source` 等辅助文本。
- 新版项目根目录：`/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion`
- 新版源码目录：`/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/src/universal_image_occlusion`
- 新版测试目录：`/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/tests`
- 新版打包输出：`/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/dist/universal_image_occlusion.ankiaddon`
- 新版 QA 产物：`/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/artifacts`

## 旧版记录

- 旧版工作区：`/Users/HaoQi/Documents/Codex/2026-08-03/new-chat/work/simple-image-occlusion`
- 旧版交付目录：`/Users/HaoQi/Documents/Codex/2026-08-03/new-chat/outputs/simple_image_occlusion`
- 旧版安装包：`/Users/HaoQi/Documents/Codex/2026-08-03/new-chat/outputs/simple_image_occlusion_clean.zip`
- 这些旧版路径只作历史记录。默认不要读取、复用、打包或继续修改旧版代码；除非用户明确要求做对比。

## 维护纪律

- 每次更新迭代必须同步修改插件内 `README.md`。
- 涉及功能、安装方式、快捷键、字段、使用流程、限制范围或测试方式的变化，都必须更新 README 后再重新打包。
- 所有新版源码、测试、文档、构建包和 QA 产物都必须写在 `/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion` 下。

## 下一版已确认需求

- 入口：用户打开 Anki 原生 Add Cards，并选择插件专用笔记类型。
- 插件控件：Add Cards 界面出现 `Add Base Image`。
- 图片：MVP 只支持单张本地图片导入。
- 遮挡：支持矩形和多边形；不区分文字遮挡/区域遮挡。
- 编辑交互：仅制卡编辑时，鼠标悬停某个遮挡区域会临时隐藏该遮挡，方便查看底图；复习时不允许 hover 偷看。
- 文本：每个遮挡区域可配置 `Question`、`Hint`、`Answer`、`Extra`，整组可记录 `Source`。
- 生成：默认每个遮挡区域生成一张卡；未来可扩展整图多遮挡一起背。
- 标签/牌组：全部使用 Anki 原生 Add Cards 流程，不做插件标签预设。
- 非目标：不做 OCR、自动识别、AI 自动挖空、批量导入、移动端编辑、自定义调度/同步/媒体存储。
