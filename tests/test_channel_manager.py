from app.config.client_settings import ClientSettings
from app.ingest.channel_manager import ChannelManager


def test_channel_manager_builds_enabled_channels():
    settings = ClientSettings.model_validate(
        {
            'selected_algorithm': 'default_algorithm',
            'ingest': {
                'enabled_channels': ['file', 'tcp', 'http'],
                'file': {'enabled': True, 'parser_type': 'jsonl_default'},
                'tcp': {'enabled': True, 'parser_type': 'tcp_json_default'},
                'http': {'enabled': True, 'parser_type': 'http_json_default'},
            },
        }
    )
    manager = ChannelManager(settings, 'default')
    channels = manager.build_channels()
    assert len(channels) == 3
