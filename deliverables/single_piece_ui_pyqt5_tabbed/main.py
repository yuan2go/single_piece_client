from __future__ import annotations

import sys
from pathlib import Path

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from app.main_window import MainWindow


BASE_DIR = Path(__file__).resolve().parent
STYLE_FILE = BASE_DIR / 'app' / 'styles.qss'


def load_stylesheet() -> str:
    return STYLE_FILE.read_text(encoding='utf-8')


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setFont(QFont('Microsoft YaHei', 10))
    app.setStyleSheet(load_stylesheet())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
