# 商业 AI 图表工具对比

> Miro / Lucidchart / Eraser — 商业工具 AI 功能矩阵与 API 集成分析。

## AI 功能对比

| 功能 | Miro | Lucidchart | Eraser | 我们的 Skill |
|------|:---:|:---:|:---:|:---:|
| AI 模型 | GPT-5.4 / Claude Opus 4.6 / Gemini 2.5 Pro | 未公开 | DiagramGPT | 工具无关 (任何 LLM) |
| 文本→思维导图 | ✅ | ✅ | ✅ | ✅ |
| 文本→流程图 | ✅ | ✅ | ✅ | ✅ |
| 手绘→数字图 | ✅ Claude Sonnet 4.6 | ❌ | ❌ | ⚠️ 通道 F OCR |
| 草图→原型 | ✅ | ❌ | ❌ | ❌ |
| 便签→数字化 | ✅ 拍照识别 | ❌ | ❌ | ❌ |
| 实时协作 | ✅ 无限人数 | ✅ | ❌ | ❌ |
| 图表即代码 | ❌ | ❌ | ✅ D2/Mermaid | ✅ |
| 自托管 | ❌ SaaS | ❌ SaaS | ❌ SaaS | ✅ 本地 |
| 价格 | $10/人/月 | $12/人/月 | 免费版可用 | 免费 |

## API 集成对比

### Miro

```javascript
// Miro Developer Platform — REST API + Web SDK
// 程序化创建思维导图节点
const miro = new Miro({ accessToken: '...' });
const board = await miro.boards.create({ name: 'AI 生成的导图' });
await board.addMindMap({
  rootNodeText: '中心主题',
  items: [
    { text: '分支A', level: 1 },
    { text: '分支B', level: 1 }
  ]
});
```

### Lucidchart

```python
# Lucid Developer API — OAuth 2.0 + REST
# 将数据导入为图表
import requests
resp = requests.post(
    "https://api.lucid.co/documents",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "title": "AI Generated Diagram",
        "data": "..."  # CSV 或 JSON
    }
)
```

### Eraser

```bash
# Eraser DiagramGPT — 图表即代码
# 通过 ChatGPT/Claude 生成 D2 代码 → 复制到 eraser.io 渲染
```

## 何时用商业工具，何时用我们的 Skill

| 场景 | 推荐 | 原因 |
|------|------|------|
| 团队实时协作白板 | Miro | 多人同时编辑 |
| 企业 Atlassian 生态 | Lucidchart | 深度 Jira/Confluence 集成 |
| 图表即代码版本控制 | **我们的 Skill** + Eraser | Git 中管理图表源码 |
| 私有化/离线/免费 | **我们的 Skill** | 完全本地 |
| 展示级交互图表 | Miro | Sidekicks AI 代理 |
| 方法论指导 | **我们的 Skill** | 唯一有思维训练内容的 |

## 关联

- [Draw.io MCP 指南](../ai-pipeline/drawio-mcp-guide.md) — 免费的专业图方案
- [Mermaid 流程图](../ai-pipeline/mermaid-flowchart.md) — 图表即代码基础
