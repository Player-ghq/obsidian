# Anki 图片遮挡插件

## 状态

- 2026-08-03：旧版 `Simple Image Occlusion` 已明确废弃，不再作为基线，不继续扩展，不再使用旧工作区或旧输出目录。
- 2026-08-03：现在要求重新开发通用图片遮挡制卡增强插件，设计文档位于 `/Users/HaoQi/Documents/Codex/anki_modules/docs/superpowers/specs/2026-08-03-universal-image-occlusion-design.md`。
- 2026-08-03：新版 `Universal Image Occlusion` 已从零开发到 `/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion`，已生成安装包 `/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/dist/universal_image_occlusion.ankiaddon`。
- 新版定位：嵌入 Anki 原生 Add Cards 流程，使用专用笔记类型 `Universal Image Occlusion`，支持单图导入及矩形/多边形遮挡；一次图片编辑把全部有序遮挡写入当前笔记，由 Anki 原生 Add 生成一条笔记和一张卡。
- 新版项目根目录：`/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion`
- 新版源码目录：`/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/src/universal_image_occlusion`
- 新版测试目录：`/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/tests`
- 新版打包输出：`/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/dist/universal_image_occlusion.ankiaddon`
- 新版 QA 产物：`/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/artifacts`
- V1 完整功能说明：`/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/docs/V1-FUNCTIONAL-SPEC.md`
- 后续版本路线图：`/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion/docs/ROADMAP.md`

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
- 2026-08-04：修复“正反面预览相同且不显示遮挡”：根因是原始 JSON 放入带引号的 HTML 属性后被 JSON 引号截断，同时前模板依赖 `Hint` 是否存在定位根节点，后模板还通过 `FrontSide` 重复显示图片。新版使用 `b64:` Base64 UTF-8 数据、显式根节点和隐藏 textarea；兼容旧 raw JSON，正反面各仅一张图。
- 2026-08-04：插件会在 profile open 时原地升级已有 `Universal Image Occlusion` 笔记类型的模板/CSS，保留旧笔记；遮挡弹窗已删除右侧文本面板，改为统一读取 Anki Add Cards 原生字段并复制到每张遮挡卡。
- 2026-08-04：全量 `unittest` 通过 39 个测试，`compileall` 通过；已用 Anki 26.05 自带 `aqt/PyQt6` 完成导入及 Qt offscreen 像素渲染检查。最终安装包 SHA-256 为 `69d090fe47218492fb5c902cf799bd2c9cf1803b0e9c8817f75a98ee6c15857b`。完整 Add Cards/真实集合制卡仍需在用户 Anki profile 手测。
- 2026-08-04：已确认下一版改为 IOE 风格原生 Qt 全画布编辑器。遮挡窗口不再创建卡片，`Done` 只把 `Image/OcclusionData` 写回当前 Add Cards 笔记，再由 Anki 原生 Add 保存一条笔记和一张卡。新卡正面覆盖全部有序遮挡，支持按钮依次永久揭示和无频闪 hover 临时揭示；背面一次性全部显示。旧 `MaskIndex` 卡继续保持单遮挡模式。规格位于 `/Users/HaoQi/Documents/Codex/anki_modules/docs/superpowers/specs/2026-08-04-ioe-style-single-card-sequential-reveal-design.md`。
- 2026-08-04：上述 IOE 风格一卡多遮挡版本已实现。编辑器支持图标工具栏、适应、指针中心缩放、中键或 Space+左键平移、重叠矩形/多边形创建、选择、移动、8 控制点缩放、顶点编辑和删除。Done 只回写当前笔记的 `Image/OcclusionData/MaskIndex`，写入前先完整检查字段，媒体仅在校验通过后加入。
- 2026-08-04：复习模板已实现 schema 2 `all_sequential`：正面全部遮挡，hover 临时显示且保持 pointer events 防频闪，按钮按创建顺序逐个永久显示，背面不创建遮挡层。schema 1、raw JSON、Base64 和非空 `MaskIndex` 保持旧单遮挡模式。
- 2026-08-04：独立代码审查提出的按钮作用域、媒体写入原子性、重叠遮挡、退化多边形和 schema 1 路由问题均已修复。最终 58 个单元测试、compileall、Anki 26.05 Qt offscreen 画布/图标测试和 21 项归档检查通过。安装包 SHA-256：`eaccc75ea5673b8a588bcb473dada3135a17d66eda7dddfd08254b60aa83ef1b`。
- 2026-08-04：已确认下一轮设计：所有复习/编辑快捷键通过 Anki `config.json` 配置，默认 `N` 依次揭示；新建 Mask 后自动切换 Select，可立即拖动；当前 schema-2 笔记可从 Add Cards、Browser、Edit Current 重新打开，只编辑 Mask、不替换图片；已有笔记打开时 `Enable mask editing` 默认关闭。规格：`/Users/HaoQi/Documents/Codex/anki_modules/docs/superpowers/specs/2026-08-04-configurable-shortcuts-reeditable-masks-design.md`。旧 schema-1 编辑暂不考虑。
- 2026-08-04：上述规格已确认，实施计划位于 `/Users/HaoQi/Documents/Codex/anki_modules/docs/superpowers/plans/2026-08-04-configurable-shortcuts-reeditable-masks.md`，按快捷键配置、Reviewer 注入、画布锁定、已有会话加载、编辑器入口、原子保存、QA 打包 7 个任务执行。
- 2026-08-04：可配置快捷键与已有 Mask 重编辑版本已实现并重新打包。默认复习快捷键为 `N`，所有编辑器快捷键均可在 Anki 插件 Config JSON 中修改或置空禁用；矩形/多边形完成后自动切换 Select，可立即拖动。
- 2026-08-04：schema-2 `all_sequential` 笔记可从 Add Cards、Browser、Edit Current 打开 `Edit Masks`。已有会话默认锁定，勾选 `Enable mask editing` 后可移动、缩放、新增和删除 Mask；不提供图片替换。保存仅修改 `OcclusionData`，使用单个 Anki 撤销事务，保留图片、文本、笔记/卡片 ID、标签、牌组、调度和复习历史。
- 2026-08-04：最终验证通过 90 个单元测试、`compileall`、Anki 26.05 自带 aqt/PyQt6 的画布与完整对话框 offscreen 冒烟测试，以及 25 项安装包清单检查。最终安装包 SHA-256：`9c35418656e7895478b7f2b600c65b19f346f15ef77658c78d6a250b7c281dc8`。剩余工作只有真实 Anki 26.05 profile 手动验收。
- 2026-08-04：新增首字段 `Index`，仅对 Add Cards 中未保存且为空的新笔记自动生成 `YYYY-MM-DD-NNN`，按本地日期和当日已保存最大编号加一；已有专用笔记类型通过 Anki `reposition_field` 原地升级，但不批量回填旧笔记。
- 2026-08-04：`config.json` 新增 `appearance.mask_color`，仅接受 `#RRGGBB`，默认 `#202124`，同时控制原生 Qt 编辑器和复习模板遮挡颜色。矩形 `R`、多边形 `P` 快捷键第二次按下切回 Select；工具栏点击仍直接选择。
- 2026-08-04：修复 macOS 工具图标持续蓝色：关闭 Select/Rectangle/Polygon 的 autoDefault、default 和焦点状态，并通过 QButtonGroup 与显式同步保证仅当前工具选中；已有锁定会话默认 Select。
- 2026-08-04：本轮最终验证通过 103 个单元测试、`compileall`、真实临时 Anki Collection 索引搜索、Anki 26.05 Qt 画布/对话框测试和 27 项安装包检查。安装包 SHA-256：`5393dd1899635460d279a5f812d918b0d2b62fa5f837bc3a42ffbd8ecf8be4a0`。

