# 工业生产环境改造说明

该目录已从 UI 原型调整为可继续工程化落地的工业现场客户端骨架。当前目标不是只做界面，而是形成现场可部署、可追踪、可恢复、可维护的桌面边缘客户端结构。

## 改造原则

1. **启动链路可控**：生产入口统一进入 `single_piece_qml_client.app:run`，启动时先解析路径、加载配置、初始化日志、执行 SQLite migration，再加载 QML。
2. **配置外置**：现场差异化配置放在 `config/app.production.json`，代码不再依赖硬编码作为唯一配置来源。
3. **运行数据隔离**：数据库、日志、临时运行文件默认进入 `runtime/`，也支持环境变量覆盖，适合现场不同设备目录策略。
4. **SQLite 工业边缘化使用**：启用 WAL、busy timeout、foreign key、基础索引，避免简单 demo 级 SQLite 用法。
5. **日志可追踪**：使用 rotating file handler，生产日志落盘到 `runtime/logs/single_piece_qml_client.log`。
6. **可测试**：新增配置加载测试，后续 PLC、相机、参数下发、日志导出都应按服务层拆分并补充单元测试。

## 关键目录

```text
pyside6_qml_client/
├── config/
│   └── app.production.json        # 生产配置模板
├── runtime/                       # 本地运行数据，部署时可独立挂载或排除 Git
├── scripts/
│   └── run.sh                     # 生产启动脚本
├── src/single_piece_qml_client/
│   ├── app.py                     # 生产启动入口
│   ├── main.py                    # 当前 UI 后端与开发入口
│   ├── core/
│   │   ├── app_config.py          # 配置加载与合并
│   │   ├── database.py            # SQLite 连接与 migration
│   │   ├── logging_config.py      # 生产日志
│   │   └── paths.py               # 路径解析与环境变量覆盖
│   └── models.py                  # QML ListModel 基础模型
├── tests/
│   └── test_app_config.py
└── qml/
    └── Main.qml
```

## 环境变量

| 变量 | 作用 | 默认值 |
|---|---|---|
| `SPC_CLIENT_RUNTIME_DIR` | 运行目录 | `pyside6_qml_client/runtime` |
| `SPC_CLIENT_CONFIG_DIR` | 配置目录 | `pyside6_qml_client/config` |
| `SPC_CLIENT_LOG_DIR` | 日志目录 | `runtime/logs` |
| `SPC_CLIENT_DB` | SQLite 数据库路径 | `runtime/single_piece_client.db` |
| `SPC_CLIENT_QML_MAIN` | QML 主文件路径 | `qml/Main.qml` |

## 生产运行

```bash
cd pyside6_qml_client
uv sync
bash scripts/run.sh
```

或：

```bash
uv run single-piece-qml-client
```

开发入口保留：

```bash
uv run single-piece-qml-client-dev
```

## 质量检查

```bash
uv run ruff check .
uv run pytest
```

## 后续生产化优先级

1. 将 `main.py` 中的 UI 后端继续拆分为 `ApplicationController`、`RealtimeService`、`ParameterService`、`LogService`。
2. 将 QML 单文件拆分为 `components/`、`pages/`、`styles/`，并建立统一主题 token。
3. 引入 PLC / 相机 / 光电 / 电柜的接口层，接口层与 QML 完全隔离。
4. 参数下发增加二次确认、操作审计、失败回滚和版本记录。
5. 增加 `.deb` 打包、systemd 用户服务、桌面快捷方式和开机自启动策略。
6. 增加现场诊断包导出：配置、日志、数据库摘要、版本信息、设备状态快照。
