from __future__ import annotations

import json
import logging
from typing import Any

from PyQt6.QtCore import QPointF, QRectF, QTimer, Qt
from PyQt6.QtGui import QColor, QPainter, QPen, QPolygonF
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app.app_context import AppContext
from app.domain.models.realtime_record import Parcel, RealtimeRecord
from app.domain.models.system_snapshot import SystemSnapshot
from app.domain.models.throughput_metrics import ThroughputMetrics


I18N = {
    'zh': {
        'window_title': '单件分离客户端 / Single Piece Client',
        'app_title': '单件分离SCS',
        'settings': '设置 / Settings',
        'query': '查询 / Query',
        'help': '帮助 / Help',
        'station_overview': '站点总览 / Station Overview',
        'site': '场地 / Site',
        'device': '设备 / Device',
        'algorithm': '算法 / Algorithm',
        'version': '版本 / Version',
        'parcel_count': '包裹数量 / Parcel Count',
        'throughput': '吞吐 / Throughput/min',
        'success_rate': '效率 / Success Rate',
        'client_status': '客户端状态 / Client Status',
        'query_logs': '查询与日志 / Query & Logs',
        'query_placeholder': '输入包裹号 / item id / keyword',
        'query_button': '查询',
        'logs_placeholder': '日志已移动到查询按钮下方',
        'channels': '数据通路 / Ingest Channels',
        'matrix': '单件分离矩阵 / Realtime Separation Matrix',
        'waiting': '等待实时数据 / Waiting for realtime data',
        'metrics': '指标与吞吐 / KPI & Throughput',
        'system': '系统状态 / System Health',
        'config': '算法配置 / Algorithm Configuration',
        'config_output': '配置输出目录 / Config Output Dir',
        'rows': '行数 m / Rows (m)',
        'cols': '列数 n / Cols (n)',
        'language': '语言 / Language',
        'show_aux': '显示辅助信息',
        'show_coord': '显示坐标',
        'preview': '预览配置',
        'write': '写入配置',
        'inject': '注入样例',
        'realtime_table_ts': '时间',
        'realtime_table_version': '版本',
        'realtime_table_parcelnum': '包裹数量',
        'realtime_table_parcels': '解析包裹数',
        'processed': '处理数 / Processed',
        'version_card': '版本 / Version',
        'realtime_parcels': '实时包裹 / Realtime Parcels',
        'calc_eff': '计算效率 / Calc Efficiency',
        'cpu': 'CPU %',
        'memory': '内存 / Memory %',
        'disk': '磁盘 / Disk %',
        'disk_free': '剩余磁盘 / Disk Free GB',
        'config_preview_placeholder': '算法配置预览显示在这里...',
        'ready': '就绪 / Ready',
        'config_dialog_title': '商用设置面板 / Settings',
        'save': '确定',
        'cancel': '取消',
        'apply': '应用',
        'tab_general': '基础设置',
        'tab_ui': '界面设置',
        'tab_display': '显示设置',
        'help_text': '当前版本支持：商用设置面板、矩阵热力显示、活跃包裹高亮与流向指示。',
        'flow_direction': '流向 / Flow',
        'matrix_status': '矩阵状态 / Matrix Status',
        'group_station': '站点设置',
        'group_matrix': '矩阵设置',
        'group_display': '显示选项',
        'group_language': '语言切换',
        'show_index': '显示行列编号',
        'show_arrow': '显示流向箭头',
    },
    'en': {
        'window_title': 'Single Piece Client',
        'app_title': 'Single Piece SCS',
        'settings': 'Settings',
        'query': 'Query',
        'help': 'Help',
        'station_overview': 'Station Overview',
        'site': 'Site',
        'device': 'Device',
        'algorithm': 'Algorithm',
        'version': 'Version',
        'parcel_count': 'Parcel Count',
        'throughput': 'Throughput/min',
        'success_rate': 'Success Rate',
        'client_status': 'Client Status',
        'query_logs': 'Query & Logs',
        'query_placeholder': 'Input item id / keyword',
        'query_button': 'Query',
        'logs_placeholder': 'Logs are shown below the query button',
        'channels': 'Ingest Channels',
        'matrix': 'Realtime Separation Matrix',
        'waiting': 'Waiting for realtime data',
        'metrics': 'KPI & Throughput',
        'system': 'System Health',
        'config': 'Algorithm Configuration',
        'config_output': 'Config Output Dir',
        'rows': 'Rows (m)',
        'cols': 'Cols (n)',
        'language': 'Language',
        'show_aux': 'Show auxiliary info',
        'show_coord': 'Show coordinates',
        'preview': 'Preview Config',
        'write': 'Write Config',
        'inject': 'Inject Sample',
        'realtime_table_ts': 'Timestamp',
        'realtime_table_version': 'Version',
        'realtime_table_parcelnum': 'ParcelNum',
        'realtime_table_parcels': 'Parsed Parcels',
        'processed': 'Processed',
        'version_card': 'Version',
        'realtime_parcels': 'Realtime Parcels',
        'calc_eff': 'Calc Efficiency',
        'cpu': 'CPU %',
        'memory': 'Memory %',
        'disk': 'Disk %',
        'disk_free': 'Disk Free GB',
        'config_preview_placeholder': 'Algorithm config preview will appear here...',
        'ready': 'Ready',
        'config_dialog_title': 'Commercial Settings Panel',
        'save': 'OK',
        'cancel': 'Cancel',
        'apply': 'Apply',
        'tab_general': 'General',
        'tab_ui': 'UI',
        'tab_display': 'Display',
        'help_text': 'Current version supports commercial settings panel, matrix heatmap, active parcel highlight, and flow direction indicators.',
        'flow_direction': 'Flow',
        'matrix_status': 'Matrix Status',
        'group_station': 'Station Settings',
        'group_matrix': 'Matrix Settings',
        'group_display': 'Display Options',
        'group_language': 'Language',
        'show_index': 'Show row/col index',
        'show_arrow': 'Show flow arrow',
    },
}


