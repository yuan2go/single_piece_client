import QtQuick
import QtQuick.Layouts

import "../components"

Rectangle {
    id: root
    color: "#0B1623"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        RowLayout {
            Layout.fillWidth: true
            Text { text: "系统设置"; color: "#E5EDF5"; font.pixelSize: 20; font.weight: Font.DemiBold }
            Text { text: "基础信息、界面方向、权限、启动策略与数据存储。"; color: "#9BA8B8"; font.pixelSize: 13 }
            Item { Layout.fillWidth: true }
            StatusBadge { text: "操作员"; tone: "offline" }
            StatusBadge { text: "部分设置只读"; tone: "warning" }
        }

        GridLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            columns: 2
            columnSpacing: 12
            rowSpacing: 12

            SectionCard {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: "基础信息"
                subtitle: "用于顶部状态栏、运行日志和现场交付识别。"

                DeviceSegment { Layout.fillWidth: true; title: "系统名称"; subtitle: "单件分离控制系统"; statusText: "已配置"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "场地名称"; subtitle: "自动供件"; statusText: "已配置"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "设备名称"; subtitle: "单件分离一号线"; statusText: "已配置"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "客户端版本"; subtitle: "A1.0.0"; statusText: "只读"; statusState: "offline" }
            }

            SectionCard {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: "界面设置"
                subtitle: "实时监控方向与现场显示选项。"

                DeviceSegment { Layout.fillWidth: true; title: "实时监控方向"; subtitle: "横向监控 / 纵向监控，当前：横向监控"; statusText: "可配置"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "显示模组速度"; subtitle: "默认开启。分离矩阵速度是生产监控核心信息。"; statusText: "开启"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "显示包裹图形"; subtitle: "显示包裹跨皮带覆盖层。"; statusText: "开启"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "刷新频率"; subtitle: "实时状态：500 ms；统计数据：1000 ms；日志：1000 ms"; statusText: "正常"; statusState: "normal" }
            }

            SectionCard {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: "权限设置"
                subtitle: "操作员、实施工程师、售后维护、管理员。"

                DeviceSegment { Layout.fillWidth: true; title: "操作员"; subtitle: "查看实时监控、启动、停止、确认报警。"; statusText: "启用"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "实施工程师"; subtitle: "查看诊断、修改普通参数、重连设备。"; statusText: "启用"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "售后维护"; subtitle: "修改通讯、相机、算法、高级参数。"; statusText: "启用"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "管理员"; subtitle: "用户权限、系统设置、导入导出配置。"; statusText: "受限"; statusState: "warning" }
            }

            SectionCard {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: "启动策略与数据存储"
                subtitle: "开机启动、默认算法、存图和统计数据保存。"

                DeviceSegment { Layout.fillWidth: true; title: "默认启动算法"; subtitle: "模式一"; statusText: "已配置"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "开机自启动"; subtitle: "当前关闭，避免现场误启动。"; statusText: "关闭"; statusState: "offline" }
                DeviceSegment { Layout.fillWidth: true; title: "图片保存"; subtitle: "路径：data；间隔：5 秒"; statusText: "关闭"; statusState: "offline" }
                DeviceSegment { Layout.fillWidth: true; title: "统计数据保存"; subtitle: "用于生产统计、售后追溯和效率分析。"; statusText: "关闭"; statusState: "offline" }
            }
        }
    }
}
