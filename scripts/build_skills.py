"""校验并生成可上传 ModelScope 的独立 Skill ZIP，不联网、不上传。

- 只打包乐飞自研 5 个 Skill（顶层目录白名单），不碰 engineering/ productivity/ 等同步来的目录
- 打包前做内部称谓脱敏检查，命中即失败，防止旧文案再次进入发布包
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
MAX_ARCHIVE_BYTES = 5 * 1024 * 1024
REQUIRED_FIELDS = ("name", "version", "description")
LEFEI_SKILLS = (
    "character-persona",
    "emotion-analytics",
    "llm-tools",
    "memory-system",
    "profile-analytics",
)
# 旧版文案残留即打包失败：这些称谓已在中性化改造中移除（commit 122783c）
DENYLIST = ("老师", "大学生")


def _front_matter(skill_file: Path) -> dict[str, str]:
    content = skill_file.read_text(encoding="utf-8-sig")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        raise ValueError(f"{skill_file}: 缺少 YAML front matter")

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line or line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def validate_skill(skill_dir: Path) -> dict[str, str]:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise ValueError(f"{skill_dir}: 缺少 SKILL.md")

    content = skill_file.read_text(encoding="utf-8-sig")
    hits = [word for word in DENYLIST if word in content]
    if hits:
        raise ValueError(f"{skill_file}: 含旧版内部称谓 {hits}，先完成脱敏再打包")

    fields = _front_matter(skill_file)
    missing = [field for field in REQUIRED_FIELDS if not fields.get(field)]
    if missing:
        raise ValueError(f"{skill_file}: 缺少字段 {', '.join(missing)}")
    if fields["name"] != skill_dir.name:
        raise ValueError(f"{skill_file}: name 必须与目录名一致")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields["name"]):
        raise ValueError(f"{skill_file}: name 必须为 kebab-case")
    if not re.fullmatch(r"\d+\.\d+\.\d+", fields["version"]):
        raise ValueError(f"{skill_file}: version 必须为 x.y.z")
    return fields


def build_skill(skill_dir: Path) -> Path:
    fields = validate_skill(skill_dir)
    archive = DIST_DIR / f"{fields['name']}-{fields['version']}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(skill_dir / "SKILL.md", "SKILL.md")

    if archive.stat().st_size > MAX_ARCHIVE_BYTES:
        raise ValueError(f"{archive}: 超过 ModelScope 5 MiB 上限")
    with zipfile.ZipFile(archive) as zf:
        if zf.namelist() != ["SKILL.md"]:
            raise ValueError(f"{archive}: ZIP 根目录只能包含一个 SKILL.md")
    return archive


def build_all() -> list[Path]:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    skill_dirs = [ROOT / name for name in LEFEI_SKILLS]
    missing = [str(d) for d in skill_dirs if not d.is_dir()]
    if missing:
        raise ValueError(f"缺少 Skill 目录: {', '.join(missing)}")
    archives = [build_skill(path) for path in skill_dirs]
    if len(archives) != 5:
        raise ValueError(f"预期 5 个 Skill，实际生成 {len(archives)} 个")
    return archives


if __name__ == "__main__":
    for archive in build_all():
        print(archive.relative_to(ROOT))
