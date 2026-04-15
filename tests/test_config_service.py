from pathlib import Path

from app.adapters.algo_config_renderer import AlgoConfigRenderer
from app.services.config_service import ConfigService


def test_config_write(tmp_path: Path):
    service = ConfigService(AlgoConfigRenderer())
    runtime = service.build_runtime_config(
        site_id='site1',
        device_id='dev1',
        target_directory=tmp_path / 'config',
        realtime_directory=tmp_path / 'realtime',
        parameters={'threshold': 0.9},
    )
    path = service.write(runtime)
    assert path.exists()
    assert '"site_id": "site1"' in path.read_text(encoding='utf-8')
