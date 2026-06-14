# 贡献指南

感谢你对 ai-mindmap-wizard 的关注！欢迎任何形式的贡献。

## 快速开始

```bash
git clone https://github.com/YajuSenpai-beep/ai-mindmap-wizard.git
cd ai-mindmap-wizard
pip install -r tools/requirements.txt
pip install pytest python-pptx

# 运行测试
pytest tests/ -v

# 运行链接检查
python tests/test_links.py .
```

## 项目结构

```
ai-mindmap-wizard/
├── SKILL.md                    # 工具入口页 + 命令速查 + 知识库索引
├── tools/                      # Python 工具链（19 个脚本）
├── tests/                      # 单元测试（59 个）+ 链接检查
├── references/                 # 知识库（9 个子目录，66 篇）
│   ├── ai-pipeline/            # AI 管道（15 篇）
│   ├── methodology/            # 方法论（9 篇）
│   ├── software/               # 软件指南（14 篇）
│   ├── diagram-types/          # 图表类型（8 篇）
│   ├── material-prep/          # 素材准备（5 篇）
│   ├── troubleshooting/        # 故障排查（3 篇）
│   ├── templates/              # 模板（6 个）
│   ├── integrations/           # 外部集成（5 篇）
│   └── advanced/               # 高级模式（1 篇）
├── tutorial/                   # 使用说明
├── docker/                     # Docker 部署
└── .github/workflows/          # CI/CD
```

## 贡献方式

### 新增图表类型

在 `references/diagram-types/` 下扩展或新增分类文件。参考现有文件的结构：

```markdown
## 概述
一句话说明该类型图表。

## 适用场景
- 场景A
- 场景B

## 绘制要点
1. 要点1
2. 要点2
```

### 改进提示词

编辑 `references/ai-pipeline/prompt-templates.md`（中文）或 `prompt-templates-en.md`（英文）。

提示词规则：
- 角色-目标-条件三要素齐全
- 工具无关，任何 LLM 可用
- 含输入输出示例

### 软件操作指南

在 `references/software/` 下新增文件。参考模板：
- 开头注明来源文件数
- 分章节用表格+代码块
- 结尾加「关联」章节交叉引用
- 文件 < 200 行

### 新增 Python 工具

在 `tools/` 下新增 `.py` 文件：
- 包含 `main()` 入口和 `argparse` CLI
- 核心函数可导入（便于测试）
- 在 `tests/test_tools.py` 中添加对应测试类

### 提交 PR 前

```bash
# 1. 运行全部测试
pytest tests/ -v

# 2. 检查链接完整性
python tests/test_links.py .

# 3. 检查 SKILL.md 格式
python -c "
import yaml
with open('SKILL.md') as f:
    content = f.read()
frontmatter = content.split('---')[1]
data = yaml.safe_load(frontmatter)
assert 'name' in data and 'description' in data
print('✅ SKILL.md valid')
"
```

## 代码风格

- Python: 遵循 PEP 8
- Markdown: 中文文档，引用文件用相对路径如 `[text](references/methodology/five-star-heart.md)`
- 提交信息: 中文描述，简洁明了

## Issue 模板

### Bug 报告
- 描述问题
- 复现步骤
- 期望行为
- 环境（OS / Python 版本）

### 功能请求
- 描述需求
- 使用场景
- 建议实现方式（可选）
