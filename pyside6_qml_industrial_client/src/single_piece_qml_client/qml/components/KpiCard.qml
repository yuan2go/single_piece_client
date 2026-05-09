import QtQuick

Rectangle {
    id: root
    property string label: ""
    property string value: ""
    property string unit: ""
    property bool primary: false

    radius: 8
    color: primary ? "#132A42" : "#101D2B"
    border.color: primary ? "#2F80ED" : "#26384A"
    border.width: 1

    Column {
        anchors.fill: parent
        anchors.margins: primary ? 14 : 10
        spacing: primary ? 8 : 3

        Text {
            text: root.label
            color: "#9BA8B8"
            font.pixelSize: 13
        }

        Row {
            spacing: 6
            baselineOffset: 0
            Text {
                text: root.value
                color: "#E5EDF5"
                font.pixelSize: root.primary ? 32 : 18
                font.weight: Font.DemiBold
            }
            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: root.unit
                color: "#9BA8B8"
                font.pixelSize: 12
            }
        }
    }
}
