from __future__ import annotations

import uuid

from single_piece_qml_client.adapters.contracts import CommandResult, ControlCommandResponse, DeviceHealth, DeviceSnapshot


class MockPlcAdapter:
    def __init__(self) -> None:
        self._running = True

    def read_snapshot(self) -> DeviceSnapshot:
        return DeviceSnapshot("plc-001", "Siemens S7-1200", DeviceHealth.ONLINE, "PLC mock adapter online", 12)

    def start(self) -> ControlCommandResponse:
        self._running = True
        return ControlCommandResponse("start", CommandResult.ACCEPTED, "设备启动命令已接受", uuid.uuid4().hex[:16])

    def stop(self) -> ControlCommandResponse:
        self._running = False
        return ControlCommandResponse("stop", CommandResult.ACCEPTED, "设备停止命令已接受", uuid.uuid4().hex[:16])


class MockCameraAdapter:
    def read_snapshot(self) -> DeviceSnapshot:
        return DeviceSnapshot("camera-group-001", "Basler camera group", DeviceHealth.ONLINE, "8 cameras online", 18)


class MockSensorAdapter:
    def read_snapshot(self) -> DeviceSnapshot:
        return DeviceSnapshot("sensor-group-001", "Photoelectric sensor group", DeviceHealth.ONLINE, "photoelectric sensors normal", 6)
