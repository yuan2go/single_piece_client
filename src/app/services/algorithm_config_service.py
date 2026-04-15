from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.config.algorithm_settings import BaseAlgorithmSettings
from app.config.client_settings import ClientSettings
from app.utils.atomic_write import atomic_write_text


class AlgorithmConfigService:
    def build_payload(
        self,
        client_settings: ClientSettings,
        algorithm_settings: BaseAlgorithmSettings,
        overrides: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = algorithm_settings.model_dump(mode='json')
        payload['site_id'] = client_settings.site_id
        payload['device_id'] = client_settings.device_id
        payload['ingest_channels'] = client_settings.ingest.enabled_channels
        if overrides:
            payload.update(overrides)
        return payload

    def render_json(
        self,
        client_settings: ClientSettings,
        algorithm_settings: BaseAlgorithmSettings,
        overrides: dict[str, Any] | None = None,
    ) -> str:
        return json.dumps(
            self.build_payload(client_settings, algorithm_settings, overrides),
            indent=2,
            ensure_ascii=False,
        )

    def write(
        self,
        client_settings: ClientSettings,
        algorithm_settings: BaseAlgorithmSettings,
        overrides: dict[str, Any] | None = None,
    ) -> Path:
        output_dir = Path(algorithm_settings.config_output_dir)
        path = output_dir / 'algo_config.json'
        atomic_write_text(path, self.render_json(client_settings, algorithm_settings, overrides))
        return path
