from __future__ import annotations

from app.config.client_settings import TcpChannelConfig
from app.domain.models.raw_message import RawMessage
from app.ingest.base import RawMessageCallback


class TcpIngestChannel:
    def __init__(self, config: TcpChannelConfig, algorithm_type: str) -> None:
        self.config = config
        self.algorithm_type = algorithm_type
        self._callback: RawMessageCallback | None = None
        self._started = False

    def set_callback(self, callback: RawMessageCallback) -> None:
        self._callback = callback

    def start(self) -> None:
        self._started = True

    def stop(self) -> None:
        self._started = False

    def ingest_text(self, payload: str) -> None:
        if not self._callback:
            return
        self._callback(
            RawMessage(
                source_type='tcp',
                source_name=f'{self.config.host}:{self.config.port}',
                algorithm_type=self.algorithm_type,
                parser_type=self.config.parser_type,
                payload=payload,
                metadata={'message_mode': self.config.message_mode},
            )
        )
