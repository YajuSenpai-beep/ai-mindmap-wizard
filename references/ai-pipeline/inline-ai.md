# 内联 AI 模式：免复制粘贴

> Notion AI 风格——在编辑器内直接触发，不需要复制提示词到另一个 AI 工具。

## 问题

通道 A 的标准流程需要用户在「我们的 Skill」和「AI 工具」之间**来回切换复制粘贴**：

```
① 我们给出提示词 → ② 用户复制
③ 打开 AI 工具 → ④ 粘贴 + 粘贴内容
⑤ 等待 AI 生成 → ⑥ 复制结果
⑦ 回到编辑器 → ⑧ 粘贴保存
```

## 三种免复制方案

### 方案 A：Claude Code 直出（最佳）

因为 Skill 本身就在 Claude Code 中运行——**Claude 自己就是 AI**：

```
用户: 把这段内容做成思维导图
      [粘贴内容]
      
Claude Code (加载了本 Skill):
  ① 分析内容
  ② 生成立即显示在对话中
  ③ 自动保存为 .md 文件
  ④ 提示下一步操作
```

**用户不需要碰任何外部工具。**

### 方案 B：Shell 管道

```bash
# 一行命令：文本 → 导图→ 多种格式
echo "[你的内容]" | python tools/pipeline.py --from-stdin -o my_project

# 从文件
python tools/pipeline.py input.txt -o output/

# 从 URL
python tools/url_to_mindmap.py https://... -o page_summary.md
```

### 方案 C：MCP 服务器集成

```bash
# 通过 MCP 让 Claude Code 直接调用外部 AI
claude mcp add diagram-gen -- npx -y mcp-diagram-generator

# 然后 Claude 可以直接：
# "用 diagram-gen 把这段文字转成思维导图"
```

## 三种方案对比

| | Claude Code 直出 | Shell 管道 | MCP 集成 |
|------|:---:|:---:|:---:|
| 零复制粘贴 | ✅ | ⚠️ 一次性 | ✅ |
| 需要外部 AI | ❌ | ❌ | ✅ |
| 灵活性 | 最高 | 中 | 中 |
| 适合场景 | 日常使用 | 批量自动化 | 需要特定引擎 |

## 关联

- [无提示词模式](no-prompt-mode.md) — 配合使用体验最佳
- [URL 一键导图](../../tools/url_to_mindmap.py) — 管道模式
- [多格式导出](../../tools/multi_export.py) — 批量导出
