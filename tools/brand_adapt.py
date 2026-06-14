#!/usr/bin/env python3
"""品牌自动适配 — 从网站/Logo 提取配色，自动映射到 Mermaid/PPT/XMind 配色方案。

使用:
  python tools/brand_adapt.py https://example.com
  python tools/brand_adapt.py --color "#1B3A5C" --name "MyBrand"
"""

import argparse
import json
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


# === 预设品牌配色库 ===
KNOWN_BRANDS = {
    "apple":     {"primary": "1D1D1F", "secondary": "86868B", "accent": "0071E3", "bg": "F5F5F7"},
    "google":    {"primary": "4285F4", "secondary": "EA4335", "accent": "FBBC04", "bg": "FFFFFF"},
    "microsoft": {"primary": "0078D4", "secondary": "106EBE", "accent": "50E6FF", "bg": "FFFFFF"},
    "notion":    {"primary": "000000", "secondary": "37352F", "accent": "E16259", "bg": "FFFFFF"},
    "stripe":    {"primary": "635BFF", "secondary": "00D924", "accent": "7A73FF", "bg": "0A0F1E"},
    "vercel":    {"primary": "000000", "secondary": "666666", "accent": "0070F3", "bg": "FAFAFA"},
}


def extract_colors_from_url(url: str) -> dict:
    """从网页提取主色。"""
    resp = requests.get(url, headers={"User-Agent": "BrandAdaptBot/1.0"}, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    colors = {"primary": "1B3A5C", "secondary": "2E86C1", "accent": "E74C3C", "bg": "FFFFFF"}

    # 方法1：CSS 变量
    for style in soup.find_all("style"):
        text = style.string or ""
        # 找最常见的自定义属性
        for match in re.finditer(r'--(?:primary|brand|accent|main)[\w-]*:\s*(#[0-9a-fA-F]{6})', text):
            colors["primary"] = match.group(1).lstrip("#").upper()

    # 方法2：meta theme-color
    meta = soup.find("meta", attrs={"name": "theme-color"})
    if meta:
        colors["primary"] = meta.get("content", "").lstrip("#").upper()

    # 方法3：logo/favicon 颜色（启发式——用页面中出现最多的非灰非白色）
    all_text = soup.get_text()
    hex_colors = re.findall(r'#([0-9a-fA-F]{6})', all_text)
    if hex_colors:
        from collections import Counter
        cnt = Counter(c.upper() for c in hex_colors if c.upper() not in ("FFFFFF", "000000", "333333", "666666", "999999"))
        if cnt:
            colors["primary"] = cnt.most_common(1)[0][0]

    return colors


def generate_mermaid_classdef(colors: dict) -> str:
    """生成 Mermaid classDef 代码。"""
    return f"""classDef primary fill:#{colors['primary']},color:#fff,stroke:#{colors['primary'][:-2]}88
classDef secondary fill:#{colors['secondary']},color:#fff,stroke:#{colors['secondary'][:-2]}88
classDef accent fill:#{colors['accent']},color:#fff
classDef background fill:#{colors['bg']},color:#333"""


def generate_ppt_scheme(colors: dict) -> str:
    """生成 PPT 配色方案参数。"""
    return f"--color \"{colors['primary']},{colors['secondary']},{colors['accent']},{colors['bg']}\""


def generate_xmind_theme(colors: dict) -> str:
    """生成 XMind 主题配色参考。"""
    return f"""中心主题: #{colors['primary']}
一级分支: #{colors['secondary']} or 浅色变体
强调色: #{colors['accent']}
背景: #{colors['bg']}"""


def main():
    parser = argparse.ArgumentParser(description="品牌自动适配——提取配色→映射到图表工具")
    parser.add_argument("url", nargs="?", help="品牌网站 URL")
    parser.add_argument("--color", help="手动指定主色 (如 #1B3A5C)")
    parser.add_argument("--name", help="品牌名称 (用于匹配预设库)")
    parser.add_argument("--output", "-o", help="输出 JSON 配色文件")
    parser.add_argument("--list", action="store_true", help="列出预设品牌")
    args = parser.parse_args()

    if args.list:
        logger.info("📋 预设品牌配色库:")
        for name, c in KNOWN_BRANDS.items():
            bar = "".join(f"\033[48;2;{int(c[k][0:2],16)};{int(c[k][2:4],16)};{int(c[k][4:6],16)}m  \033[0m" for k in ["primary", "secondary", "accent"])
            logger.info(f"  {name:15s} {bar}")
        return 0

    if args.name and args.name.lower() in KNOWN_BRANDS:
        colors = KNOWN_BRANDS[args.name.lower()]
    elif args.color:
        c = args.color.lstrip("#").upper()
        colors = {"primary": c, "secondary": c, "accent": "E74C3C", "bg": "FFFFFF"}
    elif args.url:
        if not HAS_DEPS:
            print("❌ 缺少依赖: pip install requests beautifulsoup4")
            return 1
        domain = urlparse(args.url).netloc.lower()
        for brand, c in KNOWN_BRANDS.items():
            if brand in domain:
                colors = c
                logger.info(f"🎯 匹配预设品牌: {brand}")
                break
        else:
            logger.info(f"🌐 正在提取: {args.url}")
            colors = extract_colors_from_url(args.url)
    else:
        parser.print_help()
        return 1

    logger.info("\n🎨 品牌配色方案:")
    for k, v in colors.items():
        r, g, b = int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)
        bar = f"\033[48;2;{r};{g};{b}m          \033[0m"
        logger.info(f"  {k:12s} #{v}  {bar}")

    logger.info("\n📋 Mermaid classDef:")
    logger.info(generate_mermaid_classdef(colors))
    logger.info("\n📋 PPT 命令:")
    logger.info(f"  python tools/mindmap_to_ppt.py input.md {generate_ppt_scheme(colors)}")
    logger.info("\n📋 XMind 参考:")
    logger.info(generate_xmind_theme(colors))

    if args.output:
        Path(args.output).write_text(json.dumps(colors, indent=2, ensure_ascii=False))
        logger.info(f"\n✅ 已保存: {args.output}")

    return 0


if __name__ == "__main__":
    exit(main())
