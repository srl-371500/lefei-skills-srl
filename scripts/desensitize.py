"""导出可公开提交的最小脱敏审核样本。

用法（在 backend 目录下）：
  D:\\Python314\\python.exe scripts\\desensitize.py [db路径] [输出md路径]

输出覆盖对话、画像、会话摘要、事实记忆和提醒中的自由文本。真实会话标识、
精确时间和提醒截止时间不导出；写文件前会扫描残余高置信敏感信息，命中即失败。
"""
import re
import sqlite3
import sys
from pathlib import Path

_NAME_PATTERNS = [
    re.compile(r"(?:我叫|我是|名字[是叫]|姓名[是为])([\u4e00-\u9fa5]{2,4})(?=[，。,.;；\s!！?？]|$)"),
    re.compile(r"([\u4e00-\u9fa5]{2,4})同学"),
]
_STRUCTURED_NAME = re.compile(r"(?:姓名|名字|昵称)[：:\s=]*([\u4e00-\u9fa5]{2,4})")
_PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
_EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
_QQ = re.compile(r"(?:QQ|qq)[:：\s]*(\d{5,11})")
_STUDENT_ID = re.compile(r"(?:学号|编号)[:：\s]*\d{8,12}|(?<!\d)\d{10}(?!\d)")
_ID_CARD = re.compile(r"(?<!\d)\d{17}[\dXx](?![\dXx])")
_BIRTH = re.compile(
    r"(?:生日|出生(?:日期)?)[:：\s]*\d{4}(?:[-/]|年)\d{1,2}(?:[-/]|月)\d{1,2}(?:日)?"
)
_IPV4 = re.compile(r"(?<![\d.])(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}(?![\d.])")
_ADDRESS = re.compile(
    r"(?:住在|地址[是为：:]?|家住)[^，。；;!！?？\n]{2,50}|"
    r"[\u4e00-\u9fa5]{2,9}(?:省|市)[\u4e00-\u9fa5]{1,9}(?:市|区|县)[\u4e00-\u9fa5\d]{1,30}(?:街|路|巷|号)"
)
_RESIDUAL_PATTERNS = (_PHONE, _EMAIL, _QQ, _STUDENT_ID, _ID_CARD, _IPV4)
_MAX_CELL_LENGTH = 80


def desensitize(text: str, known_names: list[str] | None = None) -> str:
    """替换自由文本中的高置信身份与联络信息。"""
    if not text:
        return text

    names = list(known_names or [])
    for pattern in _NAME_PATTERNS:
        names.extend(match.group(1) for match in pattern.finditer(text) if match.group(1))
    for name in sorted(set(names), key=len, reverse=True):
        if len(name) >= 2:
            text = text.replace(name, "同学A")

    text = _ID_CARD.sub("身份证已隐藏", text)
    text = _PHONE.sub("手机号已隐藏", text)
    text = _EMAIL.sub("邮箱已隐藏", text)
    text = _QQ.sub("QQ已隐藏", text)
    text = _STUDENT_ID.sub("学号已隐藏", text)
    text = _BIRTH.sub("生日已隐藏", text)
    text = _IPV4.sub("IP已隐藏", text)
    return _ADDRESS.sub("地址已隐藏", text)


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (table,)
    ).fetchone() is not None


def _known_names(conn: sqlite3.Connection) -> list[str]:
    names: list[str] = []
    sources = (
        ("conversations", ("user_text", "bot_text", "feeling_note")),
        ("profile", ("key", "value")),
        ("summaries", ("summary",)),
        ("memories", ("content",)),
        ("reminders", ("content", "due")),
    )
    for table, columns in sources:
        if not _table_exists(conn, table):
            continue
        if table == "profile":
            for key, value in conn.execute("SELECT key, value FROM profile"):
                if str(key or "") in {"姓名", "名字", "昵称"}:
                    names.extend(_STRUCTURED_NAME.findall(f"{key}:{value or ''}"))
        for column in columns:
            for (text,) in conn.execute(f"SELECT {column} FROM {table}"):
                for pattern in (*_NAME_PATTERNS, _STRUCTURED_NAME):
                    names.extend(match.group(1) for match in pattern.finditer(text or ""))
    return names


def _cell(value: object, known_names: list[str]) -> str:
    text = desensitize(str(value or ""), known_names)
    text = re.sub(r"\s+", " ", text).strip().replace("|", "\\|")
    return text[:_MAX_CELL_LENGTH]


