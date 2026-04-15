from __future__ import annotations

from collections.abc import Callable

from app.domain.models.raw_message import RawMessage
from app.domain.models.realtime_record import RealtimeRecord
from app.domain.models.throughput_metrics import ThroughputMetrics
from app.parsers.registry import ParserRegistry
from app.services.metrics_service import MetricsService

RecordsCallback = Callable[[list[RealtimeRecord], ThroughputMetrics], None]


class IngestPipelineService:
    def __init__(self, parser_registry: ParserRegistry, metrics_service: MetricsService) -> None:
        self.parser_registry = parser_registry
        self.metrics_service = metrics_service
        self._callbacks: list[RecordsCallback] = []

    def on_records(self, callback: RecordsCallback) -> None:
        self._callbacks.append(callback)

    def handle_raw_message(self, message: RawMessage) -> None:
        records = self.parser_registry.parse(message)
        metrics = self.metrics_service.push_records(records)
        for callback in self._callbacks:
            callback(records, metrics)
