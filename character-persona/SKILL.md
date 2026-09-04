---
name: character-persona
version: "1.0.0"
description: 乐飞(lefly-companion)角色人设模块开发指南。Use when 开发/调试角色切换、人设 prompt、开场白、角色接口，或排查"人格不一致/说话不像乐飞"问题时。
author: lefly-team
tags: [education, digital-human, persona]
---

# 角色人设（character-persona）

## 是什么

乐飞是大学生 AI 学伴数字人，支持多角色（学业/生活等场景化人格，完整清单以 `GET /api/characters` 与 `data/characters/` 语料为准）。人设决定 system prompt 的底座，与画像/记忆注入叠加构成最终人格。

## 关键文件

- `app/characters.py` — `list_characters` / `get_character` / `get_prompt`（人设 prompt 构建）
- `data/characters/` — 角色语料（UTF-8，读用 `utf-8-sig` 兜 BOM）
- `app/main.py` — `GET /api/characters`（角色列表）、`GET /api/characters/{role}`（角色详情）
- `app/chat.py` — `_system_prompt(role, query, profile, summary_text, memories)`：人设 + 画像 + 摘要 + 记忆的最终拼装处

## 注入顺序与边界

1. 人设 prompt（角色底座）
2. 用户画像（实时读取，删标签即刻"遗忘"）
3. 会话摘要 + top-k 事实记忆（`_relevant_memories` jieba 打分取最相关）
4. 老师客户端可能自带 system 注入（客户端行为，后端不覆盖）

## 开发铁律

- 改人设语料 = 改产品人格，必须老师拍板，勿顺手润色
- 角色枚举以 `characters.py` 返回为准，前端硬编码的角色名与后端不一致时以后端为准
- 情绪枚举 joy/anger/sadness/neutral 与人设无关，勿在人设语料里写死旧枚举（旧版 happy 已废弃）
