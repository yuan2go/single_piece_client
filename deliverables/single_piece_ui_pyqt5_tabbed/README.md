# single_piece_ui_pyqt5_tabbed

PyQt5 工业化 UI 示例工程，基于“单件分离高速分拣系统”设计稿整理。

## 内容

- 实时监控页
- 参数配置页（左侧分区导航 + 每类参数一个独立 tab 页）
- 独立 QSS 样式文件
- 公共组件与流程组件

## 运行方式

```bash
pip install -r requirements.txt
python main.py
```

## 目录结构

```text
single_piece_ui_pyqt5_tabbed/
├─ main.py
├─ requirements.txt
└─ app/
   ├─ main_window.py
   ├─ styles.qss
   ├─ pages/
   │  ├─ monitor_page.py
   │  └─ config_page.py
   └─ widgets/
      ├─ common.py
      └─ flow_widgets.py
```

## 说明

- 参数配置页已调整为左侧分区式 tab 导航。
- 每种参数对应一个独立页面。
- 页面风格按当前工业化暗色版本整理。
