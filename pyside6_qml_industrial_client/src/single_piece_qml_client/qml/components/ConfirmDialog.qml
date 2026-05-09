import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: root
    property string title: "确认操作"
    property string message: ""
    property string confirmText: "确认"
    property string cancelText: "取消"
    property string tone: "danger"
    signal confirmed()

    modal: true
    focus: true
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    width: 460
    height: 260

    background: Rectangle {
        radius: 12
        color: "#101D2B"
        border.color: root.tone === "danger" ? "#EB5757" : "#2F80ED"
        border.width: 1
    }

    contentItem: ColumnLayout {
        anchors.fill: parent
        anchors.margins: 18
        spacing: 14

        RowLayout {
            Layout.fillWidth: true
            Rectangle {
                Layout.preferredWidth: 5
                Layout.preferredHeight: 34
                radius: 3
                color: root.tone === "danger" ? "#EB5757" : "#2F80ED"
            }
            Text {
                Layout.fillWidth: true
                text: root.title
                color: "#E5EDF5"
                font.pixelSize: 19
                font.weight: Font.DemiBold
            }
        }

        Text {
            Layout.fillWidth: true
            Layout.fillHeight: true
            text: root.message
            color: "#C8D3DF"
            font.pixelSize: 14
            lineHeight: 1.25
            wrapMode: Text.WordWrap
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 1
            color: "#26384A"
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 10
            Item { Layout.fillWidth: true }
            IndustrialButton {
                Layout.preferredWidth: 112
                text: root.cancelText
                tone: "neutral"
                onClicked: root.close()
            }
            IndustrialButton {
                Layout.preferredWidth: 128
                text: root.confirmText
                tone: root.tone === "danger" ? "danger" : "primary"
                onClicked: {
                    root.confirmed()
                    root.close()
                }
            }
        }
    }
}
