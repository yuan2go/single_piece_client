from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

from single_piece_qml_client.backend import DemoBackend


def main() -> int:
    app = QGuiApplication(sys.argv)
    app.setApplicationName("单件分离控制系统")
    app.setOrganizationName("single_piece_client")
    QQuickStyle.setStyle("Basic")

    engine = QQmlApplicationEngine()
    backend = DemoBackend()
    engine.rootContext().setContextProperty("backend", backend)

    qml_dir = Path(__file__).resolve().parent / "qml"
    engine.addImportPath(str(qml_dir))
    engine.load(qml_dir / "Main.qml")

    if not engine.rootObjects():
        return 1
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
