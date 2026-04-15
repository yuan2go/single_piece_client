from app.domain.models.raw_message import RawMessage
from app.parsers.registry import ParserRegistry


def test_parser_registry_parses_json_message():
    registry = ParserRegistry()
    message = RawMessage(
        source_type='tcp',
        source_name='127.0.0.1:9101',
        algorithm_type='default',
        parser_type='json_default',
        payload='{"timestamp": "2026-04-15T12:00:00", "item_id": "i1", "device_id": "d1", "result": "success"}',
    )
    records = registry.parse(message)
    assert len(records) == 1
    assert records[0].item_id == 'i1'
    assert records[0].result == 'success'
