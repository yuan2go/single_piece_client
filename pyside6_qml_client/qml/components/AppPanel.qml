import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    property string title: ""
    default property alias content: body.data

    radius: 8
    color: "#14202b"
    border.color: "#263847"
    border.width: 1

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 14
        spacing: 10

        Text {
            visible: root.title.length > 0
            text: root.title
            color: "#eef5ff"
            font.pixelSize: 18
            font.bold: true
            Layout.fillWidth: true
        }

        Rectangle {
            visible: root.title.length > 0
            Layout.fillWidth: true
            height: 1
            color: "#263847"
        }

        Item {
            id: body
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
}
