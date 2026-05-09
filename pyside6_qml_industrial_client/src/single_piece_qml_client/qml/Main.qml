import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "components"
import "pages"

ApplicationWindow {
    id: root
    width: 1920
    height: 1080
    minimumWidth: 1440
    minimumHeight: 860
    visible: true
    title: "单件分离控制系统"
    color: "#0B1623"

    property int currentPage: 0

    font.family: "Noto Sans CJK SC"
    font.pixelSize: 13

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        TopStatusBar {
            Layout.fillWidth: true
            Layout.preferredHeight: 64
            runtimeData: backend.runtime
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            SideNavigation {
                Layout.preferredWidth: 110
                Layout.fillHeight: true
                currentIndex: root.currentPage
                onSelected: function(index) { root.currentPage = index }
            }

            StackLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                currentIndex: root.currentPage

                RealtimeMonitorPage {
                    runtimeData: backend.runtime
                    beltCells: backend.beltCells
                    packages: backend.packages
                }

                AlarmCenterPage {
                    alarms: backend.alarms
                }

                DeviceDiagnosisPage {}

                ParameterConfigPage {}

                LogRecordPage {
                    events: backend.events
                }

                SystemSettingsPage {}
            }

            RightStatusPanel {
                visible: root.currentPage === 0
                Layout.preferredWidth: root.currentPage === 0 ? 360 : 0
                Layout.fillHeight: true
                runtimeData: backend.runtime
                kpis: backend.kpis
                alarms: backend.alarms
            }
        }

        BottomEventPanel {
            Layout.fillWidth: true
            Layout.preferredHeight: 180
            events: backend.events
        }
    }
}
