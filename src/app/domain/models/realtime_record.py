from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class RealtimeRecord(BaseModel):
    timestamp: datetime
    item_id: str
    device_id: str
    result: str
    process_time_ms: int = 0
    exception_type: str | None = None
