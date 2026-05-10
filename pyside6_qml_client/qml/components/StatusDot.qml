import QtQuick
import QtQuick.Layouts
import "../styles"

RowLayout {
    property string label: ""
    property string value: "正常"
    property color dotColor: Theme.success

    spacing: 7

    Text {
        text: label.length > 0 ? label + "：" : ""
        color: Theme.textMuted
        font.pixelSize: Theme.fontBody
    }

    Rectangle {
        width: 10
        height: 10
        radius: 5
        color: dotColor
    }

    Text {
        text: value
        color: dotColor
        font.pixelSize: 13
        font.bold: true
    }
}
