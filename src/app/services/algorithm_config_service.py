from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from app.config.algorithm_settings import BaseAlgorithmSettings
from app.config.client_settings import ClientSettings
from app.utils.atomic_write import atomic_write_text


class AlgorithmConfigService:
    """Build and persist the final algorithm config file.

    This service merges:
    - stable client settings (site/device/channels)
    - algorithm settings (thresholds, parser type, output directory, ...)
    - optional UI override values
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

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
            self.logger.debug('Applying algorithm config overrides: %s', overrides)
        return payload

    def render_json(
        self,
        client_settings: ClientSettings,
        algorithm_settings: BaseAlgorithmSettings,
        overrides: dict[str, Any] | None = None,
    ) -> str:
        payload = self.build_payload(client_settings, algorithm_settings, overrides)
        self.logger.debug('Rendered algorithm config payload keys: %s', sorted(payload.keys()))
        return json.dumps(payload, indent=2, ensure_ascii=False)

    def write(
        self,
        client_settings: ClientSettings,
        algorithm_settings: BaseAlgorithmSettings,
        overrides: dict[str, Any] | None = None,
    ) -> Path:
        output_dir = Path(algorithm_settings.config_output_dir)
        path = output_dir / 'algo_config.json'
        self.logger.info('Writing algorithm config to %s', path)
        atomic_write_text(path, self.render_json(client_settings, algorithm_settings, overrides))
        self.logger.info('Algorithm config written successfully: %s', path)
        return path
