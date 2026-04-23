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

from app.pages.monitor_page import MonitorPage
from app.pages.config_page import ConfigPage


class NavButton(QPushButton):
    def __init__(self, text: str, active: bool = False, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(56)
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
        self.resize(1700, 980)
        self.setMinimumSize(1480, 860)

        self.monitor_page = MonitorPage()
        self.config_page = ConfigPage()

        self._build_ui()
        self._connect_signals()
        self._start_timer()

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
        sidebar.setFixedWidth(230)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        logo = QFrame()
        logo.setObjectName('sidebarLogo')
        logo_layout = QHBoxLayout(logo)
        logo_layout.setContentsMargins(20, 18, 20, 18)
        logo_layout.setSpacing(12)

        icon = QLabel('⬢')
        icon.setObjectName('logoIcon')
        title = QLabel('单件分离高速分拣系统')
        title.setObjectName('logoText')
        logo_layout.addWidget(icon)
        logo_layout.addWidget(title)
        layout.addWidget(logo)

        nav_wrap = QWidget()
        nav_layout = QVBoxLayout(nav_wrap)
        nav_layout.setContentsMargins(0, 18, 0, 0)
        nav_layout.setSpacing(8)

        self.btn_monitor = NavButton('🖥  实时监控', True)
        self.btn_config = NavButton('⚙  参数配置', False)
        nav_layout.addWidget(self.btn_monitor)
        nav_layout.addWidget(self.btn_config)
        nav_layout.addStretch()
        layout.addWidget(nav_wrap, 1)

        footer = QFrame()
        footer.setObjectName('sidebarFooter')
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(18, 18, 18, 18)
        footer_layout.setSpacing(12)

        info_card = QFrame()
        info_card.setObjectName('sideInfoCard')
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(14, 14, 14, 14)
        info_layout.setSpacing(8)

        self.state_title = QLabel('系统状态')
        self.state_title.setObjectName('sideInfoTitle')
        self.state_value = QLabel('离线')
        self.state_value.setObjectName('sideInfoOkValue')
        user_title = QLabel('当前用户')
        user_title.setObjectName('sideInfoTitle')
        user_value = QLabel('admin')
        user_value.setObjectName('sideInfoValue')

        info_layout.addWidget(self.state_title)
        info_layout.addWidget(self.state_value)
        info_layout.addSpacing(6)
        info_layout.addWidget(user_title)
        info_layout.addWidget(user_value)

        footer_layout.addWidget(info_card)
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
        top.setFixedHeight(58)

        layout = QHBoxLayout(top)
        layout.setContentsMargins(24, 10, 24, 10)
        layout.setSpacing(12)

        self.page_title = QLabel('实时监控')
        self.page_title.setObjectName('pageTopTitle')
        self.page_note = QLabel('线上生产环境，请谨慎执行启停、清空等操作')
        self.page_note.setObjectName('warningNote')

        layout.addWidget(self.page_title)
        layout.addWidget(self.page_note)
        layout.addStretch()

        layout.addWidget(self._make_chip('● 通讯正常', 'headerChipGreen'))
        layout.addWidget(self._make_chip('● 数据库', 'headerChipGreen'))
        layout.addWidget(self._make_chip('● PLC在线', 'headerChipBlue'))
        layout.addWidget(self._make_chip('🔔 12', 'headerChipRed'))
        layout.addWidget(self._make_chip('☾ 深色', 'headerChipGray'))
        layout.addWidget(self._make_chip('管理员', 'headerChipGray'))

        self.time_label = QLabel(self._now_text())
        self.time_label.setObjectName('topTime')
        layout.addWidget(self.time_label)

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
        text = self._now_text()
        self.time_label.setText(text)
        self.monitor_page.set_time(text)
        self.config_page.set_time(text)

    def _now_text(self) -> str:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def switch_page(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        self.btn_monitor.set_active(index == 0)
        self.btn_config.set_active(index == 1)

        if index == 0:
            self.page_title.setText('实时监控')
            self.page_note.setText('实时监控页面，流向为自上而下')
        else:
            self.page_title.setText('参数配置中心')
            self.page_note.setText('仅在系统离线状态下允许修改并保存参数配置')
