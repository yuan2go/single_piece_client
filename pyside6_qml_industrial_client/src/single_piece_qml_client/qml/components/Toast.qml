import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property var toastData: ({})

    visible: toastData.visible === true
    opacity: visible ? 1 : 0
    width: Math.min(parent ? parent.width * 0.42 : 520, 560)
    height: 48
    radius: 8
    color: {
        if (toastData.level === "critical") return "#4A1E26"
        if (toastData.level === "warning") return "#4A3A12"
        if (toastData.level === "success") return "#173A2B"
        return "#173454"
    }
    border.color: {
        if (toastData.level === "critical") return "#EB5757"
        if (toastData.level === "warning") return "#F2C94C"
        if (toastData.level === "success") return "#21C36B"
        return "#2F80ED"
    }
    border.width: 1
    z: 999

    Behavior on opacity { NumberAnimation { duration: 160 } }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 10

        StatusDot {
            state: toastData.level === "critical" ? "critical" : toastData.level === "warning" ? "warning" : toastData.level === "success" ? "normal" : "partial"
        }

        Text {
            Layout.fillWidth: true
            text: toastData.message || ""
            color: "#E5EDF5"
            font.pixelSize: 14
            font.weight: Font.Medium
            elide: Text.ElideRight
        }
    }
}
