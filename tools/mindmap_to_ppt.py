#!/usr/bin/env python3
"""思维导图 → PPT 自动转换器 — Gamma.app 风格。

从 Markdown 导图自动生成演示文稿。
每个 ## 一级分支 = 一张幻灯片。
"""

import argparse
import re
from pathlib import Path
from _common import logger

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    HAS_PPTX = True
except ImportError:
    HAS_PPTX = False


# 预设配色方案
COLOR_SCHEMES = {
    "professional": {"bg": "FFFFFF", "title": "1B3A5C", "body": "333333", "accent": "2E86C1"},
    "creative":   {"bg": "FFF8E7", "title": "E65100", "body": "4E342E", "accent": "FF8F00"},
    "minimal":    {"bg": "FAFAFA", "title": "212121", "body": "616161", "accent": "757575"},
    "ocean":      {"bg": "F0F8FF", "title": "0D47A1", "body": "263238", "accent": "00ACC1"},
}


def parse_md_to_slides(md_text: str) -> list[dict]:
    """解析 Markdown 导图为幻灯片结构。"""
    lines = md_text.strip().split("\n")
    slides = []
    current_slide = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        h1 = re.match(r'^#\s+(.+)', line)
        h2 = re.match(r'^##\s+(.+)', line)
        h3 = re.match(r'^###\s+(.+)', line)
        bullet = re.match(r'^[-*]\s+(.+)', line)

        if h1:
            slides.append({"title": h1.group(1), "type": "title", "bullets": []})
        elif h2:
            if current_slide:
                slides.append(current_slide)
            current_slide = {"title": h2.group(1), "type": "content", "bullets": []}
        elif h3 and current_slide:
            current_slide["bullets"].append(("sub", h3.group(1)))
        elif bullet and current_slide:
            current_slide["bullets"].append(("bullet", bullet.group(1)))

    if current_slide:
        slides.append(current_slide)
    return slides


def create_ppt(slides: list[dict], output_path: str, color_scheme: str = "professional"):
    """从幻灯片结构生成 .pptx 文件。"""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["professional"])

    for slide_data in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout

        # 背景
        bg = slide.background
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor.from_string(colors["bg"])

        if slide_data["type"] == "title":
            # 标题页
            txBox = slide.shapes.add_textbox(Inches(2), Inches(2.5), Inches(9), Inches(2))
            tf = txBox.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = slide_data["title"]
            p.font.size = Pt(44)
            p.font.bold = True
            p.font.color.rgb = RGBColor.from_string(colors["title"])
            p.alignment = 1  # center
        else:
            # 内容页
            # 标题
            txBox = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11), Inches(1))
            tf = txBox.text_frame
            p = tf.paragraphs[0]
            p.text = slide_data["title"]
            p.font.size = Pt(32)
            p.font.bold = True
            p.font.color.rgb = RGBColor.from_string(colors["title"])

            # 项目符号
            if slide_data["bullets"]:
                txBox = slide.shapes.add_textbox(Inches(1.5), Inches(2), Inches(10), Inches(5))
                tf = txBox.text_frame
                tf.word_wrap = True
                for i, (btype, text) in enumerate(slide_data["bullets"]):
                    if i == 0:
                        p = tf.paragraphs[0]
                    else:
                        p = tf.add_paragraph()
                    p.text = ("  • " if btype == "sub" else "• ") + text
                    p.font.size = Pt(20) if btype == "bullet" else Pt(18)
                    p.font.color.rgb = RGBColor.from_string(colors["body"])
                    p.space_after = Pt(8)
                # 强调第一个项目符号
                if tf.paragraphs:
                    tf.paragraphs[0].font.color.rgb = RGBColor.from_string(colors["accent"])
                    tf.paragraphs[0].font.bold = True

    prs.save(output_path)
    logger.info(f"✅ PPT 已生成: {output_path}")
    logger.info(f"   📊 {len(slides)} 张幻灯片 (配色: {color_scheme})")


def main():
    parser = argparse.ArgumentParser(
        description="思维导图 Markdown → PowerPoint — Gamma.app 风格",
        epilog="""
配色方案: professional / creative / minimal / ocean
示例:
  python mindmap_to_ppt.py my_mindmap.md -o presentation.pptx -c ocean
        """,
    )
    parser.add_argument("input", help="Markdown 导图文件")
    parser.add_argument("--output", "-o", help="输出 .pptx 路径")
    parser.add_argument("--color", "-c", default="professional",
                        choices=list(COLOR_SCHEMES.keys()), help="配色方案")
    args = parser.parse_args()

    if not HAS_PPTX:
        print("❌ 缺少依赖: pip install python-pptx")
        return 1

    md_text = Path(args.input).read_text(encoding="utf-8")
    slides = parse_md_to_slides(md_text)

    if not slides:
        print("❌ 无法解析任何幻灯片。请确保 Markdown 有 # 和 ## 标题。")
        return 1

    output = args.output or str(Path(args.input).with_suffix(".pptx"))
    create_ppt(slides, output, args.color)
    return 0


if __name__ == "__main__":
    exit(main())
