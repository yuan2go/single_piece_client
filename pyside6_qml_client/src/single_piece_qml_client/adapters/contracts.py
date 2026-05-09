from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class DeviceHealth(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class CommandResult(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    TIMEOUT = "timeout"
    FAILED = "failed"


@dataclass(frozen=True)
class DeviceSnapshot:
    device_id: str
    name: str
    health: DeviceHealth
    message: str
    latency_ms: int | None = None


@dataclass(frozen=True)
class ControlCommandResponse:
    command: str
    result: CommandResult
    message: str
    trace_id: str


class PlcAdapter(Protocol):
    def read_snapshot(self) -> DeviceSnapshot:
        """Read current PLC health snapshot."""

    def start(self) -> ControlCommandResponse:
        """Send start command to PLC."""

    def stop(self) -> ControlCommandResponse:
        """Send stop command to PLC."""


class CameraAdapter(Protocol):
    def read_snapshot(self) -> DeviceSnapshot:
        """Read current camera subsystem health snapshot."""


class SensorAdapter(Protocol):
    def read_snapshot(self) -> DeviceSnapshot:
        """Read current photoelectric sensor health snapshot."""
