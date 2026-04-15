from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from app.config.algorithm_settings import DefaultAlgorithmSettings, RoiAlgorithmSettings
from app.config.client_settings import ClientSettings

logger = logging.getLogger(__name__)


def _load_json(path: Path) -> dict[str, Any]:
    logger.debug('Loading JSON config file: %s', path)
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)


class ClientSettingsLoader:
    """Load stable client-side settings.

    These settings describe how the client itself should run:
    selected site/device, enabled ingest channels, logging level,
    and monitor sampling intervals.
    """

    def load(self, path: Path) -> ClientSettings:
        settings = ClientSettings.model_validate(_load_json(path))
        logger.info('Client settings loaded from %s', path)
        return settings


class AlgorithmSettingsLoader:
    """Load algorithm-specific settings.

    Different algorithms can have different schemas, so we resolve the concrete
    settings model using the `algorithm_type` field inside the file.
    """

    def load(self, path: Path):
        payload = _load_json(path)
        algorithm_type = payload.get('algorithm_type', 'default')
        logger.info('Algorithm settings loading from %s with type=%s', path, algorithm_type)
        if algorithm_type == 'roi':
            return RoiAlgorithmSettings.model_validate(payload)
        return DefaultAlgorithmSettings.model_validate(payload)
