# 🧠 AI Thought Visualization Engine · Mindmap Wizard

> Generate editable mind maps and flowcharts with any AI tool. From "how to think" to "how to draw" to "what tool to use" — full pipeline coverage. **19 Python scripts, 66 reference guides, 14 software guides, 116 files.**

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
- 📸 **Material Prep**: Images/PDF/Word/PPT/Audio/Video → OCR/transcription → text
- 📝 **Text → Mind Map**: Turn any article into an editable XMind mind map in 3 minutes
- 📸 **Image Digitization**: See someone's map → AI OCR → Markdown → editable
- 💡 **Topic Expansion**: Vague idea → AI expands it into a full structured outline
- 🔀 **Flowchart Generation**: Describe a process → AI generates Mermaid code → import into draw.io
- 🌐 **URL → Mindmap**: Paste any URL → auto-extract content → mindmap
- 🎬 **YouTube → Mindmap**: Video transcript → timestamped mindmap nodes

### Methodology & Decision Support
- 🧠 **Methodology**: Five-Star Heart, 7 Elements, Diverge-Converge, Mother-Child Diagrams, Multi-Perspective, Knowledge Graphs, Tufte Principles (9 files)
- 🧭 **Diagram Selection**: 37 diagram types with a purpose×audience decision matrix
- 📊 **Data Visualization**: 3-tier chart selection, Dashboard design, chart template system, industry-aware generation

### Complete Software Guides (14 Tools)
- 🗺️ **Mind Mapping**: XMind / draw.io / Obsidian Canvas / Excalidraw
- 📊 **Office Suite**: WPS / Excel / Word / PPT — beginner to professional freelancing level
- 🎨 **3D Design**: C4D modeling · OC rendering · animation · AI integration
- 📈 **Consulting Charts**: Think-Cell Chart10 — McKinsey-grade chart engine
- 📓 **Note Management**: OneNote beginner to leadership level
- 🤖 **AI-Assisted Office**: DeepSeek+KIMI for Excel/Word/PPT/WPS

### Tools & Templates
- 🛠️ **Python Toolchain (19 scripts)**: OCR engine, image dedup (pHash), content clustering (TF-IDF), LLM correction, Mermaid fixer (37 rules), Markdown→XMind, multi-format export (6 formats), mindmap→PPT, URL→mindmap, brand color adapter, MCP server, quality evaluator, diagram editor
- 📋 **Ready Templates**: Book notes / Meeting minutes / Career planning / Project kickoff / Weekly review / SWOT analysis
- 🩺 **Troubleshooting**: Anti-hallucination verification, quality self-check, 15+ common issues

---

## 🚀 Quick Start

### 1. Install

```bash
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
| Software help | "XMind shortcuts?" "Excel data visualization?" |
| Material prep | "Extract text from screenshots" "PDF to mind map" "YouTube to mindmap" |

### 3. What You'll Get

Three layers of support:

| Layer | Description |
|-------|-------------|
| 🔧 CLI Tools | 19 Python scripts covering the full pipeline: OCR → AI → Markdown → XMind/draw.io |
| 📋 AI Prompts | Universal prompt templates — copy to any LLM to generate structured Markdown |
| 📚 Knowledge Base | 66 reference guides in `references/`, open MD files directly (faster than Skill loading) |

Common commands:

| Task | Command |
|------|---------|
| Text → Mindmap | Copy the prompt from SKILL.md to any AI → get Markdown → import to XMind |
| Image/PDF → Mindmap | `python tools/pipeline.py <image_dir> <project_name>` |
| Markdown → XMind | `python tools/markdown_to_xmind.py input.md -o output.xmind` |
| Markdown → 6 formats | `python tools/multi_export.py input.md -f all` |
| Fix Mermaid syntax | `python tools/mermaid_fixer.py input.mmd` |
| Mindmap → PPT | `python tools/mindmap_to_ppt.py input.md -c professional` |
| URL → Mindmap | `python tools/url_to_mindmap.py https://example.com/article` |
| MCP server | `claude mcp add mindmap-wizard -- python tools/mcp_server.py` |

---

## 🏗️ Project Structure

