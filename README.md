# 🧠 AI 思维可视化引擎 · Mindmap Wizard

> 用任意 AI 工具一键生成可编辑的思维导图和流程图。从「怎么想」到「怎么画」到「用什么画」——全管道覆盖。**19 个 Python 脚本，66 篇参考指南，14 篇软件指南，116 个文件。**

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
- 📸 **素材准备**：图片/PDF/Word/PPT → OCR 提取 → 文本
- 📝 **文本转思维导图**：一篇文章 → 3 分钟变成 XMind 可编辑导图
- 📸 **图片数字化**：看到别人的导图想拿来改？AI 识别 → Markdown → 可编辑
- 💡 **主题扩展**：只有一个想法？AI 帮你扩展成完整框架
- 🔀 **流程图生成**：描述流程 → AI 生成 Mermaid 代码 → 导入 draw.io

### 方法论 & 选型（知识体系）
- 🧠 **方法论指导**：五星心法、7 要素、发散-收敛循环、子母图、多视角分析
- 🧭 **图表选型**：37 种图表类型，按目的和受众帮你速选
- 📊 **数据可视化**：图表三梯队选型、Dashboard 设计、图表模板体系

### 软件完全指南（14 个工具）
- 🗺️ **思维导图**：XMind / draw.io 操作大全 + 快捷键
- 📊 **数据办公**：WPS / Excel / Word / PPT —— 从入门到接单就业级
- 🎨 **3D 设计**：C4D 建模·OC渲染·动画·AI集成
- 📈 **咨询图表**：Think-Cell Chart10 麦肯锡级别图表引擎
- 📓 **笔记管理**：OneNote 从入门到领导级
- 🤖 **AI 办公**：DeepSeek+KIMI 辅助 Excel/Word/PPT/WPS

### 工具 & 模板
- 🛠️ **Python 工具链**：图片去重/批量OCR/内容聚类/LLM纠错/格式提取/Mermaid修复/Markdown→XMind/多格式导出/导图→PPT/URL→导图/品牌配色/MCP服务/质量评估（19 个脚本）
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

Skill 提供三个层次的支持：

| 层次 | 说明 |
|------|------|
| 🔧 命令行工具 | 19 个 Python 脚本覆盖全管道：OCR→AI→Markdown→XMind/draw.io |
| 📋 AI 提示词 | 通用提示词模板，复制到任意 LLM 即可生成结构化 Markdown |
| 📚 知识库 | 66 篇参考指南在 `references/` 下，直接打开 MD 文件阅读 |

高频操作命令表：

| 想做什么 | 命令 |
|---------|------|
| 文本 → 思维导图 | 复制 SKILL.md 中的提示词到任意 AI → 得到 Markdown → 导入 XMind |
| 图片/PDF → 导图 | `python tools/pipeline.py 图片目录 项目名` |
| Markdown → XMind | `python tools/markdown_to_xmind.py input.md -o output.xmind` |
| Markdown → 6 种格式 | `python tools/multi_export.py input.md -f all` |
| Mermaid 语法修复 | `python tools/mermaid_fixer.py input.mmd` |
| 导图 → PPT | `python tools/mindmap_to_ppt.py input.md -c professional` |
| URL → 导图 | `python tools/url_to_mindmap.py https://example.com/article` |
| MCP 服务 | `claude mcp add mindmap-wizard -- python tools/mcp_server.py` |

---

## 🏗️ 项目结构

