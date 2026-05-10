import QtQuick
import QtQuick.Layouts
import "../styles"

RowLayout {
    id: root
    property string label: ""
    property string value: ""
    property bool highlight: false

    Text {
        text: root.label
        color: Theme.textMuted
        font.pixelSize: Theme.fontBody
        Layout.fillWidth: true
        elide: Text.ElideRight
    }

    Text {
        text: root.value
        color: root.highlight ? Theme.success : Theme.textSecondary
        font.pixelSize: Theme.fontBody
        font.bold: root.highlight
        horizontalAlignment: Text.AlignRight
        Layout.maximumWidth: 190
        elide: Text.ElideRight
    }
}
