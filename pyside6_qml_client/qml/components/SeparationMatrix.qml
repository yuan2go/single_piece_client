import QtQuick
import QtQuick.Layouts
import "../styles"

Item {
    id: root

    Text {
        text: "分离矩阵（4 × 4）   单位：m/s"
        color: Theme.textPrimary
        font.pixelSize: 17
        font.bold: true
        anchors.left: matrix.left
        anchors.top: parent.top
        anchors.topMargin: 8
    }

    Row {
        anchors.right: matrix.right
        anchors.top: parent.top
        anchors.topMargin: 10
        spacing: 15
        Legend { colorValue: "#263645"; textValue: "无包裹" }
        Legend { colorValue: "#176fc2"; textValue: "有包裹" }
        Legend { colorValue: "#ffd323"; textValue: "包裹跨带" }
    }

    Item {
        id: matrix
        width: Math.min(parent.width - 40, 520)
        height: width * 0.78
        anchors.centerIn: parent
        anchors.verticalCenterOffset: 18
        property real cellWidth: width / 4
        property real cellHeight: height / 4

        Grid {
            anchors.fill: parent
            rows: 4
            columns: 4
            spacing: 4
            Repeater {
                model: 16
                delegate: Rectangle {
                    width: (matrix.width - 12) / 4
                    height: (matrix.height - 12) / 4
                    radius: 3
                    color: "#14212d"
                    border.color: "#28659b"

                    Column {
                        anchors.centerIn: parent
                        spacing: 6
                        Text {
                            text: (Math.floor(index / 4) + 1) + "-" + (index % 4 + 1)
                            color: "#eff6ff"
                            font.pixelSize: 17
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                        Text {
                            text: "1.30\nm/s"
                            color: "#eff6ff"
                            font.pixelSize: 18
                            horizontalAlignment: Text.AlignHCenter
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                    }

                    Rectangle {
                        width: 22
                        height: 5
                        radius: 2
                        anchors.left: parent.left
                        anchors.leftMargin: 8
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 6
                        color: Theme.accent
                        opacity: 0.75
                    }
                }
            }
        }

        Rectangle {
            x: matrix.cellWidth + 9
            y: matrix.cellHeight * 2 + 9
            width: matrix.cellWidth * 2 - 18
            height: matrix.cellHeight - 14
            radius: 5
            color: "#f5c23b"
            border.color: "#ffed73"
            border.width: 2
            opacity: 0.92
            Row {
                anchors.centerIn: parent
                spacing: 22
                PackageBox {}
                PackageBox {}
            }
        }

        Rectangle { x: 42; y: matrix.cellHeight * 3 + 26; width: 40; height: 30; radius: 3; color: "#2287dc"; opacity: 0.85 }
        Rectangle { x: matrix.cellWidth * 3 + 52; y: matrix.cellHeight * 3 + 26; width: 40; height: 30; radius: 3; color: "#2287dc"; opacity: 0.85 }
    }

    component Legend: Row {
        property color colorValue
        property string textValue
        spacing: 6
        Rectangle { width: 18; height: 12; color: colorValue; border.color: "#3b5265"; anchors.verticalCenter: parent.verticalCenter }
        Text { text: textValue; color: Theme.textMuted; font.pixelSize: 12 }
    }

    component PackageBox: Rectangle {
        width: 54
        height: 34
        radius: 3
        color: "#c9903a"
        border.color: "#a66f27"
        Rectangle { width: 12; height: 8; color: "#a66f27"; anchors.top: parent.top; anchors.horizontalCenter: parent.horizontalCenter }
    }
}
