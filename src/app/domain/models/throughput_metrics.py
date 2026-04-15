from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ThroughputMetrics(BaseModel):
    timestamp: datetime
    window_seconds: int
    processed_count: int
    success_count: int
    exception_count: int
    throughput_per_min: float
    efficiency_rate: float
