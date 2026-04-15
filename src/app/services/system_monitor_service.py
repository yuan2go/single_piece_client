from __future__ import annotations

from app.adapters.psutil_adapter import PsutilAdapter
from app.domain.models.system_snapshot import SystemSnapshot


class SystemMonitorService:
    def __init__(self, adapter: PsutilAdapter) -> None:
        self.adapter = adapter

    def collect(self) -> SystemSnapshot:
        return self.adapter.collect()
