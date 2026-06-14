# DrawIO 图表生成管道

> 从 multi-chart-draw-skills 的 DrawIO 引擎提炼。Mermaid → draw.io 的完整转换方法。

## 为什么需要 DrawIO 生成？

- Mermaid 适合流程图/序列图，但系统架构图/网络拓扑/UML 用 DrawIO 更专业
- DrawIO 的 `.drawio` 格式是开放 XML，可以程序化生成
- 结合已有的 drawio-guide.md 操作知识，补齐生成端

## 方法一：Mermaid → DrawIO 导入（推荐）

```
① AI 生成 Mermaid 代码
② 保存为 .mmd 文件
③ draw.io → 排列 → 高级 → Mermaid → 粘贴代码 → 导入
④ 在 draw.io 中调整布局和样式
```

**优点**：AI 生成部分不用变，利用现有 Mermaid 管道。

## 方法二：DrawIO XML 直接生成

### 最小 DrawIO XML 模板

```xml
<mxfile host="claude" modified="2026-01-01T00:00:00.000Z" version="21.0.0">
  <diagram name="Page-1" id="diagram-1">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10"
      guides="1" tooltips="1" connect="1" arrows="1"
      fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- 节点放在这里 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 思维导图节点模板

```xml
<!-- 中心节点 -->
<mxCell id="2" value="中心主题" style="rounded=1;whiteSpace=wrap;html=1;
  fillColor=#1ba1e2;fontColor=#ffffff;strokeColor=#006EAF;fontSize=18;"
  vertex="1" parent="1">
  <mxGeometry x="360" y="40" width="200" height="60" as="geometry" />
</mxCell>

<!-- 分支节点 -->
<mxCell id="3" value="分支A" style="rounded=1;whiteSpace=wrap;html=1;
  fillColor=#dae8fc;strokeColor=#6c8ebf;"
  vertex="1" parent="1">
  <mxGeometry x="160" y="160" width="160" height="50" as="geometry" />
</mxCell>

<!-- 连线 -->
<mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;exitX=0.5;
  exitY=1;entryX=0.5;entryY=0;endArrow=block;"
  edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### AI 生成 XML 的提示词

```
你是一位 DrawIO XML 生成专家。

请根据以下内容生成一个思维导图的 .drawio XML 文件。
要求：
1. 根节点 id="2"，分支从 id="3" 开始递增
2. 使用 mxCell 定义每个节点和连线
3. 节点位置 (x, y) 要合理排布——同级节点水平排列，子节点垂直排列
4. 颜色：中心主题用深色(如 #1ba1e2)，分支用浅色(如 #dae8fc)
5. 输出纯粹的 XML，包裹在 mxfile 根元素中
6. 生成后保存为 .drawio 文件，用 draw.io 打开

内容：[粘贴你的结构化内容]
```

## 方法三：Python 程序化生成

```python
# tools/generate_drawio.py 的简化逻辑

def generate_mindmap_drawio(structure: dict, output_path: str):
    """从层级 dict 生成 DrawIO XML 思维导图"""
    cells = []
    edge_id = 100

    def add_node(parent_id, node_data, x, y, level=0):
        nonlocal edge_id
        node_id = len(cells) + 2
        color = ["#1ba1e2", "#dae8fc", "#d5e8d4", "#fff2cc"][level % 4]
        cells.append(f'''
        <mxCell id="{node_id}" value="{node_data['text']}"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor={color};"
          vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="160" height="40" as="geometry" />
        </mxCell>''')
        cells.append(f'''
        <mxCell id="{edge_id}" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;"
          edge="1" parent="1" source="{parent_id}" target="{node_id}">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>''')
        edge_id += 1
        for i, child in enumerate(node_data.get("children", [])):
            add_node(node_id, child, x + 200, y + i * 60, level + 1)

    add_node(0, structure, 100, 40)

    xml = f'''<mxfile host="claude">
  <diagram name="Mindmap" id="d1">
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        {''.join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    Path(output_path).write_text(xml.strip())
```

## 关联

- [draw.io 操作指南](../software/drawio-guide.md) — 导入后编辑和美化
- [Mermaid 流程图](mermaid-flowchart.md) — 轻量替代方案
- [工具对照表](../software/cross-tool-mapping.md) — 何时选 DrawIO vs Mermaid
