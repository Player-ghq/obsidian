# Anki 图片遮挡插件

## 状态

- 2026-08-03：旧版 `Simple Image Occlusion` 已明确废弃，不再作为基线，不继续扩展，不再使用旧工作区或旧输出目录。
- 2026-08-03：现在要求重新开发通用图片遮挡制卡增强插件，设计文档位于 `/Users/HaoQi/Documents/Codex/anki_modules/docs/superpowers/specs/2026-08-03-universal-image-occlusion-design.md`。
- 2026-08-03：新版 `Universal Image Occlusion` 已从零开发到 `/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion`，已生成安装包 `/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/dist/universal_image_occlusion.ankiaddon`。
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

## 新版验证

- 2026-08-03：`PYTHONPATH=universal_image_occlusion/src:universal_image_occlusion python3 -m unittest discover -s universal_image_occlusion/tests -v` 通过 15 个测试。
- 2026-08-03：`python3 -m compileall -q universal_image_occlusion/src` 通过。
- 2026-08-03：`PYTHONPATH=universal_image_occlusion/src:universal_image_occlusion python3 universal_image_occlusion/scripts/package_addon.py` 通过。
- 2026-08-04：修复安装时报错“无效的插件清单”：根因是 `.ankiaddon` 缺少非 AnkiWeb 分发所需的根目录 `manifest.json`。现打包脚本会写入 `{"package":"universal_image_occlusion","name":"Universal Image Occlusion"}`，重新打包后的安装包位于 `/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/dist/universal_image_occlusion.ankiaddon`。
- 2026-08-04：manifest 修复后 `unittest` 通过 16 个测试，`compileall` 通过，打包通过，并已检查 zip 根目录包含 `manifest.json`、`__init__.py` 和源码文件。
- 2026-08-04：修复 Anki 26.05 打开 Add Cards/Browse 崩溃：本地 Anki 字节码确认 `Editor._addButton` 签名为 `(icon, cmd, tip, label, id, toggleable, disables, rightside)`，不接收 Python 回调参数。现改为先注册 `editor._links["uio_add_base_image"] = on_click`，再调用 `editor._addButton(None, "uio_add_base_image", "Add Base Image", label="Add Base Image")`。回归测试先复现 `tip must be a string, got function`，修复后全量 `unittest` 通过 17 个测试，`compileall`、打包和 zip 清单检查通过。
- 2026-08-03：当前 shell 环境没有 `aqt`，Add Cards UI 注入、QFileDialog、AnkiWebView 桥接和真实 Anki note 创建仍需在 Anki 桌面端手测。

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
