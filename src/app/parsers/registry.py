from __future__ import annotations

import json
import logging
from collections.abc import Callable
from datetime import datetime

from app.domain.models.raw_message import RawMessage
from app.domain.models.realtime_record import Parcel, RealtimeRecord

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
                timestamp=row.get('timestamp', datetime.now().isoformat()),
                item_id=str(row.get('item_id', 'unknown')),
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


def parse_single_piece_realtime(message: RawMessage) -> list[RealtimeRecord]:
    payload = json.loads(message.payload)
    parcels = [
        Parcel(
            speed=float(parcel.get('speed', 0.0)),
            points=[[float(v) for v in point] for point in parcel.get('points', [])],
        )
        for parcel in payload.get('parcels', [])
    ]
    record = RealtimeRecord(
        timestamp=datetime.now(),
        item_id='single-piece-runtime',
        device_id=str(payload.get('deviceId', 'single-piece-device')),
        result='running',
        version=str(payload.get('version', '1.0.0')),
        parcel_num=int(payload.get('parcelNum', 0)),
        realtime_efficiency=float(payload.get('efficiency', 0) or 0),
        car_speeds=[float(v) for v in payload.get('car_speeds', [])],
        parcels=parcels,
    )
    return [record]


class ParserRegistry:
    """Resolve a parser function by parser_type."""

    def __init__(self) -> None:
        self._parsers: dict[str, ParserFunc] = {
            'json_default': parse_json_default,
            'jsonl_default': parse_jsonl_default,
            'single_piece_realtime': parse_single_piece_realtime,
            'tcp_json_default': parse_single_piece_realtime,
            'http_json_default': parse_single_piece_realtime,
            'unix_json_default': parse_single_piece_realtime,
            'zmq_json_default': parse_single_piece_realtime,
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