def _append_section(lines: list[str], title: str, headers: list[str], rows: list[list[str]]) -> None:
    if not rows:
        return
    lines.extend(("", f"## {title}", "", "| " + " | ".join(headers) + " |"))
    lines.append("|" + "|".join("---" for _ in headers) + "|")
    lines.extend("| " + " | ".join(row) + " |" for row in rows)


def _assert_no_residuals(content: str, session_ids: list[str]) -> None:
    for pattern in _RESIDUAL_PATTERNS:
        if pattern.search(content):
            raise ValueError("残余敏感信息：导出内容仍包含受保护标识")
    for session_id in session_ids:
        if session_id and session_id in content:
            raise ValueError("残余敏感信息：导出内容仍包含原始会话标识")


def export(db_path: Path, out_path: Path) -> int:
    """导出当前或旧版 SQLite 数据库中的脱敏审核样本，返回导出记录数。"""
    with sqlite3.connect(db_path) as conn:
        known_names = _known_names(conn)
        lines = [
            "# 脱敏审核样本（机器自动导出）",
            "",
            "> 导出前已隐藏身份、联系方式、地址、会话标识与精确时间。",
            "> 本样本仅用于竞赛与公开发布前的合规审核，不提供真实数据库。",
        ]
        exported = 0
        session_labels: dict[str, str] = {}
        session_ids: list[str] = []

        def session_label(session_id: str) -> str:
            if session_id not in session_labels:
                session_labels[session_id] = f"会话{chr(ord('A') + len(session_labels))}"
                session_ids.append(session_id)
            return session_labels[session_id]

        if _table_exists(conn, "conversations"):
            rows = conn.execute(
                "SELECT session_id, role, user_text, bot_text, emotion, mood, anxiety_level, feeling_note "
                "FROM conversations ORDER BY id"
            ).fetchall()
            conversation_rows = []
            for turn, (sid, role, user, bot, emotion, mood, anxiety, note) in enumerate(rows, start=1):
                conversation_rows.append([
                    str(turn),
                    session_label(sid or ""),
                    _cell(role, known_names),
                    _cell(user, known_names),
                    _cell(bot, known_names),
                    _cell(emotion, known_names),
                    _cell(mood, known_names),
                    _cell(anxiety, known_names),
                    _cell(note, known_names),
                ])
            _append_section(
                lines,
                "对话（脱敏后）",
                ["轮次", "会话", "角色", "用户", "乐飞回复", "情绪", "心情", "焦虑", "快照"],
                conversation_rows,
            )
            exported += len(conversation_rows)

        if _table_exists(conn, "profile"):
            rows = conn.execute("SELECT key, value FROM profile ORDER BY key").fetchall()
            profile_rows = [[_cell(key, known_names), _cell(value, known_names)] for key, value in rows]
            _append_section(lines, "画像（脱敏后）", ["字段", "值"], profile_rows)
            exported += len(profile_rows)

        if _table_exists(conn, "summaries"):
            rows = conn.execute("SELECT session_id, summary FROM summaries ORDER BY session_id").fetchall()
            summary_rows = [
                [session_label(session_id or ""), _cell(summary, known_names)]
                for session_id, summary in rows
            ]
            _append_section(lines, "会话摘要（脱敏后）", ["会话", "摘要"], summary_rows)
            exported += len(summary_rows)

        if _table_exists(conn, "memories"):
            rows = conn.execute("SELECT key, content FROM memories ORDER BY id").fetchall()
            memory_rows = [[_cell(key, known_names), _cell(content, known_names)] for key, content in rows]
            _append_section(lines, "事实记忆（脱敏后）", ["分类", "内容"], memory_rows)
            exported += len(memory_rows)

        if _table_exists(conn, "reminders"):
            rows = conn.execute("SELECT content, due FROM reminders ORDER BY id").fetchall()
            reminder_rows = [
                [_cell(content, known_names), "已隐藏" if due else "未设置"]
                for content, due in rows
            ]
            _append_section(lines, "提醒（脱敏后）", ["内容", "截止时间"], reminder_rows)
            exported += len(reminder_rows)

    content = "\n".join(lines) + "\n"
    _assert_no_residuals(content, session_ids)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return exported


if __name__ == "__main__":
    db = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/lefei.db")
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("脱敏审核样本.md")
    count = export(db, out)
    print(f"已导出 {count} 条脱敏记录到 {out}")
