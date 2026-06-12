#!/usr/bin/env python3
"""
LLM-Based OCR Correction — use AI to fix common OCR errors in extracted text.

Supports: Claude API, OpenAI API, or local mode (prints prompts for manual use).

Usage:
  # With API key (auto-correct)
  python llm_correct.py <ocr_json_or_text> --provider claude --api-key sk-xxx

  # Without API key (prints correction prompts for manual use)
  python llm_correct.py <ocr_json_or_text> --manual
"""
import os, sys, json, argparse
from pathlib import Path


CORRECTION_PROMPT = """你是一位 OCR 文本校对专家。请纠正以下 OCR 识别结果中的明显错误。

规则：
1. 修正形近字错误（如：己→已、入→人、日→目、未→末）
2. 修正明显的断句错误和多余空格
3. 保留原文的专业术语、数字、标点
4. 不要改变原意，不要添加新内容
5. 如果某处无法确定是否正确，保持原文不动
6. 只输出纠正后的文本，不要任何额外解释

OCR 原文：
---
{text}
---

纠正后："""


def correct_with_claude(text, api_key, model="claude-fable-5"):
    """Use Claude API to correct OCR text."""
    import urllib.request
    import urllib.error

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": model,
        "max_tokens": min(len(text) * 2, 4000),
        "messages": [
            {"role": "user", "content": CORRECTION_PROMPT.format(text=text)}
        ],
    }

    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        return f"[API Error: {e.code} {e.reason}]"
    except Exception as e:
        return f"[Error: {e}]"


def correct_with_openai(text, api_key, model="gpt-4o-mini"):
    """Use OpenAI API to correct OCR text."""
    import urllib.request
    import urllib.error

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "max_tokens": min(len(text) * 2, 4000),
        "messages": [
            {"role": "user", "content": CORRECTION_PROMPT.format(text=text)}
        ],
    }

    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        return f"[API Error: {e.code} {e.reason}]"
    except Exception as e:
        return f"[Error: {e}]"


def correct_text(text, provider=None, api_key=None, model=None):
    """Correct OCR text using specified provider. If no provider, return prompt for manual use."""
    if not provider:
        return None, CORRECTION_PROMPT.format(text=text[:2000])

    if provider == 'claude':
        return correct_with_claude(text, api_key, model or "claude-fable-5"), None
    elif provider == 'openai':
        return correct_with_openai(text, api_key, model or "gpt-4o-mini"), None
    else:
        raise ValueError(f"Unknown provider: {provider}")


def correct_ocr_json(json_path, provider=None, api_key=None, model=None, dry_run=False):
    """Correct all text entries in an OCR JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    manual_prompts = []
    corrected_count = 0

    for item in items:
        text = item.get('text', '')
        if not text or len(text) < 50:
            continue

        if dry_run or not provider:
            # Collect prompts for manual use
            _, prompt = correct_text(text[:2000])
            if prompt:
                manual_prompts.append({'file': item.get('file', '?'), 'prompt': prompt})
        else:
            corrected, _ = correct_text(text, provider, api_key, model)
            if corrected and not corrected.startswith('[Error'):
                item['text'] = corrected
                corrected_count += 1

    if dry_run or not provider:
        return manual_prompts, items

    # Save corrected JSON
    if corrected_count > 0:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

    return corrected_count, items


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LLM-based OCR text correction')
    parser.add_argument('input', help='OCR JSON file or plain text')
    parser.add_argument('--provider', choices=['claude', 'openai'], help='AI provider')
    parser.add_argument('--api-key', help='API key')
    parser.add_argument('--model', help='Model name')
    parser.add_argument('--manual', action='store_true', help='Print correction prompts for manual use')
    args = parser.parse_args()

    input_path = Path(args.input)
    if input_path.suffix == '.json' and input_path.exists():
        provider = args.provider if not args.manual else None
        result, _ = correct_ocr_json(str(input_path), provider, args.api_key, args.model,
                                     dry_run=args.manual)
        if args.manual:
            print(f"\n=== {len(result)} correction prompts ===\n")
            for i, r in enumerate(result, 1):
                print(f"--- Prompt {i}: {r['file']} ---")
                print(r['prompt'])
                print()
        else:
            print(f"Corrected: {result} items")
    else:
        # Plain text input
        text = input_path.read_text(encoding='utf-8') if input_path.exists() else args.input
        corrected, prompt = correct_text(text, args.provider if not args.manual else None,
                                         args.api_key, args.model)
        if args.manual and prompt:
            print(prompt)
        elif corrected:
            print(corrected)
