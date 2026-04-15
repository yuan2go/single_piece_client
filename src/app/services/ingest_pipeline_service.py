from __future__ import annotations

import logging
from collections.abc import Callable

from app.domain.models.raw_message import RawMessage
from app.domain.models.realtime_record import RealtimeRecord
from app.domain.models.throughput_metrics import ThroughputMetrics
from app.parsers.registry import ParserRegistry
from app.services.metrics_service import MetricsService

RecordsCallback = Callable[[list[RealtimeRecord], ThroughputMetrics], None]


class IngestPipelineService:
    """Translate raw channel messages into business records and metrics.

    Main data path:
    Channel -> RawMessage -> ParserRegistry -> RealtimeRecord -> Metrics -> UI callbacks
    """

    def __init__(self, parser_registry: ParserRegistry, metrics_service: MetricsService) -> None:
        self.logger = logging.getLogger(__name__)
        self.parser_registry = parser_registry
        self.metrics_service = metrics_service
        self._callbacks: list[RecordsCallback] = []

    def on_records(self, callback: RecordsCallback) -> None:
        self._callbacks.append(callback)
        self.logger.debug('Registered ingest pipeline callback. total=%d', len(self._callbacks))

    def handle_raw_message(self, message: RawMessage) -> None:
        self.logger.debug(
            'Handling raw message: source=%s parser=%s algorithm=%s payload_len=%d',
            message.source_type,
            message.parser_type,
            message.algorithm_type,
            len(message.payload),
        )
        records = self.parser_registry.parse(message)
        if not records:
            self.logger.debug('No records parsed from message source=%s', message.source_type)
            return
        metrics = self.metrics_service.push_records(records)
        self.logger.info(
            'Parsed %d records from %s. throughput=%.2f efficiency=%.2f%%',
            len(records),
            message.source_type,
            metrics.throughput_per_min,
            metrics.efficiency_rate * 100,
        )
        for callback in self._callbacks:
            callback(records, metrics)
