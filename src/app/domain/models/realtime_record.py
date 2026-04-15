from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class Parcel(BaseModel):
    speed: float = 0.0
    points: list[list[float]] = Field(default_factory=list)


class RealtimeRecord(BaseModel):
    timestamp: datetime
    item_id: str = 'single-piece-runtime'
    device_id: str = 'unknown'
    result: str = 'running'
    process_time_ms: int = 0
    exception_type: str | None = None
    version: str = '1.0.0'
    parcel_num: int = 0
    realtime_efficiency: float = 0.0
    car_speeds: list[float] = Field(default_factory=list)
    parcels: list[Parcel] = Field(default_factory=list)
