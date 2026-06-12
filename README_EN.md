# 🧠 AI Thought Visualization Engine · Mindmap Wizard

> Generate editable mind maps and flowcharts with any AI tool. From "how to think" to "how to draw" to "what tool to use" — all in one skill.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-orange)](https://claude.ai/code)

[中文文档](README.md)

---

## 📖 What Is This?

A **Claude Code Skill** that encapsulates a battle-tested AI-powered visualization pipeline:

```
Your Material → AI Generates Structured Code → Save as Standard Format → Import into Pro Software → Editable Mind Map / Flowchart
```

Core philosophy:
- **AI handles structuring** (generates Markdown / Mermaid code)
- **Professional software handles visualization** (XMind / draw.io)
- **Tool-agnostic prompts** — works with any LLM
- Teaches not just **how to draw**, but **how to think**

---

## 🎯 What It Can Do

- 📝 **Text → Mind Map**: Turn any article into an editable XMind mind map in 3 minutes
- 📸 **Image Digitization**: See someone's mind map and want to edit it? AI OCR → Markdown → editable
- 💡 **Topic Expansion**: Only have a vague idea? AI expands it into a full structured outline
- 🔀 **Flowchart Generation**: Describe a process → AI generates Mermaid code → import into draw.io
- 🧭 **Diagram Selection**: 37 diagram types with a purpose×audience decision matrix
- 🧠 **Methodology Coaching**: Five-Star Heart Method, 7 Elements, Diverge-Converge cycle — systematic thinking training
- 🔧 **Software Guides**: XMind + draw.io operations, keyboard shortcuts
- 🩺 **Troubleshooting**: Encoding issues, import failures, rendering errors — 15+ common fixes

---

## 🚀 Quick Start

### 1. Install

```bash
# Clone into Claude Code skills directory
git clone https://github.com/YajuSenpai-beep/ai-mindmap-wizard.git \
  ~/.claude/skills/ai-mindmap-wizard
```

Or load directly in Claude Code with `/skill-name`.

### 2. Use

Type any trigger phrase in Claude Code:

```
/ai-mindmap Turn this meeting transcript into a mind map
```

Natural language triggers also work:

| You want to... | Example |
|---------------|---------|
| Quick generation | "Make a mind map from this article" |
| Draw a flowchart | "Draw a user login flowchart" |
| Need thinking help | "I want to do career planning but don't know where to start" |
| Not sure what diagram to use | "What diagram should I use for root cause analysis?" |
| Software help | "What are the XMind shortcuts?" |

### 3. What You'll Get

The skill auto-routes to the right lane based on your intent:

```
Lane A · Quick Gen    → AI prompt templates + save & import steps
Lane B · Methodology  → Five-Star Heart / 7 Elements / Diverge-Converge
Lane C · Diagram Pick → 37-type decision matrix + recommendations
Lane D · Tool Ops     → XMind/draw.io guides
Lane E · Full Pipeline → B → C → A → D all in one
```

---

## 🏗️ Project Structure

```
ai-mindmap-wizard/
├── SKILL.md                              # Main orchestrator (5-lane router)
├── README.md                             # Chinese documentation
├── README_EN.md                          # This file
├── LICENSE                               # MIT
└── references/                           # Knowledge base
    ├── methodology/                      # WHY layer
    │   ├── five-star-heart.md            #   Five-Star Heart pyramid
    │   ├── seven-elements.md             #   7 Elements (4 basic + 3 special)
    │   ├── diverge-converge.md           #   Diverge-Converge cycle + 6 laws
    │   └── application-scenarios.md      #   Learning/career/speech templates
    │
    ├── diagram-types/                    # HOW layer
    │   ├── index.md                      #   Decision matrix (purpose × audience)
    │   ├── org-hierarchy.md              #   Org charts & structure diagrams
    │   ├── process-flow.md               #   7 types of flowcharts
    │   ├── project-management.md         #   Gantt charts & timelines
    │   ├── analysis-tools.md             #   SWOT / Fishbone / Decision trees
    │   ├── technical-diagrams.md         #   ER / UML / Architecture / Topology
    │   ├── business-strategy.md          #   Business canvas / Use case diagrams
    │   └── specialized.md                #   Floor plans / Wireframes / Storyboards
    │
    ├── software/                         # WHAT layer
    │   ├── xmind-guide.md                #   XMind operations
    │   ├── drawio-guide.md               #   draw.io operations
    │   ├── cross-tool-mapping.md         #   XMind ↔ draw.io ↔ Visio comparison
    │   └── keyboard-shortcuts.md         #   Shortcut cheat sheets
    │
    ├── ai-pipeline/                      # AI Pipeline
    │   ├── text-to-mindmap.md            #   Text → Mind map
    │   ├── image-to-mindmap.md           #   Image → Mind map
    │   ├── topic-to-mindmap.md           #   Topic → Expanded outline
    │   ├── mermaid-flowchart.md          #   Mermaid flowcharts
    │   └── prompt-templates.md           #   Prompt template library
    │
    └── troubleshooting/
        └── common-issues.md              #   15+ common issues & fixes
```

---

## 🛠️ Recommended Toolchain

| Purpose | Tool | Cost |
|---------|------|------|
| AI Content Generation | DeepSeek / KIMI / Claude / ChatGPT (any) | Free tiers available |
| Mind Mapping | [XMind](https://xmind.app) | Free version available |
| Flowcharts & Diagrams | [draw.io](https://app.diagrams.net) | Completely free |
| Online Mermaid Preview | [Mermaid Live](https://mermaid.live) | Free |

> **Why not Edraw Max?** This skill focuses on free, accessible tools. XMind + draw.io cover everything most users need.

---

## 📚 Core Methodology

### Five-Star Heart Pyramid

```
              ┌──────────────┐
              │  ⑤ Visualize  │  ← Ultimate: images/colors/icons
              ├──────────────┤
              │  ④ Simplify   │  ← Evolution: keyword extraction
              │  ③ Radiate    │
              ├──────────────┤
              │  ② Logicalize │  ← Foundation: supporting everything
              │  ① Structure  │
              └──────────────┘
```

### Diverge-Converge Cycle

```
Diverge (dump all ideas → no judgment)
  ↓
Converge (circle sparks → dig deeper)
  ↓
Re-Diverge (expand around each spark)
  ↓
Final Converge (organize into structured map)
```

See [`references/methodology/`](references/methodology/).

---

## 🔌 Prompt Examples

### Text → Mind Map

```
Analyze the following content and organize it into a hierarchical mind map structure.
Output in Markdown format. Use # for central topic, ## for main branches,
### for sub-branches. Max 4 levels. Each node ≤ 15 words. Output ONLY Markdown code.

Content: [paste your text here]
```

### Process → Mermaid Flowchart

```
Convert the following process into Mermaid flowchart code.
Use graph TD. Decision nodes → {} , start/end → (), steps → [].
Node text ≤ 15 words. Output ONLY Mermaid code.

Process: [describe your process]
```

More templates in [`references/ai-pipeline/prompt-templates.md`](references/ai-pipeline/prompt-templates.md).

---

## 🤝 Contributing

Issues and PRs welcome!

- New diagram types → add/expand files under `references/diagram-types/`
- Better prompts → improve `references/ai-pipeline/prompt-templates.md`
- Software guides → contribute to `references/software/`
- Report bugs → [Issues](https://github.com/YajuSenpai-beep/ai-mindmap-wizard/issues)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## ⚠️ Honest Boundaries

**What this skill CAN do**:
- ✅ Provide tool-agnostic AI prompt templates
- ✅ Guide you through the full material-to-visualization pipeline
- ✅ Recommend the right diagram type from 37 options
- ✅ Teach mind mapping methodology
- ✅ Provide XMind / draw.io operation guides and shortcuts

**What this skill CANNOT do**:
- ❌ Call AI APIs directly (you paste the prompt into your AI tool of choice)
- ❌ Replace XMind / draw.io installation
- ❌ Guarantee 100% perfect AI output (AI is stochastic — usually needs minor tweaks)

---

## 🌐 Languages

- [中文](README.md)
- [English](README_EN.md)

---

<p align="center">
  <sub>Made with 🧠 and ☕ · Distilled from 116 tutorial videos and 72 notes</sub>
</p>
