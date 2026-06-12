# 格式提取指南 — Word/PPT/HTML/字幕 → 文本

> 这些格式本身就是文字，不需要 OCR。关键是提取结构，保留层级。

## Word (.docx) → 文本

### 手动方式
直接打开 Word，复制全部内容。标题和正文的格式会被粘贴为纯文本。

### Python 方式（保留结构）
```bash
python tools/formats.py document.docx
```
自动保留标题层级（Heading 1 → `#`, Heading 2 → `##`）和表格。

### 技巧
- 如果有大量批注和修订标记，先「接受所有修订」再提取
- 表格内容建议保留 Markdown 表格格式，方便后续 AI 理解
- 图片中的文字不会被提取——截图后用 OCR 补充

## PowerPoint (.pptx) → 文本

### 手动方式
打开 PPT → 大纲视图 → 复制大纲。这会保留层级结构但丢失表格和图片。

### Python 方式（按幻灯片）
```bash
python tools/formats.py presentation.pptx
```
每张幻灯片输出为 `## 幻灯片 N`，保留标题和正文。

### 技巧
- SmartArt 和图表中的文字通常提取不出来，需要单独截图 OCR
- 备注栏的文字默认不提取，如有重要内容手动补充
- 同一主题的多张幻灯片 → AI 可以自动合并为一张导图

## 微信文章 HTML → Markdown

```bash
python tools/wechat2md.py article.html
```

提取内容：
- 标题（og:title 元标签）
- 作者
- 原文链接
- 正文（修复懒加载图片，清理隐藏元素）

### 手动方式
从浏览器直接复制微信文章正文粘贴到 AI 工具。标题和作者手动打。

## 通用 HTML → 文本

```bash
python tools/formats.py page.html
```

自动定位 `<main>` → `<article>` → `<body>` 中的主内容区，去除导航/页脚/广告。

### 手动方式
浏览器中选中文章正文区域 → 复制。避免全选（会把导航栏、相关推荐等也复制进去）。

## 字幕 (.srt / .vtt) → 纯文本

```bash
python tools/formats.py subtitles.srt
```

自动去除时间戳和序号，输出连续文本。

### 手动方式
用文本编辑器打开 `.srt` 文件 → 删除所有序号行和时间戳行 → 合并为段落。

## 提取后检查清单

| 检查项 | 说明 |
|--------|------|
| 层级是否保留 | Word 的标题层级、PPT 的幻灯片顺序 |
| 表格是否完整 | 表格数据是否变成可读的文本 |
| 图片文字是否丢失 | Word/PPT 中的图片文字需要单独 OCR |
| 是否有乱码 | 特别是从 PDF 复制的特殊字符 |
| 内容是否完整 | 对照源文件快速扫一遍，看有没有明显缺失 |

## 关联

- [OCR 提取指南](ocr-extraction.md) — 图片/PDF 的文字提取
- [管道概览](pipeline-overview.md) — 批量处理的工具链方式
- [文本→导图流程](../ai-pipeline/text-to-mindmap.md) — 提取后进入通道 A
