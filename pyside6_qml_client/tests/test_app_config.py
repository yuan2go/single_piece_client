from __future__ import annotations

import json

from single_piece_qml_client.core.app_config import load_config


def test_load_config_creates_default_file(tmp_path):
    config = load_config(tmp_path)

    assert config.profile == "production"
    assert config.ui.title == "单件分离控制系统"
    assert config.storage.max_ui_log_rows == 300
    assert (tmp_path / "app.production.json").exists()


def test_load_config_deep_merges_partial_override(tmp_path):
    (tmp_path / "app.production.json").write_text(
        json.dumps(
            {
                "demo_mode": False,
                "ui": {"site_name": "杭州测试线"},
                "storage": {"max_ui_log_rows": 500},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    config = load_config(tmp_path)

    assert config.demo_mode is False
    assert config.ui.site_name == "杭州测试线"
    assert config.ui.title == "单件分离控制系统"
    assert config.storage.max_ui_log_rows == 500
    assert config.storage.log_retention_days == 30
