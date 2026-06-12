---
name: ai-mindmap
description: |
  思维可视化引擎：覆盖方法论(五星心法/7要素/发散收敛)、37种图表选型、AI管道(Markdown→XMind / Mermaid→draw.io)、软件操作、故障排查。
  触发词：「做思维导图」「生成导图」「思维导图」「流程图」「mindmap」「AI导图」「整理成导图」「画流程图」「怎么梳理」「怎么组织」「该用什么图」「XX图怎么画」「XMind」「draw.io」「快捷键」。
---

# 思维可视化引擎

> AI 做你的思维教练 —— 从「怎么想」到「怎么画」到「用什么画」，一条龙覆盖。

## 核心理念

```
          ┌─────────────────────────────┐
          │       思维可视化引擎          │
          │    Thought Visualization     │
          ├─────────────────────────────┤
          │                             │
          │  心法层 WHY  →  methodology/ │
          │  技法层 HOW  →  diagram-types/│
          │  工具层 WHAT →  software/    │
          │           + ai-pipeline/     │
          │                             │
          └─────────────────────────────┘
```

- **AI 负责结构化**，专业软件负责可视化
- Markdown / Mermaid 是 AI 与软件之间的通用交换语言
- 思维导图的核心不是画图，是**思维方式**（五星心法）
- 这套流程**与具体 AI 工具无关**，任何 LLM 都能套用

---

## 通道检测：你说的第一句话决定走哪条路

收到用户输入后，快速判断意图，进入对应通道：

| 通道 | 触发信号 | 用户典型说法 |
|------|---------|------------|
| **A: 快速生成** | 给了具体内容+要求生成 | 「把这篇做成思维导图」「画个XX流程图」「整理这段内容」 |
| **B: 方法指导** | 询问如何思考/组织 | 「怎么梳理」「没有思路」「不知道怎么组织」「想不清楚」 |
| **C: 图表选型** | 询问用什么图 | 「该用什么图」「这个场景适合什么」「XX图怎么画」「哪种图表」 |
| **D: 软件操作** | 询问工具怎么用 | 「XMind怎么」「draw.io」「快捷键」「导入不了」「乱码了」 |
| **E: 完整流程** | 大而全的需求 | 「帮我全面分析XX」「从零开始做XX的规划」 |

> 如果用户一句话触发多个通道（如「帮我把这个需求文档做成流程图，但我不知道用哪种」），先 C 选型 → 再 A 生成。

---

## 通道 A: 快速生成（最高频）

用户给了具体内容，快速走 AI 管道。

### A1. 确认类型

> **你想生成什么？**
> 1. 🗺️ 思维导图（Markdown → XMind）
> 2. 🔀 流程图（Mermaid → draw.io）

### A2. 确认素材来源

| 用户手头有什么 | → 加载 |
|--------------|-------|
| 可以直接粘贴的文本 | [[references/ai-pipeline/text-to-mindmap]] |
| 思维导图的图片想数字化 | [[references/ai-pipeline/image-to-mindmap]] |
| 只有一个主题/想法 | [[references/ai-pipeline/topic-to-mindmap]] |
| 要画流程图 | [[references/ai-pipeline/mermaid-flowchart]] |

### A3. 给出提示词 + 操作步骤

根据素材类型，从对应的 reference 文件中取出：
1. 贴给用户的 AI 提示词（用户复制去任意 AI 工具）
2. 保存 `.md` / `.mmd` 文件的步骤（强调 UTF-8）
3. 导入 XMind / draw.io 的步骤

### A4. 如果用户反馈「AI 输出有问题」

→ 参考 [[references/ai-pipeline/prompt-templates]] 中的优化技巧调整提示词
→ 或参考 [[references/troubleshooting/common-issues]] 排查

---

## 通道 B: 方法指导

用户不知道怎么思考/组织，需要的是方法论。

### B1. 判断需求维度

