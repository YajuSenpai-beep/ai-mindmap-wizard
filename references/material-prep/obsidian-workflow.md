# Obsidian Second Brain 工作流

> 从 claude-second-brain、markdown-memory、graph-context-for-claude-code 提炼。将思维导图 Skill 嵌入知识管理闭环。

## 核心理念

思维导图不只是「生成一次」的产物——应该成为**持续生长的知识网络**的有机部分。

```
单向流（旧）：     文本 → AI 生成导图 → 导入 XMind → 结束
双向流（新）：     文本 ↔ Obsidian ↔ AI 分析 ↔ 思维导图 ↔ 持续更新
```

## 三种整合模式

### 模式 1：AI 生成的导图 → 自动存入 Obsidian

```
① AI 生成 Markdown 导图（通道 A）
② 保存到 Obsidian vault 的指定目录
③ Obsidian 自动索引 + [[Wiki双链]] 激活
④ 通过 graph view 查看与其他笔记的关系
```

**设置**：
```bash
# 将 AI 导图输出目录设为 Obsidian vault 子目录
export MINDMAP_OUTPUT="$HOME/ObsidianVault/Mindmaps"

# 在 prompt 中指定
"请将生成的 Markdown 保存到我的 Obsidian vault 的 Mindmaps/ 目录"
```

### 模式 2：Obsidian 笔记 → AI 提炼 → 思维导图

```
① Obsidian 中有多篇笔记
② 通过 graph-context 插件推送上下文到 Claude Code
③ AI 分析交叉引用关系 → 生成综合导图
④ 导图存回 vault，标注来源笔记的 [[链接]]
```

### 模式 3：持续生长型知识图谱

```
① 初始：从一篇核心文档生成基础导图
② 每次添加新笔记 → AI 检测是否与已有导图相关
③ 如果相关 → 自动更新导图，添加新节点+标注来源
④ 如果不相关 → 建议新建独立导图
⑤ 定期运行 /lint → 找孤立节点、矛盾信息、断链
```

## 与 markdown-memory 桥接

```bash
# 安装 markdown-memory 桥接系统
npx markdown-memory

# 核心命令
/mm-resume      # 恢复上次会话上下文
/mm-save-session # 保存当前对话到 Obsidian
/mm-handoff     # 将当前上下文传递给新会话
/mm-bridge      # claude.ai ↔ Claude Code ↔ Obsidian 三向同步
```

## 与 graph-context 插件配合

在 Obsidian 中安装 `graph-context-for-claude-code` 插件后：

```
① 在 Obsidian 中选中一段文本
② Claude Code /ide 命令连接到 Obsidian
③ Claude 自动获取：
   - 选中文本的完整段落
   - 前后链接的笔记摘要
   - [[Wiki双链]] 的目标内容
   - 反向链接列表
④ 在完整上下文中生成思维导图
```

## 自动化脚本

```bash
#!/bin/bash
# scripts/sync_mindmap_to_obsidian.sh
# 将生成的导图自动同步到 Obsidian vault

VAULT="$HOME/ObsidianVault"
MINDMAP_DIR="$VAULT/Generated/Mindmaps"

mkdir -p "$MINDMAP_DIR"

# 复制最新生成的 Markdown 导图
cp "$1" "$MINDMAP_DIR/$(date +%Y%m%d_%H%M)_$(basename "$1")"

# 可选：触发 Obsidian 索引
# osascript -e 'tell application "Obsidian" to activate'
```

## 关联

- [Obsidian Canvas 指南](../software/obsidian-canvas-guide.md) — Canvas 格式的导图
- [知识图谱中间表示](../methodology/knowledge-graph.md) — 笔记间关系的结构化建模
- [增量处理](../../tools/incremental.py) — 只更新变化的部分
