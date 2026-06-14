#!/usr/bin/env python3
"""交叉引用断链检查 — 扫描所有 MD 文件中的相对链接并验证目标存在。"""

import re
import sys
from pathlib import Path


def find_md_links(content: str) -> list[tuple[str, str]]:
    """提取 Markdown 中的相对链接: [text](path) 或 [text](path.md)"""
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return [(m.group(1), m.group(2)) for m in re.finditer(pattern, content)]


def check_links(root_dir: str) -> dict:
    """扫描所有 MD 文件，检查每个链接的目标是否存在。"""
    root = Path(root_dir)
    results = {"total": 0, "ok": 0, "broken": [], "external": 0}

    for md_file in root.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        links = find_md_links(content)

        for text, target in links:
            results["total"] += 1

            # 跳过外部链接
            if target.startswith(("http://", "https://", "mailto:")):
                results["external"] += 1
                continue

            # 解析相对路径
            target_path = (md_file.parent / target).resolve()

            # 处理锚点
            if "#" in str(target_path):
                target_path = Path(str(target_path).split("#")[0])

            if target_path.exists():
                results["ok"] += 1
            else:
                results["broken"].append({
                    "source": str(md_file.relative_to(root)),
                    "link": target,
                    "resolved": str(target_path),
                })

    return results


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    results = check_links(root)

    print(f"[links] {Path(root).resolve()}")
    print(f"   total={results['total']} ok={results['ok']} external={results['external']} broken={len(results['broken'])}")

    if results["broken"]:
        print("\nBROKEN:")
        for b in results["broken"]:
            print(f"   {b['source']} -> {b['link']}  (not found: {b['resolved']})")
        return 1
    else:
        print("[links] all internal links valid")
        return 0


if __name__ == "__main__":
    exit(main())
