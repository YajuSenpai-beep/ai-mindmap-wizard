#!/usr/bin/env python3
"""自动评估管线 — 同一输入跑多模型，比较导图质量并自动选优。

使用:
  python tools/eval.py --input tests/benchmark/ --models claude,deepseek,gpt
  python tools/eval.py --input doc.md --single
"""

import argparse
import json
import re
from pathlib import Path
from _common import logger


# === 评分维度 ===
SCORE_DIMS = {
    "structure_completeness": "结构完整性 — #/##/### 层级是否合理",
    "information_density": "信息密度 — 是否提取了关键概念而非泛泛而谈",
    "conciseness": "简洁性 — 每个节点 ≤15 字",
    "depth_balance": "层级平衡 — 是否有过深或过浅的分支",
    "format_validity": "格式有效性 — 是否为合法的 Markdown",
}


def score_markdown(md_text: str) -> dict:
    """对 Markdown 导图做自动评分。"""
    lines = [l.strip() for l in md_text.split("\n") if l.strip()]
    scores = {}

    # 结构完整性
    h1 = sum(1 for l in lines if l.startswith("# "))
    h2 = sum(1 for l in lines if l.startswith("## "))
    h3 = sum(1 for l in lines if l.startswith("### "))
    leaf = sum(1 for l in lines if l.startswith("- "))
    scores["structure_completeness"] = min(10, (h1 * 4 + h2 * 2 + h3 * 1 + leaf * 0.5) / 2)

    # 信息密度 — 非空/非标题行的占比
    content_lines = [l for l in lines if not l.startswith("#")]
    scores["information_density"] = min(10, len(content_lines) / max(1, len(lines)) * 10)

    # 简洁性 — 节点长度
    node_texts = [re.sub(r'^#+\s*', '', l) for l in lines if re.match(r'^#+\s', l)]
    overlong = sum(1 for t in node_texts if len(t) > 20)
    scores["conciseness"] = max(0, 10 - overlong)

    # 层级平衡 — h2 下的平均 h3 数
    scores["depth_balance"] = min(10, (h3 / max(1, h2)) * 3 + 5)

    # 格式有效性
    scores["format_validity"] = 10 if (h1 >= 1 and "```" not in md_text[:50]) else 5

    scores["total"] = sum(scores.values()) / len(SCORE_DIMS)
    return scores


def run_benchmark(benchmark_dir: str, models: list[str]) -> dict:
    """对 benchmark 数据集跑评估。"""
    results = {}
    for case_file in sorted(Path(benchmark_dir).glob("*.txt")):
        case_name = case_file.stem
        content = case_file.read_text(encoding="utf-8")
        expected = None
        expected_file = case_file.with_suffix(".expected.md")
        if expected_file.exists():
            expected = expected_file.read_text(encoding="utf-8")

        case_results = {}
        for model in models:
            # 模拟不同模型的输出（实际应调用 API）
            # 这里用启发式模拟：不同模型 = 不同提取策略
            md = simulate_model_output(content, model)
            scores = score_markdown(md)
            case_results[model] = {"scores": scores, "markdown": md[:200]}

        case_results["_expected"] = score_markdown(expected) if expected else None
        results[case_name] = case_results

    return results


def simulate_model_output(text: str, model: str) -> str:
    """模拟不同模型的输出策略（实际使用时替换为 API 调用）。"""
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    if model == "claude":
        # Claude 风格：结构化、注重层级
        md = ["# 思维导图"]
        for i, line in enumerate(lines[:20]):
            if len(line) < 30:
                md.append(f"## {line}")
            elif len(line) < 80:
                md.append(f"### {line[:50]}")
            else:
                md.append(f"- {line[:60]}")

    elif model == "deepseek":
        # DeepSeek 风格：全面、细节丰富
        md = ["# 内容分析"]
        for i, line in enumerate(lines[:25]):
            if i < 5:
                md.append(f"## {line[:40]}")
            else:
                md.append(f"### {line[:50]}")

    else:  # gpt / default
        md = ["# 要点总结"]
        for i, line in enumerate(lines[:15]):
            md.append(f"## {line[:40]}")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="多模型导图质量自动评估")
    parser.add_argument("--input", "-i", help="benchmark 目录 或 单个文件")
    parser.add_argument("--models", "-m", default="claude,deepseek,gpt", help="要比较的模型 (逗号分隔)")
    parser.add_argument("--single", action="store_true", help="单文件模式")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    models = [m.strip() for m in args.models.split(",")]

    if args.single and args.input:
        content = Path(args.input).read_text(encoding="utf-8")
        logger.info(f"📊 单文件评估: {args.input}\n")
        for model in models:
            md = simulate_model_output(content, model)
            scores = score_markdown(md)
            logger.info(f"  [{model:12s}] total={scores['total']:.1f}  {json.dumps(scores, ensure_ascii=False)}")
        return 0

    if args.input:
        results = run_benchmark(args.input, models)
        if args.json:
            logger.info(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for case, case_results in results.items():
                logger.info(f"\n📋 {case}")
                for model, r in case_results.items():
                    if model.startswith("_"):
                        continue
                    logger.info(f"  [{model:12s}] score={r['scores']['total']:.1f}")
    else:
        # 演示模式
        demo = "人工智能正在改变我们的工作方式。从自动化到智能决策，AI的应用越来越广泛。企业需要理解AI的潜力和局限性。"
        logger.info("🧪 演示评估 (无 benchmark 目录，使用示例文本)\n")
        for model in models:
            md = simulate_model_output(demo, model)
            scores = score_markdown(md)
            logger.info(f"  [{model:12s}] total={scores['total']:.1f}")
        logger.info("\n💡 使用 --input tests/benchmark/ 指向 benchmark 数据集进行完整评估")

    return 0


if __name__ == "__main__":
    exit(main())
