# Draw.io MCP 直接生成指南

> jgraph 官方 `@drawio/mcp` 服务器集成。一行命令让 Claude Code 直接在 Draw.io 中生成和编辑图表。

## 为什么用 MCP 而非手动导入？

| | 手动导入（旧方式） | MCP 直接生成（新方式） |
|------|------|------|
| 操作步骤 | 生成 → 保存 → 打开 draw.io → 导入 | **一条指令** |
| 修改反馈 | 改代码→重新导入→检查 | **生成即所见** |
| 协作 | 需导出文件再分享 | 直接在 draw.io 中打开编辑 |

## 安装

```bash
# 一行安装官方 Draw.io MCP 服务器
claude mcp add drawio -- npx -y @drawio/mcp
```

## 四种使用模式

| 模式 | 命令 | 适用 |
|------|------|------|
| **App Server**（零安装） | 使用远程 `mcp.draw.io/mcp` | 快速体验 |
| **Tool Server** | `claude mcp add drawio -- npx -y @drawio/mcp` | 浏览器内编辑 |
| **Skill + CLI** | `npx @drawio/mcp generate --format png` | 批量生成+导出 |
| **Project Instructions** | 在 Claude Project 指令中声明 | 团队共享 |

## 支持的输入格式

```
- XML (.drawio 原生格式) → 在 Draw.io 编辑器中打开
- CSV (表格数据) → 自动转换为图表
- Mermaid.js → 先转 Draw.io XML 再渲染
```

## 在我们的管道中集成

### 方案 A：快速生成（推荐）

```
用户输入文本
  ↓
AI 生成 Mermaid 代码（现有通道 A）
  ↓
Claude Code 自动调用 Draw.io MCP
  ↓
在 Draw.io 浏览器中打开，可直接编辑
```

### 方案 B：程序化批量

```bash
# 将 Markdown 层级导出为 CSV → Draw.io MCP 自动转图表
python tools/markdown_to_csv.py input.md | \
  npx @drawio/mcp generate --format png --output diagram.png
```

### 方案 C：结合多格式导出

```
AI 一次生成 → Mermaid 代码
  ├→ Draw.io MCP → .drawio 原生文件
  ├→ markdown_to_xmind.py → .xmind
  ├→ mermaid_fixer.py 修复 → .mmd
  └→ Excalidraw→ .excalidraw
```

## 导出为 PNG

```bash
claude mcp call drawio export \
  --input diagram.drawio \
  --format png \
  --scale 2.0 \
  --output diagram.png
```

## 与现有工具的对比

| 工具 | 生成方式 | 编辑能力 | 安装 |
|------|---------|---------|------|
| `@drawio/mcp` | MCP 直接生成 | ✅ 浏览器内完整编辑 | `npx` |
| `drawio-generation.md`(我们的) | AI 生成 XML | ⚠️ 需手动保存+导入 | 无额外安装 |
| `multi-chart-draw-skills` | Skill + Python 渲染 | ❌ 仅输出图片 | `npx skills add` |

## 关联

- [DrawIO 生成管道](drawio-generation.md) — 不依赖 MCP 的手动方案
- [Mermaid 流程图](mermaid-flowchart.md) — Mermaid→DrawIO 的输入源
- [工具对照表](../software/cross-tool-mapping.md) — 各工具功能矩阵