```
ai-mindmap-wizard/
├── SKILL.md                              # Tool entry page + command reference + knowledge base index
├── README.md / README_EN.md / LICENSE
├── CHANGELOG.md / API_REFERENCE.md
├── CONTRIBUTING.md / package.json
├── pyproject.toml                        # Ruff config
│
├── tools/                                # Python toolchain (19 scripts)
│   ├── pipeline.py                       #   One-click 8-step pipeline
│   ├── ocr_engine.py                     #   Batch OCR + quality scoring
│   ├── dedup.py                          #   Image dedup (perceptual hash)
│   ├── clustering.py                     #   Content clustering (TF-IDF)
│   ├── llm_correct.py                    #   LLM OCR correction
│   ├── mermaid_fixer.py                  #   Mermaid syntax fixer (37 rules)
│   ├── markdown_to_xmind.py              #   Markdown → XMind native
│   ├── multi_export.py                   #   6-format parallel export
│   ├── mindmap_to_ppt.py                 #   Mindmap → PowerPoint (4 themes)
│   ├── url_to_mindmap.py                 #   URL → mindmap
│   ├── brand_adapt.py                    #   Brand color auto-detection
│   ├── diagram_editor.py                 #   AI read→analyze→update diagrams
│   ├── mcp_server.py                     #   MCP server (5 endpoints)
│   ├── eval.py                           #   Multi-model quality evaluator
│   ├── formats.py / incremental.py       #   Format extraction / incremental
│   ├── quality_checker.py / wechat2md.py #   Validation / WeChat
│   ├── _common.py                        #   Shared module (zero duplication)
│   ├── skill_template.md / requirements.txt
│
├── tests/                                # Test suite (59 tests)
│   ├── test_tools.py / test_links.py
│   └── benchmark/                        #   10 quality benchmark cases
│
├── docker/                               # Docker one-click deployment
├── tutorial/                             # Usage guide
└── .github/workflows/                    # CI/CD (pytest + coverage + link check + mypy + ruff)
│
└── references/                           # Knowledge base (66 docs, 9 dirs)
    ├── material-prep/ (5 files)           # INPUT: OCR, formats, multimodal, Obsidian
    ├── methodology/ (9 files)             # WHY: Five-Star Heart, 7 Elements, Tufte, etc.
    ├── diagram-types/ (8 files)           # HOW: 37 types, 7 categories
    ├── software/ (14 files)               # WHAT: 14 guides (12 software + 2 reference)
    ├── ai-pipeline/ (15 files)            # AI: text/image/topic/YouTube/D3/DrawIO/PPT
    ├── integrations/ (5 files)            # NotebookLM, VisualCave, OSS libs, commercial, local models
    ├── advanced/ (1 file)                 # 6 design patterns
    ├── templates/ (6 files)               # Ready-to-use Markdown templates
    └── troubleshooting/ (3 files)         # Anti-hallucination, quality, common issues
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
Diverge (dump all ideas → no judgment) → Converge (circle sparks → dig deeper)
  → Re-Diverge (expand around each spark) → Final Converge (organized map)
```

See [`references/methodology/`](references/methodology/).

---

## 🔌 Prompt Examples

### Text → Mind Map

```
Analyze the following content and organize it into a hierarchical mind map structure.
Output in Markdown format. Max 4 levels. Each node ≤ 15 words. Output ONLY Markdown code.

Content: [paste your text here]
```

### Process → Mermaid Flowchart

```
Convert the following process into Mermaid flowchart code.
Use graph TD. Decision nodes → {} , start/end → (), steps → [].
Output ONLY Mermaid code.

Process: [describe your process]
```

More templates in [`references/ai-pipeline/prompt-templates*.md`](references/ai-pipeline/).

---

## 🤝 Contributing

Issues and PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## ⚠️ Honest Boundaries

**What this skill CAN do**:
- ✅ Provide tool-agnostic AI prompt templates
- ✅ Guide full material-to-visualization pipeline (OCR→AI→export)
- ✅ Recommend diagram types from 37 options with decision matrix
- ✅ Teach 9 methodology frameworks for systematic thinking
- ✅ Provide 14 complete software guides (XMind/draw.io/WPS/Excel/Word/PPT/C4D/Think-Cell/OneNote/Obsidian/Excalidraw/AI office + cross-tool reference)
- ✅ Supply 19 Python scripts (OCR/dedup/clustering/Mermaid fix/Markdown→XMind/multi-format export/mindmap→PPT/MCP server/quality eval)

**What this skill CANNOT do**:
- ❌ Call AI APIs directly (you paste the prompt into your AI tool of choice)
- ❌ Replace XMind / draw.io or other commercial software installation
- ❌ Guarantee 100% perfect AI output (AI is stochastic)

---

## 🌐 Languages

- [中文](README.md)
- [English](README_EN.md)

---

<p align="center">
  <sub>Made with 🧠 and ☕ · 19 Python scripts · 66 reference guides · 14 software guides · 59 tests · 304 verified links · 116 files · 6 rounds of competitive analysis covering 60+ products</sub>
</p>
