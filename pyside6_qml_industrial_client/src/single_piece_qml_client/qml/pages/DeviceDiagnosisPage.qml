import QtQuick
import QtQuick.Layouts

import "../components"

Rectangle {
    id: root
    color: "#0B1623"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        RowLayout {
            Layout.fillWidth: true
            Text { text: "设备诊断"; color: "#E5EDF5"; font.pixelSize: 20; font.weight: Font.DemiBold }
            Text { text: "通信、视觉、传感器、执行机构与系统资源诊断"; color: "#9BA8B8"; font.pixelSize: 13 }
            Item { Layout.fillWidth: true }
            StatusBadge { text: "PLC 离线"; tone: "critical" }
            StatusBadge { text: "相机 2/4"; tone: "warning" }
        }

        GridLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            columns: 2
            columnSpacing: 12
            rowSpacing: 12

            SectionCard {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: "通信诊断"
                subtitle: "PLC / Modbus 与业务 TCP 通道状态。"
                DeviceSegment { Layout.fillWidth: true; title: "PLC / Modbus"; subtitle: "IP：192.168.2.15    端口：2100    最后错误：connection timeout"; statusText: "离线"; statusState: "fault" }
                DeviceSegment { Layout.fillWidth: true; title: "业务 TCP Client"; subtitle: "IP：192.168.1.3    端口：2000    最后心跳：12:31:50"; statusText: "待机"; statusState: "offline" }
                RowLayout { Layout.fillWidth: true; IndustrialButton { Layout.fillWidth: true; text: "重新连接" }; IndustrialButton { Layout.fillWidth: true; text: "查看日志"; tone: "neutral" } }
            }

            SectionCard {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: "视觉诊断"
                subtitle: "单件分离、缓存、2D、3D 相机状态。"
                DeviceSegment { Layout.fillWidth: true; title: "单件分离相机"; subtitle: "IP：未配置"; statusText: "未配置"; statusState: "offline" }
                DeviceSegment { Layout.fillWidth: true; title: "缓存相机"; subtitle: "IP：未配置"; statusText: "未配置"; statusState: "offline" }
                DeviceSegment { Layout.fillWidth: true; title: "2D 相机"; subtitle: "IP：192.168.1.9    端口：12345"; statusText: "在线"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "3D 相机"; subtitle: "IP：192.168.1.10    端口：12345"; statusText: "在线"; statusState: "normal" }
            }

            SectionCard {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: "执行机构与传感器"
                subtitle: "皮带、居中机、剔除机、光电、电柜。"
                DeviceSegment { Layout.fillWidth: true; title: "分离机 4×4"; subtitle: "速度矩阵已加载，运行模组：6 / 16"; statusText: "监控中"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "居中机"; subtitle: "速度：1.30 m/s"; statusText: "正常"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "剔除机"; subtitle: "剔除口：正常    状态：待机"; statusText: "待机"; statusState: "offline" }
                DeviceSegment { Layout.fillWidth: true; title: "光电 / 电柜"; subtitle: "光电：正常    电柜：离线"; statusText: "异常"; statusState: "fault" }
            }

            SectionCard {
                Layout.fillWidth: true
                Layout.fillHeight: true
                title: "系统资源"
                subtitle: "边缘客户端与算法服务运行状态。"
                DeviceSegment { Layout.fillWidth: true; title: "CPU"; subtitle: "当前利用率：39.6%"; statusText: "正常"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "内存"; subtitle: "当前利用率：95.6%，建议检查图像缓存与算法进程"; statusText: "警告"; statusState: "warning" }
                DeviceSegment { Layout.fillWidth: true; title: "磁盘"; subtitle: "当前利用率：15.2%"; statusText: "正常"; statusState: "normal" }
                DeviceSegment { Layout.fillWidth: true; title: "算法服务"; subtitle: "算法版本：1.0.3    客户端版本：A1.0.0"; statusText: "正常"; statusState: "normal" }
            }
        }
    }
}
