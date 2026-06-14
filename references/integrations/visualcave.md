# VisualCave 集成 — 交互式逐步揭示图表

> [VisualCave](https://github.com/varkart/visualcave) 是一个 agentic skill。11 种 Mermaid 图表类型，独特的逐步揭示特性。

## VisualCave 的独有功能

| 功能 | 说明 | 我们是否有 |
|------|------|:---:|
| 11 种图表类型 | Flowchart/Sequence/Class/ER/State/Timeline/MindMap/Git/Pie/Gantt/Quadrant | ✅ 部分 |
| **逐步揭示** | 按阶段分步展开复杂图表，引导观众渐进式理解 | ❌ |
| 暗色模式 | 深色 UI 适合投影/夜间工作 | ❌ |
| 复制源码 | 一键复制 Mermaid 代码 | ❌ |
| 多格式导出 | PNG/SVG/PDF/动画 GIF | ✅ multi_export |
| 跨平台 | Claude Code / Cursor / Codex / Gemini CLI | ⚠️ 仅 Claude |

## 安装

```bash
# 从 GitHub 安装
claude plugin marketplace add varkart/visualcave
claude plugin install visualcave@varkart-skills

# 或直接 npm
npx skills add varkart/visualcave
```

## 使用

```
/visualcave 帮我画一个 OAuth 2.0 的认证流程图
/visualcave 把这个系统架构画成思维导图
```

## 逐步揭示模式

这是 VisualCave 最独特的特性——复杂图表可以分阶段展示：

```
阶段 1：显示核心流程（3 个节点）
  → 观众理解基本脉络
阶段 2：展开细节分支
  → 补充异常处理路径
阶段 3：揭示所有节点和连线
  → 获得完整图表

适用场景：
  - 技术演讲的动画图表
  - 教学中的渐进式知识展示
  - 向非技术客户汇报复杂系统
```

## 在我们的管线中

VisualCave 可作为「需要演示级交互图表」时的替代输出：

```
用户需求 → 判断：
  - 快速内部用？→ Mermaid (我们的通道 A)
  - 需要动画/演示？→ VisualCave
  - 需要可编辑？→ DrawIO MCP / XMind
```

## 关联

- [Mermaid 流程图](../ai-pipeline/mermaid-flowchart.md) — 基础 Mermaid 生成
- [Draw.io MCP 指南](../ai-pipeline/drawio-mcp-guide.md) — 另一个专业渲染选择
