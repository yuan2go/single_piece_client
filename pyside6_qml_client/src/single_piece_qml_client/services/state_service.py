from __future__ import annotations

from datetime import datetime
from typing import Any

from single_piece_qml_client.core.database import Database


def _now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class StateService:
    """Persist UI-editable parameter and setting values into SQLite key-value storage."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def save_prefixed_rows(self, prefix: str, rows: list[dict[str, Any]]) -> None:
        now = _now_text()
        with self.database.session() as conn:
            for row in rows:
                key = str(row.get("key", "")).strip()
                if not key:
                    continue
                value = str(row.get("value", ""))
                conn.execute(
                    "INSERT OR REPLACE INTO kv(key, value, updated_at) VALUES(?, ?, ?)",
                    (f"{prefix}.{key}", value, now),
                )

    def load_prefix(self, prefix: str) -> dict[str, str]:
        like_expr = f"{prefix}.%"
        with self.database.session() as conn:
            rows = conn.execute("SELECT key, value FROM kv WHERE key LIKE ?", (like_expr,)).fetchall()
        return {str(row["key"]).split(".", 1)[1]: str(row["value"]) for row in rows}


def apply_saved_values(rows: list[dict[str, Any]], saved: dict[str, str]) -> list[dict[str, Any]]:
    applied: list[dict[str, Any]] = []
    for row in rows:
        item = row.copy()
        key = str(item.get("key", ""))
        if key in saved:
            item["value"] = saved[key]
        applied.append(item)
    return applied
