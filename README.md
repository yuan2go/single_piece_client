# Single Piece Client

A PyQt6 desktop edge client for single-piece separation stations.

## Commercial-oriented UI layout

- **Station Overview** header with site, device, algorithm, enabled channels, processed count, throughput, efficiency, and client status
- **Algorithm Configuration** panel for previewing and writing algorithm config files
- **Realtime Feed** table for live records
- **System Health** panel for CPU / memory / disk
- **KPI & Throughput** panel for production metrics
- **Logs / Alerts** panel for operator-facing visibility

## Data channels

- File watch via watchdog
- Local TCP server
- Local HTTP server
- Unix domain socket server
- ZeroMQ socket receiver

## Main ingest path

`Channel -> RawMessage -> ParserRegistry -> RealtimeRecord -> Metrics/UI`

## Quick start on macOS

```bash
brew install uv
cd single_piece_client
uv sync
uv run python -m app.main
```

## Test

```bash
uv run pytest
```

## Package on Ubuntu 22.04

```bash
bash scripts/build_linux.sh
bash scripts/package_deb.sh
```

## Deploy `.deb`

```bash
sudo dpkg -i dist-deb/single-piece-client_0.3.0_amd64.deb
```
