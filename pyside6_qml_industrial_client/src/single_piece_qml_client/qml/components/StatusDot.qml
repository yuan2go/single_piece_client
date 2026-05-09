import QtQuick

Rectangle {
    id: root
    property string state: "normal"
    width: 9
    height: 9
    radius: width / 2
    color: {
        if (state === "running" || state === "normal" || state === "online") return "#21C36B"
        if (state === "warning" || state === "partial") return "#F2C94C"
        if (state === "fault" || state === "offline" || state === "critical") return "#EB5757"
        return "#8A94A6"
    }
    border.color: "#26384A"
    border.width: 1
}
