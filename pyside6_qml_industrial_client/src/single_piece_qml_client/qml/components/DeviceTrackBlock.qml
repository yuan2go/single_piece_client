import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property var device: ({})
    property bool compact: false

    radius: 8
    color: "#101D2B"
    border.color: "#2A4056"
    border.width: 1
    height: compact ? 54 : 66

    RowLayout {
        anchors.fill: parent
        anchors.margins: compact ? 9 : 12
        spacing: 12

        Rectangle {
            Layout.preferredWidth: 6
            Layout.fillHeight: true
            radius: 3
            color: device.status === "normal" ? "#21C36B" : device.status === "warning" ? "#F2C94C" : "#EB5757"
        }

        ColumnLayout {
            Layout.preferredWidth: compact ? 130 : 190
            spacing: 3
            Text {
                text: device.title || "设备段"
                color: "#E5EDF5"
                font.pixelSize: compact ? 13 : 15
                font.weight: Font.DemiBold
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
            Text {
                text: "状态：" + (device.statusText || "--")
                color: "#9BA8B8"
                font.pixelSize: 12
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: compact ? 22 : 26
            radius: 4
            color: "#0B1623"
            border.color: "#26384A"
            border.width: 1

            Rectangle {
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                anchors.leftMargin: 8
                width: parent.width * 0.56
                height: 4
                radius: 2
                color: "#2F80ED"
                opacity: 0.72
            }
        }

        ColumnLayout {
            Layout.preferredWidth: compact ? 92 : 118
            spacing: 2
            Text {
                text: "速度：" + (device.speed || "--") + " " + (device.unit || "")
                color: "#E5EDF5"
                font.pixelSize: 12
                font.family: "monospace"
                horizontalAlignment: Text.AlignRight
                Layout.fillWidth: true
            }
            Text {
                text: "包裹：" + (device.packageCount || "--")
                color: "#C8D3DF"
                font.pixelSize: 12
                horizontalAlignment: Text.AlignRight
                Layout.fillWidth: true
            }
        }

        StatusDot {
            state: device.status === "normal" ? "normal" : device.status === "warning" ? "warning" : "fault"
        }
    }
}