## 维护纪律

- 每次更新迭代必须同步修改插件内 `README.md`。
- 涉及功能、安装方式、快捷键、字段、使用流程、限制范围或测试方式的变化，都必须更新 README 后再重新打包。
- 所有新版源码、测试、文档、构建包和 QA 产物都必须写在 `/Users/HaoQi/Documents/Codex/anki_modules/universal_image_occlusion` 下。

## 后续版本路线图

- V1.1（P0）：编辑器内部撤销/重做；画布显示遮挡序号；遮挡列表与拖动调整揭示顺序。
- V1.2（P1）：显示上一个、显示下一个、全部显示、重新遮挡；新增动作全部支持 Config 快捷键；移动端点击遮挡揭示及完整触屏按钮。
- V1.3（P2）：遮挡透明度、边框颜色、揭示后轮廓颜色；新图导入阶段旋转与裁剪。已有笔记图片变换暂不纳入 V1.3。
- 后续版本继续保持“一图一卡、多遮挡、默认逐个显示”，并兼容现有 schema-2 `all_sequential` 笔记。

## 待验收

- 在用户真实 Anki 26.05 profile 安装最终包并重启。
- 验证 Add Cards 新建后原生 Add 只生成一条笔记和一张卡；Browser/Edit Current 能打开已有 schema-2 笔记且默认锁定。
- 验证解锁后移动/缩放/新增/删除 Mask，不产生重复媒体、笔记或卡片，并保持调度与复习历史。
- 验证 Config 中修改 `reveal_next` 后下一张卡生效，Reviewer hover 无频闪、快捷键逐个显示、背面全显。
- 验证同一天连续添加时 Index 依次为 `001/002/003`，`appearance.mask_color` 在编辑器和下一张复习卡同步生效，`R/P` 二次按键切回 Select，三个工具仅一个高亮。
- 非目标仍为 OCR、自动识别、AI 自动挖空、批量导入、移动端编辑、自定义调度/同步/媒体存储。
