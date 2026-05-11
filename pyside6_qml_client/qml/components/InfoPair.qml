import QtQuick
import QtQuick.Layouts
import "../styles"

RowLayout {
    property string k: ""
    property string v: ""
    property color valueColor: Theme.textSecondary

    Text {
        text: k
        color: Theme.textMuted
        font.pixelSize: Theme.fontBody
        Layout.fillWidth: true
    }

    Text {
        text: v
        color: valueColor
        font.pixelSize: Theme.fontBody
        elide: Text.ElideRight
        Layout.maximumWidth: 210
    }
}
