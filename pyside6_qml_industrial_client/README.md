# PySide6 QML Industrial Client

Industrial desktop UI prototype for the single-piece separation control system.

This directory is a new PySide6 + QML implementation of the reconstructed industrial desktop UI. It keeps the current business focus: realtime monitoring, belt-speed matrix, package overlay, alarms, device diagnosis, parameter configuration, logs, and system settings.

## Requirements

- Python 3.12
- uv
- Ubuntu / Linux desktop environment with Qt runtime support

## Run

```bash
cd pyside6_qml_industrial_client
uv sync
uv run python -m single_piece_qml_client.main
```

Or run the console script after `uv sync`:

```bash
uv run single-piece-qml-client
```

## Structure

```text
pyside6_qml_industrial_client/
├── pyproject.toml
├── README.md
└── src/single_piece_qml_client/
    ├── __init__.py
    ├── backend.py
    ├── main.py
    └── qml/
        ├── Main.qml
        ├── components/
        │   ├── BeltMatrixView.qml
        │   ├── BottomEventPanel.qml
        │   ├── DeviceFlowView.qml
        │   ├── DeviceSegment.qml
        │   ├── FlowArrow.qml
        │   ├── IndustrialButton.qml
        │   ├── KpiCard.qml
        │   ├── RightStatusPanel.qml
        │   ├── SectionCard.qml
        │   ├── SideNavigation.qml
        │   ├── StatusBadge.qml
        │   ├── StatusDot.qml
        │   └── TopStatusBar.qml
        └── pages/
            ├── AlarmCenterPage.qml
            ├── DeviceDiagnosisPage.qml
            ├── LogRecordPage.qml
            ├── ParameterConfigPage.qml
            ├── RealtimeMonitorPage.qml
            └── SystemSettingsPage.qml
```

## Implemented UI modules

- Global top status bar
- Left industrial navigation
- Realtime monitor page
- Device flow view
- 4 × 4 belt-speed matrix
- Package overlay on top of the belt-speed matrix
- Right KPI / operation / alarm panel
- Bottom event log panel
- Alarm center page
- Device diagnosis page
- Parameter configuration page
- Log record page
- System settings page

## Current data source

`backend.py` provides mock data through Qt properties:

- `runtime`
- `beltCells`
- `packages`
- `kpis`
- `alarms`
- `events`

Later, real PLC / Modbus / camera / algorithm / log services can update the same properties or replace `DemoBackend` with production models.
