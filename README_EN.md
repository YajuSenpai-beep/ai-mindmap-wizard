# 🧠 AI Thought Visualization Engine · Mindmap Wizard

> Generate editable mind maps and flowcharts with any AI tool. From "how to think" to "how to draw" to "what tool to use" — full pipeline coverage. **Distilled from 4,762 source files across 60 reference documents and 11 complete software guides.**

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

### Mind Maps & Flowcharts (Core Pipeline)
- 📸 **Material Prep**: Images/PDF/Word/PPT → OCR extraction → text (Lane F)
- 📝 **Text → Mind Map**: Turn any article into an editable XMind mind map in 3 minutes (Lane A)
- 📸 **Image Digitization**: See someone's map → AI OCR → Markdown → editable
- 💡 **Topic Expansion**: Vague idea → AI expands it into a full structured outline
- 🔀 **Flowchart Generation**: Describe a process → AI generates Mermaid code → import into draw.io

### Methodology & Decision Support
- 🧠 **Methodology**: Five-Star Heart, 7 Elements, Diverge-Converge, Mother-Child Diagrams, Multi-Perspective Analysis
- 🧭 **Diagram Selection**: 37 diagram types with a purpose×audience decision matrix
- 📊 **Data Visualization**: 3-tier chart selection, Dashboard design, chart template system

### Complete Software Guides (11 Tools)
- 🗺️ **Mind Mapping**: XMind / draw.io operations + keyboard shortcuts
- 📊 **Office Suite**: WPS / Excel / Word / PPT — beginner to professional freelancing level
- 🎨 **3D Design**: C4D modeling · OC rendering · animation · AI integration
- 📈 **Consulting Charts**: Think-Cell Chart10 — McKinsey-grade chart engine
- 📓 **Note Management**: OneNote beginner to leadership level
- 🤖 **AI-Assisted Office**: DeepSeek+KIMI for Excel/Word/PPT/WPS

### Tools & Templates
- 🛠️ **Python Toolchain**: Image deduplication / batch OCR / content clustering / LLM correction / format extraction (8-step pipeline)
- 📋 **Ready Templates**: Book notes / Meeting minutes / Career planning / Project kickoff / Weekly review / SWOT analysis
- 🩺 **Troubleshooting**: Encoding issues, import failures, rendering errors, AI output quality

---

## 🚀 Quick Start

### 1. Install

```bash
# Clone into Claude Code skills directory
git clone https://github.com/YajuSenpai-beep/ai-mindmap-wizard.git \
  ~/.claude/skills/ai-mindmap-wizard
```

Or load directly in Claude Code with `/ai-mindmap`.

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
| Diagram selection | "What diagram should I use for root cause analysis?" |
| Software help | "What are the XMind shortcuts?" "How to visualize data in Excel?" |
| Material prep | "Extract text from these screenshots" "PDF to mind map" |

### 3. What You'll Get

The skill auto-routes to the right lane based on your intent:

```
Lane A · Quick Gen     → AI prompt templates + save & import steps
Lane B · Methodology   → Five-Star Heart / 7 Elements / Diverge-Converge / Mother-Child / Multi-Perspective
Lane C · Diagram Pick  → 37-type decision matrix + recommendations
Lane D · Tool Ops      → 11 complete software guides (XMind/draw.io/WPS/Excel/Word/PPT/C4D/Think-Cell/OneNote/AI Office)
Lane E · Full Pipeline → B → C → A → D all in one
Lane F · Material Prep → Image/PDF OCR → text → Lane A
```

---

## 🏗️ Project Structure

