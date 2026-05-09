import QtQuick
import QtQuick.Layouts
import "../styles"

Rectangle {
    id: root
    property var backend

    width: Theme.navWidth
    color: Theme.navBg
    border.color: "#1e3142"

    Column {
        anchors.fill: parent
        anchors.topMargin: 18

        NavItem { label: "实时监控"; icon: "▣"; page: 0; backend: root.backend }
        NavItem { label: "参数配置"; icon: "⚙"; page: 1; backend: root.backend }
        NavItem { label: "日志记录"; icon: "☷"; page: 2; backend: root.backend }
        NavItem { label: "系统设置"; icon: "◎"; page: 3; backend: root.backend }
    }

    component NavItem: Rectangle {
        property string label
        property string icon
        property int page
        property var backend

        width: Theme.navWidth
        height: 96
        color: backend.currentPage === page ? Theme.accentSoft : "transparent"

        Rectangle {
            visible: backend.currentPage === page
            width: 4
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            color: Theme.accent
        }

        Column {
            anchors.centerIn: parent
            spacing: 8
            Text {
                text: icon
                color: backend.currentPage === page ? "#33a0ff" : "#9aa9b8"
                font.pixelSize: 26
                anchors.horizontalCenter: parent.horizontalCenter
            }
            Text {
                text: label
                color: backend.currentPage === page ? "#33a0ff" : Theme.textSecondary
                font.pixelSize: 15
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }

        MouseArea {
            anchors.fill: parent
            onClicked: backend.setPage(page)
        }
    }
}
