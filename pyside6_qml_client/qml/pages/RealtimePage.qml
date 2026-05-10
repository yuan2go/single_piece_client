import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
import "../styles"

RowLayout {
    id: root
    property var backend
    spacing: Theme.pageMargin

    ColumnLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        spacing: Theme.pageMargin

        AppPanel {
            Layout.fillWidth: true
            Layout.preferredHeight: 555
            title: "设备运行流程"

            RowLayout {
                anchors.fill: parent
                spacing: 18

                ColumnLayout {
                    Layout.preferredWidth: 205
                    Layout.fillHeight: true
                    FlowBox { Layout.preferredHeight: 84; name: "供包皮带线"; icon: "↘"; line1: "速度：1.20 m/s"; line2: "包裹：110" }
                    ArrowDown {}
                    FlowBox { Layout.preferredHeight: 84; name: "滑槽"; icon: "⌁"; line1: "速度：1.00 m/s"; line2: "状态：开启" }
                    ArrowDown {}
                    FlowBox { Layout.preferredHeight: 84; name: "缓存1皮带线"; icon: "▭"; line1: "速度：1.30 m/s"; line2: "包裹：28" }
                    ArrowDown {}
                    FlowBox { Layout.preferredHeight: 84; name: "缓存2皮带线"; icon: "▭"; line1: "速度：1.30 m/s"; line2: "包裹：16" }
                }

                SeparationMatrix {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                }

                ColumnLayout {
                    Layout.preferredWidth: 210
                    Layout.fillHeight: true
                    spacing: 12
                    Text { text: "→"; color: Theme.success; font.pixelSize: 42; Layout.alignment: Qt.AlignHCenter }
                    FlowBox { Layout.preferredHeight: 72; name: "居中机"; icon: "▤"; line1: "速度：1.20 m/s"; line2: "状态：运行中" }
                    FlowBox { Layout.preferredHeight: 72; name: "剔除机"; icon: "▭"; line1: "速度：1.20 m/s"; line2: "状态：运行中" }
                    FlowBox { Layout.preferredHeight: 72; name: "供包台"; icon: "◫"; line1: "包裹：65"; line2: "正常" }
                    FlowBox { Layout.preferredHeight: 72; name: "人工线"; icon: "♙"; line1: "包裹：8"; line2: "正常" }
                    FlowBox { Layout.preferredHeight: 72; name: "循环线"; icon: "⟳"; line1: "包裹：12"; line2: "正常" }
                }
            }

            Row {
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                height: 30
                spacing: 34
                InlineInfo { label: "系统节拍"; value: backend.stats.beat + " s/件" }
                InlineInfo { label: "当前包裹"; value: backend.stats.current + " 件" }
                InlineInfo { label: "累计包裹"; value: backend.stats.total.toLocaleString() + " 件" }
                InlineInfo { label: "运行时间"; value: backend.stats.uptime; highlight: true }
                InlineInfo { label: "设备状态"; value: backend.runState; highlight: backend.runState === "运行中" }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: Theme.pageMargin

            AppPanel {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: "分离数据总览"
                GridLayout {
                    anchors.fill: parent
                    columns: 4
                    rowSpacing: 12
                    columnSpacing: 12
                    MetricCard { title: "主线数据"; icon: "▤"; a: "包裹总数"; av: backend.stats.total.toLocaleString() + " 件"; b: "平均包裹长度"; bv: backend.stats.avgLen + " mm"; c: "每小时效率"; cv: backend.stats.throughput + " 件/小时" }
                    MetricCard { title: "供包台数据"; icon: "◫"; a: "供件数量"; av: backend.stats.supply + " 件"; b: "小时效率"; bv: backend.stats.supplyEff + " 件/小时"; c: "供包台占比"; cv: backend.stats.supplyRatio + "%" }
                    MetricCard { title: "人工线数据"; icon: "♙"; a: "人工线数量"; av: backend.stats.manual + " 件"; b: "小时效率"; bv: backend.stats.manualEff + " 件/小时"; c: "人工线比例"; cv: backend.stats.manualRatio + "%" }
                    MetricCard { title: "循环线数据"; icon: "⟳"; a: "循环件数量"; av: backend.stats.cycle + " 件"; b: "小时效率"; bv: backend.stats.cycleEff + " 件/小时"; c: "循环线比例"; cv: backend.stats.cycleRatio + "%" }
                }
            }

            AppPanel {
                Layout.preferredWidth: 410
                Layout.fillHeight: true
                title: "趋势概览（最近60分钟）"
                TrendChart { anchors.fill: parent; points: backend.trend }
            }
        }
    }

    ColumnLayout {
        Layout.preferredWidth: 342
        Layout.fillHeight: true
        spacing: Theme.pageMargin

        AppPanel {
            Layout.fillWidth: true
            Layout.preferredHeight: 128
            title: "操作控制"
            RowLayout {
                anchors.fill: parent
                spacing: 14
                AppButton { text: "▶  开始"; variant: "success"; Layout.fillWidth: true; Layout.fillHeight: true; onClicked: backend.startDevice() }
                AppButton { text: "■  停止"; variant: "danger"; Layout.fillWidth: true; Layout.fillHeight: true; onClicked: backend.stopDevice() }
            }
        }

        AppPanel {
            Layout.fillWidth: true
            Layout.preferredHeight: 260
            title: "设备信息"
            ColumnLayout {
                anchors.fill: parent
                spacing: 12
                KeyValueRow { label: "设备型号"; value: "单件分离机 v2.3.1" }
                KeyValueRow { label: "PLC型号"; value: "Siemens S7-1200" }
                KeyValueRow { label: "相机型号"; value: "Basler acA2500-60gc" }
                KeyValueRow { label: "光电型号"; value: "SICK WTB4-3P2261" }
                KeyValueRow { label: "固件版本"; value: "v2.3.1" }
                KeyValueRow { label: "上次维护"; value: "2026-05-08 09:32" }
            }
        }

        AppPanel {
            Layout.fillWidth: true
            Layout.fillHeight: true
            title: "通信状态"
            GridLayout {
                anchors.fill: parent
                columns: 2
                rowSpacing: 16
                columnSpacing: 18
                CommStatus { label: "PLC通信" }
                CommStatus { label: "循环通信" }
                CommStatus { label: "光电通信" }
                CommStatus { label: "HMI通信" }
                KeyValueRow { label: "网络延迟"; value: "12 ms"; Layout.columnSpan: 2 }
                KeyValueRow { label: "丢包率"; value: "0%"; Layout.columnSpan: 2 }
            }
        }
    }

    component ArrowDown: Text {
        text: "↓"
        color: Theme.success
        font.pixelSize: 30
        Layout.fillWidth: true
        Layout.preferredHeight: 34
        horizontalAlignment: Text.AlignHCenter
    }

    component InlineInfo: RowLayout {
        property string label
        property string value
        property bool highlight: false
        spacing: 8
        Text { text: label + "："; color: "#94a6b7"; font.pixelSize: Theme.fontBody }
        Text { text: value; color: highlight ? Theme.success : Theme.textSecondary; font.pixelSize: Theme.fontBody; font.bold: highlight }
    }

    component CommStatus: RowLayout {
        property string label
        Text { text: label; color: Theme.textSecondary; font.pixelSize: Theme.fontBody; Layout.fillWidth: true }
        Rectangle { width: 9; height: 9; radius: 4.5; color: Theme.success }
        Text { text: "正常"; color: Theme.success; font.pixelSize: Theme.fontBody; font.bold: true }
    }
}
