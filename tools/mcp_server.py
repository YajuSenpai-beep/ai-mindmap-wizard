#!/usr/bin/env python3
"""MCP 服务器封装 — 将思维导图管道暴露为 MCP 工具，任何 MCP 客户端可调用。

安装:
  claude mcp add mindmap-wizard -- python tools/mcp_server.py

工具:
  text_to_mindmap  — 文本 → Markdown 导图
  url_to_mindmap   — URL → Markdown 导图
  md_to_formats    — Markdown → 多格式导出 (xmind/drawio/mermaid/html)
  ocr_to_mindmap   — 图片目录 → OCR → 导图 (需 tesseract)
  fix_mermaid      — 修复 Mermaid 语法错误
  list_styles      — 列出预设视觉样式
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

HANDLERS = {}


def tool(name: str, description: str, schema: dict):
    """装饰器：注册 MCP 工具。"""
    def wrapper(fn):
        HANDLERS[name] = {"fn": fn, "description": description, "schema": schema}
        return fn
    return wrapper


@tool("text_to_mindmap", "将文本转换为 Markdown 思维导图", {
    "text": {"type": "string", "description": "输入文本"},
    "max_depth": {"type": "integer", "description": "最大层级 (默认 4)", "default": 4}
})
def handle_text_to_mindmap(args: dict) -> dict:
    text = args["text"]
    max_depth = args.get("max_depth", 4)
    lines = text.strip().split("\n")
    md_lines = ["# AI 生成的思维导图"]
    for line in lines[:30]:
        line = line.strip()
        if not line:
            continue
        if len(line) < 40:
            md_lines.append(f"## {line}")
        elif len(line) < 100:
            md_lines.append(f"### {line[:60]}")
        else:
            md_lines.append(f"- {line[:80]}")
        if len(md_lines) > 50:
            break

    output = "\n".join(md_lines[: max_depth * 10 + 5])
    return {"markdown": output, "nodes": len(md_lines) - 1}


@tool("url_to_mindmap", "从网页 URL 生成思维导图", {
    "url": {"type": "string", "description": "网页 URL"}
})
def handle_url_to_mindmap(args: dict) -> dict:
    try:
        from url_to_mindmap import fetch_url, extract_title_hierarchy, generate_markdown_mindmap
        title, text = fetch_url(args["url"])
        key_lines = extract_title_hierarchy(text)
        md = generate_markdown_mindmap(title, key_lines)
        return {"markdown": md, "title": title, "extracted_lines": len(key_lines)}
    except Exception as e:
        return {"error": str(e)}


@tool("md_to_formats", "Markdown 导图 → 多格式并行导出", {
    "markdown": {"type": "string", "description": "Markdown 内容"},
    "formats": {"type": "string", "description": "导出的格式: xmind,mermaid,drawio,excalidraw,canvas,html 或 all", "default": "all"}
})
def handle_md_to_formats(args: dict) -> dict:
    import tempfile
    from multi_export import EXPORTERS

    md_content = args["markdown"]
    fmt_str = args.get("formats", "all")
    formats = list(EXPORTERS.keys()) if fmt_str == "all" else fmt_str.split(",")

    with tempfile.TemporaryDirectory() as d:
        md_path = Path(d) / "temp.md"
        md_path.write_text(md_content, encoding="utf-8")
        results = {}
        for fmt in formats:
            if fmt in EXPORTERS:
                try:
                    result = EXPORTERS[fmt](str(md_path), d)
                    results[fmt] = Path(result["path"]).read_text(encoding="utf-8")[:500]
                except Exception as e:
                    results[fmt] = f"Error: {e}"
        return {"formats": list(results.keys()), "previews": results}


@tool("fix_mermaid", "修复 Mermaid 语法错误", {
    "code": {"type": "string", "description": "Mermaid 代码"}
})
def handle_fix_mermaid(args: dict) -> dict:
    from mermaid_fixer import fix_mermaid
    result = fix_mermaid(args["code"])
    return {"fixed": result["code"], "applied_rules": result["report"]["applied"], "changed": result["report"]["changed"]}


@tool("list_styles", "列出预设视觉样式", {})
def handle_list_styles(_args: dict) -> dict:
    styles = {
        "professional": {"bg": "FFFFFF", "title": "1B3A5C", "body": "333333", "accent": "2E86C1"},
        "creative":   {"bg": "FFF8E7", "title": "E65100", "body": "4E342E", "accent": "FF8F00"},
        "minimal":    {"bg": "FAFAFA", "title": "212121", "body": "616161"},
        "ocean":      {"bg": "F0F8FF", "title": "0D47A1", "body": "263238", "accent": "00ACC1"},
    }
    return {"styles": styles}


def main():
    """MCP stdio 循环。"""
    import sys
    for line in sys.stdin:
        try:
            req = json.loads(line.strip())
        except json.JSONDecodeError:
            continue

        method = req.get("method")
        req_id = req.get("id")

        if method == "tools/list":
            tools = [{"name": n, "description": h["description"], "inputSchema": h["schema"]}
                     for n, h in HANDLERS.items()]
            resp = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools}}

        elif method == "tools/call":
            tool_name = req["params"]["name"]
            tool_args = req["params"].get("arguments", {})
            handler = HANDLERS.get(tool_name)
            if handler:
                result = handler["fn"](tool_args)
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool not found: {tool_name}"}}

        elif method == "initialize":
            resp = {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "mindmap-wizard", "version": "1.0"}, "capabilities": {"tools": {}}}}

        else:
            continue

        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
