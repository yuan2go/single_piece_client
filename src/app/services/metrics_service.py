from __future__ import annotations

import logging
from collections import deque
from datetime import datetime, timedelta

from app.domain.models.realtime_record import RealtimeRecord
from app.domain.models.throughput_metrics import ThroughputMetrics


class MetricsService:
    """Maintain a sliding window of realtime records and compute KPIs."""

    def __init__(self, window_seconds: int = 60) -> None:
        self.logger = logging.getLogger(__name__)
        self.window_seconds = window_seconds
        self._records: deque[RealtimeRecord] = deque()

    def push_records(self, records: list[RealtimeRecord]) -> ThroughputMetrics:
        for record in records:
            self._records.append(record)
        self._trim()
        snapshot = self.snapshot()
        self.logger.debug(
            'Metrics updated: processed=%d success=%d exception=%d throughput=%.2f efficiency=%.4f',
            snapshot.processed_count,
            snapshot.success_count,
            snapshot.exception_count,
            snapshot.throughput_per_min,
            snapshot.efficiency_rate,
        )
        return snapshot

    def _trim(self) -> None:
        threshold = datetime.now() - timedelta(seconds=self.window_seconds)
        removed = 0
        while self._records and self._records[0].timestamp < threshold:
            self._records.popleft()
            removed += 1
        if removed:
            self.logger.debug('Trimmed %d stale records from metrics window', removed)

    def snapshot(self) -> ThroughputMetrics:
        self._trim()
        processed = len(self._records)
        success = sum(1 for r in self._records if r.result.lower() == 'success')
        exception = sum(1 for r in self._records if r.exception_type)
        throughput_per_min = processed * 60 / self.window_seconds if self.window_seconds else 0.0
        efficiency_rate = success / processed if processed else 0.0
        return ThroughputMetrics(
            timestamp=datetime.now(),
            window_seconds=self.window_seconds,
            processed_count=processed,
            success_count=success,
            exception_count=exception,
            throughput_per_min=round(throughput_per_min, 2),
            efficiency_rate=round(efficiency_rate, 4),
        )
