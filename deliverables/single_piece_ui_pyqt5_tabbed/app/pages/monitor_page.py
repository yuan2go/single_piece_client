from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.widgets.common import block_card, metric_tile
from app.widgets.flow_widgets import ArrowDown, CacheGrid, LegendRow, ProcessStage


class MonitorPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.time_value = '2026-04-23 16:52:13'
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(16)

        root.addWidget(self._build_left_panel(), 4)
        root.addWidget(self._build_center_panel(), 4)
        root.addWidget(self._build_right_panel(), 4)

    def set_time(self, text: str):
        self.time_value = text
        self.time_label.setText(text)

    def _build_left_panel(self) -> QWidget:
        card, layout = block_card('实时跟踪画面（方向：自上而下）')
        layout.setSpacing(10)

        layout.addWidget(ProcessStage('供包皮带线', '0.62 m/s', '#D8A24B'))
        layout.addWidget(ArrowDown())
        layout.addWidget(ProcessStage('滑槽', '0.48 m/s', '#D8A24B'))
        layout.addWidget(ArrowDown())
        layout.addWidget(ProcessStage('缓存1皮带线', '0.56 m/s', '#59d64f'))
        layout.addWidget(ArrowDown())
        layout.addWidget(ProcessStage('缓存2皮带线', '0.58 m/s', '#59d64f'))
        layout.addWidget(ArrowDown())
        layout.addWidget(CacheGrid())
        layout.addWidget(ArrowDown())
        layout.addWidget(ProcessStage('居中机', '0.50 m/s', '#59d64f'))
        layout.addWidget(ArrowDown())
        layout.addWidget(ProcessStage('剔除机', '0.52 m/s', '#ff5f57', icon_text='✕'))
        layout.addWidget(ArrowDown())
        layout.addWidget(ProcessStage('供包台', '0.00 m/s', '#8fa3b9', status_color='#39d353', icon_text=''))
        layout.addWidget(LegendRow())

        return card

    def _build_center_panel(self) -> QWidget:
        wrap = QWidget()
        layout = QVBoxLayout(wrap)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        status_card = QFrame()
        status_card.setObjectName('monitorBlock')
        s_layout = QVBoxLayout(status_card)
        s_layout.setContentsMargins(16, 14, 16, 14)
        s_layout.setSpacing(12)

        warn = QLabel('⚠  线上生产环境，请谨慎执行启停、清空等操作！')
        warn.setObjectName('warningBanner')
        s_layout.addWidget(warn)

        row = QHBoxLayout()
        row.setSpacing(24)
        t1 = QLabel('当前状态：')
        t1.setObjectName('monitorMetaTitle')
        v1 = QLabel('离线')
        v1.setObjectName('monitorMetaOk')
        t2 = QLabel('运行模式：')
        t2.setObjectName('monitorMetaTitle')
        v2 = QLabel('模式一')
        v2.setObjectName('monitorMetaOk')
        row.addWidget(t1)
        row.addWidget(v1)
        row.addSpacing(12)
        row.addWidget(t2)
        row.addWidget(v2)
        row.addStretch()
        s_layout.addLayout(row)

        self.time_label = QLabel(self.time_value)
        self.time_label.setObjectName('bigDigitalTime')
        self.time_label.setAlignment(Qt.AlignCenter)
        s_layout.addWidget(self.time_label)
        layout.addWidget(status_card)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)
        for text, object_name in [('▶ 开启（模式一）', 'controlBtnBlue'), ('■ 停止', 'controlBtnRed'), ('⇄ 切换（模式二）', 'controlBtnBlue')]:
            btn = QLabel(text)
            btn.setObjectName(object_name)
            btn.setAlignment(Qt.AlignCenter)
            btn.setMinimumHeight(48)
            button_row.addWidget(btn)
        layout.addLayout(button_row)

        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(14)
        kpi_row.addWidget(metric_tile('包裹总数', '0', '件'))
        kpi_row.addWidget(metric_tile('小时效率', '0', '件/小时'))
        kpi_row.addWidget(metric_tile('稼动率（OEE）', '0.0', '%', 'monitorMetricValueOrange'))
        layout.addLayout(kpi_row)

        info_card, info_layout = block_card('设备信息')
        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(10)
        left = [
            ('场地：', '场地名称1'),
            ('CPU利用率：', '30.7 %'),
            ('内存利用率：', '95.5 %'),
            ('磁盘利用率：', '15.8 %'),
            ('算法版本：', '1.0.3'),
            ('客户端版本号：', 'A1.0.0'),
            ('普通件拉包间距（mm）：', '700.0'),
            ('易滑件拉包间距（mm）：', '1000.0'),
            ('电柜状态：', '离线'),
        ]
        for i, (k, v) in enumerate(left):
            key = QLabel(k)
            key.setObjectName('deviceInfoKey')
            val = QLabel(v)
            val.setObjectName('deviceInfoValueGreen' if i in (0, 8) else 'deviceInfoValue')
            grid.addWidget(key, i, 0)
            grid.addWidget(val, i, 1)
        info_layout.addLayout(grid)
        layout.addWidget(info_card)
        return wrap

    def _metric_box(self, title: str, items: list[tuple[str, str]]) -> QWidget:
        card = QFrame()
        card.setObjectName('monitorStatCard')
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(12)

        title_lb = QLabel(title)
        title_lb.setObjectName('rightSectionTitle')
        layout.addWidget(title_lb)

        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(12)
        for i, (k, v) in enumerate(items):
            key = QLabel(k)
            key.setObjectName('statKey')
            val = QLabel(v)
            val.setObjectName('statValue')
            grid.addWidget(key, i // 2, (i % 2) * 2)
            grid.addWidget(val, i // 2, (i % 2) * 2 + 1)
        layout.addLayout(grid)
        return card

    def _build_right_panel(self) -> QWidget:
        wrap = QWidget()
        layout = QVBoxLayout(wrap)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        title_card, title_layout = block_card('分离数据（左）')
        title_layout.setSpacing(14)
        title_layout.addWidget(self._metric_box('主线数据', [
            ('包裹总数', '0 件'), ('平均包裹长度', '0 mm'),
            ('最小包裹长度', '0 mm'), ('最小包裹数量', '0 件/小时'),
        ]))
        title_layout.addWidget(self._metric_box('循环线数据', [
            ('循环投放数量', '0 件'), ('循环投放数量', '0 件'), ('循环投放比例', '0.0 %'),
        ]))
        title_layout.addWidget(self._metric_box('供包台数据 / 供包数据', [
            ('供包总数量', '0 件'), ('供包台小时数量', '0 件/小时'), ('供包台小时效率', '0 件/台·小时'),
        ]))
        title_layout.addWidget(self._metric_box('人工拣数据', [
            ('人工拣数量', '0 件'), ('人工拣比例', '0.0 %'),
        ]))
        title_layout.addWidget(self._metric_box('异常分析', [
            ('异常总数', '0 件'), ('异常比例', '0.0 %'),
        ]))

        table_card = QFrame()
        table_card.setObjectName('monitorStatCard')
        t_layout = QVBoxLayout(table_card)
        t_layout.setContentsMargins(16, 14, 16, 14)
        t_layout.setSpacing(12)
        t_title = QLabel('硬件告警 / 通讯故障')
        t_title.setObjectName('rightSectionTitle')
        t_layout.addWidget(t_title)

        table = QTableWidget(1, 6)
        table.setObjectName('faultTable')
        table.setHorizontalHeaderLabels(['序号', '设备名称', '告警类型', '告警级别', '告警信息', '发生时间'])
        table.verticalHeader().setVisible(False)
        table.setItem(0, 0, QTableWidgetItem('1'))
        table.setItem(0, 1, QTableWidgetItem('modbus通信'))
        table.setItem(0, 2, QTableWidgetItem('通讯故障'))
        table.setItem(0, 3, QTableWidgetItem('严重'))
        table.setItem(0, 4, QTableWidgetItem('通讯超时'))
        table.setItem(0, 5, QTableWidgetItem('2026-04-23 16:51:32'))
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setDefaultSectionSize(90)
        table.setFixedHeight(112)
        t_layout.addWidget(table)

        footer = QLabel('◀   1   /   1   ▶                                           共 1 条')
        footer.setObjectName('tableFooterText')
        t_layout.addWidget(footer)

        title_layout.addWidget(table_card)
        layout.addWidget(title_card)
        return wrap
