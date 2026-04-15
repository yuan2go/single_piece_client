from pathlib import Path

from app.config.algorithm_settings import DefaultAlgorithmSettings
from app.config.client_settings import ClientSettings
from app.services.algorithm_config_service import AlgorithmConfigService


def test_algorithm_config_service_builds_payload():
    client = ClientSettings.model_validate({'site_id': 's1', 'device_id': 'd1'})
    algo = DefaultAlgorithmSettings(config_output_dir=Path('./runtime/test/config'))
    payload = AlgorithmConfigService().build_payload(client, algo, {'threshold': 0.9})
    assert payload['site_id'] == 's1'
    assert payload['device_id'] == 'd1'
    assert payload['threshold'] == 0.9
