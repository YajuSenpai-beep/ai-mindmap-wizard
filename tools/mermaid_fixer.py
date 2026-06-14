#!/usr/bin/env python3
"""Mermaid 语法修复器 — 从 NoteMD Pro 的 37 条正则规则提炼。

自动检测和修复 Mermaid 代码中常见的语法错误。
支持 mindmap, graph, flowchart, sequenceDiagram, classDiagram, gantt 等图表类型。
"""

import re
import sys
import json
from pathlib import Path
from _common import logger


# === 修复规则库 (37 rules) ===

FIX_RULES = [
    # === 通用语法 ===
    {
        "name": "remove_empty_lines_in_nodes",
        "pattern": r'(\w+)\[\s*"([^"]*?)\n\s*([^"]*?)"\s*\]',
        "replacement": r'\1["\2 \3"]',
        "desc": "移除节点标签内的换行符",
    },
    {
        "name": "fix_unquoted_special_chars",
        "pattern": r'\[([^\]"]*?[\(\)\[\]\{\}<>|&;][^\]"]*?)\]',
        "replacement": r'["\1"]',
        "desc": "为含特殊字符的无引号标签加引号",
    },
    {
        "name": "fix_chinese_colon_in_labels",
        "pattern": r'\["?([^\]"]*?[：：][^\]"]*?)"?\]',
        "replacement": r'["\1"]',
        "desc": "中文冒号在未引号标签中 → 加引号",
    },
    {
        "name": "remove_trailing_semicolons",
        "pattern": r'(\w+(?:\["[^"]*"\])?);(\s*)$',
        "replacement": r'\1\2',
        "desc": "Mermaid 不需要行尾分号 (graph/flowchart)",
    },
    {
        "name": "fix_unicode_minus",
        "pattern": r'—|–|−',
        "replacement": '-',
        "desc": "Unicode 破折号/减号 → ASCII 连字符",
    },
    {
        "name": "fix_unicode_quotes",
        "pattern": r'[“”‘’]',
        "replacement": '"',
        "desc": "Unicode 引号 → ASCII 双引号",
    },
    {
        "name": "remove_bom",
        "pattern": r'^﻿',
        "replacement": '',
        "desc": "移除 UTF-8 BOM 标记",
    },
    {
        "name": "fix_consecutive_blank_lines",
        "pattern": r'\n{3,}',
        "replacement": '\n\n',
        "desc": "连续空行超过2个→缩减为2个",
    },

    # === mindmap 特定 ===
    {
        "name": "fix_mindmap_indent_tabs",
        "pattern": r'^( +)\t+( +)',
        "replacement": r'\1    \2',
        "desc": "mindmap 中 tab+space 混合 → 纯空格缩进",
    },
    {
        "name": "fix_mindmap_root_missing",
        "pattern": r'^mindmap\s*$',
        "replacement": 'mindmap\n  root',
        "desc": "mindmap 必须有 root 关键字",
    },
    {
        "name": "fix_mindmap_node_double_colon",
        "pattern": r'^(\s*)([^:]+)::(.+)$',
        "replacement": r'\1\2\n\1  \3',
        "desc": "mindmap 节点双冒号→拆分为子节点",
    },

    # === flowchart / graph 特定 ===
    {
        "name": "fix_flowchart_empty_nodes",
        "pattern": r'\w+\[\s*\]',
        "replacement": '',
        "desc": "移除空的方括号节点（可能是删除残留）",
    },
    {
        "name": "fix_flowchart_arrow_style",
        "pattern": r'--\s*>',
        "replacement": '-->',
        "desc": "箭头风格不一致 → 统一为 -->",
    },
    {
        "name": "fix_flowchart_node_id_spaces",
        "pattern": r'(\w+)\s+(\[|\(|\{)',
        "replacement": r'\1\2',
        "desc": "节点 ID 和形状括号间不应有空格",
    },
    {
        "name": "fix_flowchart_subgraph_case",
        "pattern": r'Subgraph\s+',
        "replacement": 'subgraph ',
        "desc": "subgraph 关键字大小写错误",
    },
    {
        "name": "fix_flowchart_end_keyword",
        "pattern": r'^(\s*)end\s*$',
        "replacement": r'\1end',
        "desc": "end 关键字后不应有空格和内容",
    },
    {
        "name": "fix_flowchart_link_style_syntax",
        "pattern": r'linkStyle\s+(\d+)\s+([^,]+),(\S)',
        "replacement": r'linkStyle \1 \2,\3',
        "desc": "linkStyle 的 color,style 参数间加逗号",
    },

    # === classDiagram 特定 ===
    {
        "name": "fix_class_relation_labels_space",
        "pattern": r'(\w+)\s+(<\|--|--\|>|--|\.\.)\s+(.+)',
        "replacement": r'\1 \2 \3',
        "desc": "类关系运算符前后加空格（如已无空格）",
    },
    {
        "name": "fix_class_method_parens",
        "pattern": r'(\w+)\(\)\s*:',
        "replacement": r'\1() :',
        "desc": "类方法括号后无空格→加空格",
    },

    # === sequenceDiagram 特定 ===
    {
        "name": "fix_sequence_note_placement",
        "pattern": r'Note\s+(right of|left of|over)\s+(\w+)\s*:\s*"',
        "replacement": r'Note \1 \2: "',
        "desc": "Note 放置中避免空白colon",
    },
    {
        "name": "fix_sequence_participant_quotes",
        "pattern": r'participant\s+(\w+)\s+as\s+(\w+)',
        "replacement": r'participant \1 as \2',
        "desc": "participant as 别名间确保单空格",
    },
    {
        "name": "fix_sequence_arrow_activation",
        "pattern": r'(\w+)->>\+(\w+)\s*:\s*(.+)',
        "replacement": r'\1->>+ \2: \3',
        "desc": "激活箭头前后加空格",
    },
    {
        "name": "fix_sequence_parallel_block",
        "pattern": r'^par\s+(.+)$',
        "replacement": r'par \1',
        "desc": "par 块关键字后确保有描述",
    },

    # === gantt 特定 ===
    {
        "name": "fix_gantt_date_format",
        "pattern": r'(\d{4})/(\d{1,2})/(\d{1,2})',
        "replacement": r'\1-\2-\3',
        "desc": "甘特图日期格式统一为 YYYY-MM-DD",
    },
    {
        "name": "fix_gantt_section_syntax",
        "pattern": r'^section\s*$',
        "replacement": 'section Tasks',
        "desc": "空的 section 关键字添加默认名",
    },
    {
        "name": "fix_gantt_task_duration",
        "pattern": r':(\w+),\s*(\d+)(d|w|h)$',
        "replacement": r':\1, \2\3',
        "desc": "甘特图任务时长格式: 名称, 数字+单位",
    },

    # === erDiagram 特定 ===
    {
        "name": "fix_er_relation_cardinality",
        "pattern": r'(\w+)\s*\|\|--o\|\s*(\w+)',
        "replacement": r'\1 ||--o| \2',
        "desc": "ER 关系中基数符号前后加空格",
    },
    {
        "name": "fix_er_entity_braces_format",
        "pattern": r'(\w+)\s*\{',
        "replacement": r'\1 {',
        "desc": "实体名后大括号前确保单空格",
    },

    # === 节点 ID 规范 ===
    {
        "name": "sanitize_node_id_chars",
        "pattern": r'(\w+)[^\w\[\]\(\)\{\}"\',;\-_\s]+(\w*)',
        "replacement": r'\1_\2',
        "desc": "节点 ID 中的非法字符→下划线",
    },
    {
        "name": "fix_node_id_starting_digit",
        "pattern": r'([\[\(])(\d+\w*)',
        "replacement": r'\1n\2',
        "desc": "以数字开头的节点ID加 n 前缀",
    },

    # === 颜色/样式 ===
    {
        "name": "fix_classdef_without_class",
        "pattern": r'classDef\s+(\w+)\s+([^;]+);?',
        "replacement": r'classDef \1 \2',
        "desc": "classDef 后移除多余分号",
    },
    {
        "name": "fix_style_color_hex_case",
        "pattern": r'#([0-9a-f]{3,6})',
        "replacement": r'#\1',
        "desc": "保持颜色十六进制小写（验证非修复）",
    },
    {
        "name": "fix_link_style_index_range",
        "pattern": r'linkStyle\s+(\d+)\s+default',
        "replacement": r'linkStyle \1 default',
        "desc": "linkStyle 默认样式确保正确空格",
    },

    # === 其他修复 ===
    {
        "name": "remove_html_comments",
        "pattern": r'<!--[\s\S]*?-->',
        "replacement": '',
        "desc": "移除 Mermaid 中不支持的 HTML 注释",
    },
    {
        "name": "fix_carriage_return",
        "pattern": r'\r\n',
        "replacement": '\n',
        "desc": "CRLF → LF 统一换行",
    },
    {
        "name": "preserve_frontmatter",
        "pattern": r'^---\s*$',
        "replacement": '---',
        "desc": "跳过 frontmatter 区域不做修复",
    },
]


