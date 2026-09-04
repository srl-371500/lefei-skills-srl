# Qoder 验证说明

本次验证的对象是 5 个文档型 Skill 是否能被 Qoder 发现、按触发条件采用，并且其所引用的乐飞后端行为是否真实可用。两项证据缺一不可。

## 0. 不要分发敏感文件

验证包只能包含 `lefly-skill-pack/`、后端源码、`.env.example` 与测试。不要发送真实 `.env`、`data/*.db`、真实聊天记录、ModelScope Token 或上游模型 Token。

## 1. 准备 5 个 Skill

将下面 5 个目录原样复制到该 Qoder 项目版本识别的本地 Skill 目录。常见路径是 `.qoder/skills/`；如果本机 Qoder 版本使用其他目录，以它的官方说明为准。

```text
.qoder/skills/
  character-persona/SKILL.md
  emotion-analytics/SKILL.md
  llm-tools/SKILL.md
  memory-system/SKILL.md
  profile-analytics/SKILL.md
```

重启或刷新 Qoder 后，确认它显示或能读取 5 个名称与各自描述。缺少任一项即不通过。

## 2. 验证每个 Skill 的触发

在 Qoder 中分别发出以下请求，记录回答中引用的 Skill、涉及的接口或文件，以及是否保持 Skill 规定的边界。

| Skill | 触发请求 | 通过标准 |
|---|---|---|
| `character-persona` | “帮我排查 academic 角色为什么不像乐飞，并告诉我该检查哪个接口。” | 指向角色配置、`/api/characters` 或 system prompt 组装，不杜撰角色枚举。 |
| `emotion-analytics` | “情绪热力图为什么和焦虑曲线数据不一致？四个有效情绪值是什么？” | 使用 `joy/anger/sadness/neutral` 与 0-10 焦虑口径。 |
| `memory-system` | “把一条已失效的记忆改掉，应该怎样处理？” | 说明失效记忆只读、替代链语义与编辑/删除边界。 |
| `profile-analytics` | “删掉专业画像后，历史统计和记忆是否也会消失？” | 明确画像、统计、记忆是独立数据边界，不承诺未实现的级联删除。 |
| `llm-tools` | “用户说‘明天下午提醒我交作业’，系统必须做什么？” | 指向 `add_reminder`，说明工具需由宿主和运行中的后端执行，不能只口头答应。 |

## 3. 运行后端契约回归

在有后端源码的电脑上，使用项目统一解释器运行：

```powershell
cd D:\乐乐\backend
D:\Python314\python.exe -m pytest
```

通过标准：pytest 全绿。此步骤不需要真实上游模型 Token，验证接口、存储与工具 schema 的既有测试即可。

## 4. 可选的真实对话联调

仅在验证者自己配置了私有 `.env` 中的上游模型凭证时执行：

```powershell
cd D:\乐乐\backend
D:\Python314\python.exe -m app.main
```

在 Qoder 的自定义 OpenAI 配置中填写：

| 配置项 | 值 |
|---|---|
| Base URL | `http://127.0.0.1:4111/v1` |
| API Key | Qoder 必填时填本地占位值；乐飞适配层不校验它 |
| 模型名 | Qoder 必填时填 `lefei`；后端自动路由 |

通过标准：Qoder 能经 `/v1/chat/completions` 收到有效回复；“提醒我明天下午交作业”能形成实际提醒；再以同一会话查询提醒时能读到该记录。不得在截图、聊天记录或 issue 中公开真实 Token 与真实用户数据。

## 验收结论模板

```text
Qoder Skill 发现：5/5
五个触发场景：5/5
后端 pytest：通过 / 未执行（写明原因）
真实对话联调：通过 / 未执行（写明原因）
结论：可发布 / 不可发布（写明阻塞项）
```
