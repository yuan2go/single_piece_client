from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class DeviceProfile(BaseModel):
    device_id: str
    device_name: str
    device_type: str = 'single_piece_separator'
    config_output_dir: Path
    realtime_input_dir: Path
    result_format: str = 'jsonl'
    throughput_window_seconds: int = 60
    efficiency_target: float = 0.92
    extra: dict[str, Any] = Field(default_factory=dict)


class SiteProfile(BaseModel):
    site_id: str
    site_name: str
    description: str = ''
    devices: list[DeviceProfile]
