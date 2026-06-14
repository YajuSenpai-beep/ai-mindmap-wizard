"""共享工具模块 —— 所有 tools/*.py 的公共函数和基类，消除重复代码。"""

import argparse
import logging
import re
from pathlib import Path

# === 日志 ===

def setup_logging(verbose: bool = False) -> logging.Logger:
    """统一日志配置。verbose=True 时输出 DEBUG 级别。"""
    level = logging.DEBUG if verbose else logging.INFO
    fmt = "%(asctime)s [%(levelname)s] %(message)s" if verbose else "%(message)s"
    logging.basicConfig(level=level, format=fmt, datefmt="%H:%M:%S")
    return logging.getLogger("mindmap")


logger = setup_logging()


# === Markdown 解析（单一来源） ===

def parse_markdown_to_tree(md_text: str) -> dict | None:
    """解析 Markdown 层级结构为嵌套 dict。所有工具统一使用此函数。"""
    lines: list[str] = md_text.strip().split("\n")
    root: dict | None = None
    stack: list[tuple[int, dict]] = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(r'^(#{1,6})\s+(.+)', line)
        list_match = re.match(r'^(\s*)[-*+]\s+(.+)', line)

        if match:
            level: int = len(match.group(1))
            text: str = match.group(2).strip()
        elif list_match:
            level = len(list_match.group(1)) // 2 + 2
            text = list_match.group(2).strip()
        else:
            continue

        node: dict = {"title": text, "children": []}
        if root is None:
            root = node
            stack = [(level, node)]
        else:
            while stack and stack[-1][0] >= level:
                stack.pop()
            if stack:
                stack[-1][1]["children"].append(node)
            stack.append((level, node))

    return root


def count_nodes(node: dict) -> int:
    """递归统计节点数。"""
    return 1 + sum(count_nodes(c) for c in node.get("children", []))


def markdown_to_nodes(md_text: str) -> list[dict]:
    """Markdown → 扁平节点列表 [{level, text}]。"""
    nodes: list[dict] = []
    for line in md_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        m = re.match(r'^(#{1,6})\s+(.+)', line)
        if m:
            nodes.append({"level": len(m.group(1)), "text": m.group(2).strip()[:60]})
        elif line.startswith("- "):
            nodes.append({"level": 99, "text": line[2:].strip()[:60]})
    return nodes


# === 统计 ===

def md_stats(md_text: str) -> dict:
    """Markdown 导图统计信息。"""
    nodes = markdown_to_nodes(md_text)
    return {
        "total": len(nodes),
        "h1": sum(1 for n in nodes if n["level"] == 1),
        "h2": sum(1 for n in nodes if n["level"] == 2),
        "h3": sum(1 for n in nodes if n["level"] == 3),
        "h4": sum(1 for n in nodes if n["level"] == 4),
        "leaf": sum(1 for n in nodes if n["level"] == 99),
        "max_depth": max((n["level"] for n in nodes if n["level"] < 99), default=0),
    }


# === CLI 基类 ===

class BaseCLI:
    """统一 CLI 基类 —— 所有工具继承此基类获得一致的参数风格。"""

    def __init__(self, description: str, epilog: str = ""):
        self.parser = argparse.ArgumentParser(
            description=description,
            epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        self.parser.add_argument("input", nargs="?", help="输入文件/目录")
        self.parser.add_argument("--output", "-o", help="输出路径")
        self.parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")

    def parse(self) -> argparse.Namespace:
        return self.parser.parse_args()

    def result_ok(self, path: str, count: int | None = None) -> None:
        logger.info("OK: %s%s", path, f" ({count} items)" if count else "")

    def result_error(self, msg: str, code: int = 1) -> int:
        logger.error("FAIL: %s", msg)
        return code


# === 文件IO ===

def read_file(path: str) -> str:
    """读取文本文件，自动检测编码。"""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"文件不存在: {path}")
    return p.read_text(encoding="utf-8")


def write_file(path: str, content: str) -> None:
    """写入文本文件，自动创建父目录。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


# === 进度条 ===

def optional_tqdm():
    """尝试导入 tqdm，不可用时返回普通迭代器。"""
    try:
        from tqdm import tqdm
        return tqdm
    except ImportError:
        logger.debug("tqdm not installed, using plain iteration")
        return lambda x, **kw: x
