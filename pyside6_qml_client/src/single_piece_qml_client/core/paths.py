from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppPaths:
    project_root: Path
    runtime_dir: Path
    config_dir: Path
    log_dir: Path
    database_path: Path
    qml_main: Path


def _env_path(name: str, default: Path) -> Path:
    value = os.environ.get(name)
    return Path(value) if value else default


def resolve_paths() -> AppPaths:
    project_root = Path(__file__).resolve().parents[3]
    runtime_dir = _env_path("SPC_CLIENT_RUNTIME_DIR", project_root / "runtime")
    config_dir = _env_path("SPC_CLIENT_CONFIG_DIR", project_root / "config")
    log_dir = _env_path("SPC_CLIENT_LOG_DIR", runtime_dir / "logs")
    database_path = _env_path("SPC_CLIENT_DB", runtime_dir / "single_piece_client.db")
    qml_main = _env_path("SPC_CLIENT_QML_MAIN", project_root / "qml" / "Main.qml")

    for item in (runtime_dir, config_dir, log_dir, database_path.parent):
        item.mkdir(parents=True, exist_ok=True)

    return AppPaths(
        project_root=project_root,
        runtime_dir=runtime_dir,
        config_dir=config_dir,
        log_dir=log_dir,
        database_path=database_path,
        qml_main=qml_main,
    )
