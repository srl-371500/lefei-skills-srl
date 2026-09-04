# Skill 汇总（lefei-skills-srl）

本目录是 Skill 汇总仓库：AI 学伴「乐飞」（lefly-companion）自研的 5 个文档型 Skill、Matt Pocock 开源工程技能集的本地同步副本（`engineering/` + `productivity/`，27 个），以及配套数据脱敏脚本。`matt-skills-ref/` 为上游完整镜像，仅本地参考、不入库。

## 目录结构

| 目录 | 内容 | 来源 |
|---|---|---|
| `character-persona` 等 5 个顶层目录 | 乐飞自研 Skill（见下表） | 自研 |
| `engineering/`（19 个） | Matt Pocock 工程技能集（正式发布集） | 上游同步，见下 |
| `productivity/`（8 个） | Matt Pocock 生产力技能集（正式发布集） | 上游同步，见下 |
| `dist/` | 乐飞 5 个 Skill 的发布 ZIP 备份 | — |
| `scripts/` | 数据脱敏脚本 | 自研 |

## 乐飞自研 Skills（5 个）

| Skill | 中文名 | 用途 |
|---|---|---|
| `character-persona` | 乐飞角色人设 | 角色切换、人设 prompt、开场白与角色接口的开发指南 |
| `emotion-analytics` | 乐飞情绪分析 | 情绪枚举（joy/anger/sadness/neutral）、焦虑度口径、统计接口 |
| `llm-tools` | 乐飞工具调用与知识检索 | function calling 工具（情绪报告/提醒）与 jieba 关键词检索边界 |
| `memory-system` | 乐飞事实记忆 | 每 10 轮自动沉淀事实记忆、supersede 替代链、增删改边界 |
| `profile-analytics` | 乐飞用户画像 | 画像抽取与注入、标签增删改查、删除边界（不联动统计/记忆） |

覆盖乐飞后端五大核心模块（角色 / 情绪 / 工具 / 记忆 / 画像），均为纯文档型指南：不含后端源码、数据库、`.env` 或任何密钥。

## Matt Pocock Skills（27 个，上游同步）

来源：[mattpocock/skills](https://github.com/mattpocock/skills)（MIT），同步自上游 `main` 分支 commit `3cca18b`（2026-09-04）。

**Engineering（19 个）**

- 用户主动调用：`ask-matt`（技能路由器）、`grill-with-docs`、`triage`、`improve-codebase-architecture`、`setup-matt-pocock-skills`、`to-spec`、`to-tickets`、`implement`、`wayfinder`
- 模型自动调用：`prototype`、`diagnosing-bugs`、`research`、`tdd`、`domain-modeling`、`codebase-design`、`code-review`、`resolving-merge-conflicts`、`wizard`

**Productivity（8 个）**

- 用户主动调用：`grill-me`、`handoff`、`teach`、`to-questionnaire`、`wait-what`
- 模型自动调用：`grilling`、`writing-for-agents`

说明：本仓库早期（commit `fe4183d`）引入过其中 8 个（code-review / grill-with-docs / handoff / implement / setup-matt-pocock-skills / tdd / to-spec / to-tickets），本次同步已验证该 8 个与上游最新版逐字节一致，并补齐其余 19 个。上游的 `in-progress/`、`misc/`、`deprecated/` 为作者实验区，未纳入。

### 长任务推荐工作流

超大任务（单个 session 装不下）用 `wayfinder` 起手，把工作拆成 issue tracker 上的决策票逐个解决；常规流程：`grill-with-docs` 打磨方案 → `to-spec` 沉淀 spec → `to-tickets` 拆工单 → `implement` 实现（内部驱动 `/tdd` 与 `/code-review`）→ `handoff` 跨 session 交接。

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

[Apache-2.0](LICENSE)（乐飞自研部分）；`engineering/`、`productivity/` 目录内容遵循上游 [MIT](https://github.com/mattpocock/skills/blob/main/LICENSE) 许可证。
