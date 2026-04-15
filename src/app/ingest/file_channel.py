from __future__ import annotations

from pathlib import Path

from app.config.client_settings import FileChannelConfig
from app.domain.models.raw_message import RawMessage
from app.ingest.base import RawMessageCallback


class FileIngestChannel:
    def __init__(self, config: FileChannelConfig, algorithm_type: str) -> None:
        self.config = config
        self.algorithm_type = algorithm_type
        self._callback: RawMessageCallback | None = None
        self._started = False

    def set_callback(self, callback: RawMessageCallback) -> None:
        self._callback = callback

    def start(self) -> None:
        self._started = True
        path = Path(self.config.path)
        if self.config.watch_mode == 'single_file':
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path.mkdir(parents=True, exist_ok=True)

    def stop(self) -> None:
        self._started = False

    def ingest_text(self, payload: str, source_name: str | None = None) -> None:
        if not self._callback:
            return
        self._callback(
            RawMessage(
                source_type='file',
                source_name=source_name or str(self.config.path),
                algorithm_type=self.algorithm_type,
                parser_type=self.config.parser_type,
                payload=payload,
                metadata={'watch_mode': self.config.watch_mode, 'file_pattern': self.config.file_pattern},
            )
        )
