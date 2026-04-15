from __future__ import annotations

from datetime import datetime

import psutil

from app.domain.models.system_snapshot import SystemSnapshot


class PsutilAdapter:
    def collect(self) -> SystemSnapshot:
        disk = psutil.disk_usage('/')
        return SystemSnapshot(
            timestamp=datetime.now(),
            cpu_percent=float(psutil.cpu_percent(interval=None)),
            memory_percent=float(psutil.virtual_memory().percent),
            disk_percent=float(disk.percent),
            disk_free_gb=round(disk.free / 1024 / 1024 / 1024, 2),
        )
