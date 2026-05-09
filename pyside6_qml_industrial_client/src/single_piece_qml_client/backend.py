from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import QObject, Property, QTimer, Signal


class DemoBackend(QObject):
    """Small in-memory backend used by the QML industrial UI prototype.

    The class intentionally exposes plain QVariantMap / QVariantList data so the
    QML layer can be replaced later without changing the visual component tree.
    Real PLC, camera, algorithm, alarm and log services can update the same
    properties through a controller layer.
    """

    runtimeChanged = Signal()
    beltCellsChanged = Signal()
    packagesChanged = Signal()
    kpisChanged = Signal()
    alarmsChanged = Signal()
    eventsChanged = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._runtime = {
            "systemName": "单件分离控制系统",
            "siteName": "自动供件",
            "deviceName": "单件分离一号线",
            "state": "离线",
            "mode": "模式一",
            "plcState": "离线",
            "cameraState": "2/4 在线",
            "photoeyeState": "正常",
            "cabinetState": "离线",
            "alarmCount": 2,
            "user": "操作员",
            "time": "2026-05-09 12:32:02",
            "startCondition": "PLC 离线，不允许启动",
        }
        self._belt_cells = self._make_belt_cells()
        self._packages = [
            {"id": "PKG-A", "row": 0, "col": 1.05, "rowSpan": 0.62, "colSpan": 1.85, "state": "normal"},
            {"id": "PKG-B", "row": 1.18, "col": 2.1, "rowSpan": 0.58, "colSpan": 0.78, "state": "normal"},
            {"id": "PKG-C", "row": 2.06, "col": 0.12, "rowSpan": 0.66, "colSpan": 1.65, "state": "normal"},
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
            },
            {
                "level": "警告",
                "title": "内存使用率过高 95.6%",
                "target": "系统资源",
                "duration": "00:01:58",
                "suggestion": "检查算法进程与图像缓存",
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
