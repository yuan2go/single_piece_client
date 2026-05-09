from __future__ import annotations

from single_piece_qml_client.core.app_config import StorageConfig
from single_piece_qml_client.core.database import Database, migrate
from single_piece_qml_client.services.log_service import LogService
from single_piece_qml_client.services.state_service import StateService, apply_saved_values


def make_database(tmp_path):
    db = Database(tmp_path / "client.db", StorageConfig(max_ui_log_rows=5))
    with db.session() as conn:
        migrate(conn)
    return db


def test_state_service_saves_and_loads_prefixed_rows(tmp_path):
    db = make_database(tmp_path)
    service = StateService(db)

    service.save_prefixed_rows(
        "param",
        [
            {"key": "highestSpeed", "value": "2.20"},
            {"key": "lowestSpeed", "value": "0.10"},
        ],
    )

    assert service.load_prefix("param") == {
        "highestSpeed": "2.20",
        "lowestSpeed": "0.10",
    }


def test_apply_saved_values_keeps_catalog_defaults_when_missing():
    rows = [
        {"key": "highestSpeed", "value": "2.00"},
        {"key": "lowestSpeed", "value": "0.00"},
    ]

    applied = apply_saved_values(rows, {"highestSpeed": "2.50"})

    assert applied[0]["value"] == "2.50"
    assert applied[1]["value"] == "0.00"


def test_log_service_seeds_and_appends_logs(tmp_path):
    db = make_database(tmp_path)
    service = LogService(db, StorageConfig(max_ui_log_rows=5))

    service.seed_if_empty()
    seeded = service.list_recent()

    assert len(seeded) == 5
    assert seeded[0]["trace"]

    row = service.append("信息", "操作日志", "系统管理", "单元测试", "pytest", "成功", "测试日志写入")
    recent = service.list_recent()

    assert recent[0]["trace"] == row["trace"]
    assert recent[0]["content"] == "单元测试"
