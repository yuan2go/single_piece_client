from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from app.app_context import AppContext
from app.ui.main_window import MainWindow
from app.utils.exception_handler import ExceptionHandler
from app.utils.logging_helper import configure_logging


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> int:
    configure_logging()
    app = QApplication(sys.argv)
    ExceptionHandler().install()
    context = AppContext(project_root())
    window = MainWindow(context)
    window.show()
    return app.exec()


if __name__ == '__main__':
    raise SystemExit(main())
