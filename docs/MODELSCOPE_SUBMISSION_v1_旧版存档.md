# ModelScope 提交清单

## 一、提交入口

- Skills 入口：https://modelscope.cn/skills
- Token 页面：https://modelscope.cn/my/access/token
- CLI 文档：https://github.com/modelscope/modelscope_hub

本文件只说明本地上传准备，不执行登录、创建仓库或上传。

## 二、实际要上传的 5 个文件

| 序号 | 本地文件 | 建议仓库名 | 中文名 |
|---|---|---|---|
| 1 | `dist/character-persona-1.0.0.zip` | `character-persona` | 乐飞角色人设 |
| 2 | `dist/emotion-analytics-1.0.0.zip` | `emotion-analytics` | 乐飞情绪分析 |
| 3 | `dist/llm-tools-1.0.0.zip` | `llm-tools` | 乐飞工具调用与知识检索 |
| 4 | `dist/memory-system-1.0.0.zip` | `memory-system` | 乐飞事实记忆 |
| 5 | `dist/profile-analytics-1.0.0.zip` | `profile-analytics` | 乐飞用户画像 |

**每个 ZIP 是一个独立的 ModelScope Skill 提交物。** 根目录中的汇总文档、Qoder 测试说明和许可证备份不需要放进 ZIP；ZIP 内已经包含 Skill 自身的 front matter。

## 三、上传前检查

- [ ] Qoder 验证者完成 5/5 Skill 发现和触发测试。
- [ ] `dist/` 中恰好有以上 5 个 ZIP。
- [ ] 每个 ZIP 根目录恰好只有 `SKILL.md`。
- [ ] `SKILL.md` 有 `name`、`version`、`description`。
- [ ] 没有 `.env`、API Token、SQLite 数据库、真实聊天记录或真实用户信息。
- [ ] 已确认 Apache-2.0 和来源仓库的再发布授权。
- [ ] 发布者使用自己的 ModelScope `write` Token，Token 只放环境变量。

## 四、逐个创建仓库

在发布者自己的 PowerShell 中执行，先把 `<owner>` 换成自己的魔搭账号或组织名：

```powershell
D:\Python314\python.exe -m pip install modelscope-hub
$env:MODELSCOPE_API_TOKEN = "<只存在于本机环境变量中的 write Token>"
ms-hub login --token $env:MODELSCOPE_API_TOKEN

ms-hub create <owner>/character-persona --repo-type skill --category other --skill-file D:\乐乐\skills\dist\character-persona-1.0.0.zip --visibility public --license apache-2.0 --chinese-name "乐飞角色人设" --description "乐飞数字人角色人设开发指南"
ms-hub create <owner>/emotion-analytics --repo-type skill --category other --skill-file D:\乐乐\skills\dist\emotion-analytics-1.0.0.zip --visibility public --license apache-2.0 --chinese-name "乐飞情绪分析" --description "乐飞数字人情绪与焦虑分析开发指南"
ms-hub create <owner>/llm-tools --repo-type skill --category developer-tools --skill-file D:\乐乐\skills\dist\llm-tools-1.0.0.zip --visibility public --license apache-2.0 --chinese-name "乐飞工具调用与知识检索" --description "乐飞数字人 function calling 与知识检索开发指南"
ms-hub create <owner>/memory-system --repo-type skill --category other --skill-file D:\乐乐\skills\dist\memory-system-1.0.0.zip --visibility public --license apache-2.0 --chinese-name "乐飞事实记忆" --description "乐飞数字人事实记忆生命周期开发指南"
ms-hub create <owner>/profile-analytics --repo-type skill --category other --skill-file D:\乐乐\skills\dist\profile-analytics-1.0.0.zip --visibility public --license apache-2.0 --chinese-name "乐飞用户画像" --description "乐飞数字人用户画像开发指南"
```

发布后可用以下命令检查：

```powershell
ms-hub info <owner>/character-persona --repo-type skill
ms-hub list --repo-type skill --owner <owner>
```

实际 CLI 参数若随版本变化，以 `ms-hub create --help` 和魔搭网页提示为准；不要把 Token 写进命令历史、文档或截图。

## 五、工具调用边界

上传 `llm-tools` 只上传工具调用的规则文档，不会自动把 `backend/app/tools.py` 变成 ModelScope 工具服务。Qoder 要真正执行工具，需要宿主已注册工具并且乐飞后端在线。若未来要发布 MCP 服务，应另做 MCP 项目和独立安全评审，不混入本次 5 个 Skill ZIP。
