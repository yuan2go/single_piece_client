from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject, Property, Signal, Slot

from single_piece_qml_client.core.app_config import AppConfig
from single_piece_qml_client.domain.catalogs import equipment_catalog, initial_stats, initial_trend, parameter_catalog, setting_catalog
from single_piece_qml_client.models import RoleListModel
from single_piece_qml_client.services.log_service import LogService, now_text
from single_piece_qml_client.services.state_service import StateService, apply_saved_values


class ApplicationController(QObject):
    currentPageChanged = Signal()
    currentTimeChanged = Signal()
    runStateChanged = Signal()
    statsChanged = Signal()
    selectedLogChanged = Signal()
    trendChanged = Signal()
    toastChanged = Signal()

    def __init__(self, config: AppConfig, log_service: LogService, state_service: StateService) -> None:
        super().__init__()
        self._config = config
        self._log_service = log_service
        self._state_service = state_service
        self._current_page = 0
        self._current_time = now_text()
        self._run_state = "运行中"
        self._toast = ""
        self._stats = initial_stats()
        self._trend = initial_trend()
        self._selected_log: dict[str, Any] = {}
        self.equipment = RoleListModel(["name", "icon", "speed", "state", "count"], equipment_catalog())
        self.params = RoleListModel(["group", "key", "name", "value", "unit"], apply_saved_values(parameter_catalog(), state_service.load_prefix("param")))
        self.settings = RoleListModel(["group", "key", "name", "value", "unit"], apply_saved_values(setting_catalog(), state_service.load_prefix("setting")))
        self.logs = RoleListModel(["time", "level", "type", "module", "content", "operator", "result", "trace", "detail"], [])
        self._log_service.seed_if_empty()
        self.refreshLogs()
        self._selected_log = self.logs.get(0)

    @Property(int, notify=currentPageChanged)
    def currentPage(self) -> int: return self._current_page
    @Property(str, notify=currentTimeChanged)
    def currentTime(self) -> str: return self._current_time
    @Property(str, constant=True)
    def systemName(self) -> str: return self._config.ui.title
    @Property(str, constant=True)
    def siteName(self) -> str: return self._config.ui.site_name
    @Property(str, constant=True)
    def deviceName(self) -> str: return self._config.ui.device_name
    @Property(str, notify=runStateChanged)
    def runState(self) -> str: return self._run_state
    @Property(str, notify=toastChanged)
    def toast(self) -> str: return self._toast
    @Property("QVariantMap", notify=statsChanged)
    def stats(self) -> dict[str, Any]: return self._stats
    @Property("QVariantList", notify=trendChanged)
    def trend(self) -> list[dict[str, Any]]: return self._trend
    @Property("QVariantMap", notify=selectedLogChanged)
    def selectedLog(self) -> dict[str, Any]: return self._selected_log
    @Property(QObject, constant=True)
    def equipmentModel(self) -> RoleListModel: return self.equipment
    @Property(QObject, constant=True)
    def paramModel(self) -> RoleListModel: return self.params
    @Property(QObject, constant=True)
    def settingModel(self) -> RoleListModel: return self.settings
    @Property(QObject, constant=True)
    def logModel(self) -> RoleListModel: return self.logs

    @Slot(int)
    def setPage(self, page: int) -> None:
        self._current_page = page
        self.currentPageChanged.emit()

    @Slot()
    def startDevice(self) -> None:
        self._run_state = "运行中"
        self.runStateChanged.emit()
        self._add_log("启动设备", "设备启动命令已发送。")

    @Slot()
    def stopDevice(self) -> None:
        self._run_state = "已停止"
        self.runStateChanged.emit()
        self._add_log("停止设备", "设备停止命令已发送。")

    @Slot()
    def refreshLogs(self) -> None:
        self.logs.set_rows(self._log_service.list_recent())

    @Slot(int)
    def selectLog(self, row: int) -> None:
        self._selected_log = self.logs.get(row)
        self.selectedLogChanged.emit()

    @Slot(int, str)
    def updateParam(self, row: int, value: str) -> None:
        self.params.update_value(row, "value", value)

    @Slot(int, str)
    def updateSetting(self, row: int, value: str) -> None:
        self.settings.update_value(row, "value", value)

    @Slot()
    def saveParams(self) -> None:
        self._state_service.save_prefixed_rows("param", self.params.rows())
        self._add_log("保存参数", "参数已保存到 SQLite。")

    @Slot()
    def saveSettings(self) -> None:
        self._state_service.save_prefixed_rows("setting", self.settings.rows())
        self._add_log("保存系统设置", "系统设置已保存到 SQLite。")

    def _add_log(self, content: str, detail: str) -> None:
        row = self._log_service.append("信息", "操作日志", "系统管理", content, "admin", "成功", detail)
        self.logs.prepend(row, self._config.storage.max_ui_log_rows)
        self._selected_log = row
        self.selectedLogChanged.emit()
        self._toast = detail
        self.toastChanged.emit()