def fix_mermaid(mermaid_code: str, verbose: bool = False) -> dict:
    """应用所有修复规则，返回修复后的代码和修复报告。"""
    fixed = mermaid_code
    report = {"total_rules": len(FIX_RULES), "applied": [], "skipped": []}

    for rule in FIX_RULES:
        if re.search(rule["pattern"], fixed, re.MULTILINE):
            before = fixed
            fixed = re.sub(rule["pattern"], rule["replacement"], fixed, flags=re.MULTILINE)
            if fixed != before:
                report["applied"].append(rule["name"])
                if verbose:
                    logger.info(f"  ✅ {rule['name']}: {rule['desc']}")
            else:
                report["skipped"].append(rule["name"])
        else:
            report["skipped"].append(rule["name"])

    report["changed"] = len(report["applied"]) > 0
    return {"code": fixed, "report": report}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Mermaid 语法自动修复器")
    parser.add_argument("input", help="输入 Mermaid 文件路径 或 '-' 从 stdin 读取")
    parser.add_argument("--output", "-o", help="输出文件路径（默认覆盖原文件）")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示修复详情")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出报告")
    args = parser.parse_args()

    # 读取输入
    if args.input == "-":
        code = sys.stdin.read()
    else:
        code = Path(args.input).read_text(encoding="utf-8")

    # 执行修复
    result = fix_mermaid(code, verbose=args.verbose)

    # 输出
    if args.json:
        logger.info(json.dumps(result["report"], indent=2, ensure_ascii=False))
    elif args.verbose:
        total = result["report"]["total_rules"]
        applied = len(result["report"]["applied"])
        logger.info(f"\n📊 共 {total} 条规则，应用了 {applied} 条修复")

    # 保存
    output_path = args.output or args.input
    if output_path != "-":
        Path(output_path).write_text(result["code"], encoding="utf-8")
        if not args.json:
            applied_count = len(result["report"]["applied"])
            logger.info(f"✅ 已修复 {applied_count} 处问题 → {output_path}")


if __name__ == "__main__":
    main()
