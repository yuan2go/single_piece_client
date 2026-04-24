from datetime import datetime

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.pages.config_page import ConfigPage
from app.pages.monitor_page import MonitorPage


class NavButton(QPushButton):
    def __init__(self, text: str, active: bool = False, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(104)
        self.setCheckable(True)
        self.setChecked(active)
        self.setProperty('active', active)
        self.refresh_style()

    def set_active(self, active: bool) -> None:
        self.setChecked(active)
        self.setProperty('active', active)
        self.refresh_style()

    def refresh_style(self) -> None:
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('单件分离高速分拣系统')
        self.resize(1720, 980)
        self.setMinimumSize(1500, 880)

        self.monitor_page = MonitorPage()
        self.config_page = ConfigPage()

        self._build_ui()
        self._connect_signals()
        self._start_timer()
        self.switch_page(0)

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_sidebar())
        root_layout.addWidget(self._build_main_area(), 1)

    def _build_sidebar(self) -> QWidget:
        sidebar = QFrame()
        sidebar.setObjectName('sidebar')
        sidebar.setFixedWidth(122)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        logo = QFrame()
        logo.setObjectName('sidebarLogo')
        logo.setFixedHeight(72)
        logo_layout = QHBoxLayout(logo)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(0)

        icon = QLabel('⬢')
        icon.setObjectName('sidebarIconLogo')
        icon.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(icon)
        layout.addWidget(logo)

        nav_wrap = QWidget()
        nav_layout = QVBoxLayout(nav_wrap)
        nav_layout.setContentsMargins(10, 10, 10, 10)
        nav_layout.setSpacing(12)

        self.btn_monitor = NavButton('🖥\n实时监控', True)
        self.btn_config = NavButton('⚙\n参数配置', False)
        nav_layout.addWidget(self.btn_monitor)
        nav_layout.addWidget(self.btn_config)
        nav_layout.addStretch()
        layout.addWidget(nav_wrap, 1)

        footer = QFrame()
        footer.setObjectName('sidebarFooter')
        footer.setFixedHeight(76)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(0)
        menu_icon = QLabel('☰')
        menu_icon.setObjectName('sidebarFooterMenu')
        menu_icon.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(menu_icon)
        layout.addWidget(footer)

        return sidebar

    def _build_main_area(self) -> QWidget:
        wrap = QWidget()
        layout = QVBoxLayout(wrap)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_top_bar())

        self.stack = QStackedWidget()
        self.stack.addWidget(self.monitor_page)
        self.stack.addWidget(self.config_page)
        layout.addWidget(self.stack, 1)

        return wrap

    def _build_top_bar(self) -> QWidget:
        top = QFrame()
        top.setObjectName('topBar')
        top.setFixedHeight(74)

        layout = QHBoxLayout(top)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(12)

        self.app_title = QLabel('单件分离高速分拣系统')
        self.app_title.setObjectName('appTopTitle')
        layout.addWidget(self.app_title)
        layout.addStretch()

        layout.addWidget(self._make_chip('● 通讯正常', 'headerChipGreen'))
        layout.addWidget(self._make_chip('◉ 数据库', 'headerChipGreen'))
        layout.addWidget(self._make_chip('▣ PLC 在线', 'headerChipBlue'))
        layout.addWidget(self._make_chip('🔔 3', 'headerChipRed'))
        layout.addWidget(self._make_chip('☾', 'headerChipGray'))
        layout.addWidget(self._make_chip('管理员', 'headerChipGray'))

        time_wrap = QWidget()
        time_layout = QVBoxLayout(time_wrap)
        time_layout.setContentsMargins(6, 0, 0, 0)
        time_layout.setSpacing(2)
        self.time_label = QLabel(self._time_text())
        self.time_label.setObjectName('topTime')
        self.date_label = QLabel(self._date_text())
        self.date_label.setObjectName('topDate')
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.date_label)
        layout.addWidget(time_wrap)

        return top

    def _make_chip(self, text: str, object_name: str) -> QLabel:
        chip = QLabel(text)
        chip.setObjectName(object_name)
        return chip

    def _connect_signals(self) -> None:
        self.btn_monitor.clicked.connect(lambda: self.switch_page(0))
        self.btn_config.clicked.connect(lambda: self.switch_page(1))

    def _start_timer(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000)

    def _tick(self) -> None:
        full_text = self._now_text()
        self.time_label.setText(self._time_text())
        self.date_label.setText(self._date_text())
        self.monitor_page.set_time(full_text)
        self.config_page.set_time(full_text)

    def _now_text(self) -> str:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _time_text(self) -> str:
        return datetime.now().strftime('%H:%M:%S')

    def _date_text(self) -> str:
        return datetime.now().strftime('%Y-%m-%d  星期%w').replace('星期0', '星期日').replace('星期1', '星期一').replace('星期2', '星期二').replace('星期3', '星期三').replace('星期4', '星期四').replace('星期5', '星期五').replace('星期6', '星期六')

    def switch_page(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        self.btn_monitor.set_active(index == 0)
        self.btn_config.set_active(index == 1)
