from __future__ import annotations

import json
import logging
from typing import Any

from PyQt6.QtCore import QPointF, QRectF, QTimer, Qt
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
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
    QVBoxLayout,
    QWidget,
)

from app.app_context import AppContext
from app.domain.models.realtime_record import Parcel, RealtimeRecord
from app.domain.models.system_snapshot import SystemSnapshot
from app.domain.models.throughput_metrics import ThroughputMetrics


class MatrixCanvas(QWidget):
    def __init__(self, rows: int, cols: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.car_speeds: list[float] = []
        self.parcels: list[Parcel] = []
        self.show_coordinates = False
        self.show_auxiliary_info = True
        self.setMinimumHeight(420)

    def set_matrix_shape(self, rows: int, cols: int) -> None:
        self.rows = max(1, rows)
        self.cols = max(1, cols)
        self.update()

    def set_runtime_data(self, car_speeds: list[float], parcels: list[Parcel], show_coordinates: bool, show_auxiliary_info: bool) -> None:
        self.car_speeds = car_speeds
        self.parcels = parcels
        self.show_coordinates = show_coordinates
        self.show_auxiliary_info = show_auxiliary_info
        self.update()

    def _cell_rect(self, row: int, col: int) -> QRectF:
        margin = 18
        gap = 8
        grid_w = self.width() - margin * 2
        grid_h = self.height() - margin * 2
        cell_w = (grid_w - gap * (self.cols - 1)) / self.cols
        cell_h = (grid_h - gap * (self.rows - 1)) / self.rows
        x = margin + col * (cell_w + gap)
        y = margin + row * (cell_h + gap)
        return QRectF(x, y, cell_w, cell_h)

    def _speed_to_color(self, speed: float) -> QColor:
        base = QColor('#14324A')
        highlight = QColor('#00A3FF')
        ratio = max(0.0, min(speed / 2.0, 1.0))
        r = int(base.red() + (highlight.red() - base.red()) * ratio)
        g = int(base.green() + (highlight.green() - base.green()) * ratio)
        b = int(base.blue() + (highlight.blue() - base.blue()) * ratio)
        return QColor(r, g, b)

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor('#0A1726'))

        total_cells = self.rows * self.cols
        padded = self.car_speeds + [0.0] * max(0, total_cells - len(self.car_speeds))
        for idx in range(total_cells):
            row = idx // self.cols
            col = idx % self.cols
            rect = self._cell_rect(row, col)
            speed = padded[idx] if idx < len(padded) else 0.0
            painter.setBrush(self._speed_to_color(speed))
            painter.setPen(QPen(QColor('#1E5678'), 1))
            painter.drawRoundedRect(rect, 6, 6)
            painter.setPen(QColor('#E5F6FF'))
            painter.drawText(rect.adjusted(8, 6, -8, -6), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft, f'{speed:.1f}')

        painter.setPen(QPen(QColor('#78E2FF'), 2))
        for parcel in self.parcels:
            if len(parcel.points) < 4:
                continue
            points = [QPointF(float(x), float(y)) for x, y in parcel.points]
            for i in range(len(points)):
                painter.drawLine(points[i], points[(i + 1) % len(points)])
            if self.show_auxiliary_info:
                center_x = sum(p.x() for p in points) / len(points)
                center_y = sum(p.y() for p in points) / len(points)
                painter.drawText(QPointF(center_x, center_y), f'{parcel.speed:.1f}')
            if self.show_coordinates:
                for p in points:
                    painter.drawText(p + QPointF(4, -4), f'({int(p.x())},{int(p.y())})')


