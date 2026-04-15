from __future__ import annotations

from pathlib import Path

from app.adapters.psutil_adapter import PsutilAdapter
from app.config.config_loader import AlgorithmSettingsLoader, ClientSettingsLoader
from app.ingest.channel_manager import ChannelManager
from app.parsers.registry import ParserRegistry
from app.services.algorithm_config_service import AlgorithmConfigService
from app.services.ingest_pipeline_service import IngestPipelineService
from app.services.metrics_service import MetricsService
from app.services.system_monitor_service import SystemMonitorService


class AppContext:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        profiles_dir = project_root / 'profiles'
        self.client_settings = ClientSettingsLoader().load(profiles_dir / 'client_settings.json')
        self.algorithm_settings = AlgorithmSettingsLoader().load(
            profiles_dir / 'algorithms' / f'{self.client_settings.selected_algorithm}.json'
        )
        self.algorithm_config_service = AlgorithmConfigService()
        self.parser_registry = ParserRegistry()
        self.metrics_service = MetricsService(window_seconds=60)
        self.ingest_pipeline_service = IngestPipelineService(self.parser_registry, self.metrics_service)
        self.system_monitor_service = SystemMonitorService(PsutilAdapter())
        self.channel_manager = ChannelManager(self.client_settings, self.algorithm_settings)
        self.channel_manager.build_channels()
        self.channel_manager.set_callback(self.ingest_pipeline_service.handle_raw_message)

    def start(self) -> None:
        self.channel_manager.start_all()

    def stop(self) -> None:
        self.channel_manager.stop_all()

    def inject_sample_event(self) -> None:
        payload = (
            '{"timestamp": "2026-04-15T12:00:00", '
            '"item_id": "sample-001", '
            f'"device_id": "{self.client_settings.device_id}", '
            '"result": "success", '
            '"process_time_ms": 42}'
        )
        self.channel_manager.inject_sample(payload)
