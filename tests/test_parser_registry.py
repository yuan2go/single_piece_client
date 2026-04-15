from app.domain.models.raw_message import RawMessage
from app.parsers.registry import ParserRegistry


def test_parser_registry_parses_single_piece_message():
    registry = ParserRegistry()
    message = RawMessage(
        source_type='tcp',
        source_name='127.0.0.1:9101',
        algorithm_type='default',
        parser_type='single_piece_realtime',
        payload='{"version":"1.0.0","efficiency":"0","parcelNum":"1","car_speeds":[0.5,0.5,0.5,0.5],"parcels":[{"speed":2,"points":[[20,30],[160,70],[180,162],[90,183]]}]}',
    )
    records = registry.parse(message)
    assert len(records) == 1
    assert records[0].version == '1.0.0'
    assert records[0].parcel_num == 1
    assert len(records[0].parcels) == 1
