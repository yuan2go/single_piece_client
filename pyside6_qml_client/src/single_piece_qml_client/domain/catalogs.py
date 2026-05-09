from __future__ import annotations

import random
from typing import Any


def equipment_catalog() -> list[dict[str, str]]:
    return [
        {"name": "供包皮带线", "icon": "↘", "speed": "1.20 m/s", "state": "运行中", "count": "110"},
        {"name": "分离辊", "icon": "⇆", "speed": "1.30 m/s", "state": "运行中", "count": ""},
        {"name": "居中机", "icon": "▤", "speed": "1.20 m/s", "state": "运行中", "count": ""},
        {"name": "剔除机", "icon": "▭", "speed": "1.20 m/s", "state": "运行中", "count": ""},
        {"name": "供包台", "icon": "◫", "speed": "", "state": "正常", "count": "65"},
        {"name": "人工线", "icon": "♙", "speed": "", "state": "正常", "count": "8"},
        {"name": "循环线", "icon": "⟳", "speed": "", "state": "正常", "count": "12"},
    ]


def parameter_catalog() -> list[dict[str, str]]:
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


def setting_catalog() -> list[dict[str, str]]:
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


def initial_logs() -> list[tuple[str, str, str, str, str, str, str]]:
    return [
        ("信息", "通讯日志", "PLC通讯", "PLC重连成功，设备恢复通讯", "系统", "成功", "PLC连接已恢复。\nIP：192.168.2.15\n端口：5000\n响应时间：35ms"),
        ("信息", "操作日志", "系统管理", "参数保存成功：分离矩阵(4×4)", "admin", "成功", "配置写入成功。"),
        ("信息", "包裹事件", "分离矩阵", "包裹通过分离矩阵：3-2，重量：112g", "系统", "成功", "包裹横跨 3-2、3-3 两个皮带单元。"),
        ("警告", "通讯日志", "相机模块", "相机模块通讯超时，正在重试（1/3）", "系统", "重试中", "相机响应超过阈值。"),
        ("异常", "通讯日志", "相机模块", "相机模块通讯失败，已断开连接", "系统", "失败", "相机掉线，已尝试自动重连。"),
        ("警告", "系统日志", "系统管理", "磁盘使用率达到阈值：72%", "系统", "成功", "建议检查日志保留策略。"),
    ]


def initial_stats() -> dict[str, Any]:
    return {
        "total": 12458,
        "current": 85,
        "beat": 0.68,
        "uptime": "02:18:45",
        "throughput": 1024,
        "avgLen": 465,
        "supply": 65,
        "supplyEff": 625,
        "supplyRatio": 67.2,
        "manual": 8,
        "manualEff": 76,
        "manualRatio": 8.6,
        "cycle": 12,
        "cycleEff": 96,
        "cycleRatio": 12.2,
    }


def initial_trend() -> list[dict[str, int | str]]:
    return [
        {
            "label": f"{11 + i // 6:02d}:{(i % 6) * 10:02d}",
            "main": 1120 + i * 18 + random.randint(-40, 40),
            "supply": 620 + i * 10 + random.randint(-25, 25),
            "manual": 180 + i * 12,
            "cycle": 80 + i * 5,
        }
        for i in range(13)
    ]
