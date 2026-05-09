import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"

Rectangle {
    id: root
    property var runtimeData: ({})
    readonly property bool canSave: runtimeData.canSaveParameter === true

    color: "#0B1623"

    readonly property var categories: [
        "设备结构", "速度与节拍", "分离算法", "视觉与相机", "剔除规则", "通讯配置", "显示与存储", "高级维护"
    ]

    ConfirmDialog {
        id: saveConfirmDialog
        title: "确认保存参数？"
        message: "本次保存将写入当前配置。设备结构、通讯、算法和剔除规则属于生产高影响参数。\n\n请确认设备处于离线或待机状态，并已完成现场沟通。"
        confirmText: "保存配置"
        tone: "primary"
        onConfirmed: backend.saveParameters()
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        RowLayout {
            Layout.fillWidth: true
            Text { text: "参数配置"; color: "#E5EDF5"; font.pixelSize: 20; font.weight: Font.DemiBold }
            Text {
                text: root.canSave ? "当前允许保存；高风险参数仍需确认。" : "运行中只读；离线或待机状态才允许保存。"
                color: root.canSave ? "#21C36B" : "#EB5757"
                font.pixelSize: 13
            }
            Item { Layout.fillWidth: true }
            StatusBadge {
                text: "当前：" + (runtimeData.state || "--")
                tone: root.canSave ? "info" : "critical"
            }
            StatusBadge { text: "待保存 0"; tone: "info" }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 12

            Rectangle {
                Layout.preferredWidth: 170
                Layout.fillHeight: true
                radius: 10
                color: "#07101A"
                border.color: "#26384A"
                border.width: 1

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 10
                    spacing: 8

                    Text { text: "参数分类"; color: "#E5EDF5"; font.pixelSize: 15; font.weight: Font.DemiBold }

                    Repeater {
                        model: root.categories
                        delegate: Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 40
                            radius: 7
                            color: index === 0 ? "#173454" : "transparent"
                            border.color: index === 0 ? "#2F80ED" : "transparent"
                            border.width: 1
                            Text {
                                anchors.centerIn: parent
                                text: modelData
                                color: index === 0 ? "#E5EDF5" : "#9BA8B8"
                                font.pixelSize: 13
                            }
                        }
                    }

                    Item { Layout.fillHeight: true }
                }
            }

            SectionCard {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: "设备结构"
                subtitle: "将原分离机、除叠机、居中机等设备结构参数按业务语义组织。"

                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    columnSpacing: 12
                    rowSpacing: 10

                    Repeater {
                        model: [
                            {"name": "分离矩阵行数", "field": "modRows", "value": "4", "unit": "行", "risk": "中"},
                            {"name": "分离矩阵列数", "field": "modCols", "value": "4", "unit": "列", "risk": "中"},
                            {"name": "模组长度", "field": "modL", "value": "300.0", "unit": "mm", "risk": "中"},
                            {"name": "模组宽度", "field": "modW", "value": "135.0", "unit": "mm", "risk": "中"},
                            {"name": "皮带排列顺序", "field": "beltMode", "value": "0", "unit": "", "risk": "高"},
                            {"name": "除叠默认皮带数", "field": "stackBeltNum", "value": "2", "unit": "条", "risk": "中"},
                            {"name": "除叠全局包裹量", "field": "stackTop", "value": "2", "unit": "件", "risk": "中"},
                            {"name": "除叠出口包裹量", "field": "stackDown", "value": "1", "unit": "件", "risk": "中"}
                        ]
                        delegate: Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 86
                            radius: 8
                            color: "#0E1A29"
                            border.color: modelData.risk === "高" ? "#7A2A36" : "#26384A"
                            border.width: 1
                            opacity: root.canSave ? 1.0 : 0.72

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 10
                                spacing: 5
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: modelData.name; color: "#E5EDF5"; font.pixelSize: 14; font.weight: Font.DemiBold }
                                    Item { Layout.fillWidth: true }
                                    StatusBadge { text: "风险 " + modelData.risk; tone: modelData.risk === "高" ? "critical" : "info" }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "当前值"; color: "#9BA8B8"; font.pixelSize: 12 }
                                    Rectangle {
                                        Layout.preferredWidth: 110
                                        Layout.preferredHeight: 28
                                        radius: 5
                                        color: "#101D2B"
                                        border.color: "#26384A"
                                        Text { anchors.centerIn: parent; text: modelData.value + (modelData.unit === "" ? "" : " " + modelData.unit); color: "#E5EDF5"; font.pixelSize: 13 }
                                    }
                                    Text { text: "字段：" + modelData.field; color: "#708092"; font.pixelSize: 12 }
                                }
                            }
                        }
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    Item { Layout.fillWidth: true }
                    IndustrialButton { Layout.preferredWidth: 140; text: "从服务器重新加载"; tone: "neutral"; available: root.canSave }
                    IndustrialButton { Layout.preferredWidth: 110; text: "放弃修改"; tone: "neutral"; available: root.canSave }
                    IndustrialButton {
                        Layout.preferredWidth: 120
                        text: "保存配置"
                        available: root.canSave
                        onClicked: saveConfirmDialog.open()
                    }
                }
            }

            SectionCard {
                Layout.preferredWidth: 280
                Layout.fillHeight: true
                title: "参数说明 / 风险"
                subtitle: "选中参数后显示业务影响、推荐范围和修改限制。"

                Text { text: "分离矩阵行数"; color: "#E5EDF5"; font.pixelSize: 17; font.weight: Font.DemiBold }
                Text { Layout.fillWidth: true; text: "控制分离皮带矩阵的行数。该参数会影响实时监控矩阵、算法配置、包裹位置映射和模组速度展示。"; color: "#C8D3DF"; font.pixelSize: 13; wrapMode: Text.WordWrap }
                Text { text: "字段名：modRows"; color: "#9BA8B8"; font.pixelSize: 12 }
                Text { text: "推荐范围：1 - 8"; color: "#9BA8B8"; font.pixelSize: 12 }
                Text { text: "运行中修改：禁止"; color: "#EB5757"; font.pixelSize: 12 }
                Text { text: "保存后：需重新加载设备结构"; color: "#F2C94C"; font.pixelSize: 12 }
            }
        }
    }
}
