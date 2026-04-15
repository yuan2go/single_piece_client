from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class SystemSnapshot(BaseModel):
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    disk_free_gb: float