class MainWindow(QMainWindow):
    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.logger = logging.getLogger(__name__)
        self.last_record: RealtimeRecord | None = None
        self.setWindowTitle('单件分离客户端 / Single Piece Client')
        self.resize(1500, 980)
        self.setMinimumSize(1320, 860)
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
        self.context.start()
        self.statusBar().showMessage('Client started')

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
            QLabel[role="status_warn"] { color: #fbbf24; font-weight: 700; }
            QLabel[role="status_err"] { color: #f87171; font-weight: 700; }
            QLineEdit, QPlainTextEdit, QTableWidget, QSpinBox, QComboBox { background: #0a1726; border: 1px solid #1f3850; border-radius: 8px; padding: 6px; selection-background-color: #00A3FF; }
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
        """)

    def _build_top_navigation(self) -> QWidget:
        box = QFrame()
        box.setStyleSheet('QFrame {background:#0e1b2d; border:1px solid #183248; border-radius:10px;}')
        layout = QHBoxLayout(box)
        layout.setContentsMargins(12, 8, 12, 8)
        self.title_label = QLabel('单件分离SCS')
        self.title_label.setStyleSheet('QLabel {font-size: 22px; font-weight: 700; color: #00A3FF;}')
        layout.addWidget(self.title_label)
        layout.addSpacing(24)
        for text in ['设置 / Settings', '查询 / Query', '帮助 / Help']:
            btn = QPushButton(text)
            btn.setProperty('variant', 'nav')
            layout.addWidget(btn)
        layout.addStretch(1)
        return box

    def _build_header_bar(self) -> QWidget:
        box = QGroupBox('Station Overview')
        layout = QHBoxLayout(box)
        self.site_card = self._make_stat_card('Site', '-')
        self.device_card = self._make_stat_card('Device', '-')
        self.algorithm_card = self._make_stat_card('Algorithm', '-')
        self.version_card = self._make_stat_card('Version', '-')
        self.kpi_processed_card = self._make_stat_card('Parcel Count', '0')
        self.kpi_throughput_card = self._make_stat_card('Throughput/min', '0')
        self.kpi_efficiency_card = self._make_stat_card('Success Rate', '0%')
        self.kpi_status_card = self._make_stat_card('Client Status', 'RUNNING', status='ok')
        for card in [self.site_card, self.device_card, self.algorithm_card, self.version_card, self.kpi_processed_card, self.kpi_throughput_card, self.kpi_efficiency_card, self.kpi_status_card]:
            layout.addWidget(card)
        return box

    def _make_stat_card(self, title: str, value: str, status: str | None = None) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet('QFrame {background:#091827; border:1px solid #183248; border-radius:10px;}')
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        title_label = QLabel(title)
        title_label.setProperty('role', 'label')
        value_label = QLabel(value)
        value_label.setWordWrap(True)
        value_label.setProperty('role', f'status_{status}' if status else 'value')
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        frame.value_label = value_label  # type: ignore[attr-defined]
        return frame

    def _build_left_panel(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.addWidget(self._build_query_and_logs_widget())
        layout.addWidget(self._build_channel_widget())
        layout.addStretch(1)
        return widget

    def _build_center_panel(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.addWidget(self._build_matrix_widget(), 6)
        layout.addWidget(self._build_metrics_widget(), 2)
        return widget

    def _build_right_panel(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.addWidget(self._build_config_widget())
        layout.addWidget(self._build_system_widget())
        return widget

    def _build_query_and_logs_widget(self) -> QWidget:
        box = QGroupBox('Query & Logs')
        layout = QVBoxLayout(box)
        query_bar = QHBoxLayout()
        self.query_keyword = QLineEdit()
        self.query_keyword.setPlaceholderText('输入包裹号 / item id / keyword')
        self.query_action_btn = QPushButton('查询')
        self.query_action_btn.setProperty('variant', 'secondary')
        query_bar.addWidget(self.query_keyword, 1)
        query_bar.addWidget(self.query_action_btn)
        layout.addLayout(query_bar)
        self.logs_editor = QPlainTextEdit()
        self.logs_editor.setReadOnly(True)
        self.logs_editor.setPlaceholderText('日志已移动到查询按钮下方 / Logs moved below Query button')
        layout.addWidget(self.logs_editor, 1)
        return box

    def _build_config_widget(self) -> QWidget:
        box = QGroupBox('Algorithm Configuration')
        layout = QVBoxLayout(box)
        form = QFormLayout()
        self.output_dir_label = QLabel(); self.output_dir_label.setWordWrap(True)
        self.rows_spin = QSpinBox(); self.rows_spin.setRange(1, 100)
        self.cols_spin = QSpinBox(); self.cols_spin.setRange(1, 100)
        self.language_combo = QComboBox(); self.language_combo.addItems(['中文', 'English'])
        self.show_aux_checkbox = QCheckBox('显示辅助信息')
        self.show_coord_checkbox = QCheckBox('显示坐标')
        form.addRow('Config Output Dir', self.output_dir_label)
        form.addRow('Rows (m)', self.rows_spin)
        form.addRow('Cols (n)', self.cols_spin)
        form.addRow('Language', self.language_combo)
        form.addRow(self.show_aux_checkbox)
        form.addRow(self.show_coord_checkbox)
        layout.addLayout(form)
        self.rows_spin.valueChanged.connect(self._matrix_shape_changed)
        self.cols_spin.valueChanged.connect(self._matrix_shape_changed)
        self.show_aux_checkbox.toggled.connect(self._matrix_option_changed)
        self.show_coord_checkbox.toggled.connect(self._matrix_option_changed)

        buttons = QGridLayout()
        preview_btn = QPushButton('Preview Config')
        write_btn = QPushButton('Write Config'); write_btn.setProperty('variant', 'secondary')
        simulate_btn = QPushButton('Inject Sample Event'); simulate_btn.setProperty('variant', 'warn')
        preview_btn.clicked.connect(self.preview_config)
        write_btn.clicked.connect(self.write_config)
        simulate_btn.clicked.connect(self.inject_sample_event)
        buttons.addWidget(preview_btn, 0, 0)
        buttons.addWidget(write_btn, 0, 1)
        buttons.addWidget(simulate_btn, 1, 0, 1, 2)
        layout.addLayout(buttons)
        self.config_preview = QPlainTextEdit(); self.config_preview.setReadOnly(True)
        self.config_status = QLabel('Ready'); self.config_status.setProperty('role', 'status_ok')
        layout.addWidget(self.config_preview, 1)
        layout.addWidget(self.config_status)
        return box

    def _build_channel_widget(self) -> QWidget:
        box = QGroupBox('Ingest Channels')
        layout = QGridLayout(box)
        self.file_status = QLabel('-'); self.tcp_status = QLabel('-'); self.http_status = QLabel('-'); self.unix_status = QLabel('-'); self.zmq_status = QLabel('-')
        pairs = [('File', self.file_status), ('TCP', self.tcp_status), ('HTTP', self.http_status), ('Unix Socket', self.unix_status), ('ZeroMQ', self.zmq_status)]
        for idx, (name, label) in enumerate(pairs):
            row = idx // 2; col = (idx % 2) * 2
            title = QLabel(name); title.setProperty('role', 'label')
            layout.addWidget(title, row, col); layout.addWidget(label, row, col + 1)
        return box

    def _build_matrix_widget(self) -> QWidget:
        box = QGroupBox('Realtime Separation Matrix')
        layout = QVBoxLayout(box)
        top = QHBoxLayout()
        self.realtime_status = QLabel('Waiting for realtime data'); self.realtime_status.setProperty('role', 'label')
        top.addWidget(self.realtime_status); top.addStretch(1)
        layout.addLayout(top)
        self.matrix_canvas = MatrixCanvas(10, 4)
        layout.addWidget(self.matrix_canvas, 1)
        self.realtime_table = QTableWidget(0, 4)
        self.realtime_table.setHorizontalHeaderLabels(['Timestamp', 'Version', 'ParcelNum', 'ParcelCount(Parsed)'])
        self.realtime_table.verticalHeader().setVisible(False)
        layout.addWidget(self.realtime_table)
        return box

    def _build_system_widget(self) -> QWidget:
        box = QGroupBox('System Health')
        layout = QGridLayout(box)
        self.cpu_card = self._make_stat_card('CPU %', '0')
        self.memory_card = self._make_stat_card('Memory %', '0')
        self.disk_card = self._make_stat_card('Disk %', '0')
        self.disk_free_card = self._make_stat_card('Disk Free GB', '0')
        layout.addWidget(self.cpu_card, 0, 0); layout.addWidget(self.memory_card, 0, 1); layout.addWidget(self.disk_card, 1, 0); layout.addWidget(self.disk_free_card, 1, 1)
        return box

    def _build_metrics_widget(self) -> QWidget:
        box = QGroupBox('KPI & Throughput')
        layout = QGridLayout(box)
        self.processed_card = self._make_stat_card('Processed', '0')
        self.success_card = self._make_stat_card('Version', '-')
        self.exception_card = self._make_stat_card('Realtime Parcels', '0')
        self.throughput_card = self._make_stat_card('Throughput / min', '0')
        self.efficiency_card = self._make_stat_card('Calc Efficiency', '0%')
        cards = [self.processed_card, self.success_card, self.exception_card, self.throughput_card, self.efficiency_card]
        positions = [(0,0),(0,1),(0,2),(1,0),(1,1)]
        for card, (r,c) in zip(cards, positions):
            layout.addWidget(card, r, c)
        return box

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

    def _matrix_shape_changed(self) -> None:
        self.matrix_canvas.set_matrix_shape(self.rows_spin.value(), self.cols_spin.value())
        self.logs_editor.appendPlainText(f'Matrix shape changed to {self.rows_spin.value()} x {self.cols_spin.value()}')

    def _matrix_option_changed(self) -> None:
        if self.last_record:
            self.matrix_canvas.set_runtime_data(self.last_record.car_speeds, self.last_record.parcels, self.show_coord_checkbox.isChecked(), self.show_aux_checkbox.isChecked())

    def _collect_overrides(self) -> dict[str, Any]:
        return {'matrix_rows': self.rows_spin.value(), 'matrix_cols': self.cols_spin.value()}

    def preview_config(self) -> None:
        try:
            payload = self.context.algorithm_config_service.build_payload(self.context.client_settings, self.context.algorithm_settings, self._collect_overrides())
            self.config_preview.setPlainText(json.dumps(payload, indent=2, ensure_ascii=False))
            self.config_status.setText('Preview generated')
        except Exception as exc:
            self.logger.exception('Preview config failed')
            QMessageBox.critical(self, 'Preview failed', str(exc))

    def write_config(self) -> None:
        try:
            path = self.context.algorithm_config_service.write(self.context.client_settings, self.context.algorithm_settings, self._collect_overrides())
            self.preview_config(); self.config_status.setText(f'Algorithm config written: {path}')
            self.logs_editor.appendPlainText(f'Wrote algorithm config: {path}')
        except Exception as exc:
            self.logger.exception('Write config failed')
            QMessageBox.critical(self, 'Write failed', str(exc))

    def inject_sample_event(self) -> None:
        sample = {
            'version': '1.0.0',
            'efficiency': '0',
            'parcelNum': '1',
            'car_speeds': [0.5] * (self.rows_spin.value() * self.cols_spin.value()),
            'parcels': [{'speed': 2, 'points': [[20, 30], [160, 70], [180, 162], [90, 183]]}],
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
        self.matrix_canvas.set_runtime_data(record.car_speeds, record.parcels, self.show_coord_checkbox.isChecked(), self.show_aux_checkbox.isChecked())
        row = self.realtime_table.rowCount(); self.realtime_table.insertRow(row)
        values = [record.timestamp.isoformat(timespec='seconds'), record.version, str(record.parcel_num), str(len(record.parcels))]
        for col, text in enumerate(values):
            self.realtime_table.setItem(row, col, QTableWidgetItem(text))
        while self.realtime_table.rowCount() > 50:
            self.realtime_table.removeRow(0)
        self.realtime_status.setText(f'Last update: {record.timestamp.isoformat(timespec="seconds")} | parcels={record.parcel_num}')
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
