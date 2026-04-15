from __future__ import annotations

import logging
from pathlib import Path

from app.adapters.file_watch_adapter import FileWatchAdapter
from app.adapters.json_result_parser import JsonResultParser
from app.domain.models.realtime_record import RealtimeRecord


class RealtimeIngestService:
    def __init__(self, parser: JsonResultParser) -> None:
        self.parser = parser
        self._watcher: FileWatchAdapter | None = None
        self._logger = logging.getLogger(__name__)
        self._callbacks = []

    def on_records(self, callback) -> None:
        self._callbacks.append(callback)

    def _emit(self, records: list[RealtimeRecord]) -> None:
        for callback in self._callbacks:
            callback(records)

    def handle_file_change(self, path: Path) -> None:
        try:
            if path.suffix.lower() not in {'.jsonl', '.json'}:
                return
            records = self.parser.parse_lines(path)
            if records:
                self._emit(records)
        except Exception as exc:
            self._logger.exception('Failed to parse realtime file %s: %s', path, exc)

    def start_watch(self, directory: Path) -> None:
        self.stop_watch()
        watcher = FileWatchAdapter(directory, self.handle_file_change)
        watcher.start()
        self._watcher = watcher

    def stop_watch(self) -> None:
        if self._watcher:
            self._watcher.stop()
            self._watcher = None
