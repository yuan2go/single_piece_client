from __future__ import annotations

from app.config.algorithm_settings import BaseAlgorithmSettings
from app.config.client_settings import ClientSettings
from app.ingest.base import RawMessageCallback
from app.ingest.file_channel import FileIngestChannel
from app.ingest.http_channel import HttpIngestChannel
from app.ingest.tcp_channel import TcpIngestChannel
from app.ingest.unix_socket_channel import UnixSocketIngestChannel
from app.ingest.zeromq_channel import ZeroMqIngestChannel


class ChannelManager:
    def __init__(self, settings: ClientSettings, algorithm_type: str) -> None:
        self.settings = settings
        self.algorithm_type = algorithm_type
        self.channels: list[object] = []

    def build_channels(self) -> list[object]:
        channels: list[object] = []
        enabled = set(self.settings.ingest.enabled_channels)
        if 'file' in enabled and self.settings.ingest.file.enabled:
            channels.append(FileIngestChannel(self.settings.ingest.file, self.algorithm_type))
        if 'tcp' in enabled and self.settings.ingest.tcp.enabled:
            channels.append(TcpIngestChannel(self.settings.ingest.tcp, self.algorithm_type))
        if 'http' in enabled and self.settings.ingest.http.enabled:
            channels.append(HttpIngestChannel(self.settings.ingest.http, self.algorithm_type))
        if 'unix_socket' in enabled and self.settings.ingest.unix_socket.enabled:
            channels.append(UnixSocketIngestChannel(self.settings.ingest.unix_socket, self.algorithm_type))
        if 'zeromq' in enabled and self.settings.ingest.zeromq.enabled:
            channels.append(ZeroMqIngestChannel(self.settings.ingest.zeromq, self.algorithm_type))
        self.channels = channels
        return channels

    def set_callback(self, callback: RawMessageCallback) -> None:
        for channel in self.channels:
            channel.set_callback(callback)

    def start_all(self) -> None:
        for channel in self.channels:
            channel.start()

    def stop_all(self) -> None:
        for channel in self.channels:
            channel.stop()

    def enabled_channel_names(self) -> list[str]:
        names: list[str] = []
        for channel in self.channels:
            names.append(channel.__class__.__name__)
        return names
