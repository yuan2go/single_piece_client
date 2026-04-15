from __future__ import annotations

import json
from pathlib import Path

from app.domain.models.site_profile import SiteProfile


class ProfileRepository:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    def list_profiles(self) -> list[SiteProfile]:
        profiles: list[SiteProfile] = []
        for path in sorted(self.base_dir.glob('*.json')):
            with open(path, 'r', encoding='utf-8') as fh:
                payload = json.load(fh)
            profiles.append(SiteProfile.model_validate(payload))
        return profiles
