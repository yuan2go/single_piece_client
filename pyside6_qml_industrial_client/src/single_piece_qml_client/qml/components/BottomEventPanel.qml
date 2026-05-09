import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property var events: []

    color: "#08111D"
    border.color: "#26384A"
    border.width: 1

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 8

        RowLayout {
            Layout.fillWidth: true
            spacing: 6
            Repeater {
                model: ["当前报警", "操作日志", "通讯日志", "系统日志", "包裹事件"]
                delegate: Rectangle {
                    width: 92
                    height: 30
                    radius: 6
                    color: index === 0 ? "#173454" : "#101D2B"
                    border.color: index === 0 ? "#2F80ED" : "#26384A"
                    border.width: 1
                    Text {
                        anchors.centerIn: parent
                        text: modelData
                        color: index === 0 ? "#E5EDF5" : "#9BA8B8"
                        font.pixelSize: 12
                    }
                }
            }
            Item { Layout.fillWidth: true }
            Text {
                text: "最近事件"
                color: "#9BA8B8"
                font.pixelSize: 12
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 8
            color: "#0B1623"
            border.color: "#26384A"
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 8
                spacing: 2

                RowLayout {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 24
                    Text { Layout.preferredWidth: 90; text: "时间"; color: "#708092"; font.pixelSize: 12 }
                    Text { Layout.preferredWidth: 70; text: "等级"; color: "#708092"; font.pixelSize: 12 }
                    Text { Layout.preferredWidth: 110; text: "对象"; color: "#708092"; font.pixelSize: 12 }
                    Text { Layout.fillWidth: true; text: "内容"; color: "#708092"; font.pixelSize: 12 }
                }

                Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 1; color: "#26384A" }

                Repeater {
                    model: root.events
                    delegate: Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 25
                        radius: 4
                        color: index % 2 === 0 ? "#0E1A29" : "transparent"

                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: 6
                            anchors.rightMargin: 6
                            spacing: 0

                            Text { Layout.preferredWidth: 90; text: modelData.time; color: "#C8D3DF"; font.pixelSize: 12; font.family: "monospace" }
                            Text {
                                Layout.preferredWidth: 70
                                text: modelData.level
                                color: modelData.level === "严重" ? "#EB5757" : modelData.level === "警告" ? "#F2C94C" : modelData.level === "操作" ? "#2F80ED" : "#9BA8B8"
                                font.pixelSize: 12
                                font.weight: Font.DemiBold
                            }
                            Text { Layout.preferredWidth: 110; text: modelData.source; color: "#9BA8B8"; font.pixelSize: 12 }
                            Text { Layout.fillWidth: true; text: modelData.message; color: "#E5EDF5"; font.pixelSize: 12; elide: Text.ElideRight }
                        }
                    }
                }
            }
        }
    }
}
