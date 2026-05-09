import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property var runtimeData: ({})
    property var kpis: []
    property var alarms: []

    color: "#0B1623"
    border.color: "#173149"
    border.width: 1

    ConfirmDialog {
        id: stopConfirmDialog
        title: "确认停止当前设备？"
        message: "停止后将中断当前供包流程，可能影响正在处理的包裹。\n\n请确认现场人员已经沟通完成，且当前停止操作符合生产流程。"
        confirmText: "确认停止"
        tone: "danger"
        onConfirmed: backend.requestStop()
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 292
            radius: 10
            color: "#101D2B"
            border.color: "#26384A"
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 10

                Text {
                    text: "运行数据"
                    color: "#E5EDF5"
                    font.pixelSize: 16
                    font.weight: Font.DemiBold
                }

                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    columnSpacing: 8
                    rowSpacing: 8

                    Repeater {
                        model: root.kpis
                        delegate: KpiCard {
                            Layout.fillWidth: true
                            Layout.preferredHeight: modelData.primary ? 84 : 52
                            label: modelData.label
                            value: modelData.value
                            unit: modelData.unit
                            primary: modelData.primary
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 196
            radius: 10
            color: "#101D2B"
            border.color: "#26384A"
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 10

                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "操作控制"
                        color: "#E5EDF5"
                        font.pixelSize: 16
                        font.weight: Font.DemiBold
                    }
                    Item { Layout.fillWidth: true }
                    StatusBadge {
                        text: root.runtimeData.state || "--"
                        tone: root.runtimeData.state === "运行中" ? "success" : root.runtimeData.state === "故障" ? "critical" : root.runtimeData.state === "待机" ? "info" : "offline"
                    }
                }

                Text {
                    text: "启动条件：" + (root.runtimeData.startCondition || "--")
                    color: root.runtimeData.canStart ? "#21C36B" : "#EB5757"
                    font.pixelSize: 13
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }

                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    columnSpacing: 8
                    rowSpacing: 8

                    IndustrialButton {
                        Layout.fillWidth: true
                        text: root.runtimeData.state === "启动中" ? "启动中..." : "启动"
                        available: root.runtimeData.canStart === true
                        onClicked: backend.requestStart()
                    }
                    IndustrialButton {
                        Layout.fillWidth: true
                        text: root.runtimeData.state === "停止中" ? "停止中..." : "停止"
                        tone: "danger"
                        available: root.runtimeData.canStop === true
                        onClicked: stopConfirmDialog.open()
                    }
                    IndustrialButton {
                        Layout.fillWidth: true
                        text: "复位报警"
                        tone: "neutral"
                        available: root.runtimeData.canResetAlarm === true
                        onClicked: backend.resetAlarms()
                    }
                    IndustrialButton {
                        Layout.fillWidth: true
                        text: "重新连接"
                        tone: "primary"
                        available: root.runtimeData.canReconnect === true
                        onClicked: backend.reconnect()
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 10
            color: "#101D2B"
            border.color: "#26384A"
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 10

                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "当前报警"
                        color: "#E5EDF5"
                        font.pixelSize: 16
                        font.weight: Font.DemiBold
                    }
                    StatusBadge { text: String(root.runtimeData.alarmCount || root.alarms.length); tone: (root.runtimeData.alarmCount || root.alarms.length) > 0 ? "critical" : "success" }
                    Item { Layout.fillWidth: true }
                }

                Repeater {
                    model: root.alarms
                    delegate: Rectangle {
                        visible: modelData.recovered !== true
                        Layout.fillWidth: true
                        Layout.preferredHeight: modelData.level === "严重" ? 118 : 88
                        radius: 8
                        color: modelData.level === "严重" ? "#211922" : "#221F14"
                        border.color: modelData.level === "严重" ? "#EB5757" : "#F2C94C"
                        border.width: 1

                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 10

                            Rectangle {
                                Layout.preferredWidth: 5
                                Layout.fillHeight: true
                                radius: 3
                                color: modelData.level === "严重" ? "#EB5757" : "#F2C94C"
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 5

                                RowLayout {
                                    StatusBadge { text: modelData.level; tone: modelData.level === "严重" ? "critical" : "warning" }
                                    Text {
                                        text: modelData.title
                                        color: "#E5EDF5"
                                        font.pixelSize: 14
                                        font.weight: Font.DemiBold
                                        Layout.fillWidth: true
                                        elide: Text.ElideRight
                                    }
                                }
                                Text { text: "对象：" + modelData.target; color: "#C8D3DF"; font.pixelSize: 12 }
                                Text { text: "已持续：" + modelData.duration; color: "#9BA8B8"; font.pixelSize: 12 }
                                Text {
                                    visible: modelData.suggestion !== ""
                                    text: "建议：" + modelData.suggestion
                                    color: "#9BA8B8"
                                    font.pixelSize: 12
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    visible: (root.runtimeData.alarmCount || 0) === 0
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    radius: 8
                    color: "#0E1A29"
                    border.color: "#26384A"
                    Text {
                        anchors.centerIn: parent
                        text: "当前无未恢复报警"
                        color: "#21C36B"
                        font.pixelSize: 14
                        font.weight: Font.Medium
                    }
                }
            }
        }
    }
}
