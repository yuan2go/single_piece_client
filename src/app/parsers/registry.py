from __future__ import annotations

import json
import logging
from collections.abc import Callable

from app.domain.models.raw_message import RawMessage
from app.domain.models.realtime_record import RealtimeRecord

ParserFunc = Callable[[RawMessage], list[RealtimeRecord]]
logger = logging.getLogger(__name__)


def parse_json_default(message: RawMessage) -> list[RealtimeRecord]:
    payload = json.loads(message.payload)
    if isinstance(payload, list):
        rows = payload
    else:
        rows = [payload]
    records: list[RealtimeRecord] = []
    for row in rows:
        records.append(
            RealtimeRecord(
                timestamp=row['timestamp'],
                item_id=str(row['item_id']),
                device_id=str(row.get('device_id', 'unknown')),
                result=str(row.get('result', 'unknown')),
                process_time_ms=int(row.get('process_time_ms', 0)),
                exception_type=row.get('exception_type'),
            )
        )
    return records


def parse_jsonl_default(message: RawMessage) -> list[RealtimeRecord]:
    records: list[RealtimeRecord] = []
    for line in message.payload.splitlines():
        line = line.strip()
        if not line:
            continue
        records.extend(parse_json_default(message.model_copy(update={'payload': line})))
    return records


class ParserRegistry:
    """Resolve a parser function by parser_type."""

    def __init__(self) -> None:
        self._parsers: dict[str, ParserFunc] = {
            'json_default': parse_json_default,
            'jsonl_default': parse_jsonl_default,
            'tcp_json_default': parse_json_default,
            'http_json_default': parse_json_default,
            'unix_json_default': parse_json_default,
            'zmq_json_default': parse_json_default,
        }

    def register(self, parser_type: str, parser: ParserFunc) -> None:
        self._parsers[parser_type] = parser
        logger.info('Registered parser type: %s', parser_type)

    def parse(self, message: RawMessage) -> list[RealtimeRecord]:
        if message.parser_type not in self._parsers:
            logger.error('Unknown parser type: %s', message.parser_type)
            raise KeyError(f'Unknown parser type: {message.parser_type}')
        logger.debug('Parsing message with parser type: %s', message.parser_type)
        records = self._parsers[message.parser_type](message)
        logger.debug('Parsed %d records using parser type: %s', len(records), message.parser_type)
        return records
