from __future__ import annotations

from app.domain.models.site_profile import DeviceProfile, SiteProfile
from app.repositories.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, repository: ProfileRepository) -> None:
        self.repository = repository
        self._profiles = self.repository.list_profiles()

    @property
    def profiles(self) -> list[SiteProfile]:
        return self._profiles

    def get_site(self, site_id: str) -> SiteProfile:
        for site in self._profiles:
            if site.site_id == site_id:
                return site
        raise KeyError(f'Unknown site_id: {site_id}')

    def get_device(self, site_id: str, device_id: str) -> DeviceProfile:
        site = self.get_site(site_id)
        for device in site.devices:
            if device.device_id == device_id:
                return device
        raise KeyError(f'Unknown device_id: {device_id}')
