---
name: ai-mindmap
description: |
  思维可视化引擎：图片/PDF→OCR提取→AI生成Markdown→XMind/draw.io 思维导图，全管道覆盖。
  含方法论(五星心法/7要素/发散收敛)、37种图表选型、素材准备(OCR/去重/聚类)、AI管道、软件操作。
  触发词：「做思维导图」「生成导图」「思维导图」「流程图」「mindmap」「AI导图」「整理成导图」「画流程图」「怎么梳理」「怎么组织」「该用什么图」「XX图怎么画」「XMind」「draw.io」「快捷键」「演示」「demo」「模板」「提取知识」「图片转笔记」「OCR」「整理截图」「PDF转导图」。
---

# 思维可视化引擎

> 从「一堆图片/PDF」到「一张可编辑的思维导图」——全管道一站式覆盖。

## 核心理念

```
          ┌─────────────────────────────────┐
          │         思维可视化引擎            │
          │      Thought Visualization       │
          ├─────────────────────────────────┤
          │                                 │
          │  素材层 IN   →  material-prep/  │
          │  心法层 WHY  →  methodology/    │
          │  技法层 HOW  →  diagram-types/  │
          │  工具层 WHAT →  software/       │
          │           + ai-pipeline/        │
          │                                 │
          └─────────────────────────────────┘
```

- **素材 → 导图**：图片/PDF → OCR 提取 → AI 结构化 → Markdown → XMind/draw.io
- AI 负责结构化，专业软件负责可视化
- 这套流程**与具体 AI 工具无关**，任何 LLM 都能套用

---

## 通道检测：你说的第一句话决定走哪条路

收到用户输入后，快速判断意图，进入对应通道：

| 通道 | 触发信号 | 用户典型说法 |
|------|---------|------------|
| **演示** | 第一次使用/想看效果 | 「演示」「示例」「demo」「怎么用」「能做什么」 |
| **A: 快速生成** | 给了具体内容+要求生成 | 「把这篇做成思维导图」「画个XX流程图」「整理这段内容」 |
| **B: 方法指导** | 询问如何思考/组织 | 「怎么梳理」「没有思路」「不知道怎么组织」「想不清楚」 |
| **C: 图表选型** | 询问用什么图 | 「该用什么图」「这个场景适合什么」「XX图怎么画」「哪种图表」 |
| **D: 软件操作** | 询问工具怎么用 | 「XMind怎么」「draw.io」「快捷键」「导入不了」「乱码了」 |
| **E: 完整流程** | 大而全的需求 | 「帮我全面分析XX」「从零开始做XX的规划」 |
| **F: 素材准备** | 手头是图片/PDF/文档 | 「整理截图」「PDF转导图」「图片转笔记」「批量OCR」「提取知识」 |

> 通道 F 是通道 A 的上游：先把图片/PDF 变成文本，再走通道 A 生成导图。

> 如果用户一句话触发多个通道（如「帮我把这个需求文档做成流程图，但我不知道用哪种」），先 C 选型 → 再 A 生成。
> 如果用户是第一次使用或说「演示」「demo」「怎么用」，先走**演示通道**。

---

## 演示通道：30 秒看效果

这是给新用户和新触发词的快速演示路径。如果用户说「演示」「示例」「demo」「怎么用」或看起来是第一次用，走这里。

### 演示流程

> 🧠 **欢迎来到思维可视化引擎！** 让我用 30 秒演示你能做什么——

**① 先给你一个即用的示例**：

假设你想做读书笔记。这是 AI 生成的《原子习惯》思维导图 Markdown 代码：

```markdown
# 原子习惯
## 核心原理
### 习惯的复利效应
### 身份决定行为
## 四大法则
### 让它显而易见
- 执行意图
- 习惯叠加
### 让它有吸引力
- 诱惑捆绑
### 让它简单易行
- 2分钟规则
### 让它令人满足
- 即时奖励
```

> 📋 这段代码复制到 `.md` 文件 → 导入 XMind → 一张可编辑导图就出来了。

**② 你现在可以试试**：

| 你可以说 | 我会 |
|---------|------|
| 「我有一个[主题]，帮我做成导图」 | 走通道 A，给你生成提示词 |
| 「我不知道怎么梳理[主题]」 | 走通道 B，教你方法论 |
| 「[场景]该用什么图？」 | 走通道 C，帮你选型 |
| 「XMind/draw.io 怎么用？」 | 走通道 D，给操作指南 |
| 直接粘贴一段文字 | 走通道 A，马上生成 |

