# Excalidraw 手绘风格图表指南

> 从 axton-obsidian-visual-skills 提炼。Excalidraw 是手绘风格的矢量图工具，适合创意/非正式场景。

## Excalidraw 适合什么？

| 适合 | 不适合 |
|------|--------|
| 头脑风暴草稿 | 正式汇报材料 |
| 团队白板讨论 | 需要精确对齐的图表 |
| 概念草图/原型 | 复杂网络拓扑 |
| 教学/演示的非正式配图 | 对视觉统一性要求高的文档 |

## Excalidraw JSON 结构

```json
{
  "type": "excalidraw",
  "version": 2,
  "elements": [
    {
      "id": "node-1",
      "type": "rectangle",
      "x": 100, "y": 100,
      "width": 200, "height": 60,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "roughness": 1,
      "opacity": 100
    },
    {
      "id": "node-2",
      "type": "text",
      "x": 120, "y": 115,
      "width": 160, "height": 30,
      "text": "中心主题",
      "fontSize": 20,
      "fontFamily": 1
    },
    {
      "id": "arrow-1",
      "type": "arrow",
      "x": 300, "y": 130,
      "width": 100, "height": 0,
      "points": [[0, 0], [100, 0]],
      "strokeColor": "#1e1e1e",
      "strokeWidth": 2,
      "roughness": 1
    }
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff"
  }
}
```

## AI 生成 Excalidraw 的提示词

```
你是一位 Excalidraw 图表生成专家。

请根据以下内容生成一个思维导图的 Excalidraw JSON。
要求：
1. 使用手绘风格 (roughness: 1)——这是 Excalidraw 的标志性风格
2. 矩形节点 + 箭头连线
3. 颜色：中心节点 #a5d8ff (浅蓝)，一级分支 #b2f2bb (浅绿)，二级 #ffec99 (浅黄)
4. 字体大小：中心 20pt，分支 16pt，叶子 14pt
5. 元素间距：水平 250px，垂直 100px
6. 输出纯 JSON，可直接粘贴到 excalidraw.com 或 Obsidian Excalidraw 插件

内容：[粘贴你的结构化内容]
```

## 从 Markdown 到 Excalidraw

### 映射规则

```
Markdown 层级          →  Excalidraw 元素
#  中心主题            →  rectangle + text (蓝色，20pt)
## 主分支               →  rectangle + text (绿色，16pt) + arrow from 中心
### 子分支              →  rectangle + text (黄色，14pt) + arrow from 主分支
-  叶子节点            →  text (灰色，12pt) + arrow from 子分支
```

## Toolchain 集成

```bash
# 方式1: 在线使用 excalidraw.com → 粘贴 JSON → 编辑
# 方式2: Obsidian Excalidraw 插件 → 直接打开 .excalidraw 文件
# 方式3: VS Code Excalidraw 扩展 → 编辑 .excalidraw.json
```

## 关联

- [Obsidian Canvas 指南](obsidian-canvas-guide.md) — Obsidian 中的另一种可视化格式
- [draw.io 指南](drawio-guide.md) — 正式技术图
- [XMind 指南](xmind-guide.md) — 专业思维导图
