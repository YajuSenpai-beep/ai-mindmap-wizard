# 🧠 AI 思维可视化引擎 · Mindmap Wizard

> 用任意 AI 工具一键生成可编辑的思维导图和流程图。从「怎么想」到「怎么画」到「用什么画」——全管道覆盖。**4,762 个原始素材提炼，60 个文件，11 个软件完全指南。**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-orange)](https://claude.ai/code)

[English](README_EN.md)

---

## 📖 这是什么？

一个 **Claude Code Skill**，封装了一套经过验证的 AI 思维可视化工作流：

```
你的素材 → AI 生成结构化代码 → 保存为标准格式 → 导入专业软件 → 可编辑的思维导图/流程图
```

核心理念：
- **AI 负责结构化**（生成 Markdown / Mermaid 代码）
- **专业软件负责可视化**（XMind / draw.io）
- 提示词**工具无关**，任何 LLM 都能用
- **全管道覆盖**：从原始图片/PDF 一路到可编辑思维导图

---

## 🎯 能做什么

### 思维导图 & 流程图（核心管道）
- 📸 **素材准备**：图片/PDF/Word/PPT → OCR 提取 → 文本（通道 F）
- 📝 **文本转思维导图**：一篇文章 → 3 分钟变成 XMind 可编辑导图（通道 A）
- 📸 **图片数字化**：看到别人的导图想拿来改？AI 识别 → Markdown → 可编辑
- 💡 **主题扩展**：只有一个想法？AI 帮你扩展成完整框架
- 🔀 **流程图生成**：描述流程 → AI 生成 Mermaid 代码 → 导入 draw.io

### 方法论 & 选型（知识体系）
- 🧠 **方法论指导**：五星心法、7 要素、发散-收敛循环、子母图、多视角分析
- 🧭 **图表选型**：37 种图表类型，按目的和受众帮你速选
- 📊 **数据可视化**：图表三梯队选型、Dashboard 设计、图表模板体系

### 软件完全指南（11 个工具）
- 🗺️ **思维导图**：XMind / draw.io 操作大全 + 快捷键
- 📊 **数据办公**：WPS / Excel / Word / PPT —— 从入门到接单就业级
- 🎨 **3D 设计**：C4D 建模·OC渲染·动画·AI集成
- 📈 **咨询图表**：Think-Cell Chart10 麦肯锡级别图表引擎
- 📓 **笔记管理**：OneNote 从入门到领导级
- 🤖 **AI 办公**：DeepSeek+KIMI 辅助 Excel/Word/PPT/WPS

### 工具 & 模板
- 🛠️ **Python 工具链**：图片去重/批量OCR/内容聚类/LLM纠错/格式提取（8步全管道）
- 📋 **开箱模板**：读书笔记/会议纪要/职业规划/项目启动/周回顾/SWOT分析
- 🩺 **故障排查**：编码乱码、导入失败、渲染错误、AI输出质量——全面排查

---

## 🚀 快速开始

### 1. 安装

```bash
# 克隆到 Claude Code skills 目录
git clone https://github.com/YajuSenpai-beep/ai-mindmap-wizard.git \
  ~/.claude/skills/ai-mindmap-wizard
```

或者在 Claude Code 中直接使用 `/<skill-name>` 加载。

### 2. 使用

在 Claude Code 对话中输入任意触发词即可：

```
/ai-mindmap 帮我把这篇文章整理成思维导图
```

自然语言触发也支持：

| 你想说什么 | 示例 |
|-----------|------|
| 快速生成导图 | 「把这段会议记录做成思维导图」 |
| 画流程图 | 「画一个用户登录的流程图」 |
| 不知道怎么组织 | 「我想做年度计划但没思路」 |
| 不知道该用什么图 | 「分析问题根因该用什么图？」 |
| 软件不会用 | 「XMind 快捷键有哪些？」「Excel 数据可视化怎么做？」 |
| 素材准备 | 「整理这些截图里的文字」「PDF转导图」 |

### 3. 你会得到什么

Skill 会根据你的意图，自动走对应的通道：

```
通道 A · 快速生成  → AI 提示词模板 + 保存导入步骤
通道 B · 方法指导  → 五星心法 / 7要素 / 发散收敛 / 子母图 / 多视角
通道 C · 图表选型  → 37 种图表决策矩阵 + 推荐
通道 D · 软件操作  → 11 个软件完全指南（XMind/draw.io/WPS/Excel/Word/PPT/C4D/Think-Cell/OneNote/AI办公）
通道 E · 完整流程  → B → C → A → D 一站串联
通道 F · 素材准备  → 图片/PDF OCR → 文本 → 通道 A
```

---

## 🏗️ 项目结构

```
ai-mindmap-wizard/
├── SKILL.md                              # 主编排器（7 通道路由）
├── README.md                             # 中文文档（本文件）
├── README_EN.md                          # English documentation
├── LICENSE                               # MIT
├── tools/                                # Python 工具链
│   ├── pipeline.py                       #   一键全管道（8步）
│   ├── ocr_engine.py                     #   批量 OCR + 质量评分
│   ├── dedup.py                          #   图片去重（感知哈希）
│   ├── incremental.py                    #   增量处理
│   ├── clustering.py                     #   内容聚类（TF-IDF）
│   ├── llm_correct.py                    #   LLM OCR 纠错
│   ├── formats.py                        #   Word/PPT/HTML 提取
│   ├── quality_checker.py                #   交叉校验
│   ├── wechat2md.py                      #   微信文章转换
│   ├── skill_template.md                 #   写作规范模板
│   └── requirements.txt                  #   Python 依赖
└── references/                           # 知识库
    ├── material-prep/                    # 素材层 · INPUT
    │   ├── pipeline-overview.md          #   8步管道总览
    │   ├── ocr-extraction.md             #   图片/PDF OCR 技巧
    │   └── format-extraction.md          #   Word/PPT/HTML 提取
    │
    ├── methodology/                      # 心法层 · WHY
    │   ├── five-star-heart.md            #   五星心法金字塔
    │   ├── seven-elements.md             #   7 要素（4基础+3特殊）
    │   ├── diverge-converge.md           #   发散-收敛循环 + 6 法则
    │   ├── mother-child-diagram.md       #   子母图技法
    │   ├── multi-perspective.md          #   多视角分析
    │   ├── application-scenarios.md      #   学习/职业/演讲 等场景模板
    │   └── writing-standards.md          #   写作规范与质量自检
    │
    ├── diagram-types/                    # 技法层 · HOW
    │   ├── index.md                      #   决策矩阵（按目的×受众速查）
    │   ├── org-hierarchy.md              #   组织结构图
    │   ├── process-flow.md               #   7 种流程图
    │   ├── project-management.md         #   甘特图/时间线
    │   ├── analysis-tools.md             #   SWOT/鱼骨图/决策树
    │   ├── technical-diagrams.md         #   ER图/UML/架构图
    │   ├── business-strategy.md          #   商业画布/用例图
    │   └── specialized.md                #   平面图/线框图/故事板
    │
    ├── software/                         # 工具层 · WHAT（11个完全指南）
    │   ├── xmind-guide.md                #   XMind 操作指南
    │   ├── drawio-guide.md               #   draw.io 操作指南
    │   ├── onenote-guide.md              #   OneNote 从入门到领导级
    │   ├── ai-office-guide.md            #   AI 办公（DeepSeek+KIMI）
    │   ├── wps-guide.md                  #   WPS 从入门到接单（529文件提炼）
    │   ├── excel-guide.md                #   Excel 从入门到接单+数据可视化（821文件提炼）
    │   ├── word-guide.md                 #   Word 从入门到接单（1,553文件提炼）
    │   ├── ppt-guide.md                  #   PPT 从入门到接单+30种版面技法（1,085文件提炼）
    │   ├── c4d-guide.md                  #   C4D 建模·渲染·动画·AI集成（774文件提炼）
    │   ├── thinkcell-guide.md            #   Think-Cell 咨询级图表引擎（101文件提炼）
    │   ├── cross-tool-mapping.md         #   工具对照表 + 专业插件速查
    │   └── keyboard-shortcuts.md         #   快捷键速查
    │
    ├── ai-pipeline/                      # AI 管道
    │   ├── text-to-mindmap.md            #   文本 → 思维导图
    │   ├── image-to-mindmap.md           #   图片 → 思维导图
    │   ├── topic-to-mindmap.md           #   主题 → 大纲扩展
    │   ├── mermaid-flowchart.md          #   Mermaid 流程图
    │   ├── prompt-templates.md           #   中文提示词模板库
    │   └── prompt-templates-en.md        #   English prompt templates
    │
    ├── templates/                        # 开箱即用模板
    │   ├── book-notes.md                 #   读书笔记
    │   ├── meeting-minutes.md            #   会议纪要
    │   ├── career-planning.md            #   职业规划
    │   ├── project-kickoff.md            #   项目启动
    │   ├── weekly-review.md              #   周回顾
    │   └── swot-analysis.md              #   SWOT 分析
    │
    └── troubleshooting/                  # 故障排查
        ├── common-issues.md              #   常见问题速查
        └── quality-assurance.md          #   AI 输出质量自检
```

---

## 🛠️ 推荐工具链

| 用途 | 工具 | 费用 |
|------|------|------|
| AI 内容生成 | DeepSeek / KIMI / Claude / ChatGPT（任选） | 均有免费额度 |
| 思维导图 | [XMind](https://xmind.app) | 免费版可用 |
| 流程图 | [draw.io](https://app.diagrams.net) | 完全免费 |
| 在线 Mermaid 预览 | [Mermaid Live](https://mermaid.live) | 免费 |
| 咨询级数据图表 | Think-Cell Chart10 | 付费 |
| 办公文档处理 | WPS / Microsoft 365 | 免费/付费 |
| 3D 渲染 | C4D + OC 渲染器 | 付费 |

---

## 📚 核心方法论

### 五星心法金字塔

```
              ┌──────────────┐
              │  ⑤ 图示化     │  ← 终极层：图像/颜色/图标
              ├──────────────┤
              │  ④ 简单化     │  ← 进化层：关键词提取
              │  ③ 放射化     │
              ├──────────────┤
              │  ② 逻辑化     │  ← 基础层：支撑一切
              │  ① 结构化     │
              └──────────────┘
```

### 发散-收敛循环

```
发散（倒出所有想法 → 不评判）
  ↓
收敛（圈出火花 → 深入挖掘）
  ↓
再发散（围绕火花展开）
  ↓
最终收敛（整理为结构化导图）
```

详见 [`references/methodology/`](references/methodology/)。

---

## 🔌 提示词示例

### 文本 → 思维导图

```
请根据以下内容，按照思维导图的层级结构进行整理，以 Markdown 格式输出。
要求：层级不超过 4 层，每个节点不超过 20 字，只输出 Markdown 代码。
内容：[粘贴你的文本]
```

### 流程 → Mermaid 流程图

```
请将以下流程整理成 Mermaid 格式的流程图代码。
要求：使用 graph TD，决策用菱形{}，起止用()，节点≤15字，只输出代码。
流程：[描述你的流程]
```

更多模板见 [`references/ai-pipeline/prompt-templates.md`](references/ai-pipeline/prompt-templates.md)。

---

## 🤝 贡献

欢迎提 Issue 和 PR！

- 新增图表类型 → `references/diagram-types/` 下新增或扩充分类文件
- 改进提示词 → `references/ai-pipeline/prompt-templates.md`
- 补充软件操作 → `references/software/`
- 报告 Bug → [Issues](https://github.com/YajuSenpai-beep/ai-mindmap-wizard/issues)

---

## 📄 许可

MIT License — 自由使用、修改、分发。

---

## ⚠️ 诚实边界

**能做的**：
- ✅ 提供工具无关的 AI 提示词模板
- ✅ 指导从素材到可视化导图的完整流程
- ✅ 37 种图表类型的选型建议
- ✅ 思维导图方法论指导
- ✅ XMind / draw.io 操作和快捷键
- ✅ 11 个办公软件从入门到接单级的完整知识体系
- ✅ Python 工具链（OCR/去重/聚类/纠错）

**不能做的**：
- ❌ 直接调用 AI 生成内容（你需要自己去 AI 工具中提问）
- ❌ 替代 XMind / draw.io 或其他商业软件的安装
- ❌ 保证 AI 输出 100% 完美（AI 有随机性，通常需要微调）

---

## 🌐 语言

- [中文](README.md)
- [English](README_EN.md)

---

<p align="center">
  <sub>Made with 🧠 and ☕ · 从 4,762 个原始素材文件中提炼（课程视频笔记+TXT转录+PDF文档+实践文件）</sub>
</p>