**③ 或者直接用模板**：

我们准备了 6 个开箱即用的 Markdown 模板（复制 → 填空 → 导入 XMind）：
- [读书笔记](references/templates/book-notes.md)
- [会议纪要](references/templates/meeting-minutes.md)
- [职业规划](references/templates/career-planning.md)
- [项目启动](references/templates/project-kickoff.md)
- [周回顾](references/templates/weekly-review.md)
- [SWOT 分析](references/templates/swot-analysis.md)

> 选一个模板，或者直接告诉我你想做什么！

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
| 可以直接粘贴的文本 | [文本→导图流程](references/ai-pipeline/text-to-mindmap.md) |
| 思维导图的图片想数字化 | [图片→导图重建](references/ai-pipeline/image-to-mindmap.md) |
| 只有一个主题/想法 | [主题→大纲扩展](references/ai-pipeline/topic-to-mindmap.md) |
| 要画流程图 | [Mermaid流程图](references/ai-pipeline/mermaid-flowchart.md) |

### A3. 给出提示词 + 操作步骤

根据素材类型，从对应的 reference 文件中取出：
1. 贴给用户的 AI 提示词（用户复制去任意 AI 工具）
2. 保存 `.md` / `.mmd` 文件的步骤（强调 UTF-8）
3. 导入 XMind / draw.io 的步骤

### A4. 如果用户反馈「AI 输出有问题」

→ 参考 [提示词模板库](references/ai-pipeline/prompt-templates.md) 中的优化技巧调整提示词
→ 或参考 [故障排查](references/troubleshooting/common-issues.md) 排查

---

## 通道 B: 方法指导

用户不知道怎么思考/组织，需要的是方法论。

### B1. 判断需求维度

| 用户的需求 | → 推荐方法 | 加载 |
|-----------|-----------|------|
| 信息太多想梳理 | 结构化+逻辑化 | [五星心法](references/methodology/five-star-heart.md) |
| 画出来的导图不好看/不清晰 | 7 要素规范 | [7要素](references/methodology/seven-elements.md) |
| 需要创意/突破思维框 | 发散-收敛循环 | [发散-收敛](references/methodology/diverge-converge.md) |
| 具体场景（学习/职业/演讲/时间管理/活动） | 场景模板 | [应用场景](references/methodology/application-scenarios.md) |
| 知识量大、一张图装不下 | 子母图技法 | [子母图](references/methodology/mother-child-diagram.md) |
| AI 生成质量不够好/想自检 | 写作规范+质量自检 | [写作规范](references/methodology/writing-standards.md) → [质量自检](references/troubleshooting/quality-assurance.md) |

### B2. 给出方法论框架 + 可选的 AI 衔接

1. 先给用户讲清楚「这个场景应该怎么思考」
2. 然后问：「要不要我帮你生成一份 Markdown 模板，你拿去 AI 工具扩展？」
3. 如果用户要 → 衔接到通道 A

---

## 通道 C: 图表选型

用户不确定该用什么图。

### C1. 查决策矩阵

从 [决策矩阵](references/diagram-types/index.md) 中按用户目的匹配：
- 「我想分析根本原因」→ 鱼骨图
- 「我想规划项目时间」→ 甘特图
- 「我想设计系统架构」→ 架构图 / 拓扑图
- ...

### C2. 给出推荐 + 详情

1. 推荐 1-2 种图表类型
2. 从对应的分类文件加载详情：
   - 组织层级 → [组织层级图](references/diagram-types/org-hierarchy.md)
   - 流程类 → [流程图类](references/diagram-types/process-flow.md)
   - 项目管理 → [项目管理图](references/diagram-types/project-management.md)
   - 分析工具 → [分析工具图](references/diagram-types/analysis-tools.md)
   - 技术图 → [技术图表](references/diagram-types/technical-diagrams.md)
   - 商业战略 → [商业战略图](references/diagram-types/business-strategy.md)
   - 专业制图 → [专业制图](references/diagram-types/specialized.md)

### C3. 可选衔接

> 「确定了图表类型后，要不要我帮你生成 AI 提示词去画？」

---

## 通道 D: 软件操作

用户问具体工具怎么用。

| 用户问什么 | 加载 |
|-----------|------|
| XMind 怎么用 | [XMind指南](references/software/xmind-guide.md) |
| draw.io 怎么用 | [draw.io指南](references/software/drawio-guide.md) |
| XMind vs draw.io vs Visio 该用哪个 | [工具对照表](references/software/cross-tool-mapping.md) |
| 快捷键 | [快捷键](references/software/keyboard-shortcuts.md) |
| 出错了/乱码/导入失败 | [故障排查](references/troubleshooting/common-issues.md) |
| AI 生成遗漏/编造/质量差 | [质量自检](references/troubleshooting/quality-assurance.md) |

