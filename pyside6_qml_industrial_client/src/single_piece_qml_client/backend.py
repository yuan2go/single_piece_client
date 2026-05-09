from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from PySide6.QtCore import QObject, Property, QTimer, Signal, Slot


class RuntimeState(StrEnum):
    OFFLINE = "离线"
    STANDBY = "待机"
    STARTING = "启动中"
    RUNNING = "运行中"
    STOPPING = "停止中"
    FAULT = "故障"


class DemoBackend(QObject):
    """Production-shaped in-memory backend for the industrial QML UI.

    This object keeps the prototype close to the real production architecture:
    QML binds to stable Qt properties, while command slots enforce state checks
    and generate operation logs. Real PLC, Modbus, camera, algorithm and alarm
    services can later replace the in-memory data without rewriting the QML view.
    """

    runtimeChanged = Signal()
    beltCellsChanged = Signal()
    packagesChanged = Signal()
    kpisChanged = Signal()
    alarmsChanged = Signal()
    eventsChanged = Signal()
    toastChanged = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._runtime = {
            "systemName": "单件分离控制系统",
            "siteName": "自动供件",
            "deviceName": "单件分离一号线",
            "state": RuntimeState.OFFLINE.value,
            "mode": "模式一",
            "plcState": "离线",
            "cameraState": "2/4 在线",
            "photoeyeState": "正常",
            "cabinetState": "离线",
            "alarmCount": 2,
            "user": "操作员",
            "time": "2026-05-09 12:32:02",
            "startCondition": "PLC 离线，不允许启动",
            "canStart": False,
            "canStop": False,
            "canResetAlarm": True,
            "canReconnect": True,
            "canSaveParameter": True,
        }
        self._toast = {"visible": False, "level": "info", "message": ""}
        self._belt_cells = self._make_belt_cells()
        self._packages = [
            {
                "id": "PKG-A",
                "row": 0,
                "col": 1.05,
                "rowSpan": 0.62,
                "colSpan": 1.85,
                "state": "normal",
            },
            {
                "id": "PKG-B",
                "row": 1.18,
                "col": 2.1,
                "rowSpan": 0.58,
                "colSpan": 0.78,
                "state": "normal",
            },
            {
                "id": "PKG-C",
                "row": 2.06,
                "col": 0.12,
                "rowSpan": 0.66,
                "colSpan": 1.65,
                "state": "normal",
            },
        ]
        self._kpis = [
            {"label": "包裹总数", "value": "12,456", "unit": "件", "primary": True},
            {"label": "小时效率", "value": "3,200", "unit": "件/小时", "primary": True},
            {"label": "主线数量", "value": "11,820", "unit": "", "primary": False},
            {"label": "供包台数量", "value": "11,760", "unit": "", "primary": False},
            {"label": "人工线数量", "value": "320", "unit": "", "primary": False},
            {"label": "人工线比例", "value": "2.6", "unit": "%", "primary": False},
            {"label": "循环线数量", "value": "280", "unit": "", "primary": False},
            {"label": "循环线比例", "value": "2.2", "unit": "%", "primary": False},
            {"label": "重叠件数量", "value": "45", "unit": "", "primary": False},
            {"label": "异形件数量", "value": "38", "unit": "", "primary": False},
        ]
        self._alarms = [
            {
                "level": "严重",
                "title": "Modbus 通信离线",
                "target": "PLC",
                "duration": "00:03:21",
                "suggestion": "检查 PLC IP、端口、网络",
                "acknowledged": False,
                "recovered": False,
            },
            {
                "level": "警告",
                "title": "内存使用率过高 95.6%",
                "target": "系统资源",
                "duration": "00:01:58",
                "suggestion": "检查算法进程与图像缓存",
                "acknowledged": False,
                "recovered": False,
            },
        ]
        self._events = [
            {"time": "12:32:01", "level": "严重", "source": "PLC", "message": "Modbus 通信离线"},
            {"time": "12:31:58", "level": "警告", "source": "系统资源", "message": "内存使用率 95.6%"},
            {"time": "12:31:20", "level": "操作", "source": "operator", "message": "点击启动失败：PLC 离线"},
            {"time": "12:30:45", "level": "通讯", "source": "Camera", "message": "2D 相机连接正常"},
            {"time": "12:30:21", "level": "包裹", "source": "Matrix", "message": "检测到跨皮带包裹 PKG-1024"},
        ]

        self._clock = QTimer(self)
        self._clock.timeout.connect(self._update_clock)
        self._clock.start(1000)

        self._transient_timer = QTimer(self)
        self._transient_timer.setSingleShot(True)
        self._transient_timer.timeout.connect(self._complete_transient_state)

        self._toast_timer = QTimer(self)
        self._toast_timer.setSingleShot(True)
        self._toast_timer.timeout.connect(self._hide_toast)

    def _make_belt_cells(self) -> list[dict[str, object]]:
        speeds = [
            [0.00, 0.60, 0.60, 0.00],
            [0.00, 0.80, 0.80, 0.00],
            [1.00, 1.00, 0.60, 0.00],
            [0.00, 0.00, 0.00, 0.00],
        ]
        cells: list[dict[str, object]] = []
        for row, values in enumerate(speeds):
            for col, speed in enumerate(values):
                cells.append(
                    {
                        "row": row,
                        "col": col,
                        "speed": f"{speed:.2f}",
                        "status": "running" if speed > 0 else "stopped",
                    }
                )
        return cells

    def _update_clock(self) -> None:
        self._runtime["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.runtimeChanged.emit()

    def _now(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def _add_event(self, level: str, source: str, message: str) -> None:
        self._events.insert(0, {"time": self._now(), "level": level, "source": source, "message": message})
        del self._events[80:]
        self.eventsChanged.emit()

    def _show_toast(self, level: str, message: str) -> None:
        self._toast = {"visible": True, "level": level, "message": message}
        self.toastChanged.emit()
        self._toast_timer.start(2800)

    def _hide_toast(self) -> None:
        self._toast = {"visible": False, "level": "info", "message": ""}
        self.toastChanged.emit()

    def _apply_runtime_state(self, state: RuntimeState) -> None:
        self._runtime["state"] = state.value
        if state == RuntimeState.OFFLINE:
            self._runtime.update(
                {
                    "startCondition": "PLC 离线，不允许启动",
                    "canStart": False,
                    "canStop": False,
                    "canSaveParameter": True,
                }
            )
        elif state == RuntimeState.STANDBY:
            self._runtime.update(
                {
                    "startCondition": "启动条件已满足",
                    "canStart": True,
                    "canStop": False,
                    "canSaveParameter": True,
                }
            )
        elif state == RuntimeState.RUNNING:
            self._runtime.update(
                {
                    "startCondition": "设备运行中，参数保存已锁定",
                    "canStart": False,
                    "canStop": True,
                    "canSaveParameter": False,
                }
            )
        elif state in {RuntimeState.STARTING, RuntimeState.STOPPING}:
            self._runtime.update(
                {
                    "startCondition": "状态切换中，请等待",
                    "canStart": False,
                    "canStop": False,
                    "canSaveParameter": False,
                }
            )
        else:
            self._runtime.update(
                {
                    "startCondition": "设备故障，请先处理报警",
                    "canStart": False,
                    "canStop": True,
                    "canSaveParameter": False,
                }
            )
        self.runtimeChanged.emit()

    def _refresh_alarm_count(self) -> None:
        self._runtime["alarmCount"] = sum(1 for alarm in self._alarms if not alarm.get("recovered"))
        self.runtimeChanged.emit()
        self.alarmsChanged.emit()

    def _complete_transient_state(self) -> None:
        state = self._runtime["state"]
        if state == RuntimeState.STARTING.value:
            self._apply_runtime_state(RuntimeState.RUNNING)
            self._add_event("操作", "controller", "启动完成，系统进入运行中")
            self._show_toast("success", "系统已进入运行中")
        elif state == RuntimeState.STOPPING.value:
            self._apply_runtime_state(RuntimeState.STANDBY)
            self._add_event("操作", "controller", "停止完成，系统进入待机")
            self._show_toast("info", "系统已停止，当前待机")

    @Slot()
    def requestStart(self) -> None:
        if not self._runtime.get("canStart"):
            reason = str(self._runtime.get("startCondition", "当前状态不允许启动"))
            self._add_event("操作", "operator", f"启动被拒绝：{reason}")
            self._show_toast("critical", f"启动被拒绝：{reason}")
            return
        self._apply_runtime_state(RuntimeState.STARTING)
        self._add_event("操作", "operator", "执行启动命令")
        self._transient_timer.start(1200)

    @Slot()
    def requestStop(self) -> None:
        if not self._runtime.get("canStop"):
            self._add_event("操作", "operator", "停止被拒绝：当前状态不允许运行停止流程")
            self._show_toast("warning", "当前状态不允许停止")
            return
        self._apply_runtime_state(RuntimeState.STOPPING)
        self._add_event("操作", "operator", "执行停止命令")
        self._transient_timer.start(1000)

    @Slot()
    def reconnect(self) -> None:
        self._runtime["plcState"] = "在线"
        self._runtime["cabinetState"] = "在线"
        self._runtime["cameraState"] = "4/4 在线"
        for alarm in self._alarms:
            if alarm["target"] == "PLC":
                alarm["recovered"] = True
                alarm["acknowledged"] = True
        self._refresh_alarm_count()
        self._apply_runtime_state(RuntimeState.STANDBY)
        self._add_event("通讯", "PLC", "重新连接成功，PLC 与电柜恢复在线")
        self._show_toast("success", "PLC 与电柜已恢复在线，设备进入待机")

    @Slot()
    def resetAlarms(self) -> None:
        for alarm in self._alarms:
            alarm["acknowledged"] = True
        self._refresh_alarm_count()
        self._add_event("操作", "operator", "已确认当前报警")
        self._show_toast("info", "当前报警已确认")

    @Slot()
    def saveParameters(self) -> None:
        if not self._runtime.get("canSaveParameter"):
            self._add_event("操作", "engineer", "保存参数被拒绝：运行中禁止保存")
            self._show_toast("critical", "运行中禁止保存参数")
            return
        self._add_event("操作", "engineer", "保存参数成功：设备结构配置未变更")
        self._show_toast("success", "参数保存成功")

    @Property("QVariantMap", notify=runtimeChanged)
    def runtime(self) -> dict[str, object]:
        return self._runtime

    @Property("QVariantList", notify=beltCellsChanged)
    def beltCells(self) -> list[dict[str, object]]:
        return self._belt_cells

    @Property("QVariantList", notify=packagesChanged)
    def packages(self) -> list[dict[str, object]]:
        return self._packages

    @Property("QVariantList", notify=kpisChanged)
    def kpis(self) -> list[dict[str, object]]:
        return self._kpis

    @Property("QVariantList", notify=alarmsChanged)
    def alarms(self) -> list[dict[str, object]]:
        return self._alarms

    @Property("QVariantList", notify=eventsChanged)
    def events(self) -> list[dict[str, object]]:
        return self._events

    @Property("QVariantMap", notify=toastChanged)
    def toast(self) -> dict[str, object]:
        return self._toast
