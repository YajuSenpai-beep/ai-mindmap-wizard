# NotebookLM MCP 集成

> 将 Google NotebookLM 作为思维导图的另一个生成和分发渠道。

## 为什么集成 NotebookLM？

| 我们的管道 | + NotebookLM |
|-----------|-------------|
| Markdown 导图 | **交互式音频概述**（AI 播客） |
| XMind / DrawIO / Mermaid | **幻灯片自动生成** |
| 静态导出 | **云端分享链接** |

## 安装

```bash
claude mcp add notebooklm -- npx -y notebooklm-mcp
```

## 可用的 MCP 工具

```json
{
  "tools": [
    "create_notebook",
    "add_source",
    "generate_mind_map",
    "generate_audio_overview",
    "generate_video_overview",
    "generate_slide_deck",
    "generate_quiz",
    "generate_flashcards",
    "generate_report",
    "list_notebooks"
  ]
}
```

## 集成工作流

### 流程 A：从我们的管道输出 → NotebookLM

```
① 用户输入文本/音频/视频
② 通道 F (素材准备) → OCR/转录
③ 通道 A (AI 生成) → Markdown 导图
④ multi_export.py → 多种格式
⑤ + NotebookLM MCP → 同时生成播客版概述
⑥ 分享 NotebookLM 链接给团队
```

### 流程 B：直接用 NotebookLM 生成

```
① 用户提供内容源 (URL/文件/文本)
② Claude Code 通过 NotebookLM MCP 创建 notebook
③ 添加源 → 调用 generate_mind_map
④ 导图在 NotebookLM 中可交互浏览
```

## 多输出对比

| 输出类型 | 我们的工具 | NotebookLM MCP | 适用场景 |
|---------|-----------|---------------|---------|
| 思维导图 | ✅ Markdown/Mermaid/XMind | ✅ 交互式云端 | 不同格式偏好 |
| 播客概述 | ❌ | ✅ AI 对话式播客 | 团队分享/通勤学习 |
| 幻灯片 | ❌ | ✅ 自动 PPT | 汇报场景 |
| 问答卡片 | ❌ | ✅ 测验生成 | 教育场景 |

## 关联

- [多模态输入管道](../material-prep/multimodal-input.md) — 音频/视频 → NotebookLM → 导图
- [多格式导出管线](../../tools/multi_export.py) — 并行导出 6 种格式
