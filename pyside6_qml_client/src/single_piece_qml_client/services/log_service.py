from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime
from typing import Any

from single_piece_qml_client.core.app_config import StorageConfig
from single_piece_qml_client.core.database import Database
from single_piece_qml_client.domain.catalogs import initial_logs


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class LogService:
    def __init__(self, database: Database, storage: StorageConfig) -> None:
        self.database = database
        self.storage = storage

    def seed_if_empty(self) -> None:
        with self.database.session() as conn:
            if conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]:
                return
            samples = initial_logs()
            for index in range(36):
                level, category, module, content, operator, result, detail = samples[index % len(samples)]
                self._insert_row(conn, level, category, module, content, operator, result, detail)

    def list_recent(self) -> list[dict[str, Any]]:
        with self.database.session() as conn:
            sql = "SELECT time, level, type, module, content, operator, result, trace, detail FROM logs ORDER BY id DESC LIMIT ?"
            rows = conn.execute(sql, (self.storage.max_ui_log_rows,)).fetchall()
        return [dict(row) for row in rows]

    def append(self, level: str, category: str, module: str, content: str, operator: str, result: str, detail: str) -> dict[str, Any]:
        with self.database.session() as conn:
            return self._insert_row(conn, level, category, module, content, operator, result, detail)

    @staticmethod
    def _insert_row(
        conn: sqlite3.Connection,
        level: str,
        category: str,
        module: str,
        content: str,
        operator: str,
        result: str,
        detail: str,
    ) -> dict[str, Any]:
        row = {
            "time": now_text(),
            "level": level,
            "type": category,
            "module": module,
            "content": content,
            "operator": operator,
            "result": result,
            "trace": uuid.uuid4().hex[:16],
            "detail": detail,
        }
        sql = "INSERT INTO logs(time, level, type, module, content, operator, result, trace, detail) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
        conn.execute(
            sql,
            (
                row["time"],
                row["level"],
                row["type"],
                row["module"],
                row["content"],
                row["operator"],
                row["result"],
                row["trace"],
                row["detail"],
            ),
        )
        return row
