from __future__ import annotations

import logging
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
    """Application composition root.

    This class wires together configuration loading, ingest channels,
    parsing, metrics, and system monitoring. When you want to understand
    the runtime boot process, this is the best file to start with.
    """

    def __init__(self, project_root: Path) -> None:
        self.logger = logging.getLogger(__name__)
        self.project_root = project_root
        profiles_dir = project_root / 'profiles'
        self.logger.info('Initializing app context from project root: %s', project_root)

        self.client_settings = ClientSettingsLoader().load(profiles_dir / 'client_settings.json')
        self.logger.info(
            'Loaded client settings: site=%s device=%s algorithm=%s channels=%s',
            self.client_settings.site_id,
            self.client_settings.device_id,
            self.client_settings.selected_algorithm,
            self.client_settings.ingest.enabled_channels,
        )

        self.algorithm_settings = AlgorithmSettingsLoader().load(
            profiles_dir / 'algorithms' / f'{self.client_settings.selected_algorithm}.json'
        )
        self.logger.info(
            'Loaded algorithm settings: type=%s name=%s output_dir=%s parser=%s',
            self.algorithm_settings.algorithm_type,
            self.algorithm_settings.algorithm_name,
            self.algorithm_settings.config_output_dir,
            self.algorithm_settings.parser_type,
        )

        self.algorithm_config_service = AlgorithmConfigService()
        self.parser_registry = ParserRegistry()
        self.metrics_service = MetricsService(window_seconds=60)
        self.ingest_pipeline_service = IngestPipelineService(self.parser_registry, self.metrics_service)
        self.system_monitor_service = SystemMonitorService(PsutilAdapter())
        self.channel_manager = ChannelManager(self.client_settings, self.algorithm_settings)
        built_channels = self.channel_manager.build_channels()
        self.logger.info('Built %d ingest channels: %s', len(built_channels), self.channel_manager.enabled_channel_names())
        self.channel_manager.set_callback(self.ingest_pipeline_service.handle_raw_message)

    def start(self) -> None:
        self.logger.info('Starting all ingest channels')
        self.channel_manager.start_all()

    def stop(self) -> None:
        self.logger.info('Stopping all ingest channels')
        self.channel_manager.stop_all()

    def inject_sample_event(self) -> None:
        """Inject a synthetic event through the first available channel.

        Useful for local UI verification when the real algorithm process is not running.
        """
        payload = (
            '{"timestamp": "2026-04-15T12:00:00", '
            '"item_id": "sample-001", '
            f'"device_id": "{self.client_settings.device_id}", '
            '"result": "success", '
            '"process_time_ms": 42}'
        )
        self.logger.info('Injecting sample event for local verification')
        self.channel_manager.inject_sample(payload)
