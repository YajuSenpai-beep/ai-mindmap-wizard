# Prompt Template Library — Tool-Agnostic (English)

> Works with any LLM. Copy → Paste → Get structured output.

## Design Principle: Role-Goal-Constraint Framework

Every effective prompt has three elements:

| Element | Purpose | Example |
|---------|---------|---------|
| **Role** | What persona the AI adopts | "You are an information structuring expert..." |
| **Goal** | What output you want | "...organize the content into a mind map in Markdown" |
| **Constraint** | Format, length, style limits | "Max 4 levels. Max 15 words per node. Output ONLY code." |

---

## Template 1: Text → Mind Map (Markdown)

```
You are an information structuring expert who excels at distilling complex text into clear, hierarchical mind maps.

Analyze the following content and organize it into a mind map structure. Output in Markdown format.

Requirements:
- Use # for the central topic, ## for main branches, ### for sub-branches, - for leaf nodes
- Maximum 4 levels of depth
- Each node should be concise — no more than 15 words
- Output ONLY the Markdown code — no explanations, no commentary

Content:

[paste your text here]
```

**Use when**: You have text content and want a structured mind map.

---

## Template 2: Topic → Expanded Outline

```
You are a knowledge framework architect who can take any topic and build a comprehensive, well-organized outline around it.

Generate a structured mind map outline for the topic "[TOPIC]" in Markdown format.

Requirements:
- Use # for the central topic, ## for main branches, ### for sub-branches, - for leaf nodes
- Cover all key aspects of the topic with logical depth and breadth
- Maximum 4 levels of depth
- Each node should be concise
- Output ONLY the Markdown code — no explanations

Topic: [your topic]
```

**Use when**: You only have a topic idea and need AI to help expand it.

---

## Template 3: Image → Mind Map Reconstruction

```
You are an OCR and information structuring specialist. You can look at images of mind maps and accurately reproduce their structure as Markdown.

Look at this image of a mind map. Identify its hierarchical structure and text content. Output in Markdown format.

Requirements:
- Preserve the original hierarchy using # ## ### -
- Keep text content consistent with the image
- Mark any unreadable text with [?]
- Output ONLY the Markdown code

[upload the mind map image]
```

**Use when**: You have a mind map image and want a digital, editable version.

---

## Template 4: Process → Mermaid Flowchart

```
You are a process modeling expert who translates written process descriptions into precise Mermaid flowchart code.

Convert the following process into Mermaid flowchart code.

Requirements:
- Use `graph TD` for top-to-bottom flow (or `graph LR` for left-to-right)
- Start/end nodes → `()`, process steps → `[]`, decision nodes → `{}`
- Node text should be concise — max 15 words
- Output ONLY the Mermaid code block — no explanations

Process description:

[describe your process here]
```

**Use when**: You need a flowchart but don't want to draw it manually.

---

## Template 5: Structured Analysis (SWOT, Fishbone, etc.)

```
You are a business strategy consultant skilled at applying structured analytical frameworks.

Perform a [ANALYSIS METHOD] analysis on "[SUBJECT]". Output the result as structured Markdown.

Requirements:
- Structure: [describe the structure, e.g. "four quadrants for SWOT" / "6 cause categories for fishbone"]
- Each point should be concise — max 25 words
- Output ONLY the Markdown code
```

**Example**:
```
You are a business strategy consultant.

Perform a SWOT analysis on "Our new product entering a saturated market". Output as Markdown.

Requirements:
- Four quadrants: Strengths, Weaknesses, Opportunities, Threats
- 3-5 points per quadrant
- Each point max 25 words
- Output ONLY the Markdown code
```

---

## Universal Optimization Tips

| Problem | Add to the end of your prompt |
|---------|------------------------------|
| AI rambles with explanations | "Output ONLY the code. No explanations whatsoever." |
| Hierarchy too deep | "Maximum 3 levels of depth." |
| Node text too long | "Each node: maximum 10 words." |
| Structure doesn't match expectations | "Organize according to [specific structure]" + give an example |
| Content too generic | "Give specific, actionable recommendations. Avoid vague statements." |

## Multi-Turn Strategy

Don't aim for perfection in one shot. Iterate:

1. **Round 1**: Give content + "Organize into Markdown mind map"
2. **Round 2**: "The third level is too shallow. Expand branches 2 and 4."
3. **Round 3**: "Reorganize the ## Career section by timeline."

Iterative refinement beats crafting the perfect one-shot prompt.
