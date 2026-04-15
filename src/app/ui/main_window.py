from __future__ import annotations

import json
import logging
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QTabWidget,
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
        self.resize(1100, 720)

        self.tabs = QTabWidget()
        self.config_widget = self._build_config_widget()
        self.realtime_widget = self._build_realtime_widget()
        self.system_widget = self._build_system_widget()
        self.metrics_widget = self._build_metrics_widget()
        self.logs_widget = self._build_logs_widget()
        self.tabs.addTab(self.config_widget, 'Config')
        self.tabs.addTab(self.realtime_widget, 'Realtime')
        self.tabs.addTab(self.system_widget, 'System')
        self.tabs.addTab(self.metrics_widget, 'Metrics')
        self.tabs.addTab(self.logs_widget, 'Logs')
        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage('Ready')

        self.context.realtime_ingest_service.on_records(self._handle_records)
        self.system_timer = QTimer(self)
        self.system_timer.setInterval(1000)
        self.system_timer.timeout.connect(self._refresh_system)
        self.system_timer.start()
        self._load_default_profile_values()

    def _build_config_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        box = QGroupBox('Algorithm Config')
        form = QFormLayout(box)
        self.site_id_edit = QLineEdit()
        self.device_id_edit = QLineEdit()
        self.target_dir_edit = QLineEdit()
        self.realtime_dir_edit = QLineEdit()
        self.speed_edit = QLineEdit('1.0')
        self.threshold_edit = QLineEdit('0.85')
        self.config_preview = QPlainTextEdit()
        self.config_preview.setReadOnly(True)
        self.config_status = QLabel('Ready')
        form.addRow('Site ID', self.site_id_edit)
        form.addRow('Device ID', self.device_id_edit)
        form.addRow('Config Output Dir', self.target_dir_edit)
        form.addRow('Realtime Input Dir', self.realtime_dir_edit)
        form.addRow('Speed', self.speed_edit)
        form.addRow('Threshold', self.threshold_edit)
        layout.addWidget(box)
        preview_btn = QPushButton('Preview')
        write_btn = QPushButton('Write Config')
        preview_btn.clicked.connect(self.preview_config)
        write_btn.clicked.connect(self.write_config)
        layout.addWidget(preview_btn)
        layout.addWidget(write_btn)
        layout.addWidget(self.config_preview)
        layout.addWidget(self.config_status)
        return widget

    def _build_realtime_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.realtime_status = QLabel('Waiting for realtime data')
        self.realtime_table = QTableWidget(0, 5)
        self.realtime_table.setHorizontalHeaderLabels(['Timestamp', 'Item', 'Device', 'Result', 'Exception'])
        layout.addWidget(self.realtime_status)
        layout.addWidget(self.realtime_table)
        return widget

    def _build_system_widget(self) -> QWidget:
        widget = QWidget()
        form = QFormLayout(widget)
        self.cpu_label = QLabel('0')
        self.memory_label = QLabel('0')
        self.disk_label = QLabel('0')
        self.disk_free_label = QLabel('0')
        form.addRow('CPU %', self.cpu_label)
        form.addRow('Memory %', self.memory_label)
        form.addRow('Disk %', self.disk_label)
        form.addRow('Disk Free GB', self.disk_free_label)
        return widget

    def _build_metrics_widget(self) -> QWidget:
        widget = QWidget()
        form = QFormLayout(widget)
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
        return widget

    def _build_logs_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.logs_editor = QPlainTextEdit()
        self.logs_editor.setReadOnly(True)
        layout.addWidget(self.logs_editor)
        return widget

    def _load_default_profile_values(self) -> None:
        if not self.context.profile_service.profiles:
            return
        site = self.context.profile_service.profiles[0]
        device = site.devices[0]
        self.site_id_edit.setText(site.site_id)
        self.device_id_edit.setText(device.device_id)
        self.target_dir_edit.setText(str(device.config_output_dir))
        self.realtime_dir_edit.setText(str(device.realtime_input_dir))
        try:
            self.context.realtime_ingest_service.start_watch(device.realtime_input_dir)
            self.logs_editor.appendPlainText(f'Watching realtime dir: {device.realtime_input_dir}')
        except Exception as exc:
            self.logs_editor.appendPlainText(f'Watch start failed: {exc}')

    def _build_runtime_config(self):
        params = {
            'speed': float(self.speed_edit.text() or 0),
            'threshold': float(self.threshold_edit.text() or 0),
        }
        return self.context.config_service.build_runtime_config(
            site_id=self.site_id_edit.text().strip(),
            device_id=self.device_id_edit.text().strip(),
            target_directory=Path(self.target_dir_edit.text().strip()),
            realtime_directory=Path(self.realtime_dir_edit.text().strip()),
            parameters=params,
        )

    def preview_config(self) -> None:
        try:
            runtime_config = self._build_runtime_config()
            payload = self.context.config_service.diff_preview(runtime_config)
            self.config_preview.setPlainText(json.dumps(payload, indent=2, ensure_ascii=False))
            self.config_status.setText('Preview generated')
        except Exception as exc:
            QMessageBox.critical(self, 'Preview failed', str(exc))

    def write_config(self) -> None:
        try:
            runtime_config = self._build_runtime_config()
            path = self.context.config_service.write(runtime_config)
            self.preview_config()
            self.config_status.setText(f'Config written: {path}')
        except Exception as exc:
            QMessageBox.critical(self, 'Write failed', str(exc))

    def _handle_records(self, records: list[RealtimeRecord]) -> None:
        for record in records[-20:]:
            row = self.realtime_table.rowCount()
            self.realtime_table.insertRow(row)
            self.realtime_table.setItem(row, 0, QTableWidgetItem(record.timestamp.isoformat(timespec='seconds')))
            self.realtime_table.setItem(row, 1, QTableWidgetItem(record.item_id))
            self.realtime_table.setItem(row, 2, QTableWidgetItem(record.device_id))
            self.realtime_table.setItem(row, 3, QTableWidgetItem(record.result))
            self.realtime_table.setItem(row, 4, QTableWidgetItem(record.exception_type or ''))
        if records:
            self.realtime_status.setText(f'Last update: {records[-1].timestamp.isoformat(timespec="seconds")}')
        while self.realtime_table.rowCount() > 200:
            self.realtime_table.removeRow(0)
        metrics = self.context.metrics_service.push_records(records)
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

    def closeEvent(self, event) -> None:  # noqa: N802
        self.context.realtime_ingest_service.stop_watch()
        event.accept()
