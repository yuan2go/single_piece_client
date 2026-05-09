import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property var cells: []
    property var packages: []
    property int rows: 4
    property int cols: 4

    radius: 12
    color: "#0E1A29"
    border.color: "#2F80ED"
    border.width: 1

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 14
        spacing: 10

        RowLayout {
            Layout.fillWidth: true
            Text {
                text: "分离矩阵 4 × 4"
                color: "#E5EDF5"
                font.pixelSize: 16
                font.weight: Font.DemiBold
            }
            Text {
                text: "每格显示当前皮带速度"
                color: "#9BA8B8"
                font.pixelSize: 12
            }
            Item { Layout.fillWidth: true }
            Text {
                text: "速度单位：m/s"
                color: "#9BA8B8"
                font.pixelSize: 12
            }
        }

        Item {
            id: matrixCanvas
            Layout.fillWidth: true
            Layout.fillHeight: true
            property real gap: 8
            property real cellW: (width - (root.cols - 1) * gap) / root.cols
            property real cellH: (height - (root.rows - 1) * gap) / root.rows

            Repeater {
                model: root.cells
                delegate: Rectangle {
                    x: modelData.col * (matrixCanvas.cellW + matrixCanvas.gap)
                    y: modelData.row * (matrixCanvas.cellH + matrixCanvas.gap)
                    width: matrixCanvas.cellW
                    height: matrixCanvas.cellH
                    radius: 8
                    color: modelData.status === "running" ? "#132438" : "#101820"
                    border.color: modelData.status === "running" ? "#2E536F" : "#26384A"
                    border.width: 1

                    Text {
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.leftMargin: 10
                        anchors.topMargin: 8
                        text: modelData.speed
                        color: "#E5EDF5"
                        font.family: "monospace"
                        font.pixelSize: 15
                        font.weight: Font.DemiBold
                        z: 3
                    }

                    Text {
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.leftMargin: 52
                        anchors.topMargin: 10
                        text: "m/s"
                        color: "#9BA8B8"
                        font.pixelSize: 10
                        z: 3
                    }

                    StatusDot {
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.rightMargin: 10
                        anchors.topMargin: 10
                        state: modelData.status === "running" ? "running" : "stopped"
                        z: 3
                    }

                    Rectangle {
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.leftMargin: 10
                        anchors.rightMargin: 10
                        anchors.bottomMargin: 9
                        height: 4
                        radius: 2
                        color: modelData.status === "running" ? "#2F80ED" : "#3A4654"
                        opacity: modelData.status === "running" ? 0.72 : 0.38
                    }
                }
            }

            Repeater {
                model: root.packages
                delegate: Rectangle {
                    x: modelData.col * (matrixCanvas.cellW + matrixCanvas.gap) + 16
                    y: modelData.row * (matrixCanvas.cellH + matrixCanvas.gap) + matrixCanvas.cellH * 0.42
                    width: modelData.colSpan * matrixCanvas.cellW + (modelData.colSpan - 1) * matrixCanvas.gap - 32
                    height: Math.max(28, modelData.rowSpan * matrixCanvas.cellH * 0.42)
                    radius: 8
                    color: "#B8C7D9"
                    opacity: 0.58
                    border.color: "#E5EDF5"
                    border.width: 1
                    z: 2

                    Text {
                        anchors.centerIn: parent
                        text: modelData.id
                        color: "#0B1623"
                        font.pixelSize: 11
                        font.weight: Font.DemiBold
                    }
                }
            }
        }
    }
}
