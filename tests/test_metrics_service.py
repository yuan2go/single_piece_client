from datetime import datetime

from app.domain.models.realtime_record import RealtimeRecord
from app.services.metrics_service import MetricsService


def test_metrics_snapshot_counts_success_and_exception():
    service = MetricsService(window_seconds=60)
    records = [
        RealtimeRecord(timestamp=datetime.now(), item_id='1', device_id='d1', result='success'),
        RealtimeRecord(timestamp=datetime.now(), item_id='2', device_id='d1', result='fail', exception_type='no_read'),
    ]
    snapshot = service.push_records(records)
    assert snapshot.processed_count == 2
    assert snapshot.success_count == 1
    assert snapshot.exception_count == 1
