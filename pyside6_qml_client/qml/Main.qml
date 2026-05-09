import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: app
    visible: true
    width: 1536
    height: 960
    minimumWidth: 1360
    minimumHeight: 820
    title: backend.systemName + " - " + ["实时监控", "参数配置", "日志记录", "系统设置"][backend.currentPage]
    color: "#0b131b"

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 76
            color: "#0d151e"
            border.color: "#1f303f"
            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 18
                anchors.rightMargin: 18
                spacing: 18
                Text { text: "◇"; color: "#2e91ff"; font.pixelSize: 30; font.bold: true }
                Text { text: backend.systemName; color: "#f4f8fb"; font.pixelSize: 17; font.bold: true; Layout.preferredWidth: 176 }
                HeaderText { label: "场地"; value: backend.siteName; w: 158 }
                HeaderText { label: "设备名称"; value: backend.deviceName; w: 175 }
                Badge { label: "运行状态"; value: backend.runState; ok: backend.runState === "运行中" }
                Badge { label: "运行模式"; value: "自动模式"; ok: true; blue: true }
                DotText { label: "PLC状态"; value: "在线" }
                DotText { label: "相机状态"; value: "正常" }
                DotText { label: "光电状态"; value: "正常" }
                DotText { label: "机柜状态"; value: "正常" }
                Text { text: "🔔 3"; color: "#ff696b"; font.pixelSize: 15; font.bold: true }
                Item { Layout.fillWidth: true }
                Text { text: "用户：admin"; color: "#dce7f1"; font.pixelSize: 14 }
                Text { text: backend.currentTime; color: "#dce7f1"; font.pixelSize: 14 }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            Rectangle {
                Layout.preferredWidth: 128
                Layout.fillHeight: true
                color: "#101b25"
                border.color: "#1e3142"
                Column {
                    anchors.fill: parent
                    anchors.topMargin: 18
                    NavButton { label: "实时监控"; icon: "▣"; page: 0 }
                    NavButton { label: "参数配置"; icon: "⚙"; page: 1 }
                    NavButton { label: "日志记录"; icon: "☷"; page: 2 }
                    NavButton { label: "系统设置"; icon: "◎"; page: 3 }
                }
            }

            Loader {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.margins: 14
                sourceComponent: backend.currentPage === 0 ? realtimePage
                               : backend.currentPage === 1 ? paramPage
                               : backend.currentPage === 2 ? logPage
                               : settingPage
            }
        }
    }

    Rectangle {
        visible: backend.toast.length > 0
        width: toastText.width + 34
        height: 40
        radius: 20
        color: "#173553"
        border.color: "#2e91ff"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 28
        Text { id: toastText; anchors.centerIn: parent; text: backend.toast; color: "#f0f6ff"; font.pixelSize: 14 }
    }

    Component {
        id: realtimePage
        RowLayout {
            spacing: 14
            ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 14
                Panel {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 555
                    title: "设备运行流程"
                    RowLayout {
                        anchors.fill: parent
                        spacing: 18
                        ColumnLayout {
                            Layout.preferredWidth: 205
                            Layout.fillHeight: true
                            FlowBox { name: "供包皮带线"; icon: "↘"; v1: "速度：1.20 m/s"; v2: "包裹：110" }
                            ArrowDown {}
                            FlowBox { name: "滑槽"; icon: "⌁"; v1: "速度：1.00 m/s"; v2: "状态：开启" }
                            ArrowDown {}
                            FlowBox { name: "缓存1皮带线"; icon: "▭"; v1: "速度：1.30 m/s"; v2: "包裹：28" }
                            ArrowDown {}
                            FlowBox { name: "缓存2皮带线"; icon: "▭"; v1: "速度：1.30 m/s"; v2: "包裹：16" }
                        }
                        Item {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Text { text: "分离矩阵（4 × 4）   单位：m/s"; color: "#eef5ff"; font.pixelSize: 17; font.bold: true; anchors.left: matrix.left; anchors.top: parent.top; anchors.topMargin: 8 }
                            Row { anchors.right: matrix.right; anchors.top: parent.top; anchors.topMargin: 10; spacing: 15; Legend { c: "#263645"; t: "无包裹" } Legend { c: "#176fc2"; t: "有包裹" } Legend { c: "#ffd323"; t: "包裹跨带" } }
                            Item {
                                id: matrix
                                width: Math.min(parent.width - 40, 520)
                                height: width * 0.78
                                anchors.centerIn: parent
                                anchors.verticalCenterOffset: 18
                                property real cw: width / 4
                                property real ch: height / 4
                                Grid {
                                    anchors.fill: parent
                                    rows: 4; columns: 4; spacing: 4
                                    Repeater {
                                        model: 16
                                        delegate: Rectangle {
                                            width: (matrix.width - 12) / 4
                                            height: (matrix.height - 12) / 4
                                            radius: 3
                                            color: "#14212d"
                                            border.color: "#28659b"
                                            Column { anchors.centerIn: parent; spacing: 6
                                                Text { text: (Math.floor(index / 4) + 1) + "-" + (index % 4 + 1); color: "#eff6ff"; font.pixelSize: 17; anchors.horizontalCenter: parent.horizontalCenter }
                                                Text { text: "1.30\nm/s"; color: "#eff6ff"; font.pixelSize: 18; horizontalAlignment: Text.AlignHCenter; anchors.horizontalCenter: parent.horizontalCenter }
                                            }
                                            Rectangle { width: 22; height: 5; radius: 2; anchors.left: parent.left; anchors.leftMargin: 8; anchors.bottom: parent.bottom; anchors.bottomMargin: 6; color: "#2386ff"; opacity: 0.75 }
                                        }
                                    }
                                }
                                Rectangle { x: matrix.cw + 9; y: matrix.ch * 2 + 9; width: matrix.cw * 2 - 18; height: matrix.ch - 14; radius: 5; color: "#f5c23b"; border.color: "#ffed73"; border.width: 2; opacity: 0.92
                                    Row { anchors.centerIn: parent; spacing: 22; PackageBox {} PackageBox {} }
                                }
                                Rectangle { x: 42; y: matrix.ch * 3 + 26; width: 40; height: 30; radius: 3; color: "#2287dc"; opacity: 0.85 }
                                Rectangle { x: matrix.cw * 3 + 52; y: matrix.ch * 3 + 26; width: 40; height: 30; radius: 3; color: "#2287dc"; opacity: 0.85 }
                            }
                        }
                        ColumnLayout {
                            Layout.preferredWidth: 210
                            Layout.fillHeight: true
                            spacing: 12
                            Text { text: "→"; color: "#47d13e"; font.pixelSize: 42; Layout.alignment: Qt.AlignHCenter }
                            FlowBox { name: "居中机"; icon: "▤"; v1: "速度：1.20 m/s"; v2: "状态：运行中" }
                            FlowBox { name: "剔除机"; icon: "▭"; v1: "速度：1.20 m/s"; v2: "状态：运行中" }
                            FlowBox { name: "供包台"; icon: "◫"; v1: "包裹：65"; v2: "正常" }
                            FlowBox { name: "人工线"; icon: "♙"; v1: "包裹：8"; v2: "正常" }
                            FlowBox { name: "循环线"; icon: "⟳"; v1: "包裹：12"; v2: "正常" }
                        }
                    }
                    Row { anchors.left: parent.left; anchors.right: parent.right; anchors.bottom: parent.bottom; height: 30; spacing: 34
                        InfoInline { k: "系统节拍"; v: backend.stats.beat + " s/件" }
                        InfoInline { k: "当前包裹"; v: backend.stats.current + " 件" }
                        InfoInline { k: "累计包裹"; v: backend.stats.total.toLocaleString() + " 件" }
                        InfoInline { k: "运行时间"; v: backend.stats.uptime; green: true }
                        InfoInline { k: "设备状态"; v: backend.runState; green: backend.runState === "运行中" }
                    }
                }
                RowLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    spacing: 14
                    Panel { Layout.fillWidth: true; Layout.fillHeight: true; title: "分离数据总览"
                        GridLayout { anchors.fill: parent; columns: 4; rowSpacing: 12; columnSpacing: 12
                            Metric { title: "主线数据"; icon: "▤"; a: "包裹总数"; av: backend.stats.total.toLocaleString() + " 件"; b: "平均包裹长度"; bv: backend.stats.avgLen + " mm"; c: "每小时效率"; cv: backend.stats.throughput + " 件/小时" }
                            Metric { title: "供包台数据"; icon: "◫"; a: "供件数量"; av: backend.stats.supply + " 件"; b: "小时效率"; bv: backend.stats.supplyEff + " 件/小时"; c: "供包台占比"; cv: backend.stats.supplyRatio + "%" }
                            Metric { title: "人工线数据"; icon: "♙"; a: "人工线数量"; av: backend.stats.manual + " 件"; b: "小时效率"; bv: backend.stats.manualEff + " 件/小时"; c: "人工线比例"; cv: backend.stats.manualRatio + "%" }
                            Metric { title: "循环线数据"; icon: "⟳"; a: "循环件数量"; av: backend.stats.cycle + " 件"; b: "小时效率"; bv: backend.stats.cycleEff + " 件/小时"; c: "循环线比例"; cv: backend.stats.cycleRatio + "%" }
                        }
                    }
                    Panel { Layout.preferredWidth: 410; Layout.fillHeight: true; title: "趋势概览（最近60分钟）"; TrendCanvas { anchors.fill: parent; points: backend.trend } }
                }
            }
            ColumnLayout {
                Layout.preferredWidth: 342
                Layout.fillHeight: true
                spacing: 14
                Panel { Layout.fillWidth: true; Layout.preferredHeight: 128; title: "操作控制"
                    RowLayout { anchors.fill: parent; spacing: 14; ButtonX { text: "▶  开始"; variant: "success"; Layout.fillWidth: true; Layout.fillHeight: true; onClicked: backend.startDevice() } ButtonX { text: "■  停止"; variant: "danger"; Layout.fillWidth: true; Layout.fillHeight: true; onClicked: backend.stopDevice() } }
                }
                Panel { Layout.fillWidth: true; Layout.preferredHeight: 260; title: "设备信息"
                    ColumnLayout { anchors.fill: parent; spacing: 12
                        Pair { k: "设备型号"; v: "单件分离机 v2.3.1" } Pair { k: "PLC型号"; v: "Siemens S7-1200" } Pair { k: "相机型号"; v: "Basler acA2500-60gc" } Pair { k: "光电型号"; v: "SICK WTB4-3P2261" } Pair { k: "固件版本"; v: "v2.3.1" } Pair { k: "上次维护"; v: "2026-05-08 09:32" }
                    }
                }
                Panel { Layout.fillWidth: true; Layout.fillHeight: true; title: "通信状态"
                    GridLayout { anchors.fill: parent; columns: 2; rowSpacing: 16; columnSpacing: 18
                        Comm { k: "PLC通信" } Comm { k: "循环通信" } Comm { k: "光电通信" } Comm { k: "HMI通信" } Pair { k: "网络延迟"; v: "12 ms"; Layout.columnSpan: 2 } Pair { k: "丢包率"; v: "0%"; Layout.columnSpan: 2 }
                    }
                }
            }
        }
    }

    Component {
        id: paramPage
        RowLayout {
            spacing: 14
            ColumnLayout {
                Layout.fillWidth: true; Layout.fillHeight: true; spacing: 14
                RowLayout {
                    Layout.fillWidth: true; Layout.fillHeight: true; spacing: 14
                    Rectangle { Layout.preferredWidth: 140; Layout.fillHeight: true; radius: 8; color: "#14202b"; border.color: "#263847"
                        Column { anchors.fill: parent; anchors.margins: 8; spacing: 4; ParamTab { t: "分离机参数"; selected: true } ParamTab { t: "除塞机参数" } ParamTab { t: "居中机参数" } ParamTab { t: "剔除机参数" } ParamTab { t: "系统配置" } }
                    }
                    Panel { Layout.fillWidth: true; Layout.fillHeight: true; title: "参数配置"
                        Flickable { anchors.fill: parent; contentWidth: width; contentHeight: paramCol.height; clip: true
                            Column { id: paramCol; width: parent.width; spacing: 12
                                ParamSection { title: "分离机与准入配置"; groupName: "分离机与准入配置" }
                                ParamSection { title: "速度与阈值配置"; groupName: "速度与阈值配置" }
                                ParamSection { title: "算法与相机参数"; groupName: "算法与相机参数" }
                                ParamSection { title: "显示与保存配置"; groupName: "显示与保存配置" }
                            }
                        }
                    }
                }
                FooterButtons { onSave: backend.saveParams() }
            }
            RightStatus {}
        }
    }

    Component {
        id: logPage
        RowLayout {
            spacing: 14
            ColumnLayout { Layout.fillWidth: true; Layout.fillHeight: true; spacing: 14
                Panel { Layout.fillWidth: true; Layout.fillHeight: true; title: "日志记录"
                    ColumnLayout { anchors.fill: parent; spacing: 12
                        RowLayout { Layout.fillWidth: true; spacing: 12; FilterBox { v: "时间范围：近24小时" } FilterBox { v: "日志类型：全部" } FilterBox { v: "来源模块：全部" } FilterBox { v: "级别：全部" } TextField { Layout.fillWidth: true; height: 36; placeholderText: "关键字搜索"; color: "#e7f0fa"; placeholderTextColor: "#708395"; background: InputBg{} } ButtonX { text: "导出" } ButtonX { text: "刷新"; variant: "primary"; onClicked: backend.refreshLogs() } }
                        Rectangle { Layout.fillWidth: true; height: 34; color: "#182a38"; border.color: "#263847"; RowLayout { anchors.fill: parent; anchors.leftMargin: 8; TH { text: "时间"; w: 150 } TH { text: "级别"; w: 70 } TH { text: "日志类型"; w: 96 } TH { text: "来源模块"; w: 105 } TH { text: "事件内容"; fill: true } TH { text: "操作人"; w: 80 } TH { text: "结果"; w: 72 } TH { text: "TraceID"; w: 150 } } }
                        ListView { id: lv; Layout.fillWidth: true; Layout.fillHeight: true; clip: true; model: backend.logModel
                            delegate: Rectangle { width: ListView.view.width; height: 34; color: ListView.isCurrentItem ? "#174a82" : (index % 2 === 0 ? "#111c25" : "#13212c"); border.color: "#213444"; MouseArea { anchors.fill: parent; onClicked: { lv.currentIndex = index; backend.selectLog(index) } }
                                RowLayout { anchors.fill: parent; anchors.leftMargin: 8; spacing: 0
                                    TD { text: model.time; w: 150 } TD { text: model.level; w: 70; cc: model.level === "异常" ? "#ff696b" : (model.level === "警告" ? "#ffb020" : "#6ee072") } TD { text: model.type; w: 96 } TD { text: model.module; w: 105 } TD { text: model.content; fill: true } TD { text: model.operator; w: 80 } TD { text: model.result; w: 72 } TD { text: model.trace; w: 150 }
                                }
                            }
                        }
                        RowLayout { Layout.fillWidth: true; Text { text: "共 1,256 条"; color: "#c0cedb"; font.pixelSize: 14; Layout.fillWidth: true } Text { text: "1  2  3  4  5  ... 63     20 条/页"; color: "#9fb0c1"; font.pixelSize: 14 } }
                    }
                }
                Panel { Layout.fillWidth: true; Layout.preferredHeight: 150; title: "最近导出记录"
                    ColumnLayout { anchors.fill: parent; spacing: 8; ExportRow { f: "logs_20260509_121503.zip"; s: "28.6 MB" } ExportRow { f: "comm_logs_20260509.zip"; s: "12.4 MB" } ExportRow { f: "logs_20260508_week.zip"; s: "156.2 MB" } }
                }
            }
            ColumnLayout { Layout.preferredWidth: 328; Layout.fillHeight: true; spacing: 14
                Panel { Layout.fillWidth: true; Layout.preferredHeight: 192; title: "日志统计"; Donut { anchors.fill: parent } }
                Panel { Layout.fillWidth: true; Layout.preferredHeight: 206; title: "存储状态"; ColumnLayout { anchors.fill: parent; spacing: 16; Pair { k: "日志文件大小"; v: "1.36 GB" } Pair { k: "保留天数"; v: "30 天" } Pair { k: "磁盘使用率"; v: "72%" } Pair { k: "可用空间"; v: "118.4 GB / 512 GB" } } }
                Panel { Layout.fillWidth: true; Layout.fillHeight: true; title: "当前选中日志详情"
                    ColumnLayout { anchors.fill: parent; spacing: 13; Pair { k: "时间"; v: backend.selectedLog.time || "-" } Pair { k: "级别"; v: backend.selectedLog.level || "-" } Pair { k: "日志类型"; v: backend.selectedLog.type || "-" } Pair { k: "来源模块"; v: backend.selectedLog.module || "-" } Pair { k: "操作人"; v: backend.selectedLog.operator || "-" } Pair { k: "结果"; v: backend.selectedLog.result || "-" } Pair { k: "TraceID"; v: backend.selectedLog.trace || "-" } Text { text: "事件内容"; color: "#9fb0c1"; font.pixelSize: 14 } Text { text: backend.selectedLog.content || "-"; color: "#dce7f1"; font.pixelSize: 14; wrapMode: Text.WordWrap; Layout.fillWidth: true } Text { text: "详细信息"; color: "#9fb0c1"; font.pixelSize: 14 } Text { text: backend.selectedLog.detail || "-"; color: "#cdd9e5"; font.pixelSize: 13; wrapMode: Text.WordWrap; Layout.fillWidth: true } }
                }
            }
        }
    }

    Component {
        id: settingPage
        RowLayout {
            spacing: 14
            ColumnLayout { Layout.fillWidth: true; Layout.fillHeight: true; spacing: 14
                Panel { Layout.fillWidth: true; Layout.fillHeight: true; title: "系统设置"
                    Flickable { anchors.fill: parent; contentWidth: width; contentHeight: setCol.height; clip: true
                        Column { id: setCol; width: parent.width; spacing: 12
                            Row { width: parent.width; spacing: 12; SettingSection { title: "客户端设置"; groupName: "客户端设置"; width: (parent.width - 12) / 2 } SettingSection { title: "通讯与服务"; groupName: "通讯与服务"; width: (parent.width - 12) / 2 } }
                            Row { width: parent.width; spacing: 12; SettingSection { title: "数据与存储"; groupName: "数据与存储"; width: (parent.width - 12) / 2 } SettingSection { title: "用户与权限"; groupName: "用户与权限"; width: (parent.width - 12) / 2 } }
                            SettingSection { title: "界面与显示"; groupName: "界面与显示"; width: parent.width }
                        }
                    }
                }
                FooterButtons { onSave: backend.saveSettings() }
            }
            RightStatus { systemMode: true }
        }
    }

    component Panel: Rectangle {
        property string title: ""
        default property alias content: body.data
        radius: 8; color: "#14202b"; border.color: "#263847"; border.width: 1
        Column { anchors.fill: parent; anchors.margins: 16; spacing: 12
            Text { visible: title.length > 0; text: title; color: "#eef5ff"; font.pixelSize: 18; font.bold: true }
            Rectangle { visible: title.length > 0; width: parent.width; height: 1; color: "#263847" }
            Item { id: body; width: parent.width; height: parent.height - y }
        }
    }
    component HeaderText: RowLayout { property string label; property string value; property int w: 120; Layout.preferredWidth: w; spacing: 6; Text { text: label + "："; color: "#9fb0c1"; font.pixelSize: 14 } Text { text: value; color: "#dce7f1"; font.pixelSize: 14; elide: Text.ElideRight; Layout.fillWidth: true } }
    component Badge: RowLayout { property string label; property string value; property bool ok: true; property bool blue: false; spacing: 6; Text { text: label + "："; color: "#9fb0c1"; font.pixelSize: 14 } Rectangle { height: 24; width: valueText.width + 18; radius: 4; color: blue ? "#173553" : (ok ? "#153c28" : "#4a2424"); border.color: blue ? "#2386ff" : (ok ? "#217a3b" : "#ff4d4f"); Text { id: valueText; anchors.centerIn: parent; text: value; color: blue ? "#9dccff" : (ok ? "#42d851" : "#ff696b"); font.pixelSize: 13; font.bold: true } } }
    component DotText: RowLayout { property string label; property string value; spacing: 7; Text { text: label + "："; color: "#9fb0c1"; font.pixelSize: 14 } Rectangle { width: 10; height: 10; radius: 5; color: "#42d851" } Text { text: value; color: "#42d851"; font.pixelSize: 13; font.bold: true } }
    component NavButton: Rectangle { property string label; property string icon; property int page; width: 128; height: 96; color: backend.currentPage === page ? "#173553" : "transparent"; Rectangle { visible: backend.currentPage === page; width: 4; anchors.left: parent.left; anchors.top: parent.top; anchors.bottom: parent.bottom; color: "#2386ff" } Column { anchors.centerIn: parent; spacing: 8; Text { text: icon; color: backend.currentPage === page ? "#33a0ff" : "#9aa9b8"; font.pixelSize: 26; anchors.horizontalCenter: parent.horizontalCenter } Text { text: label; color: backend.currentPage === page ? "#33a0ff" : "#c2ccd6"; font.pixelSize: 15; anchors.horizontalCenter: parent.horizontalCenter } } MouseArea { anchors.fill: parent; onClicked: backend.setPage(page) } }
    component ButtonX: Button { property string variant: "normal"; function bg(){ return variant === "success" ? "#238d22" : variant === "danger" ? "#ba2525" : variant === "primary" ? "#156edb" : "#1d2b38" } background: Rectangle { radius: 5; color: parent.down ? Qt.darker(parent.bg(),1.25) : parent.bg(); border.color: Qt.lighter(parent.bg(),1.25) } contentItem: Text { text: parent.text; color: "#f0f6ff"; font.pixelSize: 14; font.bold: parent.variant !== "normal"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter } }
    component FlowBox: Rectangle { property string name; property string icon; property string v1; property string v2; Layout.fillWidth: true; Layout.preferredHeight: 84; radius: 6; color: "#162633"; border.color: "#2a4052"; RowLayout { anchors.fill: parent; anchors.margins: 12; spacing: 12; Text { text: icon; color: "#aebac6"; font.pixelSize: 31; Layout.preferredWidth: 42 } ColumnLayout { spacing: 4; Text { text: name; color: "#f0f6ff"; font.pixelSize: 16; font.bold: true } Text { text: v1; color: "#c5d1dc"; font.pixelSize: 13 } Text { text: v2; color: "#c5d1dc"; font.pixelSize: 13 } } Item { Layout.fillWidth: true } Rectangle { width: 10; height: 10; radius: 5; color: "#42d851" } } }
    component ArrowDown: Text { text: "↓"; color: "#47d13e"; font.pixelSize: 30; Layout.fillWidth: true; Layout.preferredHeight: 34; horizontalAlignment: Text.AlignHCenter }
    component Legend: Row { property color c; property string t; spacing: 6; Rectangle { width: 18; height: 12; color: c; border.color: "#3b5265"; anchors.verticalCenter: parent.verticalCenter } Text { text: t; color: "#9fb0c1"; font.pixelSize: 12 } }
    component PackageBox: Rectangle { width: 54; height: 34; radius: 3; color: "#c9903a"; border.color: "#a66f27"; Rectangle { width: 12; height: 8; color: "#a66f27"; anchors.top: parent.top; anchors.horizontalCenter: parent.horizontalCenter } }
    component InfoInline: RowLayout { property string k; property string v; property bool green: false; spacing: 8; Text { text: k + "："; color: "#94a6b7"; font.pixelSize: 14 } Text { text: v; color: green ? "#42d851" : "#dce7f1"; font.pixelSize: 14; font.bold: green } }
    component Pair: RowLayout { property string k; property string v; Text { text: k; color: "#9fb0c1"; font.pixelSize: 14; Layout.fillWidth: true } Text { text: v; color: "#dce7f1"; font.pixelSize: 14; elide: Text.ElideRight; Layout.maximumWidth: 190 } }
    component Comm: RowLayout { property string k; Text { text: k; color: "#c4cfda"; font.pixelSize: 14; Layout.fillWidth: true } Rectangle { width: 9; height: 9; radius: 4.5; color: "#42d851" } Text { text: "正常"; color: "#42d851"; font.pixelSize: 14; font.bold: true } }
    component Metric: Rectangle { property string title; property string icon; property string a; property string av; property string b; property string bv; property string c; property string cv; Layout.fillWidth: true; Layout.fillHeight: true; radius: 8; color: "#152532"; border.color: "#2a3e4f"; ColumnLayout { anchors.fill: parent; anchors.margins: 14; spacing: 12; RowLayout { Text { text: icon; color: "#99adc2"; font.pixelSize: 22 } Text { text: title; color: "#f0f5fb"; font.pixelSize: 16; font.bold: true } } Rectangle { Layout.fillWidth: true; height: 1; color: "#294052" } Pair { k: a; v: av } Pair { k: b; v: bv } Pair { k: c; v: cv } Rectangle { Layout.fillWidth: true; height: 6; radius: 3; color: "#243543"; Rectangle { width: parent.width * 0.67; height: parent.height; radius: 3; color: "#2e91ff" } } } }
    component TrendCanvas: Canvas { property var points: []; onPaint: { var ctx=getContext('2d'); ctx.reset(); var l=42,t=12,r=10,b=28,w=width-l-r,h=height-t-b; ctx.strokeStyle='#263a4c'; ctx.fillStyle='#7f91a3'; ctx.font='11px sans-serif'; for(var i=0;i<=4;i++){var y=t+h*i/4; ctx.beginPath(); ctx.moveTo(l,y); ctx.lineTo(width-r,y); ctx.stroke(); ctx.fillText(1600-400*i,2,y+4)} if(points.length<2)return; function x(i){return l+w*i/(points.length-1)} function y(v){return t+h*(1-Math.min(1600,Math.max(0,v))/1600)} var keys=['main','supply','manual','cycle']; var cols=['#338cff','#46c85a','#ffb020','#9d6dff']; for(var s=0;s<keys.length;s++){ctx.strokeStyle=cols[s]; ctx.lineWidth=2; ctx.beginPath(); for(var p=0;p<points.length;p++){var xx=x(p), yy=y(points[p][keys[s]]); if(p===0)ctx.moveTo(xx,yy); else ctx.lineTo(xx,yy)} ctx.stroke()} } onPointsChanged: requestPaint() }
    component ParamTab: Rectangle { property string t; property bool selected: false; width: parent.width; height: 52; radius: 4; color: selected ? "#176ed6" : "transparent"; Text { anchors.centerIn: parent; text: t; color: selected ? "white" : "#c4cfda"; font.pixelSize: 15; font.bold: selected } }
    component ParamSection: Rectangle { property string title; property string groupName; width: parent.width; height: grid.height + 64; radius: 8; color: "#14202b"; border.color: "#263847"; Column { anchors.fill: parent; anchors.margins: 14; spacing: 10; Text { text: title; color: "#eef6ff"; font.pixelSize: 17; font.bold: true } Rectangle { width: parent.width; height: 1; color: "#263847" } GridLayout { id: grid; width: parent.width; columns: 2; columnSpacing: 26; rowSpacing: 10; Repeater { model: backend.paramModel; delegate: EditRow { visible: model.group === groupName; Layout.preferredWidth: visible ? (grid.width - 26) / 2 : 0; Layout.preferredHeight: visible ? 36 : 0; label: model.name; val: model.value; unit: model.unit; onEdited: backend.updateParam(index, value) } } } } }
    component SettingSection: Rectangle { property string title; property string groupName; height: grid.height + 64; radius: 8; color: "#14202b"; border.color: "#263847"; Column { anchors.fill: parent; anchors.margins: 14; spacing: 10; Text { text: title; color: "#eef6ff"; font.pixelSize: 17; font.bold: true } Rectangle { width: parent.width; height: 1; color: "#263847" } GridLayout { id: grid; width: parent.width; columns: 1; rowSpacing: 10; Repeater { model: backend.settingModel; delegate: EditRow { visible: model.group === groupName; Layout.preferredWidth: visible ? grid.width : 0; Layout.preferredHeight: visible ? 36 : 0; label: model.name; val: model.value; unit: model.unit; onEdited: backend.updateSetting(index, value) } } } } }
    component EditRow: RowLayout { property string label; property string val; property string unit; signal edited(string value); spacing: 12; Text { text: label; color: "#b4c4d3"; font.pixelSize: 13; Layout.preferredWidth: 160; elide: Text.ElideRight } TextField { text: val; Layout.fillWidth: true; height: 32; color: "#e7f0fa"; background: InputBg{}; onEditingFinished: edited(text) } Text { text: unit; color: "#93a6b9"; font.pixelSize: 13; Layout.preferredWidth: 32 } }
    component InputBg: Rectangle { radius: 4; color: "#101a23"; border.color: "#2a3d4d" }
    component FooterButtons: Rectangle { signal save(); Layout.fillWidth: true; Layout.preferredHeight: 58; radius: 8; color: "#111b24"; border.color: "#263847"; RowLayout { anchors.fill: parent; anchors.rightMargin: 18; Item { Layout.fillWidth: true } ButtonX { text: "重置" } ButtonX { text: "应用"; variant: "primary" } ButtonX { text: "保存"; variant: "success"; onClicked: save() } } }
    component RightStatus: ColumnLayout { property bool systemMode: false; Layout.preferredWidth: 300; Layout.fillHeight: true; spacing: 14; Panel { Layout.fillWidth: true; Layout.preferredHeight: 548; title: "设备拓扑与状态"; ListView { anchors.fill: parent; model: backend.equipmentModel; interactive: false; delegate: Rectangle { width: ListView.view.width; height: 66; color: "transparent"; RowLayout { anchors.fill: parent; Text { text: model.icon; color: "#9aabbc"; font.pixelSize: 26; Layout.preferredWidth: 36 } ColumnLayout { Text { text: model.name; color: "#eef5fb"; font.pixelSize: 14; font.bold: true } Text { text: model.speed.length ? "速度：" + model.speed : "包裹：" + model.count; color: "#bdc9d5"; font.pixelSize: 12 } Text { text: "状态：" + model.state; color: "#bdc9d5"; font.pixelSize: 12 } } Item { Layout.fillWidth: true } Rectangle { width: 9; height: 9; radius: 4.5; color: "#42d851" } } } } } Panel { Layout.fillWidth: true; Layout.fillHeight: true; title: systemMode ? "系统信息" : "关键状态"; ColumnLayout { anchors.fill: parent; spacing: 14; Pair { k: "系统状态"; v: backend.runState } Pair { k: "PLC状态"; v: "在线" } Pair { k: "相机数量"; v: "8 个" } Pair { k: "今日处理量"; v: backend.stats.total.toLocaleString() + " 件" } Pair { k: "累计运行时间"; v: backend.stats.uptime } Pair { k: "CPU使用率"; v: "18%" } } } }
    component FilterBox: ComboBox { property string v; model: [v]; currentIndex: 0; implicitHeight: 36; implicitWidth: 130; contentItem: Text { text: v; color: "#dce7f1"; font.pixelSize: 13; verticalAlignment: Text.AlignVCenter; leftPadding: 10 }; background: InputBg{} }
    component TH: Text { property int w: 80; property bool fill: false; Layout.preferredWidth: fill ? -1 : w; Layout.fillWidth: fill; color: "#b9c8d6"; font.pixelSize: 13; font.bold: true; elide: Text.ElideRight }
    component TD: Text { property int w: 80; property bool fill: false; property color cc: "#cbd7e3"; Layout.preferredWidth: fill ? -1 : w; Layout.fillWidth: fill; color: cc; font.pixelSize: 13; elide: Text.ElideRight; verticalAlignment: Text.AlignVCenter }
    component ExportRow: RowLayout { property string f; property string s; Layout.fillWidth: true; Text { text: "2026-05-09"; color: "#cbd7e3"; font.pixelSize: 13; Layout.preferredWidth: 96 } Text { text: f; color: "#cbd7e3"; font.pixelSize: 13; Layout.fillWidth: true; elide: Text.ElideRight } Text { text: s; color: "#cbd7e3"; font.pixelSize: 13; Layout.preferredWidth: 80 } Text { text: "下载"; color: "#2d91ff"; font.pixelSize: 13; Layout.preferredWidth: 45 } }
    component Donut: Item { Canvas { anchors.left: parent.left; anchors.verticalCenter: parent.verticalCenter; width: 132; height: 132; onPaint: { var ctx=getContext('2d'); ctx.reset(); var vals=[158,322,512,264]; var cols=['#1f8cff','#28c76f','#ffb020','#7c4dff']; var total=1256,start=-Math.PI/2; for(var i=0;i<vals.length;i++){var span=Math.PI*2*vals[i]/total; ctx.beginPath(); ctx.strokeStyle=cols[i]; ctx.lineWidth=18; ctx.arc(66,66,52,start,start+span); ctx.stroke(); start+=span} ctx.beginPath(); ctx.fillStyle='#162431'; ctx.arc(66,66,34,0,Math.PI*2); ctx.fill() } } Text { text: "总数\n1,256"; color: "#eef6ff"; anchors.left: parent.left; anchors.leftMargin: 45; anchors.verticalCenter: parent.verticalCenter; horizontalAlignment: Text.AlignHCenter; font.pixelSize: 16 } Column { anchors.left: parent.left; anchors.leftMargin: 160; anchors.verticalCenter: parent.verticalCenter; spacing: 10; Text { text: "● 系统日志 158"; color: "#1f8cff"; font.pixelSize: 13 } Text { text: "● 操作日志 322"; color: "#28c76f"; font.pixelSize: 13 } Text { text: "● 通讯日志 512"; color: "#ffb020"; font.pixelSize: 13 } Text { text: "● 包裹事件 264"; color: "#7c4dff"; font.pixelSize: 13 } } }
}
