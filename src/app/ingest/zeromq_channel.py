from __future__ import annotations

import logging
import threading
import time

import zmq

from app.config.client_settings import ZeroMqChannelConfig
from app.domain.models.raw_message import RawMessage
from app.ingest.base import RawMessageCallback


class ZeroMqIngestChannel:
    def __init__(self, config: ZeroMqChannelConfig, algorithm_type: str) -> None:
        self.config = config
        self.algorithm_type = algorithm_type
        self._callback: RawMessageCallback | None = None
        self._logger = logging.getLogger(__name__)
        self._context = zmq.Context.instance()
        self._socket: zmq.Socket | None = None
        self._thread: threading.Thread | None = None
        self._running = False

    def set_callback(self, callback: RawMessageCallback) -> None:
        self._callback = callback

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._run, name='zmq-ingest', daemon=True)
        self._thread.start()

    def _run(self) -> None:
        socket_type = zmq.PULL if self.config.mode == 'pull' else zmq.SUB
        sock = self._context.socket(socket_type)
        if self.config.mode == 'sub':
            sock.setsockopt_string(zmq.SUBSCRIBE, self.config.topic)
        sock.bind(self.config.endpoint)
        self._socket = sock
        poller = zmq.Poller()
        poller.register(sock, zmq.POLLIN)
        while self._running:
            events = dict(poller.poll(200))
            if sock in events and events[sock] == zmq.POLLIN:
                payload = sock.recv_string()
                if self._callback:
                    self._callback(
                        RawMessage(
                            source_type='zeromq',
                            source_name=self.config.endpoint,
                            algorithm_type=self.algorithm_type,
                            parser_type=self.config.parser_type,
                            payload=payload,
                            metadata={'mode': self.config.mode, 'topic': self.config.topic},
                        )
                    )
            else:
                time.sleep(0.05)
        sock.close(0)
        self._socket = None

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None

    def ingest_text(self, payload: str) -> None:
        if not self._callback:
            return
        self._callback(
            RawMessage(
                source_type='zeromq',
                source_name=self.config.endpoint,
                algorithm_type=self.algorithm_type,
                parser_type=self.config.parser_type,
                payload=payload,
                metadata={'mode': self.config.mode, 'topic': self.config.topic},
            )
        )
