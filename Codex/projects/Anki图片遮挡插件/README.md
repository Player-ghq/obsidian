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
- 2026-08-04：针对“选择图片后只出现白框且无报错”增加 WebView 诊断并调整页面加载方式：`stdHtml` 改为传 body fragment/head，而不是完整 HTML 文档；图片 src 改为 `/_anki/media/<url-encoded-name>`；编辑器顶部新增可见状态栏，显示图片加载失败、JS 错误、promise 错误和 `window.pycmd` 缺失。全量 `unittest` 通过 19 个测试，`compileall`、打包和 zip 内容检查通过。调试方式：终端运行 `/Applications/Anki.app/Contents/MacOS/anki` 查看 Python/stdout；或运行 `QTWEBENGINE_REMOTE_DEBUGGING=8080 /Applications/Anki.app/Contents/MacOS/anki` 后用 Chrome 打开 `http://localhost:8080` 查看 WebView console。
- 2026-08-04：根据终端日志修复 WebView CSP 问题：Anki 26.05 拒绝执行 inline script，导致编辑器 JS 没有运行。现将编辑器 JS/CSS 移至 `web/editor.js` 和 `web/editor.css`，注册 `mw.addonManager.setWebExports("universal_image_occlusion", r"web/.*(css|js)")`，并通过 `stdHtml(css=[...], js=[...])` 从 `/_addons/universal_image_occlusion/web/...` 加载。全量 `unittest` 通过 21 个测试，`compileall`、打包和 zip 内容检查通过。
- 2026-08-04：继续修复 WebView `Cannot read properties of undefined (reading 'children')`：根因是自定义遮挡弹窗调用 `stdHtml(..., context=editor)`，Anki 26.05 会把页面按 `PageContext.EDITOR` 处理，而自定义页面没有原生 editor DOM。现改为 `context=None`，让它作为 unknown/custom WebView 加载。新增回归测试后全量 `unittest` 通过 22 个测试，`compileall`、打包和 zip 内容检查通过。
- 2026-08-04：由于 Anki 26.05 仍持续在 `/_anki/legacyPageData` 路径报 `Cannot read properties of undefined (reading 'children')`，已废弃遮挡编辑器 WebView 实现，改为原生 Qt 弹窗：`QPixmap/QPainter/QWidget` 绘制图片与遮挡，`QPushButton/QTextEdit` 处理工具栏和文本字段。`aqt_integration.py` 不再引用 `aqt.webview`、`AnkiWebView` 或 `stdHtml`，也不再注册 `setWebExports`。全量 `unittest` 通过 20 个测试，`compileall`、打包和 zip 内容检查通过。
- 2026-08-04：修复原生 Qt 遮挡框只能单击生成固定 `0.08` 大小、无法选择/移动/缩放的问题。新增独立 `geometry.py` 与 `qt_canvas.py`：矩形按实际拖拽创建，矩形和多边形可整体移动并通过 8 个控制点缩放，多边形还可单独拖动顶点，所有坐标限制在图片范围内。编辑器使用不修改原图的透明叠加层，只有遮挡区域不透明；鼠标悬停编辑区遮挡会临时显示底图，复习时无悬停揭示。
- 2026-08-04：补齐 Select 工具、整组 `Source` 输入和遮挡切换前文本保存，避免切换区域丢失 `Question/Hint/Answer/Extra`。已移除废弃的 `editor_assets.py`、`web/editor.js`、`web/editor.css` 及旧 WebView 测试，安装包只保留原生 Qt 路径。
- 2026-08-04：最终全量 `unittest` 通过 32 个测试，`compileall` 通过；使用 Anki 26.05 自带 `aqt/PyQt6` 在 Qt offscreen 环境模拟验证矩形创建/移动/缩放、多边形顶点编辑/缩放和悬停命中。最终包仍位于 `/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/dist/universal_image_occlusion.ankiaddon`，SHA-256 为 `7a221fc1872fcdfa21a6c387dc834b988c778655455799fbb57ac2ff33cd6efd`。
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
