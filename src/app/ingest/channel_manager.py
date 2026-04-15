from __future__ import annotations

import logging

from app.config.algorithm_settings import BaseAlgorithmSettings
from app.config.client_settings import ClientSettings
from app.ingest.base import RawMessageCallback
from app.ingest.file_channel import FileIngestChannel
from app.ingest.http_channel import HttpIngestChannel
from app.ingest.tcp_channel import TcpIngestChannel
from app.ingest.unix_socket_channel import UnixSocketIngestChannel
from app.ingest.zeromq_channel import ZeroMqIngestChannel


class ChannelManager:
    """Create, start, stop, and introspect all enabled ingest channels."""

    def __init__(self, settings: ClientSettings, algorithm_settings: BaseAlgorithmSettings) -> None:
        self.logger = logging.getLogger(__name__)
        self.settings = settings
        self.algorithm_settings = algorithm_settings
        self.channels: list[object] = []

    def build_channels(self) -> list[object]:
        channels: list[object] = []
        enabled = set(self.settings.ingest.enabled_channels)
        algorithm_type = self.algorithm_settings.algorithm_type
        self.logger.info('Building channels for algorithm_type=%s enabled=%s', algorithm_type, sorted(enabled))
        if 'file' in enabled and self.settings.ingest.file.enabled:
            channels.append(FileIngestChannel(self.settings.ingest.file, algorithm_type))
        if 'tcp' in enabled and self.settings.ingest.tcp.enabled:
            channels.append(TcpIngestChannel(self.settings.ingest.tcp, algorithm_type))
        if 'http' in enabled and self.settings.ingest.http.enabled:
            channels.append(HttpIngestChannel(self.settings.ingest.http, algorithm_type))
        if 'unix_socket' in enabled and self.settings.ingest.unix_socket.enabled:
            channels.append(UnixSocketIngestChannel(self.settings.ingest.unix_socket, algorithm_type))
        if 'zeromq' in enabled and self.settings.ingest.zeromq.enabled:
            channels.append(ZeroMqIngestChannel(self.settings.ingest.zeromq, algorithm_type))
        self.channels = channels
        self.logger.info('Built channels: %s', self.enabled_channel_names())
        return channels

    def set_callback(self, callback: RawMessageCallback) -> None:
        for channel in self.channels:
            channel.set_callback(callback)
        self.logger.debug('Bound callback to %d channels', len(self.channels))

    def start_all(self) -> None:
        for channel in self.channels:
            self.logger.info('Starting channel %s', channel.__class__.__name__)
            channel.start()

    def stop_all(self) -> None:
        for channel in self.channels:
            self.logger.info('Stopping channel %s', channel.__class__.__name__)
            channel.stop()

    def enabled_channel_names(self) -> list[str]:
        return [channel.__class__.__name__ for channel in self.channels]

    def inject_sample(self, payload: str) -> None:
        for channel in self.channels:
            ingest = getattr(channel, 'ingest_text', None)
            if callable(ingest):
                self.logger.info('Injecting sample payload through channel %s', channel.__class__.__name__)
                ingest(payload)
                return
        self.logger.warning('No available channel to inject sample payload')
