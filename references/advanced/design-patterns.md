# 六种高级设计模式

> 从 Agent Skills 橙皮书提炼。超越基础 SKILL.md 结构——组合式 Skill 架构。

## 模式总览

| # | 模式 | 适用场景 | 关键特征 |
|---|------|---------|---------|
| 1 | **Checklist** | 审核/检查/合规 | 逐项验证，不可跳过 |
| 2 | **Options** | 多路径选择 | 按条件路由到不同子流程 |
| 3 | **Pipeline** | 数据流处理 | 上一阶段输出=下一阶段输入 |
| 4 | **Integration** | 多系统协作 | Skill + MCP + 外部 API |
| 5 | **Swarm** | 并行大规模处理 | 多子代理并行，汇总结果 |
| 6 | **Distillation** | 知识提取固化 | 从对话/文档中蒸馏出新的 Skill |

## 1. Checklist（清单式）

将操作分解为不可跳过的验证步骤：

```markdown
### 检查 1：敏感信息
- [ ] 无硬编码密钥 → 如发现标记 CRITICAL
### 检查 2：依赖安全
- [ ] 无已知漏洞 → 如发现标记 WARNING
### 检查 3：测试覆盖
- [ ] 新增代码有测试 → 如未覆盖标记 SUGGESTION
```

## 2. Options（选项式路由）

根据输入条件路由到不同子流程：

```markdown
### 判断：目标平台
- platform=="web" → Web部署流程
- platform=="mobile" → Mobile构建流程
- platform=="desktop" → Desktop打包流程
```

## 3. Pipeline（管道式串联）

阶段化顺序处理，每阶段输出=下一阶段输入：

```
阶段1: 数据采集 → raw_data.json
  ↓
阶段2: 数据清洗 → clean_data.json  
  ↓
阶段3: 特征计算 → features.json
  ↓
阶段4: 报告生成 → report.md
```

每阶段设检查点验证输出。

## 4. Integration（集成式调用）

Skill 作为协调中心，连接 MCP 服务器 + 外部 API + 本地脚本：

```
BigQuery MCP(数据) → scripts/calc(计算) → Notion MCP(写入报告)
```

## 5. Swarm（群体协作）

大规模任务拆分为独立子任务，子代理并行处理：

```markdown
① 任务分解：拆为 N 个独立子任务
② 并行执行：每个子代理独立处理一个切片
③ 结果汇总：去重→排序→合并
```

子任务必须无依赖，子代理返回统一 JSON schema。

## 6. Distillation（蒸馏模式）

从经验中自动提取 Skill：

```
观察：同一工作流在 3+ 次对话中重复
提取：抽象通用方法（非具体数据）
固化：生成 SKILL.md
验证：用新 Skill 处理历史案例
```

## 模式选择矩阵

| 需求 | 模式 |
|------|------|
| 逐项检查不遗漏 | Checklist |
| 不同条件走不同流程 | Options |
| 阶段化顺序处理 | Pipeline |
| 协调多个外部系统 | Integration |
| 大规模并行独立处理 | Swarm |
| 从经验中自动提取知识 | Distillation |
