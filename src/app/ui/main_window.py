from __future__ import annotations

import json
import logging
from typing import Any

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QFormLayout,
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
    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        self.logger = logging.getLogger(__name__)
        self.setWindowTitle('Single Piece Client')
        self.resize(1360, 860)

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.addWidget(self._build_header())
        body = QHBoxLayout()
        body.addWidget(self._build_left_panel(), 1)
        body.addWidget(self._build_center_panel(), 2)
        body.addWidget(self._build_right_panel(), 1)
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

    def _build_header(self) -> QWidget:
        box = QGroupBox('Station Overview')
        layout = QGridLayout(box)
        self.site_card = QLabel('-')
        self.device_card = QLabel('-')
        self.algorithm_card = QLabel('-')
        self.channels_card = QLabel('-')
        self.kpi_processed = QLabel('0')
        self.kpi_throughput = QLabel('0')
        self.kpi_efficiency = QLabel('0%')
        self.kpi_status = QLabel('RUNNING')
        layout.addWidget(QLabel('Site'), 0, 0)
        layout.addWidget(self.site_card, 0, 1)
        layout.addWidget(QLabel('Device'), 0, 2)
        layout.addWidget(self.device_card, 0, 3)
        layout.addWidget(QLabel('Algorithm'), 0, 4)
        layout.addWidget(self.algorithm_card, 0, 5)
        layout.addWidget(QLabel('Channels'), 1, 0)
        layout.addWidget(self.channels_card, 1, 1, 1, 3)
        layout.addWidget(QLabel('Processed'), 1, 4)
        layout.addWidget(self.kpi_processed, 1, 5)
        layout.addWidget(QLabel('Throughput/min'), 2, 0)
        layout.addWidget(self.kpi_throughput, 2, 1)
        layout.addWidget(QLabel('Efficiency'), 2, 2)
        layout.addWidget(self.kpi_efficiency, 2, 3)
        layout.addWidget(QLabel('Client Status'), 2, 4)
        layout.addWidget(self.kpi_status, 2, 5)
        return box

    def _build_left_panel(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(self._build_config_widget())
        layout.addWidget(self._build_channel_widget())
        return widget

    def _build_center_panel(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(self._build_realtime_widget())
        layout.addWidget(self._build_metrics_widget())
        return widget

    def _build_right_panel(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(self._build_system_widget())
        layout.addWidget(self._build_logs_widget())
        return widget

    def _build_config_widget(self) -> QWidget:
        box = QGroupBox('Algorithm Configuration')
        layout = QVBoxLayout(box)
        form = QFormLayout()
        self.output_dir_label = QLabel()
        self.speed_edit = QLineEdit('1.0')
        self.threshold_edit = QLineEdit('0.85')
        form.addRow('Config Output Dir', self.output_dir_label)
        form.addRow('Speed', self.speed_edit)
        form.addRow('Threshold', self.threshold_edit)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        preview_btn = QPushButton('Preview Config')
        write_btn = QPushButton('Write Config')
        simulate_btn = QPushButton('Inject Sample Event')
        preview_btn.clicked.connect(self.preview_config)
        write_btn.clicked.connect(self.write_config)
        simulate_btn.clicked.connect(self.inject_sample_event)
        buttons.addWidget(preview_btn)
        buttons.addWidget(write_btn)
        buttons.addWidget(simulate_btn)
        layout.addLayout(buttons)

        self.config_preview = QPlainTextEdit()
        self.config_preview.setReadOnly(True)
        self.config_status = QLabel('Ready')
        layout.addWidget(self.config_preview)
        layout.addWidget(self.config_status)
        return box

    def _build_channel_widget(self) -> QWidget:
        box = QGroupBox('Ingest Channels')
        form = QFormLayout(box)
        self.file_status = QLabel('-')
        self.tcp_status = QLabel('-')
        self.http_status = QLabel('-')
        self.unix_status = QLabel('-')
        self.zmq_status = QLabel('-')
        form.addRow('File', self.file_status)
        form.addRow('TCP', self.tcp_status)
        form.addRow('HTTP', self.http_status)
        form.addRow('Unix Socket', self.unix_status)
        form.addRow('ZeroMQ', self.zmq_status)
        return box

    def _build_realtime_widget(self) -> QWidget:
        box = QGroupBox('Realtime Feed')
        layout = QVBoxLayout(box)
        self.realtime_status = QLabel('Waiting for realtime data')
        self.realtime_table = QTableWidget(0, 6)
        self.realtime_table.setHorizontalHeaderLabels(
            ['Timestamp', 'Item', 'Device', 'Result', 'Proc(ms)', 'Exception']
        )
        layout.addWidget(self.realtime_status)
        layout.addWidget(self.realtime_table)
        return box

    def _build_system_widget(self) -> QWidget:
        box = QGroupBox('System Health')
        form = QFormLayout(box)
        self.cpu_label = QLabel('0')
        self.memory_label = QLabel('0')
        self.disk_label = QLabel('0')
        self.disk_free_label = QLabel('0')
        form.addRow('CPU %', self.cpu_label)
        form.addRow('Memory %', self.memory_label)
        form.addRow('Disk %', self.disk_label)
        form.addRow('Disk Free GB', self.disk_free_label)
        return box

    def _build_metrics_widget(self) -> QWidget:
        box = QGroupBox('KPI & Throughput')
        form = QFormLayout(box)
        self.processed_label = QLabel('0')
        self.success_label = QLabel('0')
        self.exception_label = QLabel('0')
        self.throughput_label = QLabel('0')
        self.efficiency_label = QLabel('0')
        form.addRow('Processed', self.processed_label)
        form.addRow('Success', self.success_label)
        form.addRow('Exception', self.exception_label)
        form.addRow('Throughput / min', self.throughput_label)
        form.addRow('Efficiency', self.efficiency_label)
        return box

    def _build_logs_widget(self) -> QWidget:
        box = QGroupBox('Logs / Alerts')
        layout = QVBoxLayout(box)
        self.logs_editor = QPlainTextEdit()
        self.logs_editor.setReadOnly(True)
        layout.addWidget(self.logs_editor)
        return box

    def _load_context_values(self) -> None:
        client = self.context.client_settings
        algo = self.context.algorithm_settings
        self.site_card.setText(client.site_id)
        self.device_card.setText(client.device_id)
        self.algorithm_card.setText(algo.algorithm_name)
        self.channels_card.setText(', '.join(client.ingest.enabled_channels) or '-')
        self.output_dir_label.setText(str(algo.config_output_dir))
        if hasattr(algo, 'speed'):
            self.speed_edit.setText(str(getattr(algo, 'speed')))
        if hasattr(algo, 'threshold'):
            self.threshold_edit.setText(str(getattr(algo, 'threshold')))
        self._set_channel_status('file', client.ingest.file.enabled)
        self._set_channel_status('tcp', client.ingest.tcp.enabled)
        self._set_channel_status('http', client.ingest.http.enabled)
        self._set_channel_status('unix_socket', client.ingest.unix_socket.enabled)
        self._set_channel_status('zeromq', client.ingest.zeromq.enabled)
        self.logs_editor.appendPlainText(
            'Enabled channels: ' + ', '.join(self.context.channel_manager.enabled_channel_names())
        )

    def _set_channel_status(self, name: str, enabled: bool) -> None:
        target = {
            'file': self.file_status,
            'tcp': self.tcp_status,
            'http': self.http_status,
            'unix_socket': self.unix_status,
            'zeromq': self.zmq_status,
        }[name]
        target.setText('ENABLED' if enabled else 'DISABLED')

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
        except Exception as exc:
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
        except Exception as exc:
            QMessageBox.critical(self, 'Write failed', str(exc))

    def inject_sample_event(self) -> None:
        self.context.inject_sample_event()
        self.logs_editor.appendPlainText('Injected sample event through first available channel')

    def _handle_records(self, records: list[RealtimeRecord], metrics: ThroughputMetrics) -> None:
        for record in records[-20:]:
            row = self.realtime_table.rowCount()
            self.realtime_table.insertRow(row)
            self.realtime_table.setItem(row, 0, QTableWidgetItem(record.timestamp.isoformat(timespec='seconds')))
            self.realtime_table.setItem(row, 1, QTableWidgetItem(record.item_id))
            self.realtime_table.setItem(row, 2, QTableWidgetItem(record.device_id))
            self.realtime_table.setItem(row, 3, QTableWidgetItem(record.result))
            self.realtime_table.setItem(row, 4, QTableWidgetItem(str(record.process_time_ms)))
            self.realtime_table.setItem(row, 5, QTableWidgetItem(record.exception_type or ''))
        if records:
            self.realtime_status.setText(f'Last update: {records[-1].timestamp.isoformat(timespec="seconds")}')
        while self.realtime_table.rowCount() > 200:
            self.realtime_table.removeRow(0)
        self._update_metrics(metrics)
        self.logs_editor.appendPlainText(f'Received {len(records)} realtime records')

    def _refresh_system(self) -> None:
        snapshot = self.context.system_monitor_service.collect()
        self._update_system(snapshot)

    def _update_system(self, snapshot: SystemSnapshot) -> None:
        self.cpu_label.setText(f'{snapshot.cpu_percent:.1f}')
        self.memory_label.setText(f'{snapshot.memory_percent:.1f}')
        self.disk_label.setText(f'{snapshot.disk_percent:.1f}')
        self.disk_free_label.setText(f'{snapshot.disk_free_gb:.2f}')

    def _update_metrics(self, metrics: ThroughputMetrics) -> None:
        self.processed_label.setText(str(metrics.processed_count))
        self.success_label.setText(str(metrics.success_count))
        self.exception_label.setText(str(metrics.exception_count))
        self.throughput_label.setText(f'{metrics.throughput_per_min:.2f}')
        self.efficiency_label.setText(f'{metrics.efficiency_rate:.2%}')
        self.kpi_processed.setText(str(metrics.processed_count))
        self.kpi_throughput.setText(f'{metrics.throughput_per_min:.2f}')
        self.kpi_efficiency.setText(f'{metrics.efficiency_rate:.2%}')

    def closeEvent(self, event) -> None:  # noqa: N802
        self.context.stop()
        event.accept()
