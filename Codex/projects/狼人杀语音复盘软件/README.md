# 狼人杀语音复盘软件

## 项目状态

- 2026-07-20 创建第一版本地 Python MVP。
- 代码位置：`/Users/HaoQi/Documents/Codex/2026-07-20/new-chat/outputs/werewolf-review`
- 技术栈：Streamlit + faster-whisper。
- 当前能力：上传音频/视频，Whisper 转写，手动标注玩家/阶段/备注，保存 JSON 项目，导出 Markdown 复盘。
- 已创建样例项目：`data/sample_project.json`；已验证样例 Markdown 导出：`outputs/sample_export.md`。

## 当前限制

- 第一版不自动识别说话人，需要手动给每段选择玩家。
- 首次使用 Whisper 模型需要联网下载模型。
- 真实长录音效果受设备距离、背景噪音、多人抢话影响明显。

## 后续方向

- 增加说话人分离/声纹聚类，减少手动标注成本。
- 增加按玩家发言时长、发言次数、轮次分布统计。
- 增加投票记录表、身份配置、夜间行动记录。
- 增加矛盾点标签、关键词搜索和时间轴跳转。
