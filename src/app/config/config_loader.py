from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.config.algorithm_settings import DefaultAlgorithmSettings, RoiAlgorithmSettings
from app.config.client_settings import ClientSettings


def _load_json(path: Path) -> dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)


class ClientSettingsLoader:
    def load(self, path: Path) -> ClientSettings:
        return ClientSettings.model_validate(_load_json(path))


class AlgorithmSettingsLoader:
    def load(self, path: Path):
        payload = _load_json(path)
        algorithm_type = payload.get('algorithm_type', 'default')
        if algorithm_type == 'roi':
            return RoiAlgorithmSettings.model_validate(payload)
        return DefaultAlgorithmSettings.model_validate(payload)
