import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property var runtimeData: ({})

    color: "#08111D"
    border.color: "#26384A"
    border.width: 1

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 18
        anchors.rightMargin: 18
        spacing: 14

        Text {
            text: runtimeData.systemName || "单件分离控制系统"
            color: "#E5EDF5"
            font.pixelSize: 18
            font.weight: Font.DemiBold
            Layout.preferredWidth: 180
        }

        Text {
            text: "场地：" + (runtimeData.siteName || "--")
            color: "#C8D3DF"
            font.pixelSize: 14
        }

        StatusBadge { text: "状态：" + (runtimeData.state || "--"); tone: "offline" }
        StatusBadge { text: "模式：" + (runtimeData.mode || "--"); tone: "info" }

        RowLayout { spacing: 6; StatusDot { state: "offline" }; Text { text: "PLC：" + (runtimeData.plcState || "--"); color: "#E5EDF5"; font.pixelSize: 14 } }
        RowLayout { spacing: 6; StatusDot { state: "partial" }; Text { text: "相机：" + (runtimeData.cameraState || "--"); color: "#E5EDF5"; font.pixelSize: 14 } }
        RowLayout { spacing: 6; StatusDot { state: "normal" }; Text { text: "光电：" + (runtimeData.photoeyeState || "--"); color: "#E5EDF5"; font.pixelSize: 14 } }
        RowLayout { spacing: 6; StatusDot { state: "offline" }; Text { text: "电柜：" + (runtimeData.cabinetState || "--"); color: "#E5EDF5"; font.pixelSize: 14 } }

        StatusBadge { text: "报警：" + (runtimeData.alarmCount || 0); tone: "critical" }

        Item { Layout.fillWidth: true }

        Text {
            text: "用户：" + (runtimeData.user || "--")
            color: "#9BA8B8"
            font.pixelSize: 14
        }

        Text {
            text: runtimeData.time || "--"
            color: "#E5EDF5"
            font.pixelSize: 14
            font.family: "monospace"
        }
    }
}
