import QtQuick
import QtQuick.Layouts
import "../styles"
import "../components"

Rectangle {
    id: root
    property var backend

    height: Theme.topBarHeight
    color: Theme.topBarBg
    border.color: Theme.borderSoft

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 18
        anchors.rightMargin: 18
        spacing: 18

        Text { text: "◇"; color: Theme.accent; font.pixelSize: 30; font.bold: true }
        Text { text: backend.systemName; color: "#f4f8fb"; font.pixelSize: 17; font.bold: true; Layout.preferredWidth: 176 }
        HeaderItem { label: "场地"; value: backend.siteName; w: 158 }
        HeaderItem { label: "设备名称"; value: backend.deviceName; w: 175 }
        StatusBadge { label: "运行状态"; value: backend.runState; ok: backend.runState === "运行中" }
        StatusBadge { label: "运行模式"; value: "自动模式"; ok: true; blue: true }
        DotStatus { label: "PLC状态"; value: "在线" }
        DotStatus { label: "相机状态"; value: "正常" }
        DotStatus { label: "光电状态"; value: "正常" }
        DotStatus { label: "机柜状态"; value: "正常" }
        Text { text: "报警 3"; color: Theme.danger; font.pixelSize: 15; font.bold: true }
        Item { Layout.fillWidth: true }
        Text { text: "用户：admin"; color: Theme.textSecondary; font.pixelSize: Theme.fontBody }
        Text { text: backend.currentTime; color: Theme.textSecondary; font.pixelSize: Theme.fontBody }
    }

    component HeaderItem: RowLayout {
        property string label
        property string value
        property int w: 120
        Layout.preferredWidth: w
        spacing: 6
        Text { text: label + "："; color: Theme.textMuted; font.pixelSize: Theme.fontBody }
        Text { text: value; color: Theme.textSecondary; font.pixelSize: Theme.fontBody; elide: Text.ElideRight; Layout.fillWidth: true }
    }

    component DotStatus: RowLayout {
        property string label
        property string value
        spacing: 7
        Text { text: label + "："; color: Theme.textMuted; font.pixelSize: Theme.fontBody }
        Rectangle { width: 10; height: 10; radius: 5; color: Theme.success }
        Text { text: value; color: Theme.success; font.pixelSize: 13; font.bold: true }
    }
}
