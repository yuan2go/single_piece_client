import QtQuick
import QtQuick.Layouts

import "../components"

Rectangle {
    id: root
    property var alarms: []

    color: "#0B1623"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        RowLayout {
            Layout.fillWidth: true
            Text {
                text: "报警中心"
                color: "#E5EDF5"
                font.pixelSize: 20
                font.weight: Font.DemiBold
            }
            Text {
                text: "当前报警、历史报警、报警详情与处理建议"
                color: "#9BA8B8"
                font.pixelSize: 13
            }
            Item { Layout.fillWidth: true }
            StatusBadge { text: "严重 1"; tone: "critical" }
            StatusBadge { text: "警告 1"; tone: "warning" }
            StatusBadge { text: "未确认 2"; tone: "info" }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 12

            SectionCard {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: "当前报警"
                subtitle: "按等级、对象、持续时间和处理状态排序。"

                RowLayout {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 28
                    Text { Layout.preferredWidth: 80; text: "等级"; color: "#708092"; font.pixelSize: 12 }
                    Text { Layout.preferredWidth: 120; text: "对象"; color: "#708092"; font.pixelSize: 12 }
                    Text { Layout.fillWidth: true; text: "内容"; color: "#708092"; font.pixelSize: 12 }
                    Text { Layout.preferredWidth: 100; text: "持续时长"; color: "#708092"; font.pixelSize: 12 }
                    Text { Layout.preferredWidth: 90; text: "状态"; color: "#708092"; font.pixelSize: 12 }
                }

                Repeater {
                    model: root.alarms
                    delegate: Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 52
                        radius: 7
                        color: index % 2 === 0 ? "#0E1A29" : "#101D2B"
                        border.color: modelData.level === "严重" ? "#7A2A36" : "#665820"
                        border.width: 1

                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 8
                            spacing: 10
                            StatusBadge { Layout.preferredWidth: 64; text: modelData.level; tone: modelData.level === "严重" ? "critical" : "warning" }
                            Text { Layout.preferredWidth: 110; text: modelData.target; color: "#C8D3DF"; font.pixelSize: 13 }
                            Text { Layout.fillWidth: true; text: modelData.title; color: "#E5EDF5"; font.pixelSize: 13; font.weight: Font.DemiBold }
                            Text { Layout.preferredWidth: 100; text: modelData.duration; color: "#9BA8B8"; font.pixelSize: 12; font.family: "monospace" }
                            Text { Layout.preferredWidth: 90; text: "未恢复"; color: "#EB5757"; font.pixelSize: 12 }
                        }
                    }
                }
            }

            SectionCard {
                Layout.preferredWidth: 340
                Layout.fillHeight: true
                title: "报警详情"
                subtitle: "选中报警后展示原因、建议与关联操作。"

                StatusBadge { text: "严重"; tone: "critical" }
                Text { text: "Modbus 通信离线"; color: "#E5EDF5"; font.pixelSize: 18; font.weight: Font.DemiBold }
                Text { text: "对象：PLC / Modbus"; color: "#C8D3DF"; font.pixelSize: 13 }
                Text { text: "发生时间：2026-05-09 12:28:30"; color: "#9BA8B8"; font.pixelSize: 12 }
                Text { text: "持续时间：00:03:21"; color: "#9BA8B8"; font.pixelSize: 12 }

                Text {
                    Layout.fillWidth: true
                    text: "可能原因：PLC 未上电、网络断开、IP 或端口配置错误、Modbus 服务未开启。"
                    color: "#C8D3DF"
                    font.pixelSize: 13
                    wrapMode: Text.WordWrap
                }
                Text {
                    Layout.fillWidth: true
                    text: "处理建议：检查 PLC 电源，ping 192.168.2.15，检查端口 2100，查看通讯日志。"
                    color: "#C8D3DF"
                    font.pixelSize: 13
                    wrapMode: Text.WordWrap
                }

                RowLayout {
                    Layout.fillWidth: true
                    IndustrialButton { Layout.fillWidth: true; text: "重新连接" }
                    IndustrialButton { Layout.fillWidth: true; text: "确认报警"; tone: "neutral" }
                }
            }
        }
    }
}
