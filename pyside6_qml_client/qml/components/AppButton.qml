import QtQuick
import QtQuick.Controls

Button {
    id: root
    property string variant: "normal"

    function bgColor() {
        if (variant === "success") return "#238d22"
        if (variant === "danger") return "#ba2525"
        if (variant === "primary") return "#156edb"
        return "#1d2b38"
    }

    background: Rectangle {
        radius: 5
        color: root.down ? Qt.darker(root.bgColor(), 1.25) : root.bgColor()
        border.color: Qt.lighter(root.bgColor(), 1.25)
    }

    contentItem: Text {
        text: root.text
        color: "#f0f6ff"
        font.pixelSize: 14
        font.bold: root.variant !== "normal"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}