```
ai-mindmap-wizard/
├── SKILL.md                              # 工具入口页 + 命令速查 + 知识库索引
├── README.md                             # 中文文档（本文件）
├── README_EN.md                          # English documentation
├── CHANGELOG.md / API_REFERENCE.md       # 变更日志 / API 参考
├── CONTRIBUTING.md / package.json        # 贡献指南 / 包信息
├── pyproject.toml                        # Ruff 配置
├── LICENSE                               # MIT
│
├── tools/                                # Python 工具链（19 个脚本）
│   ├── pipeline.py                       #   一键全管道（8步）
│   ├── ocr_engine.py                     #   批量 OCR + 质量评分
│   ├── dedup.py                          #   图片去重（感知哈希）
│   ├── clustering.py                     #   内容聚类（TF-IDF）
│   ├── llm_correct.py                    #   LLM OCR 纠错
│   ├── mermaid_fixer.py                  #   Mermaid 语法修复（37 规则）
│   ├── markdown_to_xmind.py              #   Markdown → XMind 原生文件
│   ├── multi_export.py                   #   6 格式并行导出
│   ├── mindmap_to_ppt.py                 #   导图 → PPT（4 主题）
│   ├── url_to_mindmap.py                 #   URL → 导图
│   ├── brand_adapt.py                    #   品牌配色自动检测
│   ├── diagram_editor.py                 #   导图结构分析
│   ├── mcp_server.py                     #   MCP 服务（5 端点）
│   ├── eval.py                           #   多模型质量评估
│   ├── formats.py                        #   Word/PPT/HTML 提取
│   ├── incremental.py                    #   增量处理
│   ├── quality_checker.py                #   交叉校验
│   ├── wechat2md.py                      #   微信文章转换
│   ├── _common.py                        #   共享模块（零重复）
│   ├── skill_template.md                 #   写作规范模板
│   └── requirements.txt                  #   Python 依赖
│
├── tests/                                # 测试套件（59 个测试）
│   ├── test_tools.py                     #   工具单元测试
│   ├── test_links.py                     #   内部链接检查
│   └── benchmark/                        #   10 个质量基准案例
│
├── docker/                               # Docker 一键部署
├── tutorial/                             # 使用说明
└── .github/workflows/                    # CI/CD（pytest + coverage + link check + mypy + ruff）
│
└── references/                           # 知识库（66 篇，9 个目录）
    ├── material-prep/                    # 素材层 · INPUT（5 篇）
    │   ├── pipeline-overview.md          #   8步管道总览
    │   ├── ocr-extraction.md             #   图片/PDF OCR 技巧
    │   ├── format-extraction.md          #   Word/PPT/HTML 提取
    │   ├── multimodal-input.md           #   多模态输入
    │   └── obsidian-workflow.md          #   Obsidian 工作流
    │
    ├── methodology/                      # 心法层 · WHY（9 篇）
    │   ├── five-star-heart.md            #   五星心法金字塔
    │   ├── seven-elements.md             #   7 要素
    │   ├── diverge-converge.md           #   发散-收敛循环 + 6 法则
    │   ├── mother-child-diagram.md       #   子母图技法
    │   ├── multi-perspective.md          #   多视角分析
    │   ├── application-scenarios.md      #   学习/职业/演讲 等场景模板
    │   ├── writing-standards.md          #   写作规范与质量自检
    │   ├── knowledge-graph.md            #   知识图谱
    │   └── tufte-principles.md           #   Tufte 设计原则
    │
    ├── diagram-types/                    # 技法层 · HOW（8 篇）
    │   ├── index.md                      #   决策矩阵（按目的×受众速查）
    │   ├── org-hierarchy.md              #   组织结构图
    │   ├── process-flow.md               #   7 种流程图
    │   ├── project-management.md         #   甘特图/时间线
    │   ├── analysis-tools.md             #   SWOT/鱼骨图/决策树
    │   ├── technical-diagrams.md         #   ER图/UML/架构图
    │   ├── business-strategy.md          #   商业画布/用例图
    │   └── specialized.md                #   平面图/线框图/故事板
    │
    ├── software/                         # 工具层 · WHAT（14 篇）
    │   ├── xmind-guide.md                #   XMind 操作指南
    │   ├── drawio-guide.md               #   draw.io 操作指南
    │   ├── onenote-guide.md              #   OneNote 从入门到领导级
    │   ├── ai-office-guide.md            #   AI 办公（DeepSeek+KIMI）
    │   ├── wps-guide.md                  #   WPS 从入门到接单
    │   ├── excel-guide.md                #   Excel + 数据可视化
    │   ├── word-guide.md                 #   Word 从入门到接单
    │   ├── ppt-guide.md                  #   PPT + 30种版面技法
    │   ├── c4d-guide.md                  #   C4D 建模·渲染·动画
    │   ├── thinkcell-guide.md            #   Think-Cell 咨询图表
    │   ├── obsidian-canvas-guide.md      #   Obsidian Canvas
    │   ├── excalidraw-guide.md           #   Excalidraw 手绘
    │   ├── cross-tool-mapping.md         #   工具对照表 + 插件速查
    │   └── keyboard-shortcuts.md         #   快捷键速查
    │
    ├── ai-pipeline/                      # AI 管道（15 篇）
    │   ├── text-to-mindmap.md            #   文本 → 思维导图
    │   ├── image-to-mindmap.md           #   图片 → 思维导图
    │   ├── topic-to-mindmap.md           #   主题 → 大纲扩展
    │   ├── mermaid-flowchart.md          #   Mermaid 流程图
    │   ├── drawio-generation.md          #   DrawIO 生成
    │   ├── drawio-mcp-guide.md           #   Draw.io MCP 指南
    │   ├── d3-interactive.md             #   D3.js 交互式
    │   ├── youtube-mindmap.md            #   YouTube 时间戳导图
    │   ├── realtime-mindmap.md           #   对话实时导图
    │   ├── no-prompt-mode.md             #   无提示词模式
    │   ├── inline-ai.md                  #   内联AI免复制
    │   ├── ppt-from-mindmap.md           #   导图转PPT
    │   ├── visual-styles.md              #   高颜值预设样式
    │   ├── prompt-templates.md           #   中文提示词库
    │   └── prompt-templates-en.md        #   English prompts
    │
    ├── integrations/                     # 外部集成（5 篇）
    │   ├── notebooklm-mcp.md             #   NotebookLM MCP
    │   ├── visualcave.md                 #   VisualCave 集成
    │   ├── oss-libraries.md              #   开源库对比
    │   ├── commercial-tools.md           #   商业工具对比
    │   └── local-models.md               #   本地模型指南
    │
    ├── advanced/                         # 高级模式（1 篇）
    │   └── design-patterns.md            #   6 种设计模式
    │
    ├── templates/                        # 开箱模板（6 个）
    └── troubleshooting/                  # 故障排查（3 篇）
        ├── common-issues.md
        ├── quality-assurance.md
        └── anti-hallucination.md
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
- ✅ 14 篇软件指南（XMind/draw.io/WPS/Excel/Word/PPT/C4D/Think-Cell/OneNote/Obsidian/Excalidraw/AI办公 等）
- ✅ Python 工具链（19 个脚本：OCR/去重/聚类/纠错/Mermaid修复/Markdown→XMind/多格式导出/PPT/MCP服务 等）

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
  <sub>Made with 🧠 and ☕ · 19 个 Python 脚本 · 66 篇参考指南 · 14 篇软件指南 · 59 个测试 · 304 个验证链接 · 116 个文件 · 6 轮竞品分析覆盖 60+ 产品</sub>
</p>
