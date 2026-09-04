# 乐飞 Agent Skills（lefei-skills-srl）

AI 学伴「乐飞」（lefly-companion）项目自研的 5 个文档型 Agent Skill，以及配套数据脱敏脚本。

每个 Skill 是一个独立目录，入口为 `SKILL.md`（frontmatter 含 `name` / `version` / `description`）。`dist/` 下是对应的发布 ZIP 备份（每个 ZIP 根目录仅含一个 `SKILL.md`），可直接用于 ModelScope Skills 等平台的提交物。

## Skills 一览（5 个）

| Skill | 中文名 | 用途 |
|---|---|---|
| `character-persona` | 乐飞角色人设 | 角色切换、人设 prompt、开场白与角色接口的开发指南 |
| `emotion-analytics` | 乐飞情绪分析 | 情绪枚举（joy/anger/sadness/neutral）、焦虑度口径、统计接口 |
| `llm-tools` | 乐飞工具调用与知识检索 | function calling 工具（情绪报告/提醒）与 jieba 关键词检索边界 |
| `memory-system` | 乐飞事实记忆 | 每 10 轮自动沉淀事实记忆、supersede 替代链、增删改边界 |
| `profile-analytics` | 乐飞用户画像 | 画像抽取与注入、标签增删改查、删除边界（不联动统计/记忆） |

这 5 个 Skill 覆盖乐飞后端五大核心模块（角色 / 情绪 / 工具 / 记忆 / 画像），均为纯文档型指南：不含后端源码、数据库、`.env` 或任何密钥。

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

本仓库已做敏感信息审查，不含 API key、密码、数据库及真实用户数据。

## 许可证

[Apache-2.0](LICENSE)
