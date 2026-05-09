from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from single_piece_qml_client.core.app_config import StorageConfig


class DatabaseError(RuntimeError):
    pass


class Database:
    """SQLite connection factory for edge-side industrial clients."""

    def __init__(self, db_path: Path, storage: StorageConfig) -> None:
        self.db_path = db_path
        self.storage = storage
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            self.db_path,
            timeout=self.storage.busy_timeout_ms / 1000,
            check_same_thread=False,
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(f"PRAGMA busy_timeout = {self.storage.busy_timeout_ms}")
        if self.storage.enable_wal:
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
        return conn

    @contextmanager
    def session(self) -> Iterator[sqlite3.Connection]:
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except sqlite3.Error as exc:
            conn.rollback()
            raise DatabaseError(str(exc)) from exc
        finally:
            conn.close()


def migrate(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations(
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL,
            level TEXT NOT NULL,
            type TEXT NOT NULL,
            module TEXT NOT NULL,
            content TEXT NOT NULL,
            operator TEXT NOT NULL,
            result TEXT NOT NULL,
            trace TEXT NOT NULL,
            detail TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_logs_time ON logs(time);
        CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level);
        CREATE INDEX IF NOT EXISTS idx_logs_module ON logs(module);

        CREATE TABLE IF NOT EXISTS kv(
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
    )
    conn.execute(
        "INSERT OR IGNORE INTO schema_migrations(version, name) VALUES(1, 'initial_schema')"
    )
    conn.commit()
