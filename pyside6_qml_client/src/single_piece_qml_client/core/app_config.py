from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PlcConfig:
    host: str = "192.168.2.15"
    port: int = 502
    reconnect_enabled: bool = True
    reconnect_interval_seconds: int = 5
    max_retry_count: int = 10
    heartbeat_interval_seconds: int = 5


@dataclass(frozen=True)
class UiConfig:
    title: str = "单件分离控制系统"
    site_name: str = "自动供件产线A"
    device_name: str = "单件分离控制机"
    default_width: int = 1536
    default_height: int = 960
    min_width: int = 1360
    min_height: int = 820
    language: str = "zh-CN"
    unit: str = "m/s"


@dataclass(frozen=True)
class StorageConfig:
    log_retention_days: int = 30
    max_ui_log_rows: int = 300
    enable_wal: bool = True
    busy_timeout_ms: int = 5000


@dataclass(frozen=True)
class AppConfig:
    profile: str = "production"
    demo_mode: bool = True
    ui: UiConfig = field(default_factory=UiConfig)
    plc: PlcConfig = field(default_factory=PlcConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ConfigLoadError(RuntimeError):
    pass


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = base.copy()
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(config_dir: Path) -> AppConfig:
    config_file = config_dir / "app.production.json"
    default = AppConfig().to_dict()
    if not config_file.exists():
        config_file.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")
        return AppConfig()

    try:
        loaded = json.loads(config_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigLoadError(f"配置文件不是合法 JSON: {config_file}") from exc

    merged = _deep_merge(default, loaded)
    return AppConfig(
        profile=str(merged["profile"]),
        demo_mode=bool(merged["demo_mode"]),
        ui=UiConfig(**merged["ui"]),
        plc=PlcConfig(**merged["plc"]),
        storage=StorageConfig(**merged["storage"]),
    )
