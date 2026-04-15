from __future__ import annotations

from app.config.client_settings import UnixSocketChannelConfig
from app.domain.models.raw_message import RawMessage
from app.ingest.base import RawMessageCallback


class UnixSocketIngestChannel:
    def __init__(self, config: UnixSocketChannelConfig, algorithm_type: str) -> None:
        self.config = config
        self.algorithm_type = algorithm_type
        self._callback: RawMessageCallback | None = None

    def set_callback(self, callback: RawMessageCallback) -> None:
        self._callback = callback

    def start(self) -> None:
        return None

    def stop(self) -> None:
        return None

    def ingest_text(self, payload: str) -> None:
        if not self._callback:
            return
        self._callback(
            RawMessage(
                source_type='unix_socket',
                source_name=self.config.path,
                algorithm_type=self.algorithm_type,
                parser_type=self.config.parser_type,
                payload=payload,
                metadata={'socket_type': self.config.socket_type},
            )
        )
