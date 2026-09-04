# Changelog

## 1.0.1 - 2026-09-04

- 全部 5 个 Skill 完成内部称谓脱敏（老师版/老师客户端/大学生 → 中性表述），并升版本号。
- `scripts/build_skills.py` 重构：白名单只打包乐飞 5 个 Skill；新增打包前脱敏检查，命中旧称谓即失败。
- 仓库并入 Matt Pocock skills 正式集（engineering 19 + productivity 8，上游 commit 3cca18b）。
- 仓库迁移至乐飞项目目录，旧副本（乐乐/skills、乐乐/lefly-skill-pack）独有文档并入 docs/ 后删除。


## 1.0.0 - 2026-09-03

- 首次为 ModelScope 发布准备 5 个独立文档型 Skill。
- 为所有 `SKILL.md` 添加 `version` 元数据，`llm-tools` 声明其依赖的后端工具名。
- 增加本地校验与 ZIP 打包脚本，以及 Qoder 验证说明。
- 采用 Apache-2.0 许可证。
