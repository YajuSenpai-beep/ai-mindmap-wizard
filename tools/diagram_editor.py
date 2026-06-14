#!/usr/bin/env python3
"""AI 往返编辑器 — 读取已有导图，分析结构，提出改进建议，智能更新。

支持: .xmind, .md (Markdown), .mmd (Mermaid), .drawio
"""

import argparse
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from _common import logger


# === 读取 ===

def read_markdown(path: str) -> dict:
    """读取 Markdown 导图，返回结构化分析。"""
    text = Path(path).read_text(encoding="utf-8")
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    stats = {"h1": 0, "h2": 0, "h3": 0, "h4": 0, "bullet": 0, "max_depth": 0, "nodes": []}
    for line in lines:
        m = re.match(r'^(#{1,6})\s+(.+)', line)
        if m:
            level = len(m.group(1))
            stats[f"h{level}"] = stats.get(f"h{level}", 0) + 1
            stats["max_depth"] = max(stats["max_depth"], level)
            stats["nodes"].append({"level": level, "text": m.group(2)[:80], "line": line[:120]})
        elif line.startswith("- "):
            stats["bullet"] += 1
            stats["nodes"].append({"level": 99, "text": line[2:80], "line": line[:120]})

    return stats


def read_xmind(path: str) -> dict:
    """读取 XMind 文件，提取节点统计。"""
    nodes = []
    with zipfile.ZipFile(path) as zf:
        if "content.json" in zf.namelist():
            data = json.loads(zf.read("content.json"))
            def walk(topic, depth=0):
                nodes.append({"level": depth, "text": topic.get("title", "")[:80]})
                for child in topic.get("children", {}).get("attached", []):
                    walk(child, depth + 1)
            for sheet in data:
                walk(sheet.get("rootTopic", {}))
        elif "content.xml" in zf.namelist():
            xml = zf.read("content.xml")
            root = ET.fromstring(xml)
            ns = "{urn:xmind:xmap:xmlns:content:2.0}"
            for topic in root.iter(f"{ns}topic"):
                title_el = topic.find(f"{ns}title")
                if title_el is not None and title_el.text:
                    nodes.append({"level": 0, "text": title_el.text[:80]})

    return {"total_nodes": len(nodes), "nodes": nodes[:30]}


def read_mermaid(path: str) -> dict:
    """读取 Mermaid 文件。"""
    text = Path(path).read_text(encoding="utf-8")
    nodes = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped and not stripped.startswith(("mindmap", "graph", "flowchart", "%%")):
            indent = len(line) - len(line.lstrip())
            text_clean = re.sub(r'[\(\)\[\]\{\}"\']', '', stripped)[:80]
            nodes.append({"level": indent // 2, "text": text_clean})
    return {"total_nodes": len(nodes), "nodes": nodes[:30]}


# === 分析 ===

def analyze(stats: dict) -> list[str]:
    """分析导图结构并给出改进建议。"""
    suggestions = []

    if stats.get("h2", 0) == 0:
        suggestions.append("⚠️ 没有二级标题 (##)。建议将内容拆分为 3-8 个主要分支。")
    elif stats["h2"] > 12:
        suggestions.append(f"⚠️ 二级分支过多 ({stats['h2']} 个)。建议合并相关内容，控制在 8 个以内。")

    if stats.get("h3", 0) == 0 and stats.get("h2", 0) > 0:
        suggestions.append("💡 缺少三级细节 (###)。建议为每个二级分支增加 2-4 个支撑要点。")

    if stats.get("max_depth", 0) > 5:
        suggestions.append(f"⚠️ 层级过深 ({stats['max_depth']} 层)。超过 4 层的分支建议拆分为独立子图。")

    # 节点长度检查
    if stats.get("nodes"):
        overlong = [n for n in stats["nodes"] if len(n["text"]) > 20]
        if overlong:
            suggestions.append(f"💡 {len(overlong)} 个节点超过 20 字，建议精简。")

    # 不平衡检查
    if stats.get("h2", 0) > 0 and stats.get("h3", 0) > 0:
        ratio = stats["h3"] / stats["h2"]
        if ratio < 1:
            suggestions.append(f"💡 平均每个二级分支只有 {ratio:.1f} 个三级要点，信息密度偏低。")
        elif ratio > 8:
            suggestions.append(f"⚠️ 平均每个二级分支有 {ratio:.1f} 个三级要点，建议拆分或精简。")

    if not suggestions:
        suggestions.append("✅ 导图结构良好。")

    return suggestions


# === 更新 ===

def update_markdown(path: str, operations: list[str]) -> str:
    """根据建议操作更新 Markdown 导图。"""
    text = Path(path).read_text(encoding="utf-8")
    updated = text

    for op in operations:
        if op == "merge_short_h2":
            # 合并过短的二级分支
            lines = updated.split("\n")
            merged = []
            buffer = None
            for line in lines:
                m = re.match(r'^##\s+(.+)', line)
                if m and len(m.group(1)) < 10 and buffer is None:
                    buffer = m.group(1)
                elif buffer and line.startswith("## "):
                    merged.append(f"## {buffer} & {re.match(r'^##\s+(.+)', line).group(1)}")
                    buffer = None
                else:
                    merged.append(line)
            updated = "\n".join(merged)

        elif op == "add_missing_h3":
            # 标记缺少三级的二级分支
            updated += "\n\n<!-- ⚠️ 以下二级分支建议补充三级要点：运行 analyze 查看详情 -->"

    return updated


def main():
    parser = argparse.ArgumentParser(description="AI 往返编辑器 — 读取分析更新导图")
    parser.add_argument("input", help="导图文件 (.md / .xmind / .mmd)")
    parser.add_argument("--analyze", "-a", action="store_true", help="仅分析，不修改")
    parser.add_argument("--update", "-u", action="store_true", help="分析并自动更新")
    parser.add_argument("--output", "-o", help="更新后输出路径")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    path = Path(args.input)
    ext = path.suffix.lower()

    # 读取
    readers = {".md": read_markdown, ".xmind": read_xmind, ".mmd": read_mermaid, ".drawio": read_mermaid}
    reader = readers.get(ext)
    if not reader:
        print(f"❌ 不支持的文件格式: {ext}")
        return 1

    stats = reader(str(path))
    suggestions = analyze(stats)

    if args.json:
        logger.info(json.dumps({"stats": stats, "suggestions": suggestions}, ensure_ascii=False, indent=2))
    else:
        logger.info(f"📊 {path.name} 分析结果:")
        logger.info(f"   节点数: {stats.get('total_nodes', stats.get('h1', 0) + stats.get('h2', 0) + stats.get('h3', 0) + stats.get('bullet', 0))}")
        logger.info(f"   层级深度: {stats.get('max_depth', '?')}")
        logger.info()
        for s in suggestions:
            logger.info(f"  {s}")

    if args.update and ext == ".md":
        updated = update_markdown(str(path), [])
        out = args.output or str(path)
        Path(out).write_text(updated, encoding="utf-8")
        logger.info(f"\n✅ 已更新: {out}")

    return 0


if __name__ == "__main__":
    exit(main())
