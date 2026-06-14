# 开源思维导图库对比

> markmap / mind-elixir / Mermaid / D3.js / jsMind 五大开源库选型指南。

## 核心对比

| 库 | 输入 | 输出 | 交互 | 自定义 | 大小 |
|------|------|------|:---:|:---:|------|
| [**markmap**](https://github.com/markmap/markmap) | Markdown | SVG/HTML 交互式 | ✅ 缩放/折叠 | ⚠️ | ~50KB |
| [**mind-elixir**](https://github.com/ssshooter/mind-elixir) | JSON 节点树 | Canvas 交互式 | ✅ 拖拽编辑 | ✅ | ~60KB |
| [**Mermaid**](https://github.com/mermaid-js/mermaid) | Mermaid 语法 | SVG 静态/交互 | ⚠️ 仅缩放 | ⚠️ | ~1MB |
| [**D3.js**](https://github.com/d3/d3) | 任意数据 | SVG/Canvas 完全控制 | ✅ | ✅ | ~250KB |
| [**jsMind**](https://github.com/hizzgdev/jsmind) | JSON / Markdown | Canvas/HTML | ✅ 拖拽编辑 | ✅ | ~80KB |

## 选型决策

| 需求 | 推荐库 | 原因 |
|------|--------|------|
| Markdown → 美观导图，零代码 | **markmap** | 一行 HTML 即可渲染 |
| 需要用户可拖拽编辑 | **mind-elixir** 或 **jsMind** | 原生支持节点拖拽 |
| 程序化生成 + 完全自定义 | **D3.js** | 无任何限制 |
| 技术图表 (非纯导图) | **Mermaid** | 多图表类型 |
| 嵌入已有 Web 应用 | **markmap** (轻量) | 最小依赖 |

## 在我们的管道中

```
multi_export.py 的 html 格式 → markmap (已内置)
  → 用户打开 .html 文件 = 交互式思维导图

如果用户需要可编辑 Web 导图：
  → 生成 JSON → mind-elixir 渲染
  → 拖拽调整节点 → 导出回 Markdown
```

## markmap 速用

```html
<!-- 最小示例：将 Markdown 渲染为交互式思维导图 -->
<script src="https://cdn.jsdelivr.net/npm/markmap-autoloader"></script>
<div class="markmap">
# 中心主题
## 分支A
### 子分支
## 分支B
</div>
```

## mind-elixir 速用

```javascript
// 从 JSON 数据渲染可拖拽编辑的思维导图
import MindElixir from 'mind-elixir';

const mind = new MindElixir({
  el: '#container',
  data: {
    nodeData: {
      id: 'root',
      topic: '中心主题',
      children: [
        { id: 'b1', topic: '分支A', direction: 'right' },
        { id: 'b2', topic: '分支B', direction: 'right' }
      ]
    }
  }
});
mind.init();
```

## 关联

- [D3.js 交互式管道](../ai-pipeline/d3-interactive.md) — D3.js 完整方案
- [多格式导出管线](../../tools/multi_export.py) — markmap 的 HTML 输出实现
