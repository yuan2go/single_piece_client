import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property string title: "标题"
    property string subtitle: ""

    radius: 10
    color: "#101D2B"
    border.color: "#26384A"
    border.width: 1

    default property alias content: body.data

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 10

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 3
            Text {
                text: root.title
                color: "#E5EDF5"
                font.pixelSize: 16
                font.weight: Font.DemiBold
            }
            Text {
                visible: root.subtitle !== ""
                text: root.subtitle
                color: "#9BA8B8"
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
            }
        }

        Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 1; color: "#26384A" }

        ColumnLayout {
            id: body
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 8
        }
    }
}