class SettingsDialog(QDialog):
    def __init__(self, parent: QWidget | None, rows: int, cols: int, language: str, show_aux: bool, show_coord: bool, show_index: bool, show_arrow: bool) -> None:
        super().__init__(parent)
        self.setModal(True)
        self.resize(560, 420)
        root = QVBoxLayout(self)
        self.tabs = QTabWidget()
        root.addWidget(self.tabs)

        self.rows_spin = QSpinBox(); self.rows_spin.setRange(1, 100); self.rows_spin.setValue(rows)
        self.cols_spin = QSpinBox(); self.cols_spin.setRange(1, 100); self.cols_spin.setValue(cols)
        self.language_combo = QComboBox(); self.language_combo.addItems(['中文', 'English']); self.language_combo.setCurrentIndex(0 if language == 'zh' else 1)
        self.show_aux_checkbox = QCheckBox(); self.show_aux_checkbox.setChecked(show_aux)
        self.show_coord_checkbox = QCheckBox(); self.show_coord_checkbox.setChecked(show_coord)
        self.show_index_checkbox = QCheckBox(); self.show_index_checkbox.setChecked(show_index)
        self.show_arrow_checkbox = QCheckBox(); self.show_arrow_checkbox.setChecked(show_arrow)

        self.general_tab = QWidget(); self.ui_tab = QWidget(); self.display_tab = QWidget()
        self.tabs.addTab(self.general_tab, '')
        self.tabs.addTab(self.ui_tab, '')
        self.tabs.addTab(self.display_tab, '')

        general_layout = QVBoxLayout(self.general_tab)
        station_box = QGroupBox()
        station_form = QFormLayout(station_box)
        self.rows_label = QLabel(); self.cols_label = QLabel()
        station_form.addRow(self.rows_label, self.rows_spin)
        station_form.addRow(self.cols_label, self.cols_spin)
        general_layout.addWidget(station_box)
        general_layout.addStretch(1)
        self.station_box = station_box

        ui_layout = QVBoxLayout(self.ui_tab)
        lang_box = QGroupBox()
        lang_form = QFormLayout(lang_box)
        self.language_label = QLabel()
        lang_form.addRow(self.language_label, self.language_combo)
        ui_layout.addWidget(lang_box)
        ui_layout.addStretch(1)
        self.lang_box = lang_box

        display_layout = QVBoxLayout(self.display_tab)
        display_box = QGroupBox()
        display_form = QFormLayout(display_box)
        display_form.addRow(self.show_aux_checkbox)
        display_form.addRow(self.show_coord_checkbox)
        display_form.addRow(self.show_index_checkbox)
        display_form.addRow(self.show_arrow_checkbox)
        display_layout.addWidget(display_box)
        display_layout.addStretch(1)
        self.display_box = display_box

        bottom = QHBoxLayout()
        bottom.addStretch(1)
        self.apply_btn = QPushButton()
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.apply_btn.clicked.connect(self._emit_apply)
        bottom.addWidget(self.apply_btn)
        bottom.addWidget(self.button_box)
        root.addLayout(bottom)

        self._apply_callback = None
        self.retranslate(language)

    def on_apply(self, callback) -> None:
        self._apply_callback = callback

    def _emit_apply(self) -> None:
        if callable(self._apply_callback):
            self._apply_callback(self)

    def retranslate(self, language: str) -> None:
        tr = I18N[language]
        self.setWindowTitle(tr['config_dialog_title'])
        self.tabs.setTabText(0, tr['tab_general'])
        self.tabs.setTabText(1, tr['tab_ui'])
        self.tabs.setTabText(2, tr['tab_display'])
        self.station_box.setTitle(tr['group_matrix'])
        self.lang_box.setTitle(tr['group_language'])
        self.display_box.setTitle(tr['group_display'])
        self.rows_label.setText(tr['rows'])
        self.cols_label.setText(tr['cols'])
        self.language_label.setText(tr['language'])
        self.show_aux_checkbox.setText(tr['show_aux'])
        self.show_coord_checkbox.setText(tr['show_coord'])
        self.show_index_checkbox.setText(tr['show_index'])
        self.show_arrow_checkbox.setText(tr['show_arrow'])
        self.apply_btn.setText(tr['apply'])
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText(tr['save'])
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText(tr['cancel'])


