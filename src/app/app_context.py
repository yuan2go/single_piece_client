from __future__ import annotations

from pathlib import Path

from app.adapters.algo_config_renderer import AlgoConfigRenderer
from app.adapters.json_result_parser import JsonResultParser
from app.adapters.psutil_adapter import PsutilAdapter
from app.repositories.profile_repository import ProfileRepository
from app.services.config_service import ConfigService
from app.services.metrics_service import MetricsService
from app.services.profile_service import ProfileService
from app.services.realtime_ingest_service import RealtimeIngestService
from app.services.system_monitor_service import SystemMonitorService


class AppContext:
    def __init__(self, project_root: Path) -> None:
        profiles_dir = project_root / 'profiles'
        self.profile_service = ProfileService(ProfileRepository(profiles_dir))
        self.config_service = ConfigService(AlgoConfigRenderer())
        self.realtime_ingest_service = RealtimeIngestService(JsonResultParser())
        self.system_monitor_service = SystemMonitorService(PsutilAdapter())
        self.metrics_service = MetricsService(window_seconds=60)
