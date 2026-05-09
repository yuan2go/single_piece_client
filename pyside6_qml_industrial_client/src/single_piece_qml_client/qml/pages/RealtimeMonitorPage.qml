import QtQuick
import QtQuick.Layouts

import "../components"

Rectangle {
    id: root
    property var runtimeData: ({})
    property var beltCells: []
    property var packages: []

    color: "#0B1623"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            Text {
                text: "实时监控"
                color: "#E5EDF5"
                font.pixelSize: 20
                font.weight: Font.DemiBold
            }

            Text {
                text: "以分离皮带速度矩阵、包裹跨皮带位置、设备状态和报警为中心"
                color: "#9BA8B8"
                font.pixelSize: 13
            }

            Item { Layout.fillWidth: true }

            StatusBadge { text: "桌面客户端"; tone: "info" }
            StatusBadge { text: "离线调试视图"; tone: "offline" }
        }

        DeviceFlowView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            runtimeData: root.runtimeData
            beltCells: root.beltCells
            packages: root.packages
        }
    }
}
