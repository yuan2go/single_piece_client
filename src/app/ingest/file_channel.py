from __future__ import annotations

import logging
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from app.config.client_settings import FileChannelConfig
from app.domain.models.raw_message import RawMessage
from app.ingest.base import RawMessageCallback


class _FileEventHandler(FileSystemEventHandler):
    def __init__(self, channel: "FileIngestChannel") -> None:
        super().__init__()
        self.channel = channel

    def on_created(self, event: FileSystemEvent) -> None:
        self.channel.handle_path(Path(event.src_path), is_directory=event.is_directory)

    def on_modified(self, event: FileSystemEvent) -> None:
        self.channel.handle_path(Path(event.src_path), is_directory=event.is_directory)


class FileIngestChannel:
    """Watch a file or directory and emit incremental text chunks as RawMessage."""

    def __init__(self, config: FileChannelConfig, algorithm_type: str) -> None:
        self.config = config
        self.algorithm_type = algorithm_type
        self._callback: RawMessageCallback | None = None
        self._observer: Observer | None = None
        self._logger = logging.getLogger(__name__)
        self._offsets: dict[Path, int] = {}

    def set_callback(self, callback: RawMessageCallback) -> None:
        self._callback = callback

    def start(self) -> None:
        base_path = Path(self.config.path)
        self._logger.info('Starting file channel: mode=%s path=%s pattern=%s', self.config.watch_mode, base_path, self.config.file_pattern)
        if self.config.watch_mode == 'single_file':
            base_path.parent.mkdir(parents=True, exist_ok=True)
            if base_path.exists():
                self._offsets[base_path] = 0
                self.handle_path(base_path, is_directory=False)
            watch_target = base_path.parent
        else:
            base_path.mkdir(parents=True, exist_ok=True)
            watch_target = base_path
            for path in base_path.glob(self.config.file_pattern):
                self._offsets[path] = 0
                self.handle_path(path, is_directory=False)

        observer = Observer()
        observer.schedule(_FileEventHandler(self), str(watch_target), recursive=self.config.recursive)
        observer.start()
        self._observer = observer
        self._logger.info('File observer started on %s', watch_target)

    def stop(self) -> None:
        if self._observer:
            self._logger.info('Stopping file observer')
            self._observer.stop()
            self._observer.join(timeout=2)
            self._observer = None

    def _matches(self, path: Path) -> bool:
        if self.config.watch_mode == 'single_file':
            return path == Path(self.config.path)
        return path.match(self.config.file_pattern)

    def handle_path(self, path: Path, is_directory: bool) -> None:
        if is_directory or not path.exists() or not self._matches(path):
            return
        try:
            previous = self._offsets.get(path, 0)
            with open(path, 'r', encoding='utf-8') as fh:
                fh.seek(previous)
                payload = fh.read()
                self._offsets[path] = fh.tell()
            if payload.strip():
                self._logger.debug('Read %d chars from file %s', len(payload), path)
                self.ingest_text(payload, source_name=str(path))
        except Exception:
            self._logger.exception('Failed to ingest file path %s', path)

    def ingest_text(self, payload: str, source_name: str | None = None) -> None:
        if not self._callback:
            self._logger.warning('File channel received text before callback binding')
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
