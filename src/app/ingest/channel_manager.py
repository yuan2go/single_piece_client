from __future__ import annotations

from app.config.client_settings import ClientSettings
from app.domain.models.raw_message import RawMessage
from app.ingest.base import RawMessageCallback
from app.ingest.file_channel import FileIngestChannel
from app.ingest.tcp_channel import TcpIngestChannel


class ChannelManager:
    def __init__(self, settings: ClientSettings) -> None:
        self.settings = settings
        self.channels: list[object] = []

    def build_channels(self) -> list[object]:
        channels: list[object] = []
        algorithm_type = self.settings.selected_algorithm
        enabled = set(self.settings.ingest.enabled_channels)
        if 'file' in enabled and self.settings.ingest.file.enabled:
            channels.append(FileIngestChannel(self.settings.ingest.file, algorithm_type))
        if 'tcp' in enabled and self.settings.ingest.tcp.enabled:
            channels.append(TcpIngestChannel(self.settings.ingest.tcp, algorithm_type))
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
