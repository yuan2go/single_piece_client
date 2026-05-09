from __future__ import annotations

from single_piece_qml_client.adapters.contracts import ControlCommandResponse, PlcAdapter


class ControlService:
    def __init__(self, plc: PlcAdapter) -> None:
        self.plc = plc

    def start_device(self) -> ControlCommandResponse:
        return self.plc.start()

    def stop_device(self) -> ControlCommandResponse:
        return self.plc.stop()
