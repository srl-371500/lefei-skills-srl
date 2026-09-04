---
name: emotion-analytics
version: "1.0.1"
description: 乐飞(lefly-companion)情绪分析模块开发指南。Use when 开发/调试情绪识别、焦虑度、感受备注、情绪热力日历、情绪曲线、关键词统计相关功能，或排查统计口径问题时。
author: lefly-team
tags: [education, digital-human, analytics]
---

# 情绪分析（emotion-analytics）

## 是什么

每轮对话落库时由 LLM 判定情绪与焦虑度，支撑面板可视化：情绪热力日历、情绪曲线、关键词云、KPI。

## 关键口径（勿改，改=破坏历史数据兼容）

- 情绪枚举：`joy / anger / sadness / neutral`（旧版 `happy` 已废弃，勿混用）
- 焦虑值：0-10 整数，0=平静，10=极度焦虑；热力图按日均值深浅渲染
- 每轮可选带：`mood`（心情词）、`anxiety_level`、`feeling_note`（感受备注）

## 关键文件

- `app/analytics.py` — 统计汇总、趋势构建、LLM 抽取 prompt（`_build_llm_prompt`）
- `app/db.py` — `log_conversation(role, user_text, bot_text, emotion, ..., mood, anxiety_level, feeling_note)` 落库；`conversation_stats` 统计
- `app/main.py` — `GET /api/analytics/summary`（KPI+memories_count）、`GET /api/analytics/emotion-trend`（热力/曲线数据）、`GET /api/analytics/keywords`（jieba 关键词）

## 数据来源边界

统计全部来自 `conversations` 表。删除画像标签、删除记忆**都不影响**已生成的统计（互相独立的数据源）。清空统计用 `POST /api/admin/reset`（必须 `{"confirm": true, "user_id":...}`，绝不提供 GET 形式）。

## 开发铁律

- 关键词分词用 jieba（`app/knowledge.py` 同款），改分词口径会导致历史关键词错位
- 单测参考 `tests/test_analytics.py`、`tests/test_main.py` 的 `_seed` 灌数方法
