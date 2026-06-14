# 本地小模型：离线文本→图表

> 从 Qwen3.5-0.8B Mermaid 生成器提炼。不依赖云端 LLM，在本地运行小型专用模型做 text→diagram。

## 为什么需要本地模型？

| 方案 | 优点 | 缺点 |
|------|------|------|
| 云端 LLM (Claude/GPT) | 最灵活、质量最高 | 需网络、有费用、可能泄露数据 |
| **本地小模型** | 离线、免费、数据不外泄 | 仅限特定任务 |
| 我们现有的提示词 | 工具无关、任何 LLM | 仍需一个 LLM |

**本地小模型** 适合：敏感数据处理、批量自动化、无网络环境。

## Qwen3.5 Mermaid 生成器

[HuggingFace: SpongeBOB9684/qwen3.5-0.8b-mermaid-generator](https://huggingface.co/SpongeBOB9684/qwen3.5-0.8b-mermaid-generator)

### 技术规格

| 参数 | 值 |
|------|-----|
| 基础模型 | Qwen/Qwen3.5-0.8B |
| 微调方法 | LoRA |
| 训练数据 | 9,913 个 GitHub Mermaid 示例 |
| 支持类型 | Flowchart(54.7%) / Sequence(15.1%) / Class(10.4%) / State / ER / Gantt / MindMap / Pie / Git |
| 模型大小 | ~1.5GB (0.8B params) |

### 本地部署

```bash
# 安装
pip install transformers torch

# 运行推理
python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    'SpongeBOB9684/qwen3.5-0.8b-mermaid-generator'
)
tokenizer = AutoTokenizer.from_pretrained(
    'SpongeBOB9684/qwen3.5-0.8b-mermaid-generator'
)

prompt = '生成一个描述用户登录流程的 Mermaid 思维导图'
inputs = tokenizer(prompt, return_tensors='pt')
outputs = model.generate(**inputs, max_length=500)
print(tokenizer.decode(outputs[0]))
"
```

### 在我们的管道中集成

```
用户输入文本
  ↓
[选择模式]
  ├── 质量优先 → 走通道 A 用云端 LLM
  └── 离线/批量 → 本地 Qwen 模型生成 Mermaid
       ↓
  mermaid_fixer.py 修复语法
       ↓
  multi_export.py 导出多格式
```

### Python 封装

```python
# tools/local_diagram.py — 本地模型 text→diagram
import subprocess

def generate_diagram_local(text: str, diagram_type: str = "mindmap"):
    """使用本地 Qwen 模型生成 Mermaid 图表"""
    result = subprocess.run(
        ["python", "-c", f"""
from transformers import pipeline
gen = pipeline("text-generation", model="SpongeBOB9684/qwen3.5-0.8b-mermaid-generator")
output = gen("生成一个{diagram_type}: {text[:500]}", max_length=500)
print(output[0]['generated_text'])
"""],
        capture_output=True, text=True, timeout=60
    )
    return result.stdout
```

## 其他本地模型选项

| 模型 | 大小 | 专长 |
|------|------|------|
| Qwen Mermaid Gen | 0.8B | Mermaid 图表 |
| Ollama + CodeLlama | 7B | 通用代码生成含 Mermaid |
| Ollama + DeepSeek-Coder | 1.3B-33B | 代码/图表生成 |

## 关联

- [Mermaid 流程图](../ai-pipeline/mermaid-flowchart.md) — Mermaid 语法速查
- [Mermaid 修复器](../../tools/mermaid_fixer.py) — 修复本地模型可能产生的语法错误
