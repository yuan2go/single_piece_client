from __future__ import annotations

import json
from pathlib import Path

from app.config.algorithm_settings import BaseAlgorithmSettings
from app.config.client_settings import ClientSettings
from app.utils.atomic_write import atomic_write_text


class ConfigPersistenceService:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def save_client_settings(self, client_settings: ClientSettings) -> Path:
        path = self.project_root / 'profiles' / 'client_settings.json'
        payload = client_settings.model_dump(mode='json')
        atomic_write_text(path, json.dumps(payload, indent=2, ensure_ascii=False))
        return path

    def save_algorithm_settings(self, client_settings: ClientSettings, algorithm_settings: BaseAlgorithmSettings) -> Path:
        path = self.project_root / 'profiles' / 'algorithms' / f'{client_settings.selected_algorithm}.json'
        payload = algorithm_settings.model_dump(mode='json')
        atomic_write_text(path, json.dumps(payload, indent=2, ensure_ascii=False))
        return path

    def save_all(self, client_settings: ClientSettings, algorithm_settings: BaseAlgorithmSettings) -> tuple[Path, Path]:
        client_path = self.save_client_settings(client_settings)
        algo_path = self.save_algorithm_settings(client_settings, algorithm_settings)
        return client_path, algo_path
