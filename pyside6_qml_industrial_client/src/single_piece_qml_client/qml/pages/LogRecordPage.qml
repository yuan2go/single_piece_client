import QtQuick
import QtQuick.Layouts

import "../components"

Rectangle {
    id: root
    property var events: []

    color: "#0B1623"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        RowLayout {
            Layout.fillWidth: true
            Text { text: "日志记录"; color: "#E5EDF5"; font.pixelSize: 20; font.weight: Font.DemiBold }
            Text { text: "操作日志、报警日志、通讯日志、系统日志、包裹事件日志"; color: "#9BA8B8"; font.pixelSize: 13 }
            Item { Layout.fillWidth: true }
            StatusBadge { text: "今天"; tone: "info" }
            StatusBadge { text: "5 条"; tone: "offline" }
        }

        SectionCard {
            Layout.fillWidth: true
            Layout.preferredHeight: 76
            title: "筛选条件"
            subtitle: "用于售后排障和现场追溯。"

            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                StatusBadge { text: "类型：全部"; tone: "info" }
                StatusBadge { text: "等级：全部"; tone: "info" }
                StatusBadge { text: "时间：今天"; tone: "info" }
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 34
                    radius: 6
                    color: "#0E1A29"
                    border.color: "#26384A"
                    border.width: 1
                    Text {
                        anchors.left: parent.left
                        anchors.leftMargin: 12
                        anchors.verticalCenter: parent.verticalCenter
                        text: "关键词：PLC / 相机 / 包裹 ID / 参数名"
                        color: "#708092"
                        font.pixelSize: 13
                    }
                }
                IndustrialButton { Layout.preferredWidth: 90; text: "查询" }
            }
        }

        SectionCard {
            Layout.fillWidth: true
            Layout.fillHeight: true
            title: "日志列表"
            subtitle: "当前使用 mock 数据，后续可对接本地 rotating log、SQLite 或后端日志服务。"

            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: 30
                Text { Layout.preferredWidth: 100; text: "时间"; color: "#708092"; font.pixelSize: 12 }
                Text { Layout.preferredWidth: 80; text: "类型"; color: "#708092"; font.pixelSize: 12 }
                Text { Layout.preferredWidth: 110; text: "对象"; color: "#708092"; font.pixelSize: 12 }
                Text { Layout.fillWidth: true; text: "内容"; color: "#708092"; font.pixelSize: 12 }
                Text { Layout.preferredWidth: 100; text: "用户"; color: "#708092"; font.pixelSize: 12 }
                Text { Layout.preferredWidth: 90; text: "结果"; color: "#708092"; font.pixelSize: 12 }
            }

            Repeater {
                model: root.events
                delegate: Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 42
                    radius: 6
                    color: index % 2 === 0 ? "#0E1A29" : "#101D2B"
                    border.color: "#1E3144"
                    border.width: 1

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 10
                        anchors.rightMargin: 10
                        spacing: 0
                        Text { Layout.preferredWidth: 100; text: modelData.time; color: "#C8D3DF"; font.family: "monospace"; font.pixelSize: 13 }
                        Text {
                            Layout.preferredWidth: 80
                            text: modelData.level
                            color: modelData.level === "严重" ? "#EB5757" : modelData.level === "警告" ? "#F2C94C" : modelData.level === "操作" ? "#2F80ED" : "#9BA8B8"
                            font.pixelSize: 13
                            font.weight: Font.DemiBold
                        }
                        Text { Layout.preferredWidth: 110; text: modelData.source; color: "#9BA8B8"; font.pixelSize: 13 }
                        Text { Layout.fillWidth: true; text: modelData.message; color: "#E5EDF5"; font.pixelSize: 13; elide: Text.ElideRight }
                        Text { Layout.preferredWidth: 100; text: modelData.level === "操作" ? "operator" : "system"; color: "#9BA8B8"; font.pixelSize: 13 }
                        Text { Layout.preferredWidth: 90; text: modelData.level === "严重" ? "未恢复" : "已记录"; color: modelData.level === "严重" ? "#EB5757" : "#21C36B"; font.pixelSize: 13 }
                    }
                }
            }
        }
    }
}
