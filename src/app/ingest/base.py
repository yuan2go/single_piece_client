from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from app.domain.models.raw_message import RawMessage

RawMessageCallback = Callable[[RawMessage], None]


class IngestChannel(Protocol):
    def set_callback(self, callback: RawMessageCallback) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
