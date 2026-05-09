# PySide6 + QML 工业桌面客户端原型

该目录是基于 UI 设计稿转换的独立实现，定位为 `single_piece_client` 仓库内的新一代 QML 桌面客户端原型。

## 技术栈

- Python 3.12
- uv 项目管理
- PySide6 + Qt Quick / QML
- SQLite，本地运行数据、日志、配置持久化

## 页面范围

已按设计稿实现 4 个核心页面：

1. **实时监控**
   - 顶部全局状态栏
   - 左侧导航
   - 单件分离设备流程抽象
   - 4×4 分离矩阵，展示皮带速度与跨皮带包裹
   - 开始 / 停止操作控制
   - 设备信息、通信状态、分离数据总览、趋势概览

2. **参数配置**
   - 左侧参数分组
   - 分离机与准入配置
   - 速度与阈值配置
   - 算法与相机参数
   - 显示与保存配置
   - 右侧设备拓扑与关键状态

3. **日志记录**
   - 时间范围、日志类型、来源模块、级别、关键字过滤区
   - 日志表格
   - 日志统计环图
   - 存储状态
   - 当前选中日志详情

4. **系统设置**
   - 客户端设置
   - 通讯与服务
   - 数据与存储
   - 用户与权限
   - 界面与显示
   - 右侧设备拓扑与系统信息

## 目录结构

```text
pyside6_qml_client/
├── pyproject.toml
├── .python-version
├── README.md
├── scripts/run.sh
├── src/single_piece_qml_client/
│   ├── main.py
│   ├── backend.py
│   ├── database.py
│   └── models.py
└── qml/
    ├── Main.qml
    ├── components/
    └── pages/
```

## 本地运行

```bash
cd pyside6_qml_client
uv sync
uv run python -m single_piece_qml_client.main
```

也可以使用脚本：

```bash
bash scripts/run.sh
```

## SQLite 数据库

默认数据库路径：

```text
pyside6_qml_client/runtime/single_piece_client.db
```

可通过环境变量覆盖：

```bash
SPC_CLIENT_DB=/path/to/single_piece_client.db uv run python -m single_piece_qml_client.main
```

数据库当前用于：

- 初始化设备运行状态
- 初始化日志记录
- 保存参数配置
- 保存系统设置

## 后续可接入的真实模块

当前实现为可运行的前端与本地模拟后端骨架，便于快速评审 UI 与交互。后续建议接入：

- PLC 通讯服务
- 相机 / 光电 / 电柜状态采集
- 包裹位置实时数据源
- 参数下发服务
- 日志导出与审计
- `.deb` 打包流水线
