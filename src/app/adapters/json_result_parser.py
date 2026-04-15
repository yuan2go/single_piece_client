from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from app.domain.models.realtime_record import RealtimeRecord


class JsonResultParser:
    def parse_lines(self, path: Path) -> list[RealtimeRecord]:
        records: list[RealtimeRecord] = []
        if not path.exists():
            return records
        with open(path, 'r', encoding='utf-8') as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                payload = json.loads(line)
                records.append(
                    RealtimeRecord(
                        timestamp=datetime.fromisoformat(payload['timestamp']),
                        item_id=str(payload['item_id']),
                        device_id=str(payload['device_id']),
                        result=str(payload['result']),
                        process_time_ms=int(payload.get('process_time_ms', 0)),
                        exception_type=payload.get('exception_type'),
                    )
                )
        return records
