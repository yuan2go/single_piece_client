from __future__ import annotations

import json

from app.domain.models.runtime_config import RuntimeConfig


class AlgoConfigRenderer:
    def render(self, runtime_config: RuntimeConfig) -> str:
        payload = {
            "config_version": runtime_config.config_version,
            "site_id": runtime_config.site_id,
            "device_id": runtime_config.device_id,
            "algorithm_name": runtime_config.algorithm_name,
            "realtime_directory": str(runtime_config.realtime_directory),
            "refresh_interval_ms": runtime_config.refresh_interval_ms,
            "parameters": runtime_config.parameters,
        }
        return json.dumps(payload, indent=2, ensure_ascii=False)
