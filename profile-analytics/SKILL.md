---
name: profile-analytics
version: "1.0.1"
description: 乐飞(lefly-companion)用户画像模块开发指南。Use when 开发/调试用户画像抽取、画像标签增删改查、画像注入对话、或排查"删了画像标签但统计/记忆里还有"这类问题时。
author: lefly-team
tags: [education, digital-human, profile]
---

# 用户画像（profile-analytics）

## 是什么

乐飞为每个用户维护一张轻量画像（key-value 标签，如 年级=大三、爱好=插画）。数据存 SQLite `profile` 表，主键 `(user_id, key)`，即**每个用户独立一份**。

## 关键文件（lefly-companion）

- `app/db.py` — `upsert_profile` / `delete_profile` / `get_profile`，全部带 user_id 归一化
- `app/analytics.py` — 每 10 轮对话由 LLM 自动抽取画像增量
- `app/main.py` — 接口：
  - `GET /api/profile?user_id=` 查询
  - `POST /api/profile` 批量设置年级/专业/兴趣（空串=清除该项）
  - `PUT /api/profile/{key}`（body `{"value":...}`，空值 400，key 截 20 字/value 截 40 字）
  - `DELETE /api/profile/{key}` 按 key 硬删，缺失 404

## 注入方式

每次新对话构建 system prompt 时**实时**读 `db.get_profile()` 注入（`app/chat.py:286-291`）。删除标签后，后续新对话 AI 立刻"不再知道"该信息。

## 删除边界（已真机验证，2026-09-03）

删除画像标签只删 `profile` 表那一行，**不联动**：聊天记录、关键词统计、情绪热力、事实记忆。旧会话历史由前端随请求重发，历史文本里出现过的内容仍在该会话上下文中。要"彻底遗忘"需清空会话（面板重置按钮）+ 删除相关记忆，属产品决策，勿擅自加联动。

## 开发铁律

- 数字人客户端强制 `stream=True`、发送 `tools`、可能注入 system，改聊天协议前先读 SPEC/联调清单
- 多用户隔离：所有读写必须带 user_id；测试参考 `tests/test_main.py`
- TDD：先写失败测试再实现，统一用 `D:\Python314\python.exe -m pytest`
