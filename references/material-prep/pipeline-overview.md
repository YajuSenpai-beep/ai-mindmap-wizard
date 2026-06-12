# 素材准备管道 — 从原始文件到可用的文本

> 图片/PDF/Word/PPT → 提取文字 → 质量检查 → 内容聚类 → 准备就绪

## 管道总览

```
原始素材文件夹
    │
    ├─ [0] 图片去重    → 感知哈希检测相似图片，保留最清晰
    ├─ [1] 批量提取    → OCR(图片/PDF) + 格式提取(Word/PPT/HTML)
    ├─ [2] 质量扫描    → CJK密度/有效行/乱码率 三维评分
    ├─ [3] 自适应改进  → 低质量文件重处理
    ├─ [4] 内容聚类    → TF-IDF 语义分组
    ├─ [5] LLM 纠错    → AI修正OCR形近字（可选）
    └─ [6] 进入通道A   → 提取的文本 → AI生成Markdown → XMind
```

## 两种执行方式

### 方式一：内置 Python 工具链（推荐有 Python 环境的用户）

工具脚本位于本 skill 的 `tools/` 目录。

```bash
# 安装依赖
pip install -r tools/requirements.txt

# 一键全管道
python tools/pipeline.py /path/to/images my_project

# 分步执行
python tools/pipeline.py /path/to/images my_project --only dedup   # 只去重
python tools/pipeline.py /path/to/images my_project --only ocr     # 只OCR
python tools/pipeline.py /path/to/images my_project --only cluster # 只聚类

# 增量处理（第二次自动跳过未修改文件）
python tools/pipeline.py /path/to/images my_project

# 预览模式
python tools/pipeline.py /path/to/images my_project --dry-run
```

### 方式二：手动方案（无 Python 环境）

1. **去重**：文件管理器按大小排序，删除明显重复照片
2. **OCR**：上传图片到支持图片的 AI 工具（KIMI/Claude/ChatGPT），逐张识别
3. **排版提取**：Word/PPT 直接复制文字；PDF 能选中就复制，不能就截图
4. **质量判断**：人工扫一眼识别结果，明显乱码的重新拍照/扫描
5. **分组**：按主题手动分文件夹

## 工具安装

```bash
# Python 依赖
pip install -r tools/requirements.txt

# Tesseract OCR（系统级安装）
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Mac: brew install tesseract
# Linux: apt install tesseract-ocr

# 中文语言包
# 下载 chi_sim.traineddata → Tesseract tessdata 目录

# 可选：PaddleOCR（中文识别更好）
pip install paddlepaddle paddleocr
```

## 关联

- [OCR 提取指南](ocr-extraction.md) — 图片/PDF OCR 的详细技巧
- [格式提取指南](format-extraction.md) — Word/PPT/HTML/字幕提取
- [图片→导图重建](../ai-pipeline/image-to-mindmap.md) — 单张图片的手动方案
- [写作规范](../methodology/writing-standards.md) — AI 生成笔记的质量标准
- [质量自检](../troubleshooting/quality-assurance.md) — 生成后的校验
