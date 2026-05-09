import QtQuick
import QtQuick.Layouts
import "../styles"

Rectangle {
    id: root
    property string title: ""
    property string icon: "▤"
    property string a: ""
    property string av: ""
    property string b: ""
    property string bv: ""
    property string c: ""
    property string cv: ""

    radius: Theme.radiusPanel
    color: Theme.panelBg2
    border.color: "#2a3e4f"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 14
        spacing: 10

        RowLayout {
            Text { text: root.icon; color: "#99adc2"; font.pixelSize: 22 }
            Text { text: root.title; color: Theme.textPrimary; font.pixelSize: 16; font.bold: true }
        }
        Rectangle { Layout.fillWidth: true; height: 1; color: "#294052" }
        ValuePair { k: root.a; v: root.av }
        ValuePair { k: root.b; v: root.bv }
        ValuePair { k: root.c; v: root.cv; strong: true }
        Rectangle {
            Layout.fillWidth: true
            height: 6
            radius: 3
            color: "#243543"
            Rectangle { width: parent.width * 0.67; height: parent.height; radius: 3; color: Theme.accent }
        }
    }
}
