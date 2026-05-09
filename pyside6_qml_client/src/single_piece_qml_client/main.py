from __future__ import annotations

import os
import random
import sqlite3
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, QObject, Property, QTimer, Qt, Signal, Slot, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


class DictListModel(QAbstractListModel):
    def __init__(self, roles: list[str], rows: list[dict[str, Any]] | None = None) -> None:
        super().__init__()
        self._roles = {Qt.UserRole + i + 1: name for i, name in enumerate(roles)}
        self._names = {name: role for role, name in self._roles.items()}
        self._rows = rows or []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else len(self._rows)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid() or index.row() < 0 or index.row() >= len(self._rows):
            return None
        return self._rows[index.row()].get(self._roles.get(role, ""))

    def roleNames(self) -> dict[int, QByteArray]:  # noqa: N802
        return {role: QByteArray(name.encode()) for role, name in self._roles.items()}

    def set_rows(self, rows: list[dict[str, Any]]) -> None:
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def prepend(self, row: dict[str, Any], limit: int = 300) -> None:
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._rows.insert(0, row)
        self.endInsertRows()
        if len(self._rows) > limit:
            self.beginRemoveRows(QModelIndex(), limit, len(self._rows) - 1)
            del self._rows[limit:]
            self.endRemoveRows()

    @Slot(int, result="QVariantMap")
    def get(self, row: int) -> dict[str, Any]:
        return self._rows[row].copy() if 0 <= row < len(self._rows) else {}

    @Slot(int, str, str)
    def setValue(self, row: int, key: str, value: str) -> None:  # noqa: N802
        if 0 <= row < len(self._rows) and key in self._names:
            self._rows[row][key] = value
            idx = self.index(row, 0)
            self.dataChanged.emit(idx, idx, [self._names[key]])

    def rows(self) -> list[dict[str, Any]]:
        return [row.copy() for row in self._rows]