---

## 通道 E: 完整流程

用户要全面分析，走串联：**B 方法论 → C 选型 → A 生成 → D 操作**

1. 先用通道 B 帮用户理清思路结构
2. 再用通道 C 确认适合的图表类型
3. 用通道 A 生成 AI 提示词，用户去生成 Markdown/Mermaid
4. 用通道 D 指导导入和美化
5. 全程穿插 [故障排查](references/troubleshooting/common-issues.md) 防坑

---

## 通道 F: 素材准备

用户手头是图片/PDF/文档，还没变成文本。这是通道 A 的上游。

### F1. 确认素材类型

| 用户手头有什么 | → 加载 |
|--------------|-------|
| 图片文件夹（截图/照片） | [OCR 提取指南](references/material-prep/ocr-extraction.md) |
| PDF 文件 | [PDF 处理策略](references/ai-pipeline/image-to-mindmap.md)（PDF 处理节） |
| Word/PPT/HTML 文档 | [格式提取指南](references/material-prep/format-extraction.md) |
| 微信文章 HTML | [微信文章转换](references/material-prep/format-extraction.md) |
| 大量重复图片 | [图片去重](references/material-prep/pipeline-overview.md) |

### F2. 如果用户有 Python 环境

引导用户使用内置 Python 工具链（`tools/` 目录）：

```bash
# 安装依赖
pip install -r tools/requirements.txt

# 一键全管道（8步）
python tools/pipeline.py /path/to/images my_project

# 只做 OCR
python tools/pipeline.py /path/to/images my_project --only ocr

# 预览去重
python tools/dedup.py /path/to/images --dry-run
```

### F3. 如果用户没有 Python 环境

给手动方案：
1. **图片去重**：用文件资源管理器按大小排序，手动删除明显重复的
2. **OCR**：上传到支持图片的 AI 工具（KIMI/Claude/DeepSeek），逐张识别
3. **格式提取**：Word/PPT 直接复制文字；PDF 能选中就复制，不能就截图上传 AI
4. **进入通道 A**：提取的文字用通道 A 的标准提示词生成 Markdown 导图

### F4. 进入下一阶段

素材变成文本后，自动衔接到通道 A。

> 📋 **全管道速记**：图片/PDF → OCR（F）→ Markdown（A）→ XMind（D）→ 可编辑导图

---

## 工作流速查卡

```
┌──────────────────────────────────────────────────────────┐
│                 思维可视化引擎 · 速查                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  🎬 第一次用？→ 演示：30秒看效果 + 即用模板                 │
│  📸 手头是图片/PDF？→ 通道 F：OCR提取 → 文本 → 导图        │
│  🧠 不知道怎么想？→ 通道 B：五星心法 / 7要素 / 发散收敛     │
│  📊 不知道用什么图？→ 通道 C：37种图表按功能分类 + 决策矩阵  │
│  ⚡ 有内容要生成？→ 通道 A：AI提示词 → .md → XMind/draw.io │
│  🔧 软件不会用？→ 通道 D：XMind / draw.io 操作指南         │
│  🚀 从零开始？→ 通道 E：B→C→A→D 一站串联                 │
│  📋 直接套用？→ 6个Markdown模板，复制填空即可              │
│                                                          │
│  全管道：图片/PDF → OCR(F) → Markdown(A) → XMind(D)       │
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
- 运行 OCR（需要本地安装 Tesseract 或使用 image-knowledge-extractor 工具链）
- 替代 XMind / draw.io 的安装
- 保证 AI 输出 100% 完美 — AI 生成有随机性，通常需要微调
- 替代专业领域的深度知识（如电路设计、消防安全规范等）

## 素材来源

本 Skill 从 204 个原始素材单元中提炼（116 视频 + 72 笔记 + 16 PDF）：
- 五星心法、7要素、发散-收敛、子母图 → 源自「引爆思维」+「思维导图集训」课程
- 37 种图表类型 → 源自亿图图示实操教程，适配为工具无关知识
- AI 管道（Markdown/Mermaid）→ 源自「AI做思维导图」专题
- 软件操作 → 改写适配 XMind + draw.io（原素材为亿图图示）
- 预置模板 → 原创补充
