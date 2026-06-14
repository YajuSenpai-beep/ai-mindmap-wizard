# 质量基准数据集

10 个「输入-期望输出」对，用于评测 AI 管道质量。

## 评测维度

- 结构完整性 — #/##/### 层级合理
- 信息密度 — 提取了关键概念
- 简洁性 — 每节点 ≤15 字
- 层级平衡 — 无过深或过浅分支
- 格式有效性 — 合法 Markdown

## 使用

```bash
python tools/eval.py --input tests/benchmark/ --models claude,deepseek,gpt
```
