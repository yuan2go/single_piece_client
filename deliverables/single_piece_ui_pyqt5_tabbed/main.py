import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from app.main_window import MainWindow


def load_stylesheet() -> str:
    with open('app/styles.qss', 'r', encoding='utf-8') as f:
        return f.read()


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
