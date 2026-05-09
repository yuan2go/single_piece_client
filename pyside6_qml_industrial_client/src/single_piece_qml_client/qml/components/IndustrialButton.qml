import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    property string text: "按钮"
    property string tone: "primary"
    property bool available: true
    signal clicked()

    height: 40
    radius: 6
    opacity: available ? 1.0 : 0.45
    color: {
        if (!available) return "#2A3442"
        if (tone === "danger") return "#8F2D3A"
        if (tone === "neutral") return "#26384A"
        return "#2F80ED"
    }
    border.color: available ? "#4E9AF5" : "#3A4654"
    border.width: 1

    Text {
        anchors.centerIn: parent
        text: root.text
        color: "#E5EDF5"
        font.pixelSize: 15
        font.weight: Font.Medium
    }

    MouseArea {
        anchors.fill: parent
        enabled: root.available
        cursorShape: Qt.PointingHandCursor
        onClicked: root.clicked()
    }
}
