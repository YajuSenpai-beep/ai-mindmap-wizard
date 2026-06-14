# API 参考

20 个 Python 工具的函数签名、参数说明、使用示例。

---

## pipeline.py — 8 步全管道

```python
from tools.pipeline import run_pipeline

run_pipeline(input_dir: str, project_name: str, *,
    only: str | None = None,        # 仅运行某步 (dedup/ocr/scan/...)
    skip: list[str] | None = None,  # 跳过步骤
    output_dir: str | None = None,  # 输出目录
    dry_run: bool = False,          # 预览模式
) -> dict                           # {step: result}
```

```bash
python tools/pipeline.py /path/to/images my_project
python tools/pipeline.py /path/to/images my_project --only ocr
python tools/pipeline.py /path/to/images my_project --dry-run
```

---

## ocr_engine.py — 批量 OCR

```python
from tools.ocr_engine import ocr_images

ocr_images(image_dir: str, *,
    lang: str = "chi_sim+eng",
    output_json: str | None = None,
    quality_threshold: float = 0.6,
) -> list[dict]  # [{filename, text, confidence}]
```

```bash
python tools/ocr_engine.py /path/to/images --lang chi_sim+eng -o results.json
```

---

## dedup.py — 图片去重

```python
from tools.dedup import hamming_distance, find_duplicates

hamming_distance(hash_a: str, hash_b: str) -> int
find_duplicates(image_dir: str, *, threshold: int = 5) -> list[list[str]]
```

```bash
python tools/dedup.py /path/to/images --threshold 5 --dry-run
```

---

## mermaid_fixer.py — Mermaid 语法修复

```python
from tools.mermaid_fixer import fix_mermaid

fix_mermaid(code: str, verbose: bool = False) -> dict  # {code, report: {applied, skipped, changed}}
```

```bash
python tools/mermaid_fixer.py input.mmd -o fixed.mmd -v
python tools/mermaid_fixer.py - < input.mmd --json
```

---

## markdown_to_xmind.py — Markdown → XMind

```python
from tools.markdown_to_xmind import create_xmind, parse_markdown_to_tree

parse_markdown_to_tree(md_text: str) -> dict | None
create_xmind(markdown_path: str, output_path: str) -> None
```

```bash
python tools/markdown_to_xmind.py input.md -o output.xmind
```

---

## multi_export.py — 多格式并行导出

```python
from tools.multi_export import EXPORTERS  # dict of name→function

# 可用导出器: xmind, mermaid, drawio, excalidraw, canvas, html
for fmt, fn in EXPORTERS.items():
    result = fn(md_path, output_dir)  # → {format, path, status}
```

```bash
python tools/multi_export.py input.md -o outputs/ -f all
python tools/multi_export.py input.md -f xmind,mermaid,html
```

---

## mindmap_to_ppt.py — 导图 → PPT

```python
from tools.mindmap_to_ppt import parse_md_to_slides, create_ppt

parse_md_to_slides(md_text: str) -> list[dict]
create_ppt(slides: list[dict], output_path: str, color_scheme: str = "professional") -> None
```

```bash
python tools/mindmap_to_ppt.py input.md -o output.pptx -c ocean
# 配色: professional / creative / minimal / ocean
```

---

## url_to_mindmap.py — URL → 导图

```python
from tools.url_to_mindmap import fetch_url, extract_title_hierarchy, generate_markdown_mindmap

fetch_url(url: str) -> tuple[str, str]                     # → (title, clean_text)
extract_title_hierarchy(text: str) -> list[str]             # → 关键行
generate_markdown_mindmap(title: str, lines: list) -> str   # → Markdown
```

```bash
python tools/url_to_mindmap.py https://example.com/article -o output.md
```

---

## brand_adapt.py — 品牌配色适配

```python
from tools.brand_adapt import KNOWN_BRANDS, generate_mermaid_classdef, generate_ppt_scheme

KNOWN_BRANDS  # dict, 预设品牌: apple/google/microsoft/notion/stripe/vercel
generate_mermaid_classdef(colors: dict) -> str
generate_ppt_scheme(colors: dict) -> str
```

```bash
python tools/brand_adapt.py https://example.com
python tools/brand_adapt.py --color "#1B3A5C" --name "MyBrand" -o brand.json
python tools/brand_adapt.py --list
```

---

## diagram_editor.py — AI 往返编辑器

```python
from tools.diagram_editor import read_markdown, analyze, update_markdown

read_markdown(path: str) -> dict           # 结构统计
analyze(stats: dict) -> list[str]          # 改进建议
update_markdown(path: str, ops: list) -> str  # 自动更新
```

```bash
python tools/diagram_editor.py input.md --analyze
python tools/diagram_editor.py input.xmind --analyze --json
```

---

## mcp_server.py — MCP 服务器

```bash
claude mcp add mindmap-wizard -- python tools/mcp_server.py
```

5 个端点：`text_to_mindmap` / `url_to_mindmap` / `md_to_formats` / `fix_mermaid` / `list_styles`

---

## eval.py — 质量评估

```python
from tools.eval import score_markdown, simulate_model_output, run_benchmark

score_markdown(md_text: str) -> dict
simulate_model_output(text: str, model: str) -> str  # claude/deepseek/gpt
run_benchmark(benchmark_dir: str, models: list[str]) -> dict
```

```bash
python tools/eval.py --input tests/benchmark/ --models claude,deepseek,gpt
python tools/eval.py --input doc.md --single
```

---

## _common.py — 共享模块

```python
from tools._common import parse_markdown_to_tree, count_nodes, md_stats, read_file, write_file

parse_markdown_to_tree(md_text: str) -> dict | None
count_nodes(tree: dict) -> int
md_stats(md_text: str) -> dict  # {total, h1, h2, h3, h4, leaf, max_depth}
read_file(path: str) -> str
write_file(path: str, content: str) -> None
```

---

## 其他工具

| 工具 | 入口 | 核心依赖 |
|------|------|---------|
| `clustering.py` | `cluster_by_content(docs, min_similarity)` | sklearn |
| `formats.py` | `extract_docx(p)` / `extract_pptx(p)` / `extract_html(h)` | python-docx/pptx |
| `llm_correct.py` | `correct_ocr_text(text, provider, api_key)` | requests |
| `wechat2md.py` | `convert(html)` | html2text |
| `incremental.py` | `detect_new_files(processed, current)` | — |
| `quality_checker.py` | 交叉校验 | — |
