# bili2text

## 2026-07-31 项目状态

- 已将视频/音频转文字核心逻辑抽成 `transcriber.py`，支持本地 `mp3/mp4/wav/m4a/flv/mov/mkv/avi/webm/aac/ogg/flac` 等文件。
- GUI 入口为 `window.py`，支持选择本地媒体、输出目录、Whisper 模型、分段分钟数，默认约 5 分钟分段并输出带时间段标题的 txt。
- CLI 入口为 `main.py`：`.venv/bin/python main.py <文件路径> --model small --segment-minutes 5`。
- 项目虚拟环境 `.venv` 已安装依赖；`requirements.txt` 已改为 UTF-8，并使用 `openai-whisper==20250625`、`audioop-lts==0.2.2`、`setuptools<81` 兼容 Python 3.13。
- 已实现 `imageio-ffmpeg` 回退：系统没有 `ffmpeg` 时，会创建 `.runtime/ffmpeg` 链接供 Whisper 调用。
- 验证通过：单元测试 3 个通过、py_compile 通过、`main.py` 端到端 1 秒 wav 烟测通过。

## 后续可选

- 用真实中文讲话音频/视频验证转写质量和 5 分钟长文件输出。
- 如需交付给非开发用户，可再做 PyInstaller 打包。