class MatrixCanvas(QWidget):
    def __init__(self, rows: int, cols: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.car_speeds: list[float] = []
        self.parcels: list[Parcel] = []
        self.show_coordinates = False
        self.show_auxiliary_info = True
        self.show_index = True
        self.show_arrow = True
        self.setMinimumHeight(440)

    def set_matrix_shape(self, rows: int, cols: int) -> None:
        self.rows = max(1, rows)
        self.cols = max(1, cols)
        self.update()

    def set_runtime_data(self, car_speeds: list[float], parcels: list[Parcel], show_coordinates: bool, show_auxiliary_info: bool, show_index: bool, show_arrow: bool) -> None:
        self.car_speeds = car_speeds
        self.parcels = parcels
        self.show_coordinates = show_coordinates
        self.show_auxiliary_info = show_auxiliary_info
        self.show_index = show_index
        self.show_arrow = show_arrow
        self.update()

    def _inner_rect(self) -> QRectF:
        margin = 28
        return QRectF(margin, margin, max(1, self.width() - margin * 2), max(1, self.height() - margin * 2 - 26))

    def _cell_rect(self, row: int, col: int) -> QRectF:
        rect = self._inner_rect()
        gap = 8
        cell_w = (rect.width() - gap * (self.cols - 1)) / self.cols
        cell_h = (rect.height() - gap * (self.rows - 1)) / self.rows
        x = rect.left() + col * (cell_w + gap)
        y = rect.top() + row * (cell_h + gap)
        return QRectF(x, y, cell_w, cell_h)

    def _speed_to_color(self, speed: float) -> QColor:
        base = QColor('#14324A')
        highlight = QColor('#00A3FF')
        ratio = max(0.0, min(speed / 2.0, 1.0))
        r = int(base.red() + (highlight.red() - base.red()) * ratio)
        g = int(base.green() + (highlight.green() - base.green()) * ratio)
        b = int(base.blue() + (highlight.blue() - base.blue()) * ratio)
        return QColor(r, g, b)

    def _scaled_points(self, parcel: Parcel) -> list[QPointF]:
        if len(parcel.points) < 2:
            return []
        all_points = [pt for p in self.parcels for pt in p.points if len(pt) >= 2]
        if not all_points:
            return []
        xs = [float(pt[0]) for pt in all_points]
        ys = [float(pt[1]) for pt in all_points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        span_x = max(max_x - min_x, 1.0)
        span_y = max(max_y - min_y, 1.0)
        usable = self._inner_rect().adjusted(14, 14, -14, -14)
        return [
            QPointF(
                usable.left() + ((float(x) - min_x) / span_x) * usable.width(),
                usable.top() + ((float(y) - min_y) / span_y) * usable.height(),
            )
            for x, y in parcel.points
        ]

    def _active_cells(self) -> set[tuple[int, int]]:
        active: set[tuple[int, int]] = set()
        rect = self._inner_rect()
        for parcel in self.parcels:
            pts = self._scaled_points(parcel)
            if not pts:
                continue
            center_x = sum(p.x() for p in pts) / len(pts)
            center_y = sum(p.y() for p in pts) / len(pts)
            rel_x = max(0.0, min(0.999, (center_x - rect.left()) / max(rect.width(), 1.0)))
            rel_y = max(0.0, min(0.999, (center_y - rect.top()) / max(rect.height(), 1.0)))
            col = min(self.cols - 1, int(rel_x * self.cols))
            row = min(self.rows - 1, int(rel_y * self.rows))
            active.add((row, col))
        return active

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor('#081421'))
        painter.setPen(QPen(QColor('#183248'), 1))
        painter.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 10, 10)

        total_cells = self.rows * self.cols
        padded = self.car_speeds + [0.0] * max(0, total_cells - len(self.car_speeds))
        active_cells = self._active_cells()

        for idx in range(total_cells):
            row = idx // self.cols
            col = idx % self.cols
            rect = self._cell_rect(row, col)
            speed = padded[idx]
            painter.setBrush(self._speed_to_color(speed))
            pen_color = QColor('#46c7ff') if (row, col) in active_cells else QColor('#1E5678')
            pen_width = 2 if (row, col) in active_cells else 1
            painter.setPen(QPen(pen_color, pen_width))
            painter.drawRoundedRect(rect, 6, 6)
            painter.setPen(QColor('#E5F6FF'))
            painter.drawText(rect.adjusted(8, 6, -8, -6), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft, f'{speed:.1f}')
            if self.show_index:
                painter.setPen(QColor('#8ccdf0'))
                painter.drawText(rect.adjusted(8, 0, -8, -6), Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight, f'R{row+1}C{col+1}')

        if self.show_index:
            painter.setPen(QColor('#7eb8d6'))
            for col in range(self.cols):
                rect = self._cell_rect(0, col)
                painter.drawText(QRectF(rect.left(), 6, rect.width(), 18), Qt.AlignmentFlag.AlignCenter, str(col + 1))
            for row in range(self.rows):
                rect = self._cell_rect(row, 0)
                painter.drawText(QRectF(4, rect.top(), 18, rect.height()), Qt.AlignmentFlag.AlignCenter, str(row + 1))

        if self.show_arrow:
            rect = self._inner_rect()
            y = rect.bottom() + 16
            painter.setPen(QPen(QColor('#00A3FF'), 3))
            painter.drawLine(rect.left(), y, rect.right() - 24, y)
            painter.drawLine(rect.right() - 24, y, rect.right() - 38, y - 8)
            painter.drawLine(rect.right() - 24, y, rect.right() - 38, y + 8)
            painter.setPen(QColor('#8ccdf0'))
            painter.drawText(QRectF(rect.left(), y + 4, rect.width(), 18), Qt.AlignmentFlag.AlignCenter, 'FLOW')

        for parcel in self.parcels:
            points = self._scaled_points(parcel)
            if len(points) < 4:
                continue
            polygon = QPolygonF(points)
            painter.setBrush(QColor(0, 163, 255, 60))
            painter.setPen(QPen(QColor('#78E2FF'), 2))
            painter.drawPolygon(polygon)
            if self.show_auxiliary_info:
                center_x = sum(p.x() for p in points) / len(points)
                center_y = sum(p.y() for p in points) / len(points)
                painter.setPen(QColor('#ffffff'))
                painter.drawText(QPointF(center_x, center_y), f'{parcel.speed:.1f}')
            if self.show_coordinates:
                painter.setPen(QColor('#b8ecff'))
                for raw, p in zip(parcel.points, points):
                    painter.drawText(p + QPointF(4, -4), f'({int(raw[0])},{int(raw[1])})')


