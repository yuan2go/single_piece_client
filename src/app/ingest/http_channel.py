from __future__ import annotations

import logging
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from app.config.client_settings import HttpChannelConfig
from app.domain.models.raw_message import RawMessage
from app.ingest.base import RawMessageCallback


class HttpIngestChannel:
    def __init__(self, config: HttpChannelConfig, algorithm_type: str) -> None:
        self.config = config
        self.algorithm_type = algorithm_type
        self._callback: RawMessageCallback | None = None
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None
        self._logger = logging.getLogger(__name__)

    def set_callback(self, callback: RawMessageCallback) -> None:
        self._callback = callback

    def start(self) -> None:
        callback = self._callback
        channel = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                if self.path != channel.config.endpoint:
                    self.send_response(404)
                    self.end_headers()
                    return
                length = int(self.headers.get('Content-Length', '0'))
                payload = self.rfile.read(length).decode('utf-8', errors='ignore')
                if payload and callback:
                    callback(
                        RawMessage(
                            source_type='http',
                            source_name=f'http://{channel.config.host}:{channel.config.port}{channel.config.endpoint}',
                            algorithm_type=channel.algorithm_type,
                            parser_type=channel.config.parser_type,
                            payload=payload,
                        )
                    )
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK')

            def log_message(self, format: str, *args) -> None:  # noqa: A003
                channel._logger.debug('HTTP ingest: ' + format, *args)

        self._server = ThreadingHTTPServer((self.config.host, self.config.port), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, name='http-ingest', daemon=True)
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
                source_type='http',
                source_name=f'http://{self.config.host}:{self.config.port}{self.config.endpoint}',
                algorithm_type=self.algorithm_type,
                parser_type=self.config.parser_type,
                payload=payload,
            )
        )
