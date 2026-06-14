# D3.js 交互式可视化管道

> 从 NTCoding/claude-skillz data-visualization 提炼。当 Mermaid 不够时——自定义 SVG 交互。

## 什么时候用 D3.js 而非 Mermaid？

| 需求 | Mermaid | D3.js |
|------|:---:|:---:|
| 快速流程图 | ✅ 最佳 | ⚠️ 杀鸡用牛刀 |
| 思维导图 | ✅ mindmap | ✅ 更灵活的布局 |
| 网络关系图 | ❌ | ✅ force-directed |
| 数据驱动的动态图表 | ❌ | ✅ 专为此设计 |
| 出版物级自定义样式 | ❌ | ✅ 完全控制 |
| 地理可视化 | ❌ | ✅ GeoJSON+D3 |
| 需要交互（缩放/拖拽/筛选） | ❌ | ✅ 原生支持 |

## 渲染引擎选择

| 技术 | 适用场景 | 元素上限 |
|------|---------|---------|
| SVG | 交互、缩放、少元素 | < 1,000 |
| Canvas | 大量数据点 | 1,000 – 10,000 |
| WebGL | 大规模实时可视化 | > 10,000 |

## 从 Markdown 到 D3 思维导图

### 模板

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Interactive Mindmap</title></head>
<body>
<div id="mindmap"></div>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
// 从 Markdown 层级数据生成 D3 思维导图
const data = {
  name: "中心主题",
  children: [
    { name: "分支A", children: [
      { name: "子分支A1" },
      { name: "子分支A2" }
    ]},
    { name: "分支B", children: [
      { name: "子分支B1" }
    ]}
  ]
};

const width = 1200, height = 800;
const svg = d3.select("#mindmap").append("svg")
  .attr("width", width).attr("height", height);

const g = svg.append("g").attr("transform", "translate(80,400)");

const tree = d3.tree().size([height - 100, width - 200]);
const root = d3.hierarchy(data);
tree(root);

// 画连线
g.selectAll(".link")
  .data(root.links())
  .join("path")
  .attr("class", "link")
  .attr("d", d3.linkHorizontal()
    .x(d => d.y).y(d => d.x))
  .attr("fill", "none").attr("stroke", "#999");

// 画节点
const node = g.selectAll(".node")
  .data(root.descendants())
  .join("g")
  .attr("transform", d => `translate(${d.y},${d.x})`);

node.append("circle").attr("r", 5).attr("fill", "#1ba1e2");
node.append("text").attr("dx", 10).attr("dy", 4)
  .text(d => d.data.name).style("font-size", "14px");
</script>
</body>
</html>
```

## AI 生成 D3 的提示词

```
你是一位 D3.js 数据可视化专家。

请根据以下层级数据生成一个交互式 D3.js 思维导图。
要求：
1. 使用 d3.tree() 水平布局
2. 节点颜色按层级：根=#1ba1e2, L1=#4CAF50, L2=#FF9800, L3=#9C27B0
3. 添加缩放 (d3.zoom) 和拖拽 (d3.drag) 交互
4. 节点悬停高亮 + tooltip 显示详情
5. 输出完整可运行的 HTML 文件

数据：[以 JSON 提供层级结构]
```

## 在我们的管道中集成

```
用户数据 → multi_export.py（生成 .html markmap 版）
         → 或 D3.js 模板（生成高交互版）
         → 两个都提供，用户选择：
           - markmap: 快速美观，零定制
           - D3.js:  完全交互，可定制
```

## 感知准确性层级

选择可视化编码时，按此次序（从最准确到最不准确）：

```
位置 (Position)        → 散点图 X/Y 轴
长度 (Length)          → 条形图的条高
角度 (Angle)           → 饼图的扇区角度
面积 (Area)            → 气泡图
饱和度 (Saturation)    → 热力图
颜色 (Color Hue)       → 分类标签（准确度最低）
```

**原则**：最重要的数据用位置或长度编码。不要用颜色表示精确数值（因为 8% 男性色盲，且人对颜色的感知非线性）。

## 关联

- [Mermaid 流程图](mermaid-flowchart.md) — 简单场景首选
- [Draw.io MCP 生成](drawio-mcp-guide.md) — 专业图表的另一路径
- [Tufte 可视化原则](../methodology/tufte-principles.md) — D3.js 图表的设计依据
