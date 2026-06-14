# YouTube 时间戳思维导图

> Mapify 风格——视频的每个关键节点链接到精确时间戳。

## 为什么做 YouTube 导图？

- 1 小时视频 = 无法搜索、难以回顾
- 思维导图 + 时间戳 = 可视化目录 + 一键跳转

## 管道

```
YouTube URL
  ↓ yt-dlp-mcp 提取字幕
纯文本转录
  ↓ AI 结构化
Markdown 导图（每个 ## 节点含 YouTube 时间戳链接）
  ↓ multi_export.py
HTML 交互式导图（点击节点 = 跳转到视频对应时刻）
```

## 时间戳 Markdown 格式

```markdown
# 视频标题
## [0:00] 开场与背景 ([链接](https://youtube.com/watch?v=xxx&t=0s))
## [3:15] 核心概念一 ([链接](https://youtube.com/watch?v=xxx&t=195s))
### [4:30] 案例讲解 ([链接](https://youtube.com/watch?v=xxx&t=270s))
## [12:00] 核心概念二 ([链接](https://youtube.com/watch?v=xxx&t=720s))
```

## 一键脚本

```bash
#!/bin/bash
# scripts/youtube_to_mindmap.sh
URL="$1"
VIDEO_ID=$(echo "$URL" | grep -oP 'v=\K[^&]+')

# 步骤1：提取字幕
claude mcp call yt-dlp get_transcript --url "$URL" > /tmp/transcript.txt

# 步骤2：AI 生成含时间戳的导图
cat /tmp/transcript.txt | python -c "
import sys
text = sys.stdin.read()
# 用 AI prompt 模版包装
print(f'''你是一位视频内容结构化专家。
将以下视频转录整理为思维导图，每个节点标注时间戳 (格式: [MM:SS])。

{text[:5000]}

要求：层级 ≤3，节点 ≤15字，保留关键时间标签。''')
"

# 步骤3：导出
python multi_export.py /tmp/transcript_mindmap.md -f html
echo "✅ 交互式 HTML 已生成（点击节点跳转视频）"
```

## 关联

- [多模态输入管道](../material-prep/multimodal-input.md) — 音频/视频处理
- [url_to_mindmap.py](../../tools/url_to_mindmap.py) — 网页一键转导图
- [对话转导图](realtime-mindmap.md) — 实时对话场景
