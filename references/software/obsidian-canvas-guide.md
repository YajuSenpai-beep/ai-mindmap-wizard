# Obsidian Canvas 思维导图指南

> 从 axton-obsidian-visual-skills 和 claude-canvas 提炼。Obsidian Canvas 是自由布局的交互式画布。

## Canvas vs XMind vs draw.io

| | Obsidian Canvas | XMind | draw.io |
|------|:---:|:---:|:---:|
| 自由布局 | ✅ 任意拖拽 | ⚠️ 受限于布局算法 | ✅ |
| 双向链接 | ✅ `[[Wiki Links]]` | ❌ | ❌ |
| 本地文件 | ✅ 纯 JSON | ❌ 专有格式 | ⚠️ XML |
| 层级结构 | ⚠️ 需手动组织 | ✅ 原生 | ⚠️ 需手动 |
| 导出格式 | PNG | PNG/PDF/SVG/OPML | PNG/SVG/PDF/HTML |
| 适合场景 | 知识管理+可视化 | 专业导图制作 | 技术图/架构图 |

## Canvas JSON 格式

### 最小 Canvas 文件

```json
{
  "nodes": [
    {
      "id": "a1b2c3d4e5f6",
      "type": "text",
      "text": "# 中心主题",
      "x": 0, "y": 0,
      "width": 300, "height": 80,
      "color": "1"
    },
    {
      "id": "a1b2c3d4e5f7",
      "type": "text",
      "text": "## 分支A",
      "x": 400, "y": 0,
      "width": 250, "height": 60,
      "color": "4"
    }
  ],
  "edges": [
    {
      "id": "e1e2e3e4e5e6",
      "fromNode": "a1b2c3d4e5f6",
      "toNode": "a1b2c3d4e5f7",
      "fromSide": "right",
      "toSide": "left"
    }
  ]
}
```

### 6 种预设颜色

| color 值 | 视觉效果 |
|----------|---------|
| `"1"` | 深红 |
| `"2"` | 橙色 |
| `"3"` | 黄色 |
| `"4"` | 绿色 |
| `"5"` | 青色 |
| `"6"` | 紫色 |

## AI 生成 Canvas 的提示词

```
你是一位 Obsidian Canvas 专家。

请根据以下内容生成一个思维导图的 Canvas JSON 文件。
要求：
1. 中心节点放在 (0, 0)，type="text"
2. 分支节点水平排列（每级向右偏移 400px）
3. 同级节点垂直排列（每个间距 100px）
4. 节点宽度根据内容长度自适应（200-400px）
5. 使用 color "1"-"6" 按层级循环着色
6. 用 edges 数组连接所有父子节点
7. 输出纯 JSON，可直接保存为 .canvas 文件

内容：[粘贴你的结构化内容]
```

## 布局算法推荐

| 导图类型 | 布局 | 说明 |
|---------|------|------|
| 思维导图 | 中心节点在左，分支向右展开 | 标准布局 |
| 知识图谱 | radial (围绕中心) | 适合关系型概念网络 |
| 层级图 | top-down (grid) | 组织架构/分类 |
| 时间线 | left-to-right (linear) | 项目阶段/历史 |
| 对比图 | 双中心节点，左右对称 | SWOT/对比分析 |

## 导入导出

### 导入
- 将生成的 `.canvas` JSON 文件放入 Obsidian vault 任意位置
- 在 Obsidian 中打开即显示为交互式 Canvas

### 导出
- Canvas → 右键 → Export to image → PNG
- 第三方插件 → SVG/PDF

## 关联

- [XMind 指南](xmind-guide.md) — 专业思维导图
- [draw.io 指南](drawio-guide.md) — 技术图表
- [知识图谱中间表示](../methodology/knowledge-graph.md) — 知识图谱 → Canvas JSON 自动生成
