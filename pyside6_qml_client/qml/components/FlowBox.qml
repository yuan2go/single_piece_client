import QtQuick
import QtQuick.Layouts
import "../styles"

Rectangle {
    id: root
    property string name: ""
    property string icon: "▭"
    property string line1: ""
    property string line2: ""
    property bool ok: true

    radius: 6
    color: "#162633"
    border.color: "#2a4052"

    RowLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        Text {
            text: root.icon
            color: "#aebac6"
            font.pixelSize: 31
            Layout.preferredWidth: 42
            horizontalAlignment: Text.AlignHCenter
        }

        ColumnLayout {
            spacing: 4
            Layout.fillWidth: true

            Text { text: root.name; color: Theme.textPrimary; font.pixelSize: 16; font.bold: true }
            Text { text: root.line1; color: Theme.textSecondary; font.pixelSize: 13 }
            Text { text: root.line2; color: Theme.textSecondary; font.pixelSize: 13 }
        }

        Rectangle {
            width: 10
            height: 10
            radius: 5
            color: root.ok ? Theme.success : Theme.danger
        }
    }
}