class Backend(QObject):
    currentPageChanged = Signal()
    currentTimeChanged = Signal()
    runStateChanged = Signal()
    statsChanged = Signal()
    selectedLogChanged = Signal()
    trendChanged = Signal()
    toastChanged = Signal()

    def __init__(self, root: Path) -> None:
        super().__init__()
        self.root = root
        self.db_path = Path(os.getenv("SPC_CLIENT_DB", root / "runtime" / "single_piece_client.db"))
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.db_path)
        self.db.row_factory = sqlite3.Row
        self._init_db()
        self._current_page = 0
        self._current_time = ""
        self._run_state = "运行中"
        self._toast = ""
        self._selected_log: dict[str, Any] = {}
        self._stats = {
            "total": 12458, "current": 85, "beat": 0.68, "uptime": "02:18:45",
            "throughput": 1024, "avgLen": 465, "supply": 65, "supplyEff": 625,
            "supplyRatio": 67.2, "manual": 8, "manualEff": 76, "manualRatio": 8.6,
            "cycle": 12, "cycleEff": 96, "cycleRatio": 12.2,
        }
        self._trend = self._make_trend()
        self.equipment = DictListModel(["name", "icon", "speed", "state", "count"], self._equipment())
        self.params = DictListModel(["group", "key", "name", "value", "unit"], self._params())
        self.settings = DictListModel(["group", "key", "name", "value", "unit"], self._settings())
        self.logs = DictListModel(["time", "level", "type", "module", "content", "operator", "result", "trace", "detail"], [])
        self._seed_logs()
        self.refreshLogs()
        self._selected_log = self.logs.get(0)
        timer = QTimer(self)
        timer.timeout.connect(self._tick)
        timer.start(1000)
        self._tick()
        data_timer = QTimer(self)
        data_timer.timeout.connect(self._simulate)
        data_timer.start(3000)

    def _init_db(self) -> None:
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT, level TEXT, type TEXT, module TEXT, content TEXT,
            operator TEXT, result TEXT, trace TEXT, detail TEXT
        );
        CREATE TABLE IF NOT EXISTS kv(key TEXT PRIMARY KEY, value TEXT, updated_at TEXT);
        """)
        self.db.commit()

    @Property(int, notify=currentPageChanged)
    def currentPage(self) -> int: return self._current_page
    @Property(str, notify=currentTimeChanged)
    def currentTime(self) -> str: return self._current_time
    @Property(str, constant=True)
    def systemName(self) -> str: return "单件分离控制系统"
    @Property(str, constant=True)
    def siteName(self) -> str: return "自动供件产线A"
    @Property(str, constant=True)
    def deviceName(self) -> str: return "单件分离控制机"
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
    def equipmentModel(self) -> DictListModel: return self.equipment
    @Property(QObject, constant=True)
    def paramModel(self) -> DictListModel: return self.params
    @Property(QObject, constant=True)
    def settingModel(self) -> DictListModel: return self.settings
    @Property(QObject, constant=True)
    def logModel(self) -> DictListModel: return self.logs

    @Slot(int)
    def setPage(self, page: int) -> None:
        self._current_page = page
        self.currentPageChanged.emit()

    @Slot()
    def startDevice(self) -> None:
        self._run_state = "运行中"
        self.runStateChanged.emit()
        self._add_log("信息", "操作日志", "系统管理", "启动设备", "admin", "成功", "设备启动命令已发送。")
        self._toast_msg("设备启动命令已发送")

    @Slot()
    def stopDevice(self) -> None:
        self._run_state = "已停止"
        self.runStateChanged.emit()
        self._add_log("信息", "操作日志", "系统管理", "停止设备", "admin", "成功", "设备停止命令已发送。")
        self._toast_msg("设备停止命令已发送")

    @Slot()
    def refreshLogs(self) -> None:
        rows = [dict(r) for r in self.db.execute("SELECT time,level,type,module,content,operator,result,trace,detail FROM logs ORDER BY id DESC LIMIT 300")]
        self.logs.set_rows(rows)

    @Slot(int)
    def selectLog(self, row: int) -> None:
        self._selected_log = self.logs.get(row)
        self.selectedLogChanged.emit()

    @Slot(int, str)
    def updateParam(self, row: int, value: str) -> None:
        self.params.setValue(row, "value", value)

    @Slot(int, str)
    def updateSetting(self, row: int, value: str) -> None:
        self.settings.setValue(row, "value", value)

    @Slot()
    def saveParams(self) -> None:
        for r in self.params.rows():
            self.db.execute("INSERT OR REPLACE INTO kv VALUES(?,?,?)", ("param." + r["key"], r["value"], self._now()))
        self.db.commit()
        self._add_log("信息", "操作日志", "参数配置", "参数保存成功：分离矩阵(4×4)", "admin", "成功", "参数已保存到 SQLite。")
        self._toast_msg("参数已保存到 SQLite")

    @Slot()
    def saveSettings(self) -> None:
        for r in self.settings.rows():
            self.db.execute("INSERT OR REPLACE INTO kv VALUES(?,?,?)", ("setting." + r["key"], r["value"], self._now()))
        self.db.commit()
        self._add_log("信息", "操作日志", "系统设置", "系统设置保存成功", "admin", "成功", "系统设置已保存到 SQLite。")
        self._toast_msg("系统设置已保存到 SQLite")

    def _tick(self) -> None:
        self._current_time = self._now()
        self.currentTimeChanged.emit()

    def _simulate(self) -> None:
        if self._run_state != "运行中":
            return
        self._stats["total"] += random.randint(3, 8)
        self._stats["current"] = max(40, min(130, self._stats["current"] + random.randint(-4, 5)))
        self._stats["throughput"] = max(900, min(1350, self._stats["throughput"] + random.randint(-30, 36)))
        self._stats["beat"] = round(max(0.52, min(0.82, self._stats["beat"] + random.uniform(-0.02, 0.02))), 2)
        self.statsChanged.emit()
        p = self._trend[-1].copy()
        p["label"] = datetime.now().strftime("%H:%M")
        for k, lo, hi in [("main", 1000, 1450), ("supply", 540, 820), ("manual", 160, 420), ("cycle", 60, 190)]:
            p[k] = max(lo, min(hi, p[k] + random.randint(-40, 45)))
        self._trend = self._trend[1:] + [p]
        self.trendChanged.emit()

    def _add_log(self, level: str, typ: str, module: str, content: str, operator: str, result: str, detail: str) -> None:
        row = {"time": self._now(), "level": level, "type": typ, "module": module, "content": content, "operator": operator, "result": result, "trace": uuid.uuid4().hex[:16], "detail": detail}
        self.db.execute("INSERT INTO logs(time,level,type,module,content,operator,result,trace,detail) VALUES(:time,:level,:type,:module,:content,:operator,:result,:trace,:detail)", row)
        self.db.commit()
        self.logs.prepend(row)
        self._selected_log = row
        self.selectedLogChanged.emit()

    def _toast_msg(self, msg: str) -> None:
        self._toast = msg
        self.toastChanged.emit()
        QTimer.singleShot(2400, lambda: (setattr(self, "_toast", ""), self.toastChanged.emit()))

    def _seed_logs(self) -> None:
        if self.db.execute("SELECT COUNT(*) FROM logs").fetchone()[0]:
            return
        demo = [
            ("信息", "通讯日志", "PLC通讯", "PLC重连成功，设备恢复通讯", "系统", "成功", "PLC连接已恢复。\nIP：192.168.2.15\n端口：5000\n响应时间：35ms"),
            ("信息", "操作日志", "系统管理", "参数保存成功：分离矩阵(4×4)", "admin", "成功", "配置写入成功。"),
            ("信息", "包裹事件", "分离矩阵", "包裹通过分离矩阵：3-2，重量：112g", "系统", "成功", "包裹横跨 3-2、3-3 两个皮带单元。"),
            ("警告", "通讯日志", "相机模块", "相机模块通讯超时，正在重试（1/3）", "系统", "重试中", "相机响应超过阈值。"),
            ("异常", "通讯日志", "相机模块", "相机模块通讯失败，已断开连接", "系统", "失败", "相机掉线，已尝试自动重连。"),
            ("警告", "系统日志", "系统管理", "磁盘使用率达到阈值：72%", "系统", "成功", "建议检查日志保留策略。"),
        ]
        for i in range(36):
            level, typ, mod, content, op, res, detail = demo[i % len(demo)]
            self._add_log(level, typ, mod, content, op, res, detail)

    @staticmethod
    def _now() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _equipment() -> list[dict[str, str]]:
        return [
            {"name": "供包皮带线", "icon": "↘", "speed": "1.20 m/s", "state": "运行中", "count": "110"},
            {"name": "分离辊", "icon": "⇆", "speed": "1.30 m/s", "state": "运行中", "count": ""},
            {"name": "居中机", "icon": "▤", "speed": "1.20 m/s", "state": "运行中", "count": ""},
            {"name": "剔除机", "icon": "▭", "speed": "1.20 m/s", "state": "运行中", "count": ""},
            {"name": "供包台", "icon": "◫", "speed": "", "state": "正常", "count": "65"},
            {"name": "人工线", "icon": "♙", "speed": "", "state": "正常", "count": "8"},
            {"name": "循环线", "icon": "⟳", "speed": "", "state": "正常", "count": "12"},
        ]

    @staticmethod
    def _params() -> list[dict[str, str]]:
        return [
            {"group": "分离机与准入配置", "key": "modRows", "name": "排数(modRows)", "value": "4", "unit": ""},
            {"group": "分离机与准入配置", "key": "modCols", "name": "列数(modCols)", "value": "4", "unit": ""},
            {"group": "分离机与准入配置", "key": "modL", "name": "模组长度", "value": "300.0", "unit": "mm"},
            {"group": "分离机与准入配置", "key": "modW", "name": "模组宽度", "value": "135.0", "unit": "mm"},
            {"group": "分离机与准入配置", "key": "defaultSpeed", "name": "默认速度", "value": "1.00", "unit": "m/s"},
            {"group": "速度与阈值配置", "key": "highestSpeed", "name": "最高速度", "value": "2.00", "unit": "m/s"},
            {"group": "速度与阈值配置", "key": "lowestSpeed", "name": "最低速度", "value": "0.00", "unit": "m/s"},
            {"group": "速度与阈值配置", "key": "entrySpeed", "name": "入口包裹阈值", "value": "0.60", "unit": ""},
            {"group": "算法与相机参数", "key": "minBeltNum", "name": "算法层数", "value": "4", "unit": ""},
            {"group": "算法与相机参数", "key": "cameraIp", "name": "单件分离相机IP", "value": "192.168.2.15", "unit": ""},
            {"group": "显示与保存配置", "key": "imgInterval", "name": "剔除间隔", "value": "5", "unit": "秒"},
            {"group": "显示与保存配置", "key": "imgPath", "name": "图片路径", "value": "data", "unit": ""},
        ]

    @staticmethod
    def _settings() -> list[dict[str, str]]:
        return [
            {"group": "客户端设置", "key": "startup", "name": "开机启动", "value": "开启", "unit": ""},
            {"group": "客户端设置", "key": "scale", "name": "窗口缩放", "value": "100%", "unit": ""},
            {"group": "通讯与服务", "key": "plcIp", "name": "PLC IP", "value": "192.168.2.15", "unit": ""},
            {"group": "通讯与服务", "key": "plcPort", "name": "PLC端口", "value": "502", "unit": ""},
            {"group": "通讯与服务", "key": "hmiPort", "name": "HMI服务端口", "value": "5000", "unit": ""},
            {"group": "数据与存储", "key": "logDays", "name": "日志保留天数", "value": "30", "unit": "天"},
            {"group": "数据与存储", "key": "imagePath", "name": "图片保存路径", "value": "data/", "unit": ""},
            {"group": "用户与权限", "key": "user", "name": "当前用户", "value": "admin", "unit": ""},
            {"group": "用户与权限", "key": "role", "name": "角色", "value": "管理员", "unit": ""},
            {"group": "界面与显示", "key": "language", "name": "语言", "value": "简体中文", "unit": ""},
            {"group": "界面与显示", "key": "unit", "name": "单位", "value": "m/s", "unit": ""},
        ]

    @staticmethod
    def _make_trend() -> list[dict[str, int | str]]:
        return [{"label": f"{11 + i // 6:02d}:{(i % 6) * 10:02d}", "main": 1120 + i * 18 + random.randint(-40, 40), "supply": 620 + i * 10 + random.randint(-25, 25), "manual": 180 + i * 12, "cycle": 80 + i * 5} for i in range(13)]


def main() -> int:
    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
    app = QGuiApplication(sys.argv)
    root = Path(__file__).resolve().parents[2]
    backend = Backend(root)
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("backend", backend)
    engine.load(QUrl.fromLocalFile(str(root / "qml" / "Main.qml")))
    if not engine.rootObjects():
        return 1
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
