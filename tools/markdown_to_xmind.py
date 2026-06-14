#!/usr/bin/env python3
"""Markdown → XMind 原生 .xmind 文件生成器

从 Markdown 层级结构直接生成可编辑的 XMind 文件，
跳过「Markdown → 手动导入 XMind」的步骤。
"""

import json
import zipfile
import uuid
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _common import parse_markdown_to_tree, count_nodes, logger
from xml.etree import ElementTree as ET



def build_xmind_json(root: dict) -> dict:
    """将嵌套 dict 转为 XMind JSON 格式（XMind 2020+ 原生格式）。"""

    def build_topic(node):
        topic = {
            "id": uuid.uuid4().hex[:26],
            "class": "topic",
            "title": node["title"],
        }
        if node.get("children"):
            children_topics = []
            for child in node["children"]:
                ct = build_topic(child)
                if ct:
                    children_topics.append(ct)
            if children_topics:
                topic["children"] = {"attached": children_topics}
        return topic

    root_topic = build_topic(root)
    return {
        "id": uuid.uuid4().hex[:26],
        "class": "sheet",
        "title": "sheet1",
        "rootTopic": root_topic,
    }


def build_xmind_xml(root: dict) -> str:
    """构建兼容旧版 XMind 的 XML content.xml。"""
    ns = "urn:xmind:xmap:xmlns:content:2.0"

    def build_topic_el(node):
        el = ET.Element("topic", {"id": uuid.uuid4().hex[:26]})
        title_el = ET.SubElement(el, "title")
        title_el.text = node["title"]
        if node.get("children"):
            children_el = ET.SubElement(el, "children")
            topics_el = ET.SubElement(children_el, "topics", {"type": "attached"})
            for child in node["children"]:
                topics_el.append(build_topic_el(child))
        return el

    root_el = ET.Element("xmap-content", {"xmlns": ns, "version": "2.0"})
    sheet_el = ET.SubElement(root_el, "sheet", {"id": uuid.uuid4().hex[:26]})
    sheet_el.append(build_topic_el(root))

    ET.indent(root_el, space="  ")
    xml_body = ET.tostring(root_el, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_body


def create_xmind(markdown_path: str, output_path: str):
    """从 Markdown 文件生成 .xmind 文件。"""
    md_text = Path(markdown_path).read_text(encoding="utf-8")
    tree = parse_markdown_to_tree(md_text)

    if tree is None:
        raise ValueError("无法从 Markdown 中解析出任何内容。请确保有 # 标题。")

    # 构建 JSON
    xmind_json = build_xmind_json(tree)
    xmind_xml = build_xmind_xml(tree)

    # 创建 metadata (XMind 2020+ 需要)
    import time
    ts = int(time.time() * 1000)
    metadata = {
        "creator": {
            "name": "AI Mindmap Wizard",
            "version": "1.0"
        },
        "created": ts,
        "modified": ts,
    }

    # 创建 manifest.json (XMind 2020+ 使用此文件替代 META-INF/manifest.xml)
    manifest = {
        "file-entries": {
            "content.json": {},
            "metadata.json": {},
            "content.xml": {},
        }
    }

    # 打包为 .xmind (本质是 zip)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        zf.writestr("content.json", json.dumps([xmind_json], ensure_ascii=False, indent=2))
        zf.writestr("metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2))
        zf.writestr("content.xml", xmind_xml)

    node_count = count_nodes(tree)
    logger.info(f"✅ 已生成 XMind 文件: {output_path}")
    logger.info(f"   📊 {node_count} 个节点 | 根主题: {tree['title']}")



def main():
    parser = argparse.ArgumentParser(
        description="Markdown → XMind 原生文件生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python markdown_to_xmind.py input.md -o output.xmind
  python markdown_to_xmind.py notes.md                # 输出 notes.xmind
        """,
    )
    parser.add_argument("input", help="输入的 Markdown 文件")
    parser.add_argument("--output", "-o", help="输出 .xmind 文件路径（默认同目录同名 .xmind）")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 文件不存在: {args.input}")
        return 1

    output_path = args.output or str(input_path.with_suffix(".xmind"))
    create_xmind(str(input_path), output_path)
    return 0


if __name__ == "__main__":
    exit(main())
