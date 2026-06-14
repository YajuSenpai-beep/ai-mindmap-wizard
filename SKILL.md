---
name: ai-mindmap
description: |
  思维可视化引擎：图片/PDF→OCR→AI→Markdown→XMind/draw.io，全管道覆盖。
  触发词：「做思维导图」「生成导图」「流程图」「mindmap」「画流程图」「XMind」「draw.io」「OCR」「提取知识」。
---

# 思维可视化引擎

> 核心价值在 `tools/` 目录的 19 个 Python 脚本。工具干活，文档查阅——各司其职。

## 高频操作

| 想做什么 | 怎么做 |
|---------|-------|
| 文本 → 思维导图 | 用下方提示词，复制到任意 AI → 得到 Markdown → 导入 XMind |
| 图片/PDF → 导图 | `pip install -r tools/requirements.txt && python tools/pipeline.py 图片目录 项目名` |
| Markdown → XMind 原生文件 | `python tools/markdown_to_xmind.py input.md -o output.xmind` |
| Markdown → 6 种格式 | `python tools/multi_export.py input.md -f all` |
| Mermaid 语法修复 | `python tools/mermaid_fixer.py input.mmd` |
| 导图 → PPT | `python tools/mindmap_to_ppt.py input.md -c professional` |
| URL → 导图 | `python tools/url_to_mindmap.py https://example.com/article` |
| 导图结构分析 | `python tools/diagram_editor.py input.md --analyze` |
| 品牌配色适配 | `python tools/brand_adapt.py --name notion` |
| MCP 服务 | `claude mcp add mindmap-wizard -- python tools/mcp_server.py` |
| 质量评估 | `python tools/eval.py --input tests/benchmark/ --models claude,deepseek` |

## AI 提示词

```
你是一位信息结构化专家。将以下内容整理为思维导图 Markdown。
要求：# 中心主题 / ## 主要分支 / ### 细节 / - 叶子。层级≤4，每节点≤15字，只输出 Markdown。
内容：[粘贴]
```

## 知识库

66 篇参考指南在 `references/` 下。**直接打开阅读比通过 Skill 加载更快**：

| 目录 | 内容 | 入口 |
|------|------|------|
| methodology/ | 9 篇：五星心法·7要素·发散收敛·子母图·多视角·Tufte原则·知识图谱 | [索引](references/methodology/) |
| diagram-types/ | 8 篇：37 种图表选型矩阵 | [速查](references/diagram-types/index.md) |
| software/ | 14 篇：XMind·draw.io·WPS·Excel·Word·PPT·C4D·Think-Cell·Obsidian·Excalidraw 等 | [目录](references/software/) |
| ai-pipeline/ | 15 篇：文本/图片/主题→导图·D3·DrawIO·Mermaid·YouTube·对话·无提示词 | [目录](references/ai-pipeline/) |
| material-prep/ | 5 篇：OCR·格式提取·Obsidian·多模态·管道总览 | [目录](references/material-prep/) |
| troubleshooting/ | 3 篇：防幻觉·质量自检·常见问题 | [目录](references/troubleshooting/) |
| integrations/ | 5 篇：NotebookLM·VisualCave·开源库·商业工具·本地模型 | [目录](references/integrations/) |
| advanced/ | 1 篇：6 种设计模式 | [查看](references/advanced/design-patterns.md) |
| templates/ | 6 个：读书笔记·会议纪要·职业规划·项目启动·周回顾·SWOT | [目录](references/templates/) |

## 诚实边界

- 工具链是本地 Python 脚本，AI 提示词需手动复制到任意 LLM
- 知识库是静态 MD 文件，直接打开阅读比通过 Skill 加载更快
- 不替代 XMind/draw.io，不保证 AI 输出 100% 完美