class MainWindow(QMainWindow):
    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.logger = logging.getLogger(__name__)
        self.last_record: RealtimeRecord | None = None
        self.language = context.client_settings.ui.language
        self.show_index = True
        self.show_arrow = True
        self._apply_theme()

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(12)
        root_layout.addWidget(self._build_top_navigation())
        root_layout.addWidget(self._build_header_bar())

        body = QHBoxLayout()
        body.setSpacing(12)
        body.addWidget(self._build_left_panel(), 4)
        body.addWidget(self._build_center_panel(), 8)
        body.addWidget(self._build_right_panel(), 4)
        root_layout.addLayout(body)
        self.setCentralWidget(root)

        self.context.ingest_pipeline_service.on_records(self._handle_records)
        self.system_timer = QTimer(self)
        self.system_timer.setInterval(self.context.client_settings.monitor.sample_interval_ms)
        self.system_timer.timeout.connect(self._refresh_system)
        self.system_timer.start()

        self._load_context_values()
        self._apply_language()
        self.context.start()
        self.statusBar().showMessage('Client started')

    def trm(self, key: str) -> str:
        return I18N[self.language][key]

    def _apply_theme(self) -> None:
        self.setStyleSheet("""
            QWidget { background: #0b1220; color: #e5e7eb; font-size: 13px; }
            QMainWindow { background: #08101d; }
            QGroupBox { border: 1px solid #1d3448; border-radius: 10px; margin-top: 10px; padding-top: 12px; background: #111827; font-weight: 600; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 6px 0 6px; color: #00A3FF; }
            QLabel[role="label"] { color: #8ca4b8; font-size: 12px; }
            QLabel[role="value"] { color: #f8fafc; font-size: 18px; font-weight: 700; }
            QLabel[role="status_ok"] { color: #00A3FF; font-weight: 700; }
            QLabel[role="status_off"] { color: #94a3b8; font-weight: 700; }
            QLineEdit, QPlainTextEdit, QTableWidget, QSpinBox, QComboBox, QTabWidget::pane { background: #0a1726; border: 1px solid #1f3850; border-radius: 8px; padding: 6px; selection-background-color: #00A3FF; }
            QPushButton { background: #00A3FF; color: white; border: none; border-radius: 8px; padding: 8px 12px; font-weight: 600; }
            QPushButton:hover { background: #13b0ff; }
            QPushButton[variant="secondary"] { background: #27455d; }
            QPushButton[variant="warn"] { background: #b45309; }
            QPushButton[variant="nav"] { background: transparent; border-radius: 6px; color: #dbeafe; padding: 8px 20px; border: 1px solid transparent; }
            QPushButton[variant="nav"]:hover { background: #0b2033; border: 1px solid #00A3FF; }
            QCheckBox { spacing: 8px; }
            QHeaderView::section { background: #102235; color: #cbd5e1; border: none; padding: 8px; font-weight: 600; }
            QTableWidget { gridline-color: #173247; }
            QStatusBar { background: #111827; color: #cbd5e1; }
            QTabBar::tab { background: #102235; color: #dbeafe; padding: 8px 16px; margin-right: 4px; border-top-left-radius: 6px; border-top-right-radius: 6px; }
            QTabBar::tab:selected { background: #00A3FF; color: white; }
        """)

    def _build_top_navigation(self) -> QWidget:
        box = QFrame()
        box.setStyleSheet('QFrame {background:#0e1b2d; border:1px solid #183248; border-radius:10px;}')
        layout = QHBoxLayout(box)
        layout.setContentsMargins(12, 8, 12, 8)
        self.title_label = QLabel()
        self.title_label.setStyleSheet('QLabel {font-size: 22px; font-weight: 700; color: #00A3FF;}')
        layout.addWidget(self.title_label)
        layout.addSpacing(24)
        self.settings_btn = QPushButton(); self.settings_btn.setProperty('variant', 'nav'); self.settings_btn.clicked.connect(self.open_settings_dialog)
        self.query_btn = QPushButton(); self.query_btn.setProperty('variant', 'nav')
        self.help_btn = QPushButton(); self.help_btn.setProperty('variant', 'nav'); self.help_btn.clicked.connect(self.show_help)
        layout.addWidget(self.settings_btn); layout.addWidget(self.query_btn); layout.addWidget(self.help_btn)
        layout.addStretch(1)
        return box

    def _build_header_bar(self) -> QWidget:
        self.header_box = QGroupBox()
        layout = QHBoxLayout(self.header_box)
        self.site_card = self._make_stat_card('', '-')
        self.device_card = self._make_stat_card('', '-')
        self.algorithm_card = self._make_stat_card('', '-')
        self.version_card = self._make_stat_card('', '-')
        self.kpi_processed_card = self._make_stat_card('', '0')
        self.kpi_throughput_card = self._make_stat_card('', '0')
        self.kpi_efficiency_card = self._make_stat_card('', '0%')
        self.kpi_status_card = self._make_stat_card('', 'RUNNING', status='ok')
        for card in [self.site_card, self.device_card, self.algorithm_card, self.version_card, self.kpi_processed_card, self.kpi_throughput_card, self.kpi_efficiency_card, self.kpi_status_card]:
            layout.addWidget(card)
        return self.header_box

    def _make_stat_card(self, title: str, value: str, status: str | None = None) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet('QFrame {background:#091827; border:1px solid #183248; border-radius:10px;}')
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        title_label = QLabel(title); title_label.setProperty('role', 'label')
        value_label = QLabel(value); value_label.setWordWrap(True); value_label.setProperty('role', f'status_{status}' if status else 'value')
        layout.addWidget(title_label); layout.addWidget(value_label)
        frame.title_label = title_label  # type: ignore[attr-defined]
        frame.value_label = value_label  # type: ignore[attr-defined]
        return frame

    def _build_left_panel(self) -> QWidget:
        widget = QWidget(); layout = QVBoxLayout(widget); layout.setSpacing(12)
        layout.addWidget(self._build_query_and_logs_widget()); layout.addWidget(self._build_channel_widget()); layout.addStretch(1)
        return widget

    def _build_center_panel(self) -> QWidget:
        widget = QWidget(); layout = QVBoxLayout(widget); layout.setSpacing(12)
        layout.addWidget(self._build_matrix_widget(), 6); layout.addWidget(self._build_metrics_widget(), 2)
        return widget

    def _build_right_panel(self) -> QWidget:
        widget = QWidget(); layout = QVBoxLayout(widget); layout.setSpacing(12)
        layout.addWidget(self._build_config_widget()); layout.addWidget(self._build_system_widget())
        return widget

    def _build_query_and_logs_widget(self) -> QWidget:
        self.query_logs_box = QGroupBox()
        layout = QVBoxLayout(self.query_logs_box)
        query_bar = QHBoxLayout()
        self.query_keyword = QLineEdit()
        self.query_action_btn = QPushButton(); self.query_action_btn.setProperty('variant', 'secondary')
        query_bar.addWidget(self.query_keyword, 1); query_bar.addWidget(self.query_action_btn)
        layout.addLayout(query_bar)
        self.logs_editor = QPlainTextEdit(); self.logs_editor.setReadOnly(True)
        layout.addWidget(self.logs_editor, 1)
        return self.query_logs_box

    def _build_config_widget(self) -> QWidget:
        self.config_box = QGroupBox()
        layout = QVBoxLayout(self.config_box)
        form = QFormLayout()
        self.output_dir_label = QLabel(); self.output_dir_label.setWordWrap(True)
        self.rows_spin = QSpinBox(); self.rows_spin.setRange(1, 100)
        self.cols_spin = QSpinBox(); self.cols_spin.setRange(1, 100)
        self.language_combo = QComboBox(); self.language_combo.addItems(['中文', 'English'])
        self.show_aux_checkbox = QCheckBox(); self.show_coord_checkbox = QCheckBox(); self.show_index_checkbox = QCheckBox(); self.show_arrow_checkbox = QCheckBox()
        self.rows_label = QLabel(); self.cols_label = QLabel(); self.lang_label = QLabel(); self.output_label = QLabel()
        form.addRow(self.output_label, self.output_dir_label)
        form.addRow(self.rows_label, self.rows_spin)
        form.addRow(self.cols_label, self.cols_spin)
        form.addRow(self.lang_label, self.language_combo)
        form.addRow(self.show_aux_checkbox)
        form.addRow(self.show_coord_checkbox)
        form.addRow(self.show_index_checkbox)
        form.addRow(self.show_arrow_checkbox)
        layout.addLayout(form)
        self.rows_spin.valueChanged.connect(self._matrix_shape_changed)
        self.cols_spin.valueChanged.connect(self._matrix_shape_changed)
        self.show_aux_checkbox.toggled.connect(self._matrix_option_changed)
        self.show_coord_checkbox.toggled.connect(self._matrix_option_changed)
        self.show_index_checkbox.toggled.connect(self._matrix_option_changed)
        self.show_arrow_checkbox.toggled.connect(self._matrix_option_changed)
        self.language_combo.currentIndexChanged.connect(self._language_combo_changed)

        buttons = QGridLayout()
        self.preview_btn = QPushButton()
        self.write_btn = QPushButton(); self.write_btn.setProperty('variant', 'secondary')
        self.simulate_btn = QPushButton(); self.simulate_btn.setProperty('variant', 'warn')
        self.preview_btn.clicked.connect(self.preview_config)
        self.write_btn.clicked.connect(self.write_config)
        self.simulate_btn.clicked.connect(self.inject_sample_event)
        buttons.addWidget(self.preview_btn, 0, 0); buttons.addWidget(self.write_btn, 0, 1); buttons.addWidget(self.simulate_btn, 1, 0, 1, 2)
        layout.addLayout(buttons)
        self.config_preview = QPlainTextEdit(); self.config_preview.setReadOnly(True)
        self.config_status = QLabel(); self.config_status.setProperty('role', 'status_ok')
        layout.addWidget(self.config_preview, 1); layout.addWidget(self.config_status)
        return self.config_box

    def _build_channel_widget(self) -> QWidget:
        self.channel_box = QGroupBox()
        layout = QGridLayout(self.channel_box)
        self.file_title = QLabel(); self.tcp_title = QLabel(); self.http_title = QLabel(); self.unix_title = QLabel(); self.zmq_title = QLabel()
        self.file_status = QLabel('-'); self.tcp_status = QLabel('-'); self.http_status = QLabel('-'); self.unix_status = QLabel('-'); self.zmq_status = QLabel('-')
        pairs = [(self.file_title, self.file_status), (self.tcp_title, self.tcp_status), (self.http_title, self.http_status), (self.unix_title, self.unix_status), (self.zmq_title, self.zmq_status)]
        for idx, (title, label) in enumerate(pairs):
            row = idx // 2; col = (idx % 2) * 2
            title.setProperty('role', 'label'); layout.addWidget(title, row, col); layout.addWidget(label, row, col + 1)
        return self.channel_box

    def _build_matrix_widget(self) -> QWidget:
        self.matrix_box = QGroupBox()
        layout = QVBoxLayout(self.matrix_box)
        top = QHBoxLayout()
        self.realtime_status = QLabel(); self.realtime_status.setProperty('role', 'label')
        self.matrix_status = QLabel(); self.matrix_status.setProperty('role', 'status_ok')
        top.addWidget(self.realtime_status); top.addStretch(1); top.addWidget(self.matrix_status)
        layout.addLayout(top)
        self.matrix_canvas = MatrixCanvas(10, 4)
        layout.addWidget(self.matrix_canvas, 1)
        self.realtime_table = QTableWidget(0, 4)
        self.realtime_table.verticalHeader().setVisible(False)
        layout.addWidget(self.realtime_table)
        return self.matrix_box

    def _build_system_widget(self) -> QWidget:
        self.system_box = QGroupBox()
        layout = QGridLayout(self.system_box)
        self.cpu_card = self._make_stat_card('', '0')
        self.memory_card = self._make_stat_card('', '0')
        self.disk_card = self._make_stat_card('', '0')
        self.disk_free_card = self._make_stat_card('', '0')
        layout.addWidget(self.cpu_card, 0, 0); layout.addWidget(self.memory_card, 0, 1); layout.addWidget(self.disk_card, 1, 0); layout.addWidget(self.disk_free_card, 1, 1)
        return self.system_box

    def _build_metrics_widget(self) -> QWidget:
        self.metrics_box = QGroupBox()
        layout = QGridLayout(self.metrics_box)
        self.processed_card = self._make_stat_card('', '0')
        self.success_card = self._make_stat_card('', '-')
        self.exception_card = self._make_stat_card('', '0')
        self.throughput_card = self._make_stat_card('', '0')
        self.efficiency_card = self._make_stat_card('', '0%')
        cards = [self.processed_card, self.success_card, self.exception_card, self.throughput_card, self.efficiency_card]
        positions = [(0,0),(0,1),(0,2),(1,0),(1,1)]
        for card, (r,c) in zip(cards, positions): layout.addWidget(card, r, c)
        return self.metrics_box

    def _apply_language(self) -> None:
        self.setWindowTitle(self.trm('window_title'))
        self.title_label.setText(self.trm('app_title'))
        self.settings_btn.setText(self.trm('settings'))
        self.query_btn.setText(self.trm('query'))
        self.help_btn.setText(self.trm('help'))
        self.header_box.setTitle(self.trm('station_overview'))
        self.site_card.title_label.setText(self.trm('site'))
        self.device_card.title_label.setText(self.trm('device'))
        self.algorithm_card.title_label.setText(self.trm('algorithm'))
        self.version_card.title_label.setText(self.trm('version'))
        self.kpi_processed_card.title_label.setText(self.trm('parcel_count'))
        self.kpi_throughput_card.title_label.setText(self.trm('throughput'))
        self.kpi_efficiency_card.title_label.setText(self.trm('success_rate'))
        self.kpi_status_card.title_label.setText(self.trm('client_status'))
        self.query_logs_box.setTitle(self.trm('query_logs'))
        self.query_keyword.setPlaceholderText(self.trm('query_placeholder'))
        self.query_action_btn.setText(self.trm('query_button'))
        self.logs_editor.setPlaceholderText(self.trm('logs_placeholder'))
        self.channel_box.setTitle(self.trm('channels'))
        self.file_title.setText('File'); self.tcp_title.setText('TCP'); self.http_title.setText('HTTP'); self.unix_title.setText('Unix Socket'); self.zmq_title.setText('ZeroMQ')
        self.matrix_box.setTitle(self.trm('matrix'))
        self.realtime_status.setText(self.trm('waiting'))
        self.matrix_status.setText(self.trm('matrix_status'))
        self.realtime_table.setHorizontalHeaderLabels([self.trm('realtime_table_ts'), self.trm('realtime_table_version'), self.trm('realtime_table_parcelnum'), self.trm('realtime_table_parcels')])
        self.metrics_box.setTitle(self.trm('metrics'))
        self.processed_card.title_label.setText(self.trm('processed'))
        self.success_card.title_label.setText(self.trm('version_card'))
        self.exception_card.title_label.setText(self.trm('realtime_parcels'))
        self.throughput_card.title_label.setText(self.trm('throughput'))
        self.efficiency_card.title_label.setText(self.trm('calc_eff'))
        self.system_box.setTitle(self.trm('system'))
        self.cpu_card.title_label.setText(self.trm('cpu'))
        self.memory_card.title_label.setText(self.trm('memory'))
        self.disk_card.title_label.setText(self.trm('disk'))
        self.disk_free_card.title_label.setText(self.trm('disk_free'))
        self.config_box.setTitle(self.trm('config'))
        self.output_label.setText(self.trm('config_output'))
        self.rows_label.setText(self.trm('rows'))
        self.cols_label.setText(self.trm('cols'))
        self.lang_label.setText(self.trm('language'))
        self.show_aux_checkbox.setText(self.trm('show_aux'))
        self.show_coord_checkbox.setText(self.trm('show_coord'))
        self.show_index_checkbox.setText(self.trm('show_index'))
        self.show_arrow_checkbox.setText(self.trm('show_arrow'))
        self.preview_btn.setText(self.trm('preview'))
        self.write_btn.setText(self.trm('write'))
        self.simulate_btn.setText(self.trm('inject'))
        self.config_preview.setPlaceholderText(self.trm('config_preview_placeholder'))
        self.config_status.setText(self.trm('ready'))

    def _load_context_values(self) -> None:
        client = self.context.client_settings
        algo = self.context.algorithm_settings
        self.site_card.value_label.setText(client.site_id)
        self.device_card.value_label.setText(client.device_id)
        self.algorithm_card.value_label.setText(algo.algorithm_name)
        self.version_card.value_label.setText('1.0.0')
        self.output_dir_label.setText(str(algo.config_output_dir))
        self.rows_spin.setValue(client.ui.matrix_rows)
        self.cols_spin.setValue(client.ui.matrix_cols)
        self.language_combo.setCurrentIndex(0 if client.ui.language == 'zh' else 1)
        self.show_aux_checkbox.setChecked(client.ui.show_auxiliary_info)
        self.show_coord_checkbox.setChecked(client.ui.show_coordinates)
        self.show_index_checkbox.setChecked(self.show_index)
        self.show_arrow_checkbox.setChecked(self.show_arrow)
        self.matrix_canvas.set_matrix_shape(client.ui.matrix_rows, client.ui.matrix_cols)
        self._set_channel_status(self.file_status, client.ingest.file.enabled)
        self._set_channel_status(self.tcp_status, client.ingest.tcp.enabled)
        self._set_channel_status(self.http_status, client.ingest.http.enabled)
        self._set_channel_status(self.unix_status, client.ingest.unix_socket.enabled)
        self._set_channel_status(self.zmq_status, client.ingest.zeromq.enabled)
        self.logs_editor.appendPlainText('Enabled channels: ' + ', '.join(self.context.channel_manager.enabled_channel_names()))

    def _set_channel_status(self, label: QLabel, enabled: bool) -> None:
        label.setText('ONLINE' if enabled else 'OFF')
        label.setProperty('role', 'status_ok' if enabled else 'status_off')
        label.style().unpolish(label); label.style().polish(label)

    def _apply_dialog_values(self, dlg: SettingsDialog) -> None:
        self.rows_spin.setValue(dlg.rows_spin.value())
        self.cols_spin.setValue(dlg.cols_spin.value())
        self.language = 'zh' if dlg.language_combo.currentIndex() == 0 else 'en'
        self.language_combo.setCurrentIndex(dlg.language_combo.currentIndex())
        self.show_aux_checkbox.setChecked(dlg.show_aux_checkbox.isChecked())
        self.show_coord_checkbox.setChecked(dlg.show_coord_checkbox.isChecked())
        self.show_index_checkbox.setChecked(dlg.show_index_checkbox.isChecked())
        self.show_arrow_checkbox.setChecked(dlg.show_arrow_checkbox.isChecked())
        self._apply_language()
        self._matrix_shape_changed()
        self._matrix_option_changed()

    def open_settings_dialog(self) -> None:
        dlg = SettingsDialog(self, self.rows_spin.value(), self.cols_spin.value(), self.language, self.show_aux_checkbox.isChecked(), self.show_coord_checkbox.isChecked(), self.show_index_checkbox.isChecked(), self.show_arrow_checkbox.isChecked())
        dlg.on_apply(self._apply_dialog_values)
        if dlg.exec():
            self._apply_dialog_values(dlg)
            self.logs_editor.appendPlainText(f'Settings updated: {self.rows_spin.value()} x {self.cols_spin.value()}, lang={self.language}')

    def show_help(self) -> None:
        QMessageBox.information(self, self.trm('help'), self.trm('help_text'))

    def _language_combo_changed(self) -> None:
        self.language = 'zh' if self.language_combo.currentIndex() == 0 else 'en'
        self._apply_language()

    def _matrix_shape_changed(self) -> None:
        self.matrix_canvas.set_matrix_shape(self.rows_spin.value(), self.cols_spin.value())
        self.logs_editor.appendPlainText(f'Matrix shape changed to {self.rows_spin.value()} x {self.cols_spin.value()}')

    def _matrix_option_changed(self) -> None:
        self.show_index = self.show_index_checkbox.isChecked()
        self.show_arrow = self.show_arrow_checkbox.isChecked()
        if self.last_record:
            self.matrix_canvas.set_runtime_data(self.last_record.car_speeds, self.last_record.parcels, self.show_coord_checkbox.isChecked(), self.show_aux_checkbox.isChecked(), self.show_index, self.show_arrow)

    def _collect_overrides(self) -> dict[str, Any]:
        return {'matrix_rows': self.rows_spin.value(), 'matrix_cols': self.cols_spin.value(), 'language': self.language}

    def preview_config(self) -> None:
        try:
            payload = self.context.algorithm_config_service.build_payload(self.context.client_settings, self.context.algorithm_settings, self._collect_overrides())
            self.config_preview.setPlainText(json.dumps(payload, indent=2, ensure_ascii=False))
            self.config_status.setText(self.trm('ready'))
        except Exception as exc:
            self.logger.exception('Preview config failed')
            QMessageBox.critical(self, 'Preview failed', str(exc))

    def write_config(self) -> None:
        try:
            path = self.context.algorithm_config_service.write(self.context.client_settings, self.context.algorithm_settings, self._collect_overrides())
            self.preview_config()
            self.logs_editor.appendPlainText(f'Wrote algorithm config: {path}')
        except Exception as exc:
            self.logger.exception('Write config failed')
            QMessageBox.critical(self, 'Write failed', str(exc))

    def inject_sample_event(self) -> None:
        sample = {
            'version': '1.0.0',
            'efficiency': '0',
            'parcelNum': '2',
            'car_speeds': [0.2 + (i % self.cols_spin.value()) * 0.25 for i in range(self.rows_spin.value() * self.cols_spin.value())],
            'parcels': [
                {'speed': 2.0, 'points': [[20, 30], [160, 70], [180, 162], [90, 183]]},
                {'speed': 1.2, 'points': [[180, 120], [300, 135], [320, 220], [210, 232]]},
            ],
        }
        self.context.channel_manager.inject_sample(json.dumps(sample))
        self.logs_editor.appendPlainText('Injected sample single-piece realtime payload')

    def _handle_records(self, records: list[RealtimeRecord], metrics: ThroughputMetrics) -> None:
        if not records:
            return
        record = records[-1]
        self.last_record = record
        self.version_card.value_label.setText(record.version)
        self.kpi_processed_card.value_label.setText(str(record.parcel_num))
        self.success_card.value_label.setText(record.version)
        self.exception_card.value_label.setText(str(len(record.parcels)))
        self.matrix_canvas.set_runtime_data(record.car_speeds, record.parcels, self.show_coord_checkbox.isChecked(), self.show_aux_checkbox.isChecked(), self.show_index, self.show_arrow)
        row = self.realtime_table.rowCount(); self.realtime_table.insertRow(row)
        values = [record.timestamp.isoformat(timespec='seconds'), record.version, str(record.parcel_num), str(len(record.parcels))]
        for col, text in enumerate(values):
            self.realtime_table.setItem(row, col, QTableWidgetItem(text))
        while self.realtime_table.rowCount() > 50:
            self.realtime_table.removeRow(0)
        self.realtime_status.setText(f"{self.trm('waiting').split(' / ')[0] if ' / ' in self.trm('waiting') else self.trm('waiting')}: {record.timestamp.isoformat(timespec='seconds')} | parcels={record.parcel_num}")
        self.matrix_status.setText(f"{self.trm('matrix_status').split(' / ')[0] if ' / ' in self.trm('matrix_status') else self.trm('matrix_status')}: {self.rows_spin.value()} x {self.cols_spin.value()}")
        self._update_metrics(metrics)
        self.logs_editor.appendPlainText(f'Received runtime payload version={record.version} parcelNum={record.parcel_num}')

    def _refresh_system(self) -> None:
        snapshot = self.context.system_monitor_service.collect(); self._update_system(snapshot)

    def _update_system(self, snapshot: SystemSnapshot) -> None:
        self.cpu_card.value_label.setText(f'{snapshot.cpu_percent:.1f}')
        self.memory_card.value_label.setText(f'{snapshot.memory_percent:.1f}')
        self.disk_card.value_label.setText(f'{snapshot.disk_percent:.1f}')
        self.disk_free_card.value_label.setText(f'{snapshot.disk_free_gb:.2f}')

    def _update_metrics(self, metrics: ThroughputMetrics) -> None:
        self.processed_card.value_label.setText(str(metrics.processed_count))
        self.throughput_card.value_label.setText(f'{metrics.throughput_per_min:.2f}')
        self.efficiency_card.value_label.setText(f'{metrics.efficiency_rate:.2%}')
        self.kpi_throughput_card.value_label.setText(f'{metrics.throughput_per_min:.2f}')
        self.kpi_efficiency_card.value_label.setText(f'{metrics.efficiency_rate:.2%}')

    def closeEvent(self, event) -> None:  # noqa: N802
        self.context.stop(); event.accept()
