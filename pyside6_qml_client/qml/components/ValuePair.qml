import QtQuick
import QtQuick.Layouts
import "../styles"

RowLayout {
    id: root
    property string k: ""
    property string v: ""
    property bool strong: false

    Text {
        text: root.k
        color: Theme.textMuted
        font.pixelSize: Theme.fontBody
        Layout.fillWidth: true
        elide: Text.ElideRight
    }

    Text {
        text: root.v
        color: root.strong ? Theme.success : Theme.textSecondary
        font.pixelSize: Theme.fontBody
        font.bold: root.strong
        horizontalAlignment: Text.AlignRight
        elide: Text.ElideRight
        Layout.maximumWidth: 210
    }
}
