from __future__ import annotations

import logging
import os
import socketserver
import threading

from app.config.client_settings import UnixSocketChannelConfig
from app.domain.models.raw_message import RawMessage
from app.ingest.base import RawMessageCallback


class _ThreadingUnixStreamServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = True


class UnixSocketIngestChannel:
    def __init__(self, config: UnixSocketChannelConfig, algorithm_type: str) -> None:
        self.config = config
        self.algorithm_type = algorithm_type
        self._callback: RawMessageCallback | None = None
        self._server: _ThreadingUnixStreamServer | None = None
        self._thread: threading.Thread | None = None
        self._logger = logging.getLogger(__name__)

    def set_callback(self, callback: RawMessageCallback) -> None:
        self._callback = callback

    def start(self) -> None:
        if os.path.exists(self.config.path):
            os.unlink(self.config.path)
        callback = self._callback
        channel = self

        class Handler(socketserver.StreamRequestHandler):
            def handle(self) -> None:
                payload = self.rfile.read().decode('utf-8', errors='ignore').strip()
                if payload and callback:
                    callback(
                        RawMessage(
                            source_type='unix_socket',
                            source_name=channel.config.path,
                            algorithm_type=channel.algorithm_type,
                            parser_type=channel.config.parser_type,
                            payload=payload,
                            metadata={'socket_type': channel.config.socket_type},
                        )
                    )

        self._server = _ThreadingUnixStreamServer(self.config.path, Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, name='unix-ingest', daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        if os.path.exists(self.config.path):
            os.unlink(self.config.path)
        self._thread = None

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
