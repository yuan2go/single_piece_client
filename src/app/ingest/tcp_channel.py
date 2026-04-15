from __future__ import annotations

import logging
import socketserver
import threading

from app.config.client_settings import TcpChannelConfig
from app.domain.models.raw_message import RawMessage
from app.ingest.base import RawMessageCallback


class _ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


class TcpIngestChannel:
    def __init__(self, config: TcpChannelConfig, algorithm_type: str) -> None:
        self.config = config
        self.algorithm_type = algorithm_type
        self._callback: RawMessageCallback | None = None
        self._server: _ThreadingTCPServer | None = None
        self._thread: threading.Thread | None = None
        self._logger = logging.getLogger(__name__)

    def set_callback(self, callback: RawMessageCallback) -> None:
        self._callback = callback

    def start(self) -> None:
        callback = self._callback
        channel = self

        class Handler(socketserver.BaseRequestHandler):
            def handle(self) -> None:
                chunks: list[str] = []
                while True:
                    data = self.request.recv(4096)
                    if not data:
                        break
                    chunks.append(data.decode('utf-8', errors='ignore'))
                    if channel.config.message_mode == 'line' and '\n' in chunks[-1]:
                        break
                payload = ''.join(chunks).strip()
                if payload and callback:
                    callback(
                        RawMessage(
                            source_type='tcp',
                            source_name=f'{channel.config.host}:{channel.config.port}',
                            algorithm_type=channel.algorithm_type,
                            parser_type=channel.config.parser_type,
                            payload=payload,
                            metadata={'message_mode': channel.config.message_mode},
                        )
                    )

        self._server = _ThreadingTCPServer((self.config.host, self.config.port), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, name='tcp-ingest', daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        self._thread = None

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
