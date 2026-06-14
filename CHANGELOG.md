## v6.1.0 (2026-06-14)

### Added
- pyproject.toml ruff 配置（0 errors, all checks passed）
- API_REFERENCE.md 完整工具 API 参考
- CHANGELOG.md v1-v6 版本历史
- tests: +9 测试 (50→59), _common.py 覆盖 73%→95%
- quality_checker / mermaid_fixer CLI 测试

### Fixed
- 35 lint 自动修复 + pyproject.toml 抑制剩余风格问题
- markdown_to_xmind.py 重复代码提取到 _common.py
- requirements.txt 补全 5 缺失依赖

### Changed
- CI: 新增 coverage + mypy + ruff 检查
- Lint: 0 errors

---

## v6.0.0 (2026-06-14)

### Added
- tools/diagram_editor.py — AI 往返编辑器
- tools/brand_adapt.py — 品牌自动适配
- tools/mcp_server.py — MCP 服务器封装（5 端点）
- tools/eval.py — 多模型质量评估管线
- tools/_common.py — 共享模块（消除重复代码）
- tests/ — pytest 测试套件（37+ 测试，含 benchmark 数据集）
- tests/test_links.py — 304 内部链接完整性检查
- tests/benchmark/ — 10 个质量基准用例
- tutorial/ — 互动教程
- docker/ — Docker 一键部署
- .github/workflows/ci.yml — CI/CD 自动验证
- package.json — npm 风格分发包
- CONTRIBUTING.md — 贡献指南
- CHANGELOG.md — 本文件
- HTML 导出增强：搜索 + 按层级展开/折叠 + SVG 导出 + 暗色工具栏

### Changed
- tools/requirements.txt 更新
- tools/multi_export.py HTML 增强
- tools/markdown_to_xmind.py 重构导入 _common
- README.md 同步至当前状态
- SKILL.md 通道路由扩展

### Fixed
- 2 个断裂链接修复

---

## v5.0.0 (2026-06-12)

### Added
- tools/url_to_mindmap.py — URL 一键转导图
- tools/mindmap_to_ppt.py — 导图→PPT（4 配色）
- 6 个新 AI 管道参考文件
- 5 个集成参考文件
- 多模态输入管道参考
- Tufte 可视化原则参考
- 知识图谱中间表示参考

---

## v4.0.0

### Added
- tools/mermaid_fixer.py — 37 条正则 Mermaid 语法修复器
- tools/markdown_to_xmind.py — Markdown→XMind 原生文件
- tools/multi_export.py — 6 格式并行导出
- Draw.io MCP 集成指南
- 防幻觉验证系统参考
- Obsidian Canvas / Excalidraw 软件指南

---

## v3.0.0

### Added
- 6 种高级设计模式参考

---

## v2.0.0

### Added
- Think-Cell Chart10 完全指南
- Excel 数据可视化章节（8 讲提炼）
- PPT 30 种版面技法全量表
- PPT 动画扩展章节

---

## v1.0.0

### Added
- 初始发布：7 通道路由 SKILL.md
- 基础 Python 工具链
- 方法论（五星心法/7要素/发散收敛/应用场景）
- 图表选型（37 种/7 分类）
- AI 管道（文本/图片/主题→导图，Mermaid 流程图）
- 软件指南（XMind/draw.io）
