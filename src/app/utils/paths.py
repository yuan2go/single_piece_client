from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QStandardPaths

APP_NAME = 'single-piece-client'


def app_data_dir() -> Path:
    base = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation))
    path = base / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def app_log_dir() -> Path:
    path = app_data_dir() / 'logs'
    path.mkdir(parents=True, exist_ok=True)
    return path
