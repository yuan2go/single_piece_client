import QtQuick
import QtQuick.Layouts
import "../styles"

RowLayout {
    id: root
    property string label: ""
    property string value: ""
    property bool ok: true
    property bool blue: false
    spacing: 6

    Text {
        text: root.label + "："
        color: Theme.textMuted
        font.pixelSize: Theme.fontBody
    }

    Rectangle {
        height: 24
        width: valueText.width + 18
        radius: 4
        color: root.blue ? Theme.accentSoft : (root.ok ? Theme.successSoft : Theme.dangerSoft)
        border.color: root.blue ? Theme.accent : (root.ok ? "#217a3b" : Theme.danger)

        Text {
            id: valueText
            anchors.centerIn: parent
            text: root.value
            color: root.blue ? "#9dccff" : (root.ok ? Theme.success : Theme.danger)
            font.pixelSize: 13
            font.bold: true
        }
    }
}
