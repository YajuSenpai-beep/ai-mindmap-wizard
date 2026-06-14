# 思维导图 → 演示文稿

> Gamma.app 风格——把 Markdown 导图一键转为专业 PPT。

## 管道

```
Markdown 导图 (通道 A 输出)
  ↓ mindmap_to_ppt.py
.pptx 演示文稿（4 种预设配色）
  ↓
用 PowerPoint / WPS / Google Slides 打开编辑
```

## 转换规则

| Markdown | PPT 幻灯片 |
|----------|-----------|
| `# 标题` | 封面页（居中大字） |
| `## 分支` | 内容页标题 |
| `### 子分支` | 缩进项目符号 |
| `- 叶子` | 项目符号 |

## 四种配色方案

```bash
# 专业蓝 — 商务汇报
python mindmap_to_ppt.py notes.md -o report.pptx -c professional

# 创意橙 — 营销提案
python mindmap_to_ppt.py brain_dump.md -o pitch.pptx -c creative

# 极简灰白 — 学术演示
python mindmap_to_ppt.py research.md -o defense.pptx -c minimal

# 海洋蓝绿 — 技术分享
python mindmap_to_ppt.py architecture.md -o tech_talk.pptx -c ocean
```

## 在通道 A 后使用

```
用户内容 → 通道 A → AI 生成 Markdown 导图
        ↓
  [选择输出]
  ├── XMind (.xmind)    ← markdown_to_xmind.py
  ├── 演示文稿 (.pptx)  ← mindmap_to_ppt.py
  ├── 交互 HTML         ← markmap (multi_export.py)
  └── 全部格式          ← multi_export.py -f all
```

## 关联

- [文本→导图](text-to-mindmap.md) — 上游生成
- [多格式导出](../../tools/multi_export.py) — 并行导出
- [PPT 完全指南](../software/ppt-guide.md) — 手动美化进阶
