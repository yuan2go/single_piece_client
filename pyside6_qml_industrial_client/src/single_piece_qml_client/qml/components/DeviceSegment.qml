import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property string title: "设备段"
    property string subtitle: ""
    property string statusText: "正常"
    property string statusState: "normal"
    property bool large: false

    radius: 10
    color: "#101D2B"
    border.color: "#26384A"
    border.width: 1
    height: large ? 82 : 58

    RowLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        Rectangle {
            Layout.preferredWidth: 7
            Layout.fillHeight: true
            radius: 4
            color: statusState === "normal" ? "#21C36B" : statusState === "warning" ? "#F2C94C" : statusState === "offline" ? "#8A94A6" : "#EB5757"
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 4
            Text {
                text: root.title
                color: "#E5EDF5"
                font.pixelSize: root.large ? 16 : 14
                font.weight: Font.DemiBold
            }
            Text {
                text: root.subtitle
                color: "#9BA8B8"
                font.pixelSize: 12
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
        }

        RowLayout {
            spacing: 7
            StatusDot { state: root.statusState }
            Text {
                text: root.statusText
                color: "#C8D3DF"
                font.pixelSize: 13
            }
        }
    }
}
