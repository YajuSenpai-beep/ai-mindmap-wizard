# 知识图谱中间表示

> 从 llmapper-skill 的 RDF 生成层提炼。在「文本」和「可视化」之间增加一个结构化中间层。

## 为什么需要中间表示？

当前管道：`文本 → AI生成Markdown → 导入XMind`

问题：Markdown 是**线性层级**，但真实知识是**网状结构**。引入中间表示层：

```
文本 → 概念提取 → 关系建模 → 知识图谱 → 多种可视化输出
         ↑            ↑           ↑
      概念节点      边/关系    可导出为:
                              Markdown / Mermaid / DrawIO / XMind / Obsidian
```

## 概念提取

### 从文本中提取节点

```
输入文本 → AI 识别:
  1. 核心概念（名词、术语、主题）
  2. 属性（概念的量化/定性特征）
  3. 实例（概念的具体案例）
```

**提示词模板**：

```
请从以下文本中提取所有关键概念，以 JSON 格式输出：

{
  "concepts": [
    {
      "id": "c1",
      "name": "概念名",
      "type": "core|attribute|instance",
      "definition": "一句话定义",
      "source": "源文档位置"
    }
  ]
}

规则：
- 每个概念必须能在原文中找到对应
- core=核心主题，attribute=量化的属性，instance=具体例子
- 如果概念间有明显的层级关系，标记 parent_id
```

## 关系建模

### 关系类型

| 关系 | 含义 | 示例 |
|------|------|------|
| `contains` | 包含/组成 | 「五星心法」→ contains →「结构化」 |
| `precedes` | 前置/顺序 | 「结构化」→ precedes →「逻辑化」 |
| `depends_on` | 依赖 | 「放射化」→ depends_on →「逻辑化」 |
| `example_of` | 举例 | 「鱼骨图」→ example_of →「分析工具」 |
| `conflicts_with` | 冲突 | — |
| `same_as` | 同义 | — |

### JSON 输出格式

```json
{
  "nodes": [
    {"id": "n1", "label": "五星心法", "type": "framework"},
    {"id": "n2", "label": "结构化", "type": "step"},
    {"id": "n3", "label": "逻辑化", "type": "step"}
  ],
  "edges": [
    {"from": "n1", "to": "n2", "relation": "contains"},
    {"from": "n2", "to": "n3", "relation": "precedes"}
  ]
}
```

## 从知识图谱导出多种格式

### 导出为 Markdown (思维导图)

```python
def kg_to_markdown(nodes, edges):
    """知识图谱 → Markdown 层级"""
    root = find_root(nodes, edges)  # 没有入边的节点
    lines = [f"# {root['label']}"]
    for child in get_children(root, edges):
        lines.append(f"## {child['label']}")
        for grandchild in get_children(child, edges):
            lines.append(f"### {grandchild['label']}")
    return "\n".join(lines)
```

### 导出为 Mermaid

```python
def kg_to_mermaid(nodes, edges):
    """知识图谱 → Mermaid mindmap"""
    lines = ["mindmap", f"  root(({find_root(nodes, edges)['label']}))"]
    for edge in edges:
        indent = "    " * (get_depth(edge["from"]) + 1)
        lines.append(f"{indent}{edge['to']}")
    return "\n".join(lines)
```

### 导出为 DrawIO XML

参见 [DrawIO 生成管道](../ai-pipeline/drawio-generation.md)。

### 导出为 Obsidian Canvas

参见 [Obsidian Canvas 指南](../software/obsidian-canvas-guide.md)。

## 实践中何时使用

| 场景 | 是否使用中间层 | 原因 |
|------|:---:|------|
| 简单文本 → 导图 | ❌ 直接用 Markdown | 线性层级已足够 |
| 多文档知识融合 | ✅ | 需要处理重叠/冲突/互补概念 |
| 复杂领域建模 | ✅ | 网状关系 → 中间层 → 选择最佳可视化 |
| 研究综述 | ✅ | 多源概念→知识图谱→导出多种图 |

## 关联

- [多视角分析](multi-perspective.md) — 从不同维度分析同一知识图谱
- [子母图技法](mother-child-diagram.md) — 用知识图谱自动生成子母图结构
- [DrawIO 生成管道](../ai-pipeline/drawio-generation.md) — 知识图谱 → DrawIO
