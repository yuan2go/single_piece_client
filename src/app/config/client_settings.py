from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

ChannelType = Literal['file', 'tcp', 'http', 'unix_socket', 'zeromq']


class FileChannelConfig(BaseModel):
    enabled: bool = False
    watch_mode: Literal['directory', 'single_file'] = 'directory'
    path: Path = Path('./runtime/realtime')
    file_pattern: str = '*.jsonl'
    recursive: bool = False
    parser_type: str = 'jsonl_default'


class TcpChannelConfig(BaseModel):
    enabled: bool = False
    host: str = '127.0.0.1'
    port: int = 9101
    message_mode: Literal['line', 'raw'] = 'line'
    parser_type: str = 'tcp_json_default'


class HttpChannelConfig(BaseModel):
    enabled: bool = False
    host: str = '127.0.0.1'
    port: int = 9102
    endpoint: str = '/events'
    parser_type: str = 'http_json_default'


class UnixSocketChannelConfig(BaseModel):
    enabled: bool = False
    path: str = '/tmp/single_piece_algo.sock'
    socket_type: Literal['stream', 'datagram'] = 'stream'
    parser_type: str = 'unix_json_default'


class ZeroMqChannelConfig(BaseModel):
    enabled: bool = False
    mode: Literal['pull', 'sub'] = 'pull'
    endpoint: str = 'tcp://127.0.0.1:5555'
    topic: str = ''
    parser_type: str = 'zmq_json_default'


class IngestSettings(BaseModel):
    enabled_channels: list[ChannelType] = Field(default_factory=list)
    file: FileChannelConfig = Field(default_factory=FileChannelConfig)
    tcp: TcpChannelConfig = Field(default_factory=TcpChannelConfig)
    http: HttpChannelConfig = Field(default_factory=HttpChannelConfig)
    unix_socket: UnixSocketChannelConfig = Field(default_factory=UnixSocketChannelConfig)
    zeromq: ZeroMqChannelConfig = Field(default_factory=ZeroMqChannelConfig)


class MonitorSettings(BaseModel):
    enabled: bool = True
    sample_interval_ms: int = 1000
    monitor_cpu: bool = True
    monitor_memory: bool = True
    monitor_disk: bool = True


class ClientSettings(BaseModel):
    app_name: str = 'single-piece-client'
    site_id: str = 'hz_demo'
    device_id: str = 'spc_01'
    selected_algorithm: str = 'default_algorithm'
    ui_refresh_ms: int = 1000
    log_level: str = 'INFO'
    ingest: IngestSettings = Field(default_factory=IngestSettings)
    monitor: MonitorSettings = Field(default_factory=MonitorSettings)
