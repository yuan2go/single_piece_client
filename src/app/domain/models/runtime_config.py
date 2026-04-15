from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class RuntimeConfig(BaseModel):
    config_version: int = 1
    site_id: str
    device_id: str
    algorithm_name: str = 'default_algo'
    target_directory: Path
    realtime_directory: Path
    config_filename: str = 'algo_config.json'
    refresh_interval_ms: int = 1000
    monitor_cpu: bool = True
    monitor_memory: bool = True
    monitor_disk: bool = True
    max_queue_size: int = 1000
    parameters: dict[str, str | int | float | bool] = Field(default_factory=dict)
