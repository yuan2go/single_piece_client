from __future__ import annotations

import json
from pathlib import Path

from app.adapters.algo_config_renderer import AlgoConfigRenderer
from app.domain.models.runtime_config import RuntimeConfig
from app.utils.atomic_write import atomic_write_text


class ConfigService:
    def __init__(self, renderer: AlgoConfigRenderer) -> None:
        self.renderer = renderer

    def build_runtime_config(
        self,
        site_id: str,
        device_id: str,
        target_directory: Path,
        realtime_directory: Path,
        parameters: dict[str, str | int | float | bool],
    ) -> RuntimeConfig:
        return RuntimeConfig(
            site_id=site_id,
            device_id=device_id,
            target_directory=target_directory,
            realtime_directory=realtime_directory,
            parameters=parameters,
        )

    def render(self, runtime_config: RuntimeConfig) -> str:
        return self.renderer.render(runtime_config)

    def write(self, runtime_config: RuntimeConfig) -> Path:
        path = runtime_config.target_directory / runtime_config.config_filename
        atomic_write_text(path, self.render(runtime_config))
        return path

    def diff_preview(self, runtime_config: RuntimeConfig) -> dict[str, object]:
        return json.loads(self.render(runtime_config))
