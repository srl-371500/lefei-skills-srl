# Qoder 测试说明

这份说明交给另一位验证者使用。测试对象是 `skills/` 下的 5 个文档型 Skill，不是魔搭上传流程。测试完成后请记录结果，再由项目成员自己上传 ModelScope。

## 1. 准备 Skill

将以下 5 个目录复制到 Qoder 当前版本识别的本地 Skill 目录，常见路径为项目内 `.qoder/skills/`：

```text
.qoder/skills/
  character-persona/SKILL.md
  emotion-analytics/SKILL.md
  llm-tools/SKILL.md
  memory-system/SKILL.md
  profile-analytics/SKILL.md
```

刷新或重启 Qoder，确认能识别 5 个名称及其描述。缺少任何一个就记为未通过，不要自行修改 `SKILL.md`。

## 2. 五个触发测试

每项使用一个新对话，记录 Qoder 是否采用了对应 Skill，以及回答是否保持文件中规定的接口和边界。

| Skill | 测试问题 | 通过标准 |
|---|---|---|
| `character-persona` | “排查 academic 角色为什么不像乐飞，应该检查哪些文件和接口？” | 指向角色配置、`/api/characters` 或 system prompt 组装，不杜撰角色枚举。 |
| `emotion-analytics` | “情绪热力图和焦虑曲线口径不一致时怎么查？四个情绪值是什么？” | 使用 `joy/anger/sadness/neutral`，并保持焦虑值 0-10。 |
| `memory-system` | “一条已经失效的记忆还能不能编辑？替代链怎么保留？” | 说明失效记忆只读、supersede 演变链和删除边界。 |
| `profile-analytics` | “删除专业画像后，历史统计和事实记忆会不会一起消失？” | 说明画像、统计、记忆是独立数据边界，不承诺级联删除。 |
| `llm-tools` | “用户说‘明天下午提醒我交作业’，系统必须做什么？” | 指向 `add_reminder`，说明需要宿主工具注册和在线后端，不能只口头答应。 |

## 3. 后端静态回归

如果验证者拿到了后端源码，在后端目录执行：

```powershell
cd D:\乐乐\backend
D:\Python314\python.exe -m pytest
```

通过标准：测试全绿。此步骤不需要向验证者提供真实 `.env` 或数据库。

## 4. 真实工具调用联调（可选）

只有验证者有权使用一份私有上游模型配置时才执行。启动后端：

```powershell
cd D:\乐乐\backend
D:\Python314\python.exe -m app.main
```

Qoder 自定义 OpenAI 配置：

| 配置项 | 值 |
|---|---|
| Base URL | `http://127.0.0.1:4111/v1` |
| API Key | Qoder 必填时填本地占位值，不能填真实上游 Token |
| 模型名 | `lefei` |

用同一个会话依次验证：

1. “明天下午 3 点提醒我交数媒作业。”
2. “我有哪些未完成提醒？”
3. “查看我最近的情绪状态。”

通过标准：Qoder 发起了合适的工具调用；提醒确实能在后端记录并被后续查询读到；情绪报告引用真实后端记录。若 Qoder 只输出文字而没有工具调用，应记录为工具联调未通过，不要把文档 Skill 本身判定为可执行 MCP。

## 5. 结果记录模板

```text
Skill 发现：5/5
character-persona：通过/失败，证据：
emotion-analytics：通过/失败，证据：
memory-system：通过/失败，证据：
profile-analytics：通过/失败，证据：
llm-tools：通过/失败，证据：
后端 pytest：通过/未执行，原因：
真实工具调用：通过/未执行，原因：
是否建议上传 ModelScope：是/否，阻塞项：
```

## 6. 数据与密钥边界

不要把真实 `.env`、数据库、聊天记录、截图中的 Token 或真实个人信息交给验证者。需要测试数据时，使用验证者自己生成的虚构内容和临时 SQLite 库；测试结果只记录“通过/失败”和脱敏后的行为证据。
