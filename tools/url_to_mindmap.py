#!/usr/bin/env python3
"""URL 一键转思维导图 — Mapify 风格，从任意网页直接提取内容生成导图。

支持：普通网页、Wikipedia、GitHub README、技术文档等。
"""

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse
from _common import logger

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


def fetch_url(url: str) -> tuple:
    """抓取网页，返回 (title, clean_text)。"""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MindmapWizard/1.0)"
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or "utf-8"

    soup = BeautifulSoup(resp.text, "html.parser")

    # 移除脚本和样式
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    title = soup.title.string if soup.title else urlparse(url).path.strip("/")

    # 提取正文（按常见内容选择器优先级）
    content_selectors = [
        "article", "main", '[role="main"]',
        ".content", ".post-content", ".article-content",
        ".markdown-body", "#readme",  # GitHub
        "#bodyContent", "#mw-content-text",  # Wikipedia
        ".entry-content", ".post-body",
    ]
    content = None
    for sel in content_selectors:
        content = soup.select_one(sel)
        if content:
            break
    if not content:
        content = soup.body

    # 清理文本
    text = content.get_text(separator="\n", strip=True)
    text = re.sub(r'\n{3,}', '\n\n', text)  # 压缩空行
    text = text[:8000]  # 限制长度避免 token 爆炸

    return (title.strip(), text)


def extract_title_hierarchy(text: str) -> list[str]:
    """从 HTML 文本中提取标题层级。"""
    lines = text.split("\n")
    key_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 跳过太短的行（可能是导航）
        if len(line) < 5:
            continue
        # 保留可能是标题/关键句的行
        if len(line) < 200 and not line.startswith(("http", "©", "All rights")):
            key_lines.append(line)
    return key_lines[:60]  # 最多 60 行


def generate_markdown_mindmap(title: str, key_lines: list[str]) -> str:
    """将提取的标题层级转为 Markdown 思维导图。"""
    lines = [f"# {title}"]
    for i, line in enumerate(key_lines):
        # 根据长度和位置推断层级
        if len(line) < 30:
            lines.append(f"## {line}")
        elif len(line) < 80:
            lines.append(f"### {line}")
        else:
            lines.append(f"- {line[:80]}")
        if i > 40:
            break
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="URL → 思维导图 Markdown — Mapify 风格一键转换",
        epilog="""
示例:
  python url_to_mindmap.py https://en.wikipedia.org/wiki/Mind_map
  python url_to_mindmap.py https://github.com/user/repo -o output.md
        """,
    )
    parser.add_argument("url", help="目标网页 URL")
    parser.add_argument("--output", "-o", help="输出 Markdown 文件路径")
    parser.add_argument("--youtube", action="store_true", help="YouTube 专用模式（通过 yt-dlp-mcp 提取字幕）")
    args = parser.parse_args()

    if not HAS_DEPS:
        print("❌ 缺少依赖。请安装: pip install requests beautifulsoup4")
        return 1

    logger.info(f"🌐 正在抓取: {args.url}")
    try:
        title, text = fetch_url(args.url)
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        return 1

    key_lines = extract_title_hierarchy(text)
    md = generate_markdown_mindmap(title, key_lines)

    output = args.output or f"{re.sub(r'[^\w]', '_', title[:40])}.md"
    Path(output).write_text(md, encoding="utf-8")

    logger.info(f"✅ 已生成: {output}")
    logger.info(f"   📊 {len(key_lines)} 行关键内容 → {len(md.split(chr(10)))} 行导图")
    logger.info("   💡 下一步: 用通道 A 的提示词让 AI 美化这个 Markdown")

    # 提示可选后续步骤
    logger.info("\n📋 可选:")
    logger.info(f"   python multi_export.py {output} -f all   → 并行导出 6 种格式")
    logger.info(f"   python markdown_to_xmind.py {output}     → 转 XMind 原生文件")
    return 0


if __name__ == "__main__":
    exit(main())
