from __future__ import annotations

import pytest
from PySide6.QtCore import QCoreApplication

from single_piece_qml_client.backend import DemoBackend


@pytest.fixture(scope="module")
def qt_app() -> QCoreApplication:
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    return app


def test_offline_start_is_rejected(qt_app: QCoreApplication) -> None:
    backend = DemoBackend()

    assert backend.runtime["state"] == "离线"
    assert backend.runtime["canStart"] is False

    backend.requestStart()

    assert backend.runtime["state"] == "离线"
    assert backend.events[0]["level"] == "操作"
    assert "启动被拒绝" in backend.events[0]["message"]


def test_reconnect_enables_standby_start(qt_app: QCoreApplication) -> None:
    backend = DemoBackend()

    backend.reconnect()

    assert backend.runtime["state"] == "待机"
    assert backend.runtime["plcState"] == "在线"
    assert backend.runtime["cabinetState"] == "在线"
    assert backend.runtime["canStart"] is True
    assert backend.runtime["canSaveParameter"] is True


def test_save_parameter_is_blocked_when_running(qt_app: QCoreApplication) -> None:
    backend = DemoBackend()
    backend.reconnect()
    backend._apply_runtime_state(backend.__class__.__mro__[0].__dict__["__annotations__"] if False else __import__("single_piece_qml_client.backend", fromlist=["RuntimeState"]).RuntimeState.RUNNING)

    assert backend.runtime["canSaveParameter"] is False

    backend.saveParameters()

    assert "保存参数被拒绝" in backend.events[0]["message"]
