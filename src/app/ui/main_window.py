from __future__ import annotations

import json
import logging
from typing import Any

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
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
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.app_context import AppContext
from app.domain.models.realtime_record import RealtimeRecord
from app.domain.models.system_snapshot import SystemSnapshot
from app.domain.models.throughput_metrics import ThroughputMetrics


class MainWindow(QMainWindow):
    """Main operator-facing window.

    Updated UI goals:
    - main theme color uses #00A3FF
    - top navigation provides Settings / Query / Help entry points
    - logs panel is moved below the Query button area
    - center area remains the primary realtime and KPI workspace
    """

    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.logger = logging.getLogger(__name__)
        self.setWindowTitle('单件分离客户端 / Single Piece Client')
        self.resize(1460, 940)
        self.setMinimumSize(1280, 820)
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
        body.addWidget(self._build_center_panel(), 7)
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
        self.logger.info('Main window initialized and client started')
        self.statusBar().showMessage('Client started')

    def _apply_theme(self) -> None:
        self.setStyleSheet(
            """
            QWidget {
                background: #0b1220;
                color: #e5e7eb;
                font-size: 13px;
            }
            QMainWindow { background: #08101d; }
            QGroupBox {
                border: 1px solid #1d3448;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 12px;
                background: #111827;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 6px 0 6px;
                color: #00A3FF;
            }
            QLabel[role="label"] { color: #8ca4b8; font-size: 12px; }
            QLabel[role="value"] { color: #f8fafc; font-size: 18px; font-weight: 700; }
            QLabel[role="status_ok"] { color: #00A3FF; font-weight: 700; }
            QLabel[role="status_off"] { color: #94a3b8; font-weight: 700; }
            QLabel[role="status_warn"] { color: #fbbf24; font-weight: 700; }
            QLabel[role="status_err"] { color: #f87171; font-weight: 700; }
            QLineEdit, QPlainTextEdit, QTableWidget {
                background: #0a1726;
                border: 1px solid #1f3850;
                border-radius: 8px;
                padding: 6px;
                selection-background-color: #00A3FF;
            }
            QPushButton {
                background: #00A3FF;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
                font-weight: 600;
            }
            QPushButton:hover { background: #13b0ff; }
            QPushButton[variant="secondary"] { background: #27455d; }
            QPushButton[variant="warn"] { background: #b45309; }
            QPushButton[variant="nav"] {
                background: transparent;
                border-radius: 6px;
                color: #dbeafe;
                padding: 8px 20px;
                border: 1px solid transparent;
            }
            QPushButton[variant="nav"]:hover {
                background: #0b2033;
                border: 1px solid #00A3FF;
            }
            QHeaderView::section {
                background: #102235;
                color: #cbd5e1;
                border: none;
                padding: 8px;
                font-weight: 600;
            }
            QTableWidget { gridline-color: #173247; }
            QStatusBar { background: #111827; color: #cbd5e1; }
            """
        )

    def _build_top_navigation(self) -> QWidget:
        box = QFrame()
        box.setStyleSheet('QFrame {background:#0e1b2d; border:1px solid #183248; border-radius:10px;}')
        layout = QHBoxLayout(box)
        layout.setContentsMargins(12, 8, 12, 8)
        self.title_label = QLabel('单件分离SCS')
        self.title_label.setStyleSheet('QLabel {font-size: 22px; font-weight: 700; color: #00A3FF;}')
        layout.addWidget(self.title_label)
        layout.addSpacing(24)

        self.settings_btn = QPushButton('设置 / Settings')
        self.settings_btn.setProperty('variant', 'nav')
        self.query_btn = QPushButton('查询 / Query')
        self.query_btn.setProperty('variant', 'nav')
        self.help_btn = QPushButton('帮助 / Help')
        self.help_btn.setProperty('variant', 'nav')
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.query_btn)
        layout.addWidget(self.help_btn)
        layout.addStretch(1)
        return box

    def _build_header_bar(self) -> QWidget:
        box = QGroupBox('Station Overview')
        layout = QHBoxLayout(box)
        layout.setSpacing(10)
        self.site_card = self._make_stat_card('Site', '-')
        self.device_card = self._make_stat_card('Device', '-')
        self.algorithm_card = self._make_stat_card('Algorithm', '-')
        self.version_card = self._make_stat_card('Version', '-')
        self.kpi_processed_card = self._make_stat_card('Parcel Count', '0')
        self.kpi_throughput_card = self._make_stat_card('Throughput/min', '0')
        self.kpi_efficiency_card = self._make_stat_card('Success Rate', '0%')
        self.kpi_status_card = self._make_stat_card('Client Status', 'RUNNING', status='ok')
        for card in [
            self.site_card,
            self.device_card,
            self.algorithm_card,
            self.version_card,
            self.kpi_processed_card,
            self.kpi_throughput_card,
            self.kpi_efficiency_card,
            self.kpi_status_card,
        ]:
            layout.addWidget(card)
        return box

    def _make_stat_card(self, title: str, value: str, status: str | None = None) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.NoFrame)
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
        layout.addWidget(self._build_realtime_widget(), 3)
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
        self.output_dir_label = QLabel()
        self.output_dir_label.setWordWrap(True)
        self.speed_edit = QLineEdit('1.0')
        self.threshold_edit = QLineEdit('0.85')
        form.addRow('Config Output Dir', self.output_dir_label)
        form.addRow('Speed', self.speed_edit)
        form.addRow('Threshold', self.threshold_edit)
        layout.addLayout(form)

        buttons = QGridLayout()
        preview_btn = QPushButton('Preview Config')
        write_btn = QPushButton('Write Config')
        write_btn.setProperty('variant', 'secondary')
        simulate_btn = QPushButton('Inject Sample Event')
        simulate_btn.setProperty('variant', 'warn')
        preview_btn.clicked.connect(self.preview_config)
        write_btn.clicked.connect(self.write_config)
        simulate_btn.clicked.connect(self.inject_sample_event)
        buttons.addWidget(preview_btn, 0, 0)
        buttons.addWidget(write_btn, 0, 1)
        buttons.addWidget(simulate_btn, 1, 0, 1, 2)
        layout.addLayout(buttons)

        self.config_preview = QPlainTextEdit()
        self.config_preview.setReadOnly(True)
        self.config_preview.setPlaceholderText('Algorithm config preview will appear here...')
        self.config_status = QLabel('Ready')
        self.config_status.setProperty('role', 'status_ok')
        layout.addWidget(self.config_preview, 1)
        layout.addWidget(self.config_status)
        return box

    def _build_channel_widget(self) -> QWidget:
        box = QGroupBox('Ingest Channels')
        layout = QGridLayout(box)
        self.file_status = QLabel('-')
        self.tcp_status = QLabel('-')
        self.http_status = QLabel('-')
        self.unix_status = QLabel('-')
        self.zmq_status = QLabel('-')
        pairs = [
            ('File', self.file_status),
            ('TCP', self.tcp_status),
            ('HTTP', self.http_status),
            ('Unix Socket', self.unix_status),
            ('ZeroMQ', self.zmq_status),
        ]
        for idx, (name, label) in enumerate(pairs):
            row = idx // 2
            col = (idx % 2) * 2
            title = QLabel(name)
            title.setProperty('role', 'label')
            layout.addWidget(title, row, col)
            layout.addWidget(label, row, col + 1)
        return box

    def _build_realtime_widget(self) -> QWidget:
        box = QGroupBox('Realtime Feed')
        layout = QVBoxLayout(box)
        self.realtime_status = QLabel('Waiting for realtime data')
        self.realtime_status.setProperty('role', 'label')
        self.realtime_table = QTableWidget(0, 6)
        self.realtime_table.setHorizontalHeaderLabels(
            ['Timestamp', 'Item', 'Device', 'Result', 'Proc(ms)', 'Exception']
        )
        self.realtime_table.verticalHeader().setVisible(False)
        self.realtime_table.setAlternatingRowColors(True)
        self.realtime_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.realtime_status)
        layout.addWidget(self.realtime_table, 1)
        return box

    def _build_system_widget(self) -> QWidget:
        box = QGroupBox('System Health')
        layout = QGridLayout(box)
        self.cpu_card = self._make_stat_card('CPU %', '0')
        self.memory_card = self._make_stat_card('Memory %', '0')
        self.disk_card = self._make_stat_card('Disk %', '0')
        self.disk_free_card = self._make_stat_card('Disk Free GB', '0')
        layout.addWidget(self.cpu_card, 0, 0)
        layout.addWidget(self.memory_card, 0, 1)
        layout.addWidget(self.disk_card, 1, 0)
        layout.addWidget(self.disk_free_card, 1, 1)
        return box

    def _build_metrics_widget(self) -> QWidget:
        box = QGroupBox('KPI & Throughput')
        layout = QGridLayout(box)
        self.processed_card = self._make_stat_card('Processed', '0')
        self.success_card = self._make_stat_card('Success', '0')
        self.exception_card = self._make_stat_card('Exception', '0')
        self.throughput_card = self._make_stat_card('Throughput / min', '0')
        self.efficiency_card = self._make_stat_card('Efficiency', '0%')
        cards = [
            self.processed_card,
            self.success_card,
            self.exception_card,
            self.throughput_card,
            self.efficiency_card,
        ]
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
        for card, (r, c) in zip(cards, positions):
            layout.addWidget(card, r, c)
        return box

    def _load_context_values(self) -> None:
        client = self.context.client_settings
        algo = self.context.algorithm_settings
        self.site_card.value_label.setText(client.site_id)
        self.device_card.value_label.setText(client.device_id)
        self.algorithm_card.value_label.setText(algo.algorithm_name)
        self.version_card.value_label.setText(getattr(algo, 'version', '1.0.0') if hasattr(algo, 'version') else '1.0.0')
        self.output_dir_label.setText(str(algo.config_output_dir))
        if hasattr(algo, 'speed'):
            self.speed_edit.setText(str(getattr(algo, 'speed')))
        if hasattr(algo, 'threshold'):
            self.threshold_edit.setText(str(getattr(algo, 'threshold')))
        self._set_channel_status(self.file_status, client.ingest.file.enabled)
        self._set_channel_status(self.tcp_status, client.ingest.tcp.enabled)
        self._set_channel_status(self.http_status, client.ingest.http.enabled)
        self._set_channel_status(self.unix_status, client.ingest.unix_socket.enabled)
        self._set_channel_status(self.zmq_status, client.ingest.zeromq.enabled)
        self.logs_editor.appendPlainText('Enabled channels: ' + ', '.join(self.context.channel_manager.enabled_channel_names()))
        self.logger.info('UI loaded context values for site=%s device=%s', client.site_id, client.device_id)

    def _set_channel_status(self, label: QLabel, enabled: bool) -> None:
        label.setText('ONLINE' if enabled else 'OFF')
        label.setProperty('role', 'status_ok' if enabled else 'status_off')
        label.style().unpolish(label)
        label.style().polish(label)

    def _collect_overrides(self) -> dict[str, Any]:
        overrides: dict[str, Any] = {}
        if self.speed_edit.text().strip():
            overrides['speed'] = float(self.speed_edit.text())
        if self.threshold_edit.text().strip():
            overrides['threshold'] = float(self.threshold_edit.text())
        return overrides

    def preview_config(self) -> None:
        try:
            payload = self.context.algorithm_config_service.build_payload(
                self.context.client_settings,
                self.context.algorithm_settings,
                self._collect_overrides(),
            )
            self.config_preview.setPlainText(json.dumps(payload, indent=2, ensure_ascii=False))
            self.config_status.setText('Preview generated')
            self.logger.info('Previewed algorithm config')
        except Exception as exc:
            self.logger.exception('Preview config failed')
            QMessageBox.critical(self, 'Preview failed', str(exc))

    def write_config(self) -> None:
        try:
            path = self.context.algorithm_config_service.write(
                self.context.client_settings,
                self.context.algorithm_settings,
                self._collect_overrides(),
            )
            self.preview_config()
            self.config_status.setText(f'Algorithm config written: {path}')
            self.logs_editor.appendPlainText(f'Wrote algorithm config: {path}')
            self.logger.info('Wrote algorithm config through UI: %s', path)
        except Exception as exc:
            self.logger.exception('Write config failed')
            QMessageBox.critical(self, 'Write failed', str(exc))

    def inject_sample_event(self) -> None:
        self.context.inject_sample_event()
        self.logs_editor.appendPlainText('Injected sample event through first available channel')
        self.logger.info('Injected sample event from UI')

    def _handle_records(self, records: list[RealtimeRecord], metrics: ThroughputMetrics) -> None:
        for record in records[-20:]:
            row = self.realtime_table.rowCount()
            self.realtime_table.insertRow(row)
            items = [
                record.timestamp.isoformat(timespec='seconds'),
                record.item_id,
                record.device_id,
                record.result,
                str(record.process_time_ms),
                record.exception_type or '',
            ]
            for col, text in enumerate(items):
                item = QTableWidgetItem(text)
                if col == 3:
                    self._color_result_item(item, record.result)
                self.realtime_table.setItem(row, col, item)
        if records:
            self.realtime_status.setText(f'Last update: {records[-1].timestamp.isoformat(timespec="seconds")}')
        while self.realtime_table.rowCount() > 300:
            self.realtime_table.removeRow(0)
        self._update_metrics(metrics)
        self.logs_editor.appendPlainText(f'Received {len(records)} realtime records')
        self.logger.info('UI received %d records', len(records))

    def _color_result_item(self, item: QTableWidgetItem, result: str) -> None:
        val = result.lower()
        if val == 'success':
            item.setForeground(QColor('#00A3FF'))
        elif val in {'fail', 'error'}:
            item.setForeground(QColor('#f87171'))
        else:
            item.setForeground(QColor('#fbbf24'))

    def _refresh_system(self) -> None:
        snapshot = self.context.system_monitor_service.collect()
        self._update_system(snapshot)

    def _update_system(self, snapshot: SystemSnapshot) -> None:
        self.cpu_card.value_label.setText(f'{snapshot.cpu_percent:.1f}')
        self.memory_card.value_label.setText(f'{snapshot.memory_percent:.1f}')
        self.disk_card.value_label.setText(f'{snapshot.disk_percent:.1f}')
        self.disk_free_card.value_label.setText(f'{snapshot.disk_free_gb:.2f}')

    def _update_metrics(self, metrics: ThroughputMetrics) -> None:
        self.processed_card.value_label.setText(str(metrics.processed_count))
        self.success_card.value_label.setText(str(metrics.success_count))
        self.exception_card.value_label.setText(str(metrics.exception_count))
        self.throughput_card.value_label.setText(f'{metrics.throughput_per_min:.2f}')
        self.efficiency_card.value_label.setText(f'{metrics.efficiency_rate:.2%}')
        self.kpi_processed_card.value_label.setText(str(metrics.processed_count))
        self.kpi_throughput_card.value_label.setText(f'{metrics.throughput_per_min:.2f}')
        self.kpi_efficiency_card.value_label.setText(f'{metrics.efficiency_rate:.2%}')

    def closeEvent(self, event) -> None:  # noqa: N802
        self.logger.info('Closing main window and stopping app context')
        self.context.stop()
        event.accept()
