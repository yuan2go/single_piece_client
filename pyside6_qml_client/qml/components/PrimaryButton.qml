import QtQuick
import QtQuick.Controls
import "../styles"

Button {
    id: root
    property string variant: "normal"

    function bg() {
        if (variant === "success") return "#238d22"
        if (variant === "danger") return "#ba2525"
        if (variant === "primary") return "#156edb"
        return "#1d2b38"
    }

    background: Rectangle {
        radius: 5
        color: root.down ? Qt.darker(root.bg(), 1.25) : root.bg()
        border.color: Qt.lighter(root.bg(), 1.25)
    }

    contentItem: Text {
        text: root.text
        color: "#f0f6ff"
        font.pixelSize: Theme.fontBody
        font.bold: root.variant !== "normal"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}
