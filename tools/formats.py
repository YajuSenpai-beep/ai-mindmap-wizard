#!/usr/bin/env python3
"""
Extended Format Support — extract text from Word, PowerPoint, and generic HTML.

Usage:
  python formats.py <input_dir> --type docx|pptx|html [--output-dir ./text/]
"""
import os
import sys
import re
import argparse
from pathlib import Path
from _common import logger


def extract_docx(path):
    """Extract text from .docx file. Returns structured text with headings."""
    try:
        from docx import Document
    except ImportError:
        sys.exit("请安装 python-docx: pip install python-docx")

    doc = Document(path)
    paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        # Detect heading levels from style
        if para.style.name.startswith('Heading'):
            level = para.style.name.split()[-1]
            try:
                level_num = int(level)
                prefix = '#' * level_num
            except ValueError:
                prefix = '##'
            paragraphs.append(f"{prefix} {text}")
        else:
            paragraphs.append(text)

    # Extract tables
    for i, table in enumerate(doc.tables):
        rows = []
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            rows.append(' | '.join(cells))
        if rows:
            paragraphs.append(f"\n**表 {i+1}:**")
            paragraphs.append('\n'.join(rows))

    return '\n\n'.join(paragraphs)


def extract_pptx(path):
    """Extract text from .pptx file. Returns slide-by-slide text."""
    try:
        from pptx import Presentation
    except ImportError:
        sys.exit("请安装 python-pptx: pip install python-pptx")

    prs = Presentation(path)
    slides = []
    for i, slide in enumerate(prs.slides, 1):
        slide_lines = [f"## 幻灯片 {i}"]
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    text = para.text.strip()
                    if text:
                        slide_lines.append(text)
            if shape.has_table:
                table = shape.table
                rows = []
                for row in table.rows:
                    cells = [cell.text.strip() for cell in row.cells]
                    rows.append(' | '.join(cells))
                if rows:
                    slide_lines.append('\n' + '\n'.join(rows))
        slides.append('\n'.join(slide_lines))

    return '\n\n---\n\n'.join(slides)


def extract_html(path):
    """Extract text from generic HTML file. Returns Markdown-like text."""
    try:
        from bs4 import BeautifulSoup
        from html2text import HTML2Text
    except ImportError:
        sys.exit("请安装 beautifulsoup4 html2text lxml: pip install beautifulsoup4 html2text lxml")

    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    # Remove script, style, nav, footer
    for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()

    # Find main content
    main = soup.find('main') or soup.find('article') or soup.find('body')
    if not main:
        return "(no extractable content)"

    h = HTML2Text()
    h.body_width = 0
    h.protect_links = True
    md = h.handle(str(main)).strip()
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md


def extract_subtitles(path):
    """Extract text from SRT/VTT subtitle files."""
    text = Path(path).read_text(encoding='utf-8')
    # Remove timestamps and index numbers
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        # Skip index numbers, timestamps, and WEBVTT header
        if (re.match(r'^\d+$', line) or
            re.match(r'^\d{2}:\d{2}:\d{2}[,\.]\d{3}', line) or
            '-->' in line or
            line == 'WEBVTT' or
            not line):
            continue
        lines.append(line)
    return '\n'.join(lines)


def extract_file(path, file_type=None):
    """
    Extract text from a file. Auto-detect type from extension.
    Returns (text, file_type).
    """
    ext = Path(path).suffix.lower()

    type_map = {
        '.docx': ('docx', extract_docx),
        '.pptx': ('pptx', extract_pptx),
        '.html': ('html', extract_html),
        '.htm':  ('html', extract_html),
        '.srt':  ('subtitle', extract_subtitles),
        '.vtt':  ('subtitle', extract_subtitles),
    }

    if ext in type_map:
        ftype, func = type_map[ext]
        return func(path), ftype

    return None, None


def batch_extract(input_dir, output_dir=None):
    """Extract text from all supported files in input_dir."""
    base = Path(input_dir)
    supported = {'.docx', '.pptx', '.html', '.htm', '.srt', '.vtt'}

    results = {}
    for root, dirs, files in os.walk(base):
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in supported:
                path = str(Path(root) / f)
                text, ftype = extract_file(path)
                if text:
                    results[path] = {'type': ftype, 'text': text}

    if output_dir:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        for path, data in results.items():
            fname = Path(path).stem + '.txt'
            with open(out / fname, 'w', encoding='utf-8') as f:
                f.write(data['text'])
        logger.info(f"Extracted {len(results)} files → {output_dir}")

    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract text from Word/PPT/HTML/subtitle files')
    parser.add_argument('input', help='Input file or directory')
    parser.add_argument('--type', choices=['docx', 'pptx', 'html', 'subtitle', 'auto'],
                        default='auto', help='File type (default: auto-detect)')
    parser.add_argument('--output-dir', help='Save extracted text files to directory')
    args = parser.parse_args()

    if os.path.isfile(args.input):
        text, ftype = extract_file(args.input, args.type)
        if text:
            logger.info(text)
        else:
            logger.info(f"Unsupported or empty: {args.input}")
    else:
        batch_extract(args.input, args.output_dir)
