---
name: llm-tools
version: "1.0.0"
description: 乐飞(lefly-companion)LLM 工具调用与知识检索开发指南。Use when 开发/调试 function calling 工具、DashScope 接入、知识库语料检索，或排查"模型没调工具/检索不中"问题时。
author: lefly-team
tags: [education, digital-human, tool-calling]
requires:
  tools: [get_emotion_report, add_reminder, list_reminders]
---

# LLM 工具调用与知识检索（llm-tools）

## 工具调用（function calling）

工具定义与执行在 `app/tools.py`，当前 **3 个工具**：

1. `get_emotion_report` — 查询用户近期情绪报告（读 conversations 统计）
2. `add_reminder` — 新增提醒/待办（落 `reminders` 表）
3. `list_reminders` — 列出提醒（支持按 session_id、include_done 过滤）

链路：`/chat/completions` 兼容层把 tools 随请求发给 DashScope（qwen-turbo，OpenAI 兼容接口），模型返回 tool_call 后在服务端执行并回填。工具执行结果会落库的只有提醒类，查询类只读。

## 客户端约束（老师版，改协议前必读）

- 老师数字人客户端**强制 `stream=True`**、**发送 `tools` 字段**、可能自带 system 注入
- 自研版/其他客户端可能是非流式——两套协议行为不同，勿把一方的假设套到另一方

## 知识检索（不是工具调用）

`app/knowledge.py` 用 jieba 分词对 `data/knowledge/` 语料（academic/career/life/skills 四大类 12 篇 md）做**关键词打分检索**，取 top-k 注入 prompt。没有向量化、没有 function calling，属于轻量检索。语料一律 UTF-8，读文件用 `encoding="utf-8-sig"` 兜 BOM。

## 密钥与配置

- `DASHSCOPE_API_KEY` 只走 `.env`（gitignore 已覆盖），缺 key 时启动报清晰中文错误
- 模型/地址/端口在 `app/config.py`：qwen-turbo、端口默认 4111

## 开发铁律

- 新增工具：先在 `tools.py` 定义 schema + 执行器，再补 `/chat/completions` 透传测试，勿在 chat.py 里散落 if-else
- 报错时把 DashScope 响应体 `response.text` 拼进异常信息，别吞
