import QtQuick
import QtQuick.Layouts
import "../styles"

Rectangle {
    id: root
    property string title: ""
    default property alias content: body.data

    radius: Theme.radiusPanel
    color: Theme.panelBg
    border.color: Theme.border
    border.width: 1

    Column {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12

        Text {
            visible: root.title.length > 0
            text: root.title
            color: Theme.textPrimary
            font.pixelSize: Theme.fontTitle
            font.bold: true
        }

        Rectangle {
            visible: root.title.length > 0
            width: parent.width
            height: 1
            color: Theme.border
        }

        Item {
            id: body
            width: parent.width
            height: parent.height - y
        }
    }
}
