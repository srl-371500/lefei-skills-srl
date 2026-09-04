# 乐飞 Agent Skills（lefei-skills-srl）

大学生 AI 学伴「乐飞」项目日常使用的 Agent 工程技能集（8 个 Skill）与配套数据脱敏脚本。

每个 Skill 目录遵循通用约定：`SKILL.md` 为入口（frontmatter 含 `name` / `description`），`agents/openai.yaml` 为 OpenAI 兼容 Agent 的清单文件，附属 `*.md` 为按需加载的参考文档。

## Skills 一览（8 个）

| Skill | 用途 |
|---|---|
| `tdd` | 测试驱动开发：红-绿-重构节奏，含 mocking 与测试组织参考文档 |
| `code-review` | 双轴代码评审：按仓库编码规范（Standards）与原始 spec（Spec）并行审查一段改动 |
| `to-spec` | 把当前对话沉淀为 spec 并发布到项目的 issue tracker（纯综合，不追问） |
| `to-tickets` | 把计划 / spec / 对话拆成一串可追踪的 tracer-bullet 工单，声明阻塞关系 |
| `implement` | 基于 spec 或一组工单实现一段工作 |
| `grill-with-docs` | 用连续追问打磨方案，边问边沉淀 ADR 与术语表 |
| `handoff` | 把当前会话压缩成交接文档，供下一个 Agent 接手 |
| `setup-matt-pocock-skills` | 一次性配置仓库：issue tracker、triage 标签体系、领域文档布局 |

> 以上技能源自 Matt Pocock 的 engineering skills 集合，在本项目中实际使用与验证。

## 脱敏脚本

`scripts/desensitize.py`：从乐飞后端 SQLite 数据库导出可公开提交的脱敏审核样本。

- 仅依赖 Python 标准库（`re` / `sqlite3` / `pathlib`），无第三方依赖
- 自动隐藏姓名、手机号、邮箱、QQ、学号、身份证、生日、IP、地址等高置信身份信息
- 不导出真实会话标识与精确时间；写文件前二次扫描残余敏感信息，命中即失败退出

用法：

```bash
python scripts/desensitize.py [db路径] [输出md路径]
```

## 安全声明

本仓库已做敏感信息审查，不含 API key、密码及个人隐私数据。
