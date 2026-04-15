from __future__ import annotations

from pathlib import Path
from typing import Callable

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class _Handler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[Path], None]) -> None:
        super().__init__()
        self.callback = callback

    def on_created(self, event) -> None:
        if not event.is_directory:
            self.callback(Path(event.src_path))

    def on_modified(self, event) -> None:
        if not event.is_directory:
            self.callback(Path(event.src_path))


class FileWatchAdapter:
    def __init__(self, directory: Path, callback: Callable[[Path], None]) -> None:
        self.directory = directory
        self.callback = callback
        self._observer: Observer | None = None

    def start(self) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        handler = _Handler(self.callback)
        observer = Observer()
        observer.schedule(handler, str(self.directory), recursive=False)
        observer.start()
        self._observer = observer

    def stop(self) -> None:
        if self._observer:
            self._observer.stop()
            self._observer.join(timeout=2)
            self._observer = None
