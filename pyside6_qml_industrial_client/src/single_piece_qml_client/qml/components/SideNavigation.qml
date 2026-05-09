import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
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
                {"label": "实时监控", "active": true, "badge": ""},
                {"label": "报警中心", "active": false, "badge": "2"},
                {"label": "设备诊断", "active": false, "badge": ""},
                {"label": "参数配置", "active": false, "badge": ""},
                {"label": "日志记录", "active": false, "badge": ""},
                {"label": "系统设置", "active": false, "badge": ""}
            ]

            delegate: Rectangle {
                Layout.fillWidth: true
                Layout.leftMargin: 10
                Layout.rightMargin: 10
                height: 48
                radius: 8
                color: modelData.active ? "#173454" : "transparent"
                border.color: modelData.active ? "#2F80ED" : "transparent"
                border.width: 1

                Text {
                    anchors.centerIn: parent
                    text: modelData.label
                    color: modelData.active ? "#E5EDF5" : "#9BA8B8"
                    font.pixelSize: 14
                    font.weight: modelData.active ? Font.DemiBold : Font.Normal
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
