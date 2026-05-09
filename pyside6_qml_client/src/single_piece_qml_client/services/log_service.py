from __future__ import annotations

from datetime import datetime
from typing import Any

from single_piece_qml_client.core.app_config import StorageConfig
from single_piece_qml_client.core.database import Database


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class LogService:
    def __init__(self, database: Database, storage: StorageConfig) -> None:
        self.database = database
        self.storage = storage

    def seed_if_empty(self) -> None:
        return

    def list_recent(self) -> list[dict[str, Any]]:
        return []
