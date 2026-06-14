# 多模态输入管道：音频/视频 → 思维导图

> 从 DeLive、yt-dlp-mcp、NotebookLM MCP 等工具提炼。扩展素材准备通道 (F) 覆盖音频和视频。

## 管道概览

```
音频/视频源
  ├── YouTube URL → yt-dlp-mcp 提取字幕 → 文本
  ├── 本地音视频 → DeLive (12 ASR 引擎) → 转录文本
  ├── 播客 → 小宇宙/喜马拉雅 → Get笔记 API → 转录文本
  └── 会议录音 → 系统音频捕获 → whisper.cpp → 文本

  ↓ 转录为文本后

  AI 结构化 → Markdown → 走通道 A 生成导图
```

## 方案一：YouTube/视频 URL → 导图

### 安装 yt-dlp-mcp

```bash
claude mcp add yt-dlp -- npx -y yt-dlp-mcp
```

### 集成流程

```
① 用户提供 YouTube/Bilibili 链接
② yt-dlp-mcp 自动下载字幕 (VTT) → 提取纯文本
③ AI 收到完整转录文本
④ 走通道 A 的标准提示词 → 生成思维导图 Markdown
⑤ multi_export.py 并行导出多种格式
```

### 一站式命令

```bash
# 从 YouTube 视频直接生成思维导图
python tools/pipeline.py --input-type youtube --url "https://youtube.com/watch?v=xxx" --output my_mindmap
```

## 方案二：本地音频/会议录音 → 导图

### 安装 DeLive

[DeLive](https://github.com/XimilalaXiang/DeLive) — 系统音频捕获 + 12 ASR 引擎 + AI Review Desk。

```bash
# 下载对应平台版本
# 配置 ASR 引擎 (推荐 Groq 免费额度 或 whisper.cpp 本地)
# 启动 DeLive → 系统托盘常驻
```

### 工作流

```
① DeLive 实时捕获系统音频（浏览器/会议/播放器）
② 选择 ASR 引擎转录 → 文本流式输出
③ 在 AI Review Desk 中：
   - 自动生成章节分段
   - 提取关键词
   - 生成结构化简报
   - **生成思维导图**
④ 导出 Markdown → 走通道 A 进一步美化
```

## 方案三：NotebookLM MCP → 导图

### 安装

```bash
claude mcp add notebooklm -- npx -y notebooklm-mcp
```

### 直接生成导图

```python
# NotebookLM MCP 原生支持思维导图生成
mcp_call("notebooklm", "generate_mind_map", {
    "notebook_id": "abc456",
    "source_type": "video",  # 或 "audio", "url", "text"
    "output_format": "markdown"
})
```

### 还能同时生成

| 输出 | MCP 工具 |
|------|---------|
| 思维导图 | `generate_mind_map` |
| 播客音频 | `generate_audio_overview` |
| 幻灯片 | `generate_slide_deck` |
| 视频概述 | `generate_video_overview` |
| 问答卡片 | `generate_quiz` |

## 方案四：多模态一站式 (qiaomu)

[qiaomu-anything-to-notebooklm](https://github.com/joeseesun/qiaomu-anything-to-notebooklm) — Claude Code Skill，15+ 输入源。

```
输入: YouTube / 小宇宙播客 / B站 / 微信文章 / PDF / EPUB / DOCX
  ↓ 自动提取/转录
NotebookLM 处理
  ↓
输出: 思维导图 + PPT + 播客 + 报告 + 视频
```

## 在我们的通道中的位置

```
通道 F (素材准备) 扩展：
  原有：图片/PDF/Word/PPT/HTML → OCR → 文本
  新增：音频/视频/播客/会议 → 转录 → 文本 → 通道 A
```

## 关联

- [OCR 提取指南](ocr-extraction.md) — 图片/PDF 的静态文本提取
- [格式提取](format-extraction.md) — Word/PPT/HTML 文档
- [对话转导图](../ai-pipeline/realtime-mindmap.md) — 实时对话场景
