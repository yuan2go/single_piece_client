import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    property string text: ""
    property string tone: "info"
    height: 26
    radius: 5
    color: {
        if (tone === "critical") return "#4A1E26"
        if (tone === "warning") return "#4A3A12"
        if (tone === "success") return "#173A2B"
        if (tone === "offline") return "#26313F"
        return "#173454"
    }
    border.color: {
        if (tone === "critical") return "#EB5757"
        if (tone === "warning") return "#F2C94C"
        if (tone === "success") return "#21C36B"
        return "#2F80ED"
    }
    border.width: 1

    implicitWidth: label.implicitWidth + 18

    Text {
        id: label
        anchors.centerIn: parent
        text: root.text
        color: "#E5EDF5"
        font.pixelSize: 13
        font.weight: Font.Medium
    }
}
