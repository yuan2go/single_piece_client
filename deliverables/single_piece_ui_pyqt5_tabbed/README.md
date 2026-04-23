# single_piece_ui_pyqt5_tabbed

PyQt5 工业化 UI 示例工程，基于“单件分离高速分拣系统”设计稿整理。

## 内容

- 实时监控页
- 参数配置页（左侧分区导航 + 每类参数一个独立 tab 页）
- 独立 QSS 样式文件
- 公共组件与流程组件
- 使用 uv 管理依赖
- 附带 VS Code 调试配置，可直接启动调试

## 环境要求

- Python 3.12
- uv

## 安装与运行

```bash
cd deliverables/single_piece_ui_pyqt5_tabbed
uv sync
uv run python main.py
```

## 直接调试

如果你在 VS Code 中打开仓库根目录，可以直接使用仓库内的 `.vscode/launch.json` 启动：

- `Single Piece UI (uv)`

该配置会以项目目录为工作目录启动主程序，适合直接调试页面布局和交互。

## 目录结构

```text
single_piece_ui_pyqt5_tabbed/
├─ .vscode/
│  └─ launch.json
├─ main.py
├─ pyproject.toml
├─ .python-version
├─ .gitignore
└─ app/
   ├─ __init__.py
   ├─ main_window.py
   ├─ styles.qss
   ├─ pages/
   │  ├─ __init__.py
   │  ├─ monitor_page.py
   │  └─ config_page.py
   └─ widgets/
      ├─ __init__.py
      ├─ common.py
      └─ flow_widgets.py
```

## 说明

- 参数配置页已调整为左侧分区式 tab 导航。
- 每种参数对应一个独立页面。
- 页面风格按当前工业化暗色版本整理。
- 主程序通过相对脚本路径加载 QSS，因此从项目目录或调试器启动都可正常运行。
