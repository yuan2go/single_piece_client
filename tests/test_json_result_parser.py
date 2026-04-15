from pathlib import Path

from app.adapters.json_result_parser import JsonResultParser


def test_json_result_parser_reads_jsonl(tmp_path: Path):
    path = tmp_path / 'records.jsonl'
    path.write_text(
        '{"timestamp": "2026-04-15T12:00:00", "item_id": "1", "device_id": "d1", "result": "success"}\n',
        encoding='utf-8',
    )
    parser = JsonResultParser()
    records = parser.parse_lines(path)
    assert len(records) == 1
    assert records[0].item_id == '1'