| 用户的需求 | → 推荐方法 | 加载 |
|-----------|-----------|------|
| 信息太多想梳理 | 结构化+逻辑化 | [[references/methodology/five-star-heart]] |
| 画出来的导图不好看/不清晰 | 7 要素规范 | [[references/methodology/seven-elements]] |
| 需要创意/突破思维框 | 发散-收敛循环 | [[references/methodology/diverge-converge]] |
| 具体场景（学习/职业/演讲/时间管理/活动） | 场景模板 | [[references/methodology/application-scenarios]] |

### B2. 给出方法论框架 + 可选的 AI 衔接

1. 先给用户讲清楚「这个场景应该怎么思考」
2. 然后问：「要不要我帮你生成一份 Markdown 模板，你拿去 AI 工具扩展？」
3. 如果用户要 → 衔接到通道 A

---

## 通道 C: 图表选型

用户不确定该用什么图。

### C1. 查决策矩阵

从 [[references/diagram-types/index]] 中按用户目的匹配：
- 「我想分析根本原因」→ 鱼骨图
- 「我想规划项目时间」→ 甘特图
- 「我想设计系统架构」→ 架构图 / 拓扑图
- ...

### C2. 给出推荐 + 详情

1. 推荐 1-2 种图表类型
2. 从对应的分类文件加载详情：
   - 组织层级 → [[references/diagram-types/org-hierarchy]]
   - 流程类 → [[references/diagram-types/process-flow]]
   - 项目管理 → [[references/diagram-types/project-management]]
   - 分析工具 → [[references/diagram-types/analysis-tools]]
   - 技术图 → [[references/diagram-types/technical-diagrams]]
   - 商业战略 → [[references/diagram-types/business-strategy]]
   - 专业制图 → [[references/diagram-types/specialized]]

### C3. 可选衔接

> 「确定了图表类型后，要不要我帮你生成 AI 提示词去画？」

---

## 通道 D: 软件操作

用户问具体工具怎么用。

| 用户问什么 | 加载 |
|-----------|------|
| XMind 怎么用 | [[references/software/xmind-guide]] |
| draw.io 怎么用 | [[references/software/drawio-guide]] |
| XMind vs draw.io vs Visio 该用哪个 | [[references/software/cross-tool-mapping]] |
| 快捷键 | [[references/software/keyboard-shortcuts]] |
| 出错了/乱码/导入失败 | [[references/troubleshooting/common-issues]] |

---

## 通道 E: 完整流程

用户要全面分析，走串联：**B 方法论 → C 选型 → A 生成 → D 操作**

1. 先用通道 B 帮用户理清思路结构
2. 再用通道 C 确认适合的图表类型
3. 用通道 A 生成 AI 提示词，用户去生成 Markdown/Mermaid
4. 用通道 D 指导导入和美化
5. 全程穿插 [[references/troubleshooting/common-issues]] 防坑

---

## 工作流速查卡

```
┌──────────────────────────────────────────────────────────┐
│                 思维可视化引擎 · 速查                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  🧠 不知道怎么想？→ 通道 B：五星心法 / 7要素 / 发散收敛     │
│  📊 不知道用什么图？→ 通道 C：37种图表按功能分类 + 决策矩阵  │
│  ⚡ 有内容要生成？→ 通道 A：AI提示词 → .md → XMind/draw.io │
│  🔧 软件不会用？→ 通道 D：XMind / draw.io 操作指南         │
│  🚀 从零开始？→ 通道 E：B→C→A→D 一站串联                 │
│                                                          │
│  核心工具链：任意 AI + XMind + draw.io（全免费）           │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## 诚实边界

**能做的**：
- 提供工具无关的 AI 提示词模板，拿到任何 LLM 都能用
- 指导从素材到可视化导图的完整流程
- 37 种图表类型的选型建议和绘制要点
- 思维导图方法论（五星心法、7 要素、发散-收敛）
- XMind 和 draw.io 的操作指导和快捷键
- 帮助诊断导入过程中常见的格式/编码问题

**不能做的**：
- 直接调用 AI 生成内容（你需要自己去任意 AI 工具中提问）
- 替代 XMind / draw.io 的安装
- 保证 AI 输出 100% 完美 — AI 生成有随机性，通常需要微调
- 替代专业领域的深度知识（如电路设计、消防安全规范等）
