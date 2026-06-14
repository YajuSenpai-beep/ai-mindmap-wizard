# 互动教程

step-by-step 引导你创建第一个思维导图。

---

## 入门：3 分钟生成第一张导图

### 第 1 步：准备素材
找一段你想整理的文字——一篇文章、一段会议记录、或者一个想法。

### 第 2 步：在 Claude Code 中加载 Skill
```
/ai-mindmap 把这段内容整理成思维导图
```
然后粘贴你的内容。

### 第 3 步：得到 Markdown 导图
Claude 会输出类似这样的结构化 Markdown：
```markdown
# 主题
## 分支A
### 要点1
### 要点2
## 分支B
### 要点3
```

### 第 4 步：导入 XMind
1. 将 Markdown 保存为 `.md` 文件（UTF-8 编码）
2. 打开 XMind → 文件 → 导入 → Markdown
3. 选择刚才保存的文件 → 完成

### 第 5 步（可选）：一键转其他格式
```bash
python tools/multi_export.py my_mindmap.md -f all
```

---

## 进阶：使用 Python 工具链

### 场景 1：从截图生成导图
```bash
pip install -r tools/requirements.txt
python tools/pipeline.py /path/to/screenshots/ my_project
```

### 场景 2：从 URL 直接生成
```bash
python tools/url_to_mindmap.py https://en.wikipedia.org/wiki/Mind_map
```

### 场景 3：导图转 PPT
```bash
python tools/mindmap_to_ppt.py my_mindmap.md -c professional
```

---

## 深入学习路径

1. [方法论基础](../references/methodology/five-star-heart.md) — 五星心法
2. [图表选型](../references/diagram-types/index.md) — 37 种图表何时用
3. [提示词模板](../references/ai-pipeline/prompt-templates.md) — 高级生成技巧
4. [软件操作](../references/software/xmind-guide.md) — XMind 完整指南
