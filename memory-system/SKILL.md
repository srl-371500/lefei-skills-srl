---
name: memory-system
version: "1.0.0"
description: 乐飞(lefly-companion)事实记忆模块开发指南。Use when 开发/调试记忆沉淀、记忆时间线、记忆编辑删除、替代链(supersede)语义，或排查"记忆改不了/删不干净"问题时。
author: lefly-team
tags: [education, digital-human, memory]
---

# 事实记忆（memory-system）

## 是什么

Mem0 式增量记忆：每 10 轮对话自动沉淀一条带时间戳的事实记忆（如「竞赛：蓝桥杯备赛中」）。新事实产生时，旧同类记忆**不物理删除**，而是打上 `superseded_by` 指向替代它的新记忆，形成可追溯的演变链。

## 存储与核心语义

- SQLite `memories` 表：`id / user_id / key / content / created_at / source_turn / superseded_by`
- **失效记忆是历史轨迹**：`superseded_by IS NOT NULL` 的条目前端划线展示，只读
- 硬删一条记忆**不得连带**恢复或删除它的替代链上下游

## 接口（app/main.py）

- `GET /api/memories?key=&limit=&include_superseded=&user_id=`（limit 上限 50）
- `PUT /api/memories/{id}`（body `{"content":...}`）— 仅未失效记忆可编辑；已失效或不存在统一 404；空内容 400
- `DELETE /api/memories/{id}` — 按 id 硬删，缺失 404
- db 层：`add_memory / list_memories / supersede_memory / update_memory / delete_memory`（app/db.py，均带 user_id 隔离）

## 前端入口

完整状态面板（static/index.html + app.js）记忆时间线：未失效条目双击编辑、× 确认撤回；失效条目只读划线。接口语义与 UI 行为一一对应，改接口必须同步测试 `tests/test_main.py` 记忆段。

## 开发铁律

- 一切读写带 user_id（跨用户 id 互不可见，已有测试覆盖）
- 时间线展示用 `include_superseded=true` 才能看到演变链
- 测试覆盖点：更新、创建、空值 400、删除成功、缺失 404、失效不可编辑、跨用户隔离
