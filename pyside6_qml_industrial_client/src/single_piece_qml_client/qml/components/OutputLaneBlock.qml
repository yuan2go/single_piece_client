import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property var device: ({})

    radius: 8
    color: "#101D2B"
    border.color: "#2A4056"
    border.width: 1
    height: 70

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 5

        RowLayout {
            Layout.fillWidth: true
            Text {
                text: device.title || "输出线"
                color: "#E5EDF5"
                font.pixelSize: 14
                font.weight: Font.DemiBold
            }
            Item { Layout.fillWidth: true }
            StatusDot { state: device.status === "normal" ? "normal" : "warning" }
        }

        RowLayout {
            Layout.fillWidth: true
            Text { text: "包裹"; color: "#9BA8B8"; font.pixelSize: 12 }
            Item { Layout.fillWidth: true }
            Text {
                text: String(device.packageCount || "0")
                color: "#E5EDF5"
                font.pixelSize: 20
                font.weight: Font.DemiBold
            }
        }

        Text {
            text: device.statusText || "--"
            color: "#9BA8B8"
            font.pixelSize: 12
        }
    }
}
