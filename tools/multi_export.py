#!/usr/bin/env python3
"""多格式导出管线：从一份 Markdown 同时生成 XMind + DrawIO + Mermaid + Excalidraw + Canvas + HTML。

一次输入，六种格式并行输出。
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from _common import logger


def export_xmind(md_path: str, output_dir: str):
    """Markdown → XMind 原生文件"""
    output = str(Path(output_dir) / (Path(md_path).stem + ".xmind"))
    try:
        from markdown_to_xmind import create_xmind
        create_xmind(md_path, output)
        return {"format": "xmind", "path": output, "status": "ok"}
    except ImportError:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "markdown_to_xmind.py"),
             md_path, "-o", output],
            capture_output=True, text=True
        )
        return {"format": "xmind", "path": output, "status": "ok" if result.returncode == 0 else "failed", "error": result.stderr.strip()}


def export_mermaid(md_path: str, output_dir: str):
    """Markdown → 经过修复的 Mermaid 代码"""
    import re
    content = Path(md_path).read_text(encoding="utf-8")

    # 简化版 Markdown → Mermaid mindmap
    lines = content.strip().split("\n")
    mermaid = ["mindmap"]
    indent_map = {"#": 2, "##": 4, "###": 6, "####": 8}

    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = re.match(r'^(#{1,6})\s+(.+)', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            spaces = "  " * indent_map.get("#" * level, 2 if level <= 2 else level * 2)
            mermaid.append(f"{spaces}{text}")

    mermaid_code = "\n".join(mermaid)

    # 运行修复器
    output = str(Path(output_dir) / (Path(md_path).stem + ".mmd"))
    Path(output).write_text(mermaid_code, encoding="utf-8")

    try:
        from mermaid_fixer import fix_mermaid
        result = fix_mermaid(mermaid_code)
        Path(output).write_text(result["code"], encoding="utf-8")
    except ImportError:
        pass

    return {"format": "mermaid", "path": output, "status": "ok"}


def export_drawio(md_path: str, output_dir: str):
    """Markdown → DrawIO XML"""
    import re
    content = Path(md_path).read_text(encoding="utf-8")
    lines = [l.strip() for l in content.split("\n") if l.strip().startswith("#")]

    cells = []
    _x, y = 40, 40
    colors = ["#1ba1e2", "#dae8fc", "#d5e8d4", "#fff2cc", "#f8cecc", "#e1d5e7"]

    for i, line in enumerate(lines[:50]):  # 最多 50 个节点
        match = re.match(r'^(#{1,6})\s+(.+)', line)
        if not match:
            continue
        level = len(match.group(1))
        text = match.group(2).strip()
        color = colors[min(level - 1, len(colors) - 1)]
        nx = 40 + (level - 1) * 220
        ny = y + i * 50 - (level - 1) * 25
        cells.append(f'''
    <mxCell id="n{i}" value="{text}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={color};" vertex="1" parent="1">
      <mxGeometry x="{nx}" y="{ny}" width="200" height="40" as="geometry" />
    </mxCell>''')

    xml = f'''<mxfile host="claude">
  <diagram name="Mindmap" id="d1">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        {''.join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    output = str(Path(output_dir) / (Path(md_path).stem + ".drawio"))
    Path(output).write_text(xml, encoding="utf-8")
    return {"format": "drawio", "path": output, "status": "ok"}


def export_excalidraw(md_path: str, output_dir: str):
    """Markdown → Excalidraw JSON"""
    import re
    content = Path(md_path).read_text(encoding="utf-8")
    lines = [l.strip() for l in content.split("\n") if l.strip().startswith("#")]

    elements = []
    element_id = 0
    y = 100
    colors_bg = ["#a5d8ff", "#b2f2bb", "#ffec99", "#ffc9c9", "#d0bfff", "#99e9f2"]

    for i, line in enumerate(lines[:50]):
        match = re.match(r'^(#{1,6})\s+(.+)', line)
        if not match:
            continue
        level = len(match.group(1))
        text = match.group(2).strip()
        bg = colors_bg[min(level - 1, len(colors_bg) - 1)]
        x = 100 + (level - 1) * 280
        font_size = max(20 - (level - 1) * 2, 12)

        elements.append({
            "id": f"node-{element_id}",
            "type": "rectangle",
            "x": x, "y": y,
            "width": 250, "height": 50,
            "strokeColor": "#1e1e1e",
            "backgroundColor": bg,
            "fillStyle": "solid",
            "strokeWidth": 2,
            "roughness": 1,
            "opacity": 100
        })
        elements.append({
            "id": f"text-{element_id}",
            "type": "text",
            "x": x + 10, "y": y + 10,
            "width": 230, "height": 30,
            "text": text,
            "fontSize": font_size,
            "fontFamily": 1
        })
        element_id += 1
        y += 70

    excalidraw = {
        "type": "excalidraw",
        "version": 2,
        "elements": elements,
        "appState": {"viewBackgroundColor": "#ffffff"}
    }
    output = str(Path(output_dir) / (Path(md_path).stem + ".excalidraw"))
    Path(output).write_text(json.dumps(excalidraw, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"format": "excalidraw", "path": output, "status": "ok"}


def export_canvas(md_path: str, output_dir: str):
    """Markdown → Obsidian Canvas JSON"""
    import re
    content = Path(md_path).read_text(encoding="utf-8")
    lines = [l.strip() for l in content.split("\n") if l.strip().startswith("#")]

    nodes = []
    edges = []
    colors = ["1", "4", "5", "2", "6", "3"]
    prev_parent = None

    for i, line in enumerate(lines[:50]):
        match = re.match(r'^(#{1,6})\s+(.+)', line)
        if not match:
            continue
        level = len(match.group(1))
        text = match.group(2).strip()
        node_id = f"n{i:04d}"
        x = (level - 1) * 450
        y = i * 100

        nodes.append({
            "id": node_id, "type": "text",
            "text": f"{'#' * level} {text}",
            "x": x, "y": y,
            "width": 400, "height": 80,
            "color": colors[min(level - 1, len(colors) - 1)]
        })

        if i > 0 and prev_parent is not None:
            edges.append({
                "id": f"e{i:04d}",
                "fromNode": prev_parent,
                "toNode": node_id,
                "fromSide": "right",
                "toSide": "left"
            })
        prev_parent = node_id

    canvas = {"nodes": nodes, "edges": edges}
    output = str(Path(output_dir) / (Path(md_path).stem + ".canvas"))
    Path(output).write_text(json.dumps(canvas, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"format": "canvas", "path": output, "status": "ok"}


def export_html(md_path: str, output_dir: str):
    """Markdown → 交互式 HTML（基于 markmap），含搜索 + 按层级展开/折叠 + 导出。"""
    content = Path(md_path).read_text(encoding="utf-8")
    html = f'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>交互式思维导图</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: system-ui, -apple-system, sans-serif; background: #1a1a2e; }}
  #toolbar {{
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    display: flex; gap: 8px; padding: 10px 16px;
    background: rgba(26,26,46,0.95); backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255,255,255,0.1);
  }}
  #toolbar input {{
    flex: 1; max-width: 280px; padding: 8px 14px; border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.15); background: rgba(255,255,255,0.08);
    color: #e0e0e0; font-size: 14px; outline: none;
  }}
  #toolbar input:focus {{ border-color: #00E5FF; background: rgba(0,229,255,0.08); }}
  #toolbar button {{
    padding: 8px 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15);
    background: rgba(255,255,255,0.06); color: #ccc; cursor: pointer;
    font-size: 13px; white-space: nowrap; transition: all 0.2s;
  }}
  #toolbar button:hover {{ background: rgba(0,229,255,0.15); border-color: #00E5FF; color: #fff; }}
  #toolbar button.active {{ background: rgba(0,229,255,0.2); border-color: #00E5FF; }}
  #mindmap {{ width: 100vw; height: calc(100vh - 52px); margin-top: 52px; }}
  .markmap {{ background: #1a1a2e; }}
  svg {{ background: #1a1a2e !important; }}
  .markmap-node text {{ fill: #e0e0e0 !important; font-size: 14px !important; }}
  .markmap-link {{ stroke: rgba(0,229,255,0.3) !important; }}
  .markmap-node circle {{ fill: #00E5FF !important; stroke: #00E5FF !important; }}
</style>
</head>
<body>
<div id="toolbar">
  <input id="search" placeholder="🔍 搜索节点..." oninput="doSearch(this.value)">
  <button onclick="expandAll()" title="展开全部">📂 展开</button>
  <button onclick="collapseAll()" title="折叠全部">📁 折叠</button>
  <button onclick="expandLevel(2)" title="展开到第2层">L2</button>
  <button onclick="expandLevel(3)" title="展开到第3层">L3</button>
  <button onclick="expandLevel(4)" title="展开到第4层">L4</button>
  <button onclick="exportSVG()" title="导出 SVG">💾 SVG</button>
  <span style="color:#888;font-size:12px;margin-left:auto;align-self:center;" id="info"></span>
</div>
<div class="markmap" id="mindmap-container">
{content}
</div>
<script src="https://cdn.jsdelivr.net/npm/markmap-autoloader"></script>
<script>
  setTimeout(() => {{
    const svg = document.querySelector('#mindmap-container svg');
    if (svg) {{
      document.getElementById('info').textContent =
        '节点: ' + svg.querySelectorAll('.markmap-node').length;
      // 默认折叠到第2层
      const nodes = svg.querySelectorAll('.markmap-node');
      nodes.forEach(n => {{
        const depth = parseInt(n.getAttribute('data-depth') || '0');
        if (depth > 2) n.style.display = 'none';
      }});
    }}
  }}, 500);

  function doSearch(q) {{
    const svg = document.querySelector('#mindmap-container svg');
    if (!svg) return;
    const nodes = svg.querySelectorAll('.markmap-node');
    const qLower = q.toLowerCase();
    nodes.forEach(n => {{
      const text = (n.textContent || '').toLowerCase();
      if (!qLower || text.includes(qLower)) {{
        n.style.display = '';
        n.style.opacity = '1';
        // 显示祖先
        let p = n.closest('g')?.parentElement?.closest('g');
        while (p) {{ p.style.display = ''; p = p.parentElement?.closest('g'); }}
      }} else {{
        n.style.opacity = '0.2';
      }}
    }});
  }}

  function expandAll() {{
    document.querySelectorAll('.markmap-node').forEach(n => {{ n.style.display = ''; }});
  }}
  function collapseAll() {{
    document.querySelectorAll('.markmap-node').forEach(n => {{
      const d = parseInt(n.getAttribute('data-depth') || '0');
      if (d > 1) n.style.display = 'none';
    }});
  }}
  function expandLevel(lvl) {{
    document.querySelectorAll('.markmap-node').forEach(n => {{
      const d = parseInt(n.getAttribute('data-depth') || '0');
      n.style.display = d <= lvl ? '' : 'none';
    }});
  }}
  function exportSVG() {{
    const svg = document.querySelector('#mindmap-container svg');
    if (!svg) return;
    const clone = svg.cloneNode(true);
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    const blob = new Blob([clone.outerHTML], {{type: 'image/svg+xml'}});
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
    a.download = 'mindmap.svg'; a.click();
  }}
</script>
</body>
</html>'''
    output = str(Path(output_dir) / (Path(md_path).stem + ".html"))
    Path(output).write_text(html, encoding="utf-8")
    return {"format": "html", "path": output, "status": "ok"}


EXPORTERS = {
    "xmind": export_xmind,
    "mermaid": export_mermaid,
    "drawio": export_drawio,
    "excalidraw": export_excalidraw,
    "canvas": export_canvas,
    "html": export_html,
}


def main():
    parser = argparse.ArgumentParser(
        description="多格式导出管线 — 从 Markdown 一次生成六种格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
格式:
  xmind      → .xmind (XMind 原生)
  mermaid    → .mmd (Mermaid mindmap)
  drawio     → .drawio (Draw.io XML)
  excalidraw → .excalidraw (手绘风)
  canvas     → .canvas (Obsidian Canvas)
  html       → .html (交互式 markmap)
  all        → 全部六种格式

示例:
  python multi_export.py input.md -o outputs/ -f all
  python multi_export.py input.md -f xmind,mermaid
        """,
    )
    parser.add_argument("input", help="输入的 Markdown 文件")
    parser.add_argument("--output", "-o", default=".", help="输出目录")
    parser.add_argument("--format", "-f", default="all",
                        help="导出格式: xmind,mermaid,drawio,excalidraw,canvas,html,all")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 文件不存在: {args.input}")
        return 1

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    formats = list(EXPORTERS.keys()) if args.format == "all" else args.format.split(",")

    results = []
    try:
        from tqdm import tqdm
    except ImportError:
        tqdm = lambda x, **kw: x
    for fmt in formats:
        if fmt not in EXPORTERS:
            logger.info(f"⚠️ 未知格式: {fmt}，跳过")
            continue
        try:
            result = EXPORTERS[fmt](str(input_path), str(output_dir))
            results.append(result)
            logger.info(f"✅ {result['format']:12s} → {result['path']}")
        except Exception as e:
            results.append({"format": fmt, "status": "failed", "error": str(e)})
            print(f"❌ {fmt:12s} → {e}")

    ok = sum(1 for r in results if r["status"] == "ok")
    logger.info(f"\n📊 {ok}/{len(results)} 格式导出成功 → {output_dir}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    exit(main())
