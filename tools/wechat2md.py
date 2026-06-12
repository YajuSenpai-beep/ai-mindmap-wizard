#!/usr/bin/env python3
"""
微信公众平台 HTML → Markdown 转换器。

用法:
  python wechat2md.py article.html              # 单文件
  python wechat2md.py *.html                     # 批量
  python wechat2md.py --dir ./wechat_exports/    # 整个目录

输出：同目录同名 .md 文件，包含标题、原文链接、作者、正文。
适用于：从浏览器"另存为"的微信文章 HTML，或批量导出的微信文章。
依赖：beautifulsoup4, html2text, lxml
"""
import sys, re, os, argparse
from bs4 import BeautifulSoup
from html2text import HTML2Text
from pathlib import Path


def convert(html_path: str) -> str:
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    # 标题
    title_tag = soup.find("meta", property="og:title")
    title = title_tag["content"] if title_tag else os.path.splitext(os.path.basename(html_path))[0]

    # 正文
    content = soup.find("div", id="js_content")
    if not content:
        content = soup.find("div", class_="rich_media_content")
    if not content:
        raise ValueError("未找到文章正文（#js_content / .rich_media_content）")

    # 修复微信懒加载图片：data-src → src
    for img in content.find_all("img"):
        data_src = img.get("data-src", "")
        if data_src:
            img["src"] = data_src

    # 清理隐藏元素和微信自定义标签
    for tag in content.find_all(["script", "style"]):
        tag.decompose()
    for tag in content.find_all(style=re.compile(r"display\s*:\s*none|visibility\s*:\s*hidden")):
        tag.decompose()
    for tag in content.find_all(["mp-common-profile", "mp-common-clipboard", "mp-common-miniprogram"]):
        tag.unwrap()

    # HTML → Markdown
    h = HTML2Text()
    h.body_width = 0
    h.protect_links = True
    h.mark_code = True
    md = h.handle(str(content)).strip()
    md = re.sub(r"\n{3,}", "\n\n", md)
    # 去除文末赞/在看行
    md = re.sub(r"^__\s*\n\s*\S+\s*\n\s*，赞\s*\d+\s*\n\s*\n\s*", "", md, count=1)

    # 作者
    author_tag = soup.find(string=re.compile(r"var nickname"))
    author = "未知"
    if author_tag:
        m = re.search(r'var nickname = htmlDecode\("(.+?)"\)', author_tag.string or "")
        if m:
            author = m.group(1)

    # 原文链接（从 saved from url 注释提取）
    url_match = re.search(r"saved from url=\(.+?\)(.+?)\s", str(soup), re.IGNORECASE)
    source_url = url_match.group(1).strip() if url_match else ""

    # 组装输出
    out = f"# {title}\n\n"
    if source_url:
        out += f"> 原文: {source_url}\n"
    out += f"> 作者: {author}\n\n"
    out += md

    out_path = os.path.splitext(html_path)[0] + ".md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)

    return out_path


def main():
    parser = argparse.ArgumentParser(description="微信公众平台 HTML → Markdown")
    parser.add_argument("paths", nargs="*", help="HTML 文件路径（支持通配符）")
    parser.add_argument("--dir", help="处理目录下所有 .html 文件")
    args = parser.parse_args()

    files = []
    if args.dir:
        files = sorted(Path(args.dir).glob("*.html"))
    else:
        files = args.paths

    if not files:
        parser.print_help()
        sys.exit(1)

    success = 0
    for path in files:
        path_str = str(path)
        if not os.path.isfile(path_str):
            print(f"跳过: {path_str} (文件不存在)")
            continue
        try:
            out = convert(path_str)
            print(f"OK  {path_str} → {out}")
            success += 1
        except Exception as e:
            print(f"ERR {path_str}: {e}")

    print(f"\n完成: {success}/{len(files)}")


if __name__ == "__main__":
    main()
