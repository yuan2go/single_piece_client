import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property int currentIndex: 0
    signal selected(int index)

    color: "#07101A"
    border.color: "#173149"
    border.width: 1

    ColumnLayout {
        anchors.fill: parent
        anchors.topMargin: 18
        anchors.bottomMargin: 18
        spacing: 8

        Repeater {
            model: [
                {"label": "实时监控", "badge": ""},
                {"label": "报警中心", "badge": "2"},
                {"label": "设备诊断", "badge": ""},
                {"label": "参数配置", "badge": ""},
                {"label": "日志记录", "badge": ""},
                {"label": "系统设置", "badge": ""}
            ]

            delegate: Rectangle {
                Layout.fillWidth: true
                Layout.leftMargin: 10
                Layout.rightMargin: 10
                height: 48
                radius: 8
                property bool active: index === root.currentIndex
                color: active ? "#173454" : "transparent"
                border.color: active ? "#2F80ED" : "transparent"
                border.width: 1

                Text {
                    anchors.centerIn: parent
                    text: modelData.label
                    color: parent.active ? "#E5EDF5" : "#9BA8B8"
                    font.pixelSize: 14
                    font.weight: parent.active ? Font.DemiBold : Font.Normal
                }

                Rectangle {
                    visible: modelData.badge !== ""
                    width: 20
                    height: 20
                    radius: 10
                    color: "#EB5757"
                    anchors.right: parent.right
                    anchors.rightMargin: 5
                    anchors.top: parent.top
                    anchors.topMargin: 5
                    Text {
                        anchors.centerIn: parent
                        text: modelData.badge
                        color: "#FFFFFF"
                        font.pixelSize: 11
                        font.weight: Font.Bold
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.selected(index)
                }
            }
        }

        Item { Layout.fillHeight: true }

        Text {
            Layout.alignment: Qt.AlignHCenter
            text: "v0.1 QML"
            color: "#516070"
            font.pixelSize: 11
        }
    }
}
