import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property var runtimeData: ({})
    property var beltCells: []
    property var packages: []

    radius: 12
    color: "#0D1826"
    border.color: "#26384A"
    border.width: 1

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 10

        RowLayout {
            Layout.fillWidth: true
            Text {
                text: "实时跟踪画面"
                color: "#E5EDF5"
                font.pixelSize: 18
                font.weight: Font.DemiBold
            }
            Text {
                text: "方向：↓    速度单位：m/s    显示：速度 / 包裹 / 传感器"
                color: "#9BA8B8"
                font.pixelSize: 13
            }
            Item { Layout.fillWidth: true }
            StatusBadge { text: "生产模式"; tone: "info" }
        }

        DeviceSegment {
            Layout.fillWidth: true
            title: "供包皮带线"
            subtitle: "速度：1.00 m/s    光电：在线    相机：在线"
            statusText: "正常"
            statusState: "normal"
        }

        FlowArrow { Layout.alignment: Qt.AlignHCenter }

        RowLayout {
            Layout.fillWidth: true
            spacing: 10
            DeviceSegment {
                Layout.fillWidth: true
                title: "滑槽"
                subtitle: "状态：正常    包裹汇入缓存区"
                statusText: "正常"
                statusState: "normal"
            }
            DeviceSegment {
                Layout.fillWidth: true
                title: "缓存1皮带线"
                subtitle: "速度：0.60 m/s    包裹：3"
                statusText: "在线"
                statusState: "normal"
            }
            DeviceSegment {
                Layout.fillWidth: true
                title: "缓存2皮带线"
                subtitle: "速度：0.80 m/s    包裹：2"
                statusText: "在线"
                statusState: "normal"
            }
        }

        FlowArrow { Layout.alignment: Qt.AlignHCenter }

        BeltMatrixView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: 340
            cells: root.beltCells
            packages: root.packages
        }

        FlowArrow { Layout.alignment: Qt.AlignHCenter }

        DeviceSegment {
            Layout.fillWidth: true
            large: true
            title: "居中机"
            subtitle: "速度：1.30 m/s    导向排正：正常    光电：在线"
            statusText: "正常"
            statusState: "normal"
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 10
            DeviceSegment {
                Layout.fillWidth: true
                title: "剔除机"
                subtitle: "状态：待机    剔除口：正常"
                statusText: "待机"
                statusState: "offline"
            }
            DeviceSegment {
                Layout.fillWidth: true
                title: "正常供包台"
                subtitle: "主路径    小时效率：3,200 件/小时"
                statusText: "正常"
                statusState: "normal"
            }
            DeviceSegment {
                Layout.fillWidth: true
                title: "人工线 / 循环线"
                subtitle: "人工线：320    循环线：280"
                statusText: "监控"
                statusState: "warning"
            }
        }
    }
}
