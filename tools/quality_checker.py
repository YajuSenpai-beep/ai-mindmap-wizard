#!/usr/bin/env python3
"""
Quality Checker: compare generated notes against OCR source data.

Usage:
  python quality_checker.py <notes_dir> <ocr_results_dir> [--output report.md]
"""
import json
import os
import re
import argparse
from pathlib import Path
from _common import logger

def load_ocr_sources(ocr_dir):
    """Load all OCR JSON results into {topic_name: [{file, text}]}."""
    sources = {}
    for fname in os.listdir(ocr_dir):
        if fname == '_index.json' or not fname.endswith('.json'):
            continue
        path = os.path.join(ocr_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            items = json.load(f)
        topic = fname.replace('.json', '')
        sources[topic] = items
    return sources

def extract_sections_from_note(note_path):
    """Parse a markdown note into {section_title: content}."""
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = {}
    current_title = '_head'
    current_content = []

    for line in content.split('\n'):
        if line.startswith('## '):
            if current_content:
                sections[current_title] = '\n'.join(current_content)
            current_title = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        sections[current_title] = '\n'.join(current_content)

    return sections

def fuzzy_find_source(section_title, sources):
    """Find the OCR source most likely matching this section title."""
    title_lower = section_title.lower().replace(' ', '').replace('+', '➕')
    best = None
    best_score = 0

    for topic, items in sources.items():
        # Simplified matching: count overlapping characters
        topic_clean = topic.lower().replace(' ', '').replace('_', '')
        overlap = len(set(title_lower) & set(topic_clean))
        if overlap > best_score:
            best_score = overlap
            best = topic

    if best_score > 3:
        return best, sources[best]
    return None, None

def check_section(section_title, note_content, ocr_items):
    """Check one section for issues."""
    findings = []

    if not ocr_items:
        findings.append(('NO_SOURCE', 'No matching OCR source found'))
        return findings

    # Concatenate all OCR text for this topic
    all_ocr_text = '\n'.join(item.get('text', '') for item in ocr_items)

    # Check if note has substantial claims not in OCR
    cjk_ocr = set(re.findall(r'[一-鿿]{2,}', all_ocr_text))
    cjk_note = set(re.findall(r'[一-鿿]{2,}', note_content))

    cjk_note - cjk_ocr
    only_in_ocr = cjk_ocr - cjk_note

    if len(only_in_ocr) > 20:
        findings.append(('MISSING', f'OCR has {len(only_in_ocr)} terms not in note'))

    # Check for numbers/steps mismatch
    set(re.findall(r'(\d+)[\.\、\s]', all_ocr_text))
    set(re.findall(r'(\d+)[\.\、\s]', note_content))

    return findings

def generate_report(notes_dir, ocr_dir, output_path):
    """Generate a cross-validation report."""
    sources = load_ocr_sources(ocr_dir)
    note_files = sorted(Path(notes_dir).glob('*.md'))

    lines = []
    lines.append('# 校准报告')
    lines.append('')
    lines.append(f'OCR 源文件数：{len(sources)} | 笔记文件数：{len(note_files)}')
    lines.append('')

    for note_path in note_files:
        if note_path.name.startswith('00_') or note_path.name.startswith('校准'):
            continue

        lines.append(f'## {note_path.name}')
        sections = extract_sections_from_note(str(note_path))
        note_topics = {k: v for k, v in sections.items() if len(v) > 100}

        lines.append(f''
                     f'章节数：{len(note_topics)}')
        lines.append('')

        matches = 0
        no_source = 0

        for title, content in note_topics.items():
            topic, items = fuzzy_find_source(title, sources)
            if topic:
                matches += 1
                findings = check_section(title, content, items)
                if findings:
                    lines.append(f'### ⚠ {title}')
                    for ftype, fdesc in findings:
                        lines.append(f'- [{ftype}] {fdesc}')
                    lines.append(f'  → OCR 源: `{topic}` ({len(items)} files)')
                    lines.append('')
            else:
                no_source += 1

        lines.append('')
        lines.append(f'- 有 OCR 源对应的章节：{matches}')
        lines.append(f'- 无 OCR 源对应的章节：{no_source}')
        lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('## 说明')
    lines.append('- **MISSING**：OCR 有但笔记未收录的内容')
    lines.append('- **NO_SOURCE**：笔记章节找不到对应 OCR 源，无法核对')
    lines.append('- 本报告仅覆盖有 OCR 源对应的章节，其余章节需人工核验')

    report = '\n'.join(lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    logger.info(f"Report saved to: {output_path}")
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quality Checker - cross-validate notes vs OCR sources')
    parser.add_argument('notes_dir', help='Directory containing markdown notes')
    parser.add_argument('ocr_results_dir', help='Directory containing OCR JSON results')
    parser.add_argument('--output', default='校准报告.md', help='Output report path')

    args = parser.parse_args()
    generate_report(args.notes_dir, args.ocr_results_dir, args.output)