```
ai-mindmap-wizard/
├── SKILL.md                              # Main orchestrator (7-lane router)
├── README.md                             # Chinese documentation
├── README_EN.md                          # This file
├── LICENSE                               # MIT
├── tools/                                # Python toolchain
│   ├── pipeline.py                       #   One-click 8-step pipeline
│   ├── ocr_engine.py                     #   Batch OCR + quality scoring
│   ├── dedup.py                          #   Image dedup (perceptual hash)
│   ├── incremental.py                    #   Incremental processing
│   ├── clustering.py                     #   Content clustering (TF-IDF)
│   ├── llm_correct.py                    #   LLM OCR correction
│   ├── formats.py                        #   Word/PPT/HTML extraction
│   ├── quality_checker.py                #   Cross-validation
│   ├── wechat2md.py                      #   WeChat article conversion
│   ├── skill_template.md                 #   Writing template
│   └── requirements.txt                  #   Python dependencies
└── references/                           # Knowledge base
    ├── material-prep/                    # INPUT layer
    │   ├── pipeline-overview.md          #   8-step pipeline overview
    │   ├── ocr-extraction.md             #   Image/PDF OCR techniques
    │   └── format-extraction.md          #   Office format extraction
    │
    ├── methodology/                      # WHY layer
    │   ├── five-star-heart.md            #   Five-Star Heart pyramid
    │   ├── seven-elements.md             #   7 Elements (4 basic + 3 special)
    │   ├── diverge-converge.md           #   Diverge-Converge cycle
    │   ├── mother-child-diagram.md       #   Mother-Child diagrams
    │   ├── multi-perspective.md          #   Multi-perspective analysis
    │   ├── application-scenarios.md      #   Learning/career/speech templates
    │   └── writing-standards.md          #   Quality standards & self-check
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
    ├── software/                         # WHAT layer (11 complete guides)
    │   ├── xmind-guide.md                #   XMind operations
    │   ├── drawio-guide.md               #   draw.io operations
    │   ├── onenote-guide.md              #   OneNote beginner to leadership
    │   ├── ai-office-guide.md            #   AI-assisted office (DeepSeek+KIMI)
    │   ├── wps-guide.md                  #   WPS beginner to freelancing (529 files)
    │   ├── excel-guide.md                #   Excel + data viz (821 files)
    │   ├── word-guide.md                 #   Word beginner to freelancing (1,553 files)
    │   ├── ppt-guide.md                  #   PPT + 30 layout techniques (1,085 files)
    │   ├── c4d-guide.md                  #   C4D modeling·rendering·animation (774 files)
    │   ├── thinkcell-guide.md            #   Think-Cell consulting charts (101 files)
    │   ├── cross-tool-mapping.md         #   Tool comparison + plugin quick-ref
    │   └── keyboard-shortcuts.md         #   Shortcut cheat sheets
    │
    ├── ai-pipeline/                      # AI Pipeline
    │   ├── text-to-mindmap.md            #   Text → Mind map
    │   ├── image-to-mindmap.md           #   Image → Mind map
    │   ├── topic-to-mindmap.md           #   Topic → Expanded outline
    │   ├── mermaid-flowchart.md          #   Mermaid flowcharts
    │   ├── prompt-templates.md           #   Chinese prompt library
    │   └── prompt-templates-en.md        #   English prompt library
    │
    ├── templates/                        # Ready-to-use templates
    │   ├── book-notes.md                 #   Book notes
    │   ├── meeting-minutes.md            #   Meeting minutes
    │   ├── career-planning.md            #   Career planning
    │   ├── project-kickoff.md            #   Project kickoff
    │   ├── weekly-review.md              #   Weekly review
    │   └── swot-analysis.md              #   SWOT analysis
    │
    └── troubleshooting/                  # Troubleshooting
        ├── common-issues.md              #   15+ common issues & fixes
        └── quality-assurance.md          #   AI output quality self-check
```

---

## 🛠️ Recommended Toolchain

| Purpose | Tool | Cost |
|---------|------|------|
| AI Content Generation | DeepSeek / KIMI / Claude / ChatGPT (any) | Free tiers available |
| Mind Mapping | [XMind](https://xmind.app) | Free version available |
| Flowcharts & Diagrams | [draw.io](https://app.diagrams.net) | Completely free |
| Online Mermaid Preview | [Mermaid Live](https://mermaid.live) | Free |
| Consulting-Grade Charts | Think-Cell Chart10 | Paid |
| Office Documents | WPS / Microsoft 365 | Free/Paid |
| 3D Rendering | C4D + OC Renderer | Paid |

> **Why not Edraw Max?** This skill focuses on accessible tools. XMind + draw.io cover everything most users need for mind mapping and diagramming.

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

More templates in [`references/ai-pipeline/prompt-templates.md`](references/ai-pipeline/prompt-templates.md) (Chinese) and [`references/ai-pipeline/prompt-templates-en.md`](references/ai-pipeline/prompt-templates-en.md) (English).

---

## 🤝 Contributing

Issues and PRs welcome!

- New diagram types → add/expand files under `references/diagram-types/`
- Better prompts → improve `references/ai-pipeline/prompt-templates*.md`
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
- ✅ Provide 11 complete software guides from beginner to professional level
- ✅ Supply a Python toolchain for OCR/dedup/clustering/correction

**What this skill CANNOT do**:
- ❌ Call AI APIs directly (you paste the prompt into your AI tool of choice)
- ❌ Replace XMind / draw.io or other commercial software installation
- ❌ Guarantee 100% perfect AI output (AI is stochastic — usually needs minor tweaks)

---

## 🌐 Languages

- [中文](README.md)
- [English](README_EN.md)

---

<p align="center">
  <sub>Made with 🧠 and ☕ · Distilled from 4,762 source files (course notes + TXT transcriptions + PDFs + practice files)</sub>
</p>
