# Single Piece Client

A PyQt6 desktop edge client for single-piece separation stations.

## Current architecture

- Stable **client settings** for app/runtime/ingest/monitor behavior
- Variable **algorithm settings** for algorithm-specific fields and render rules
- Multi-channel ingest skeleton: file / tcp / http / unix socket / zeromq
- Parser registry that turns raw messages into unified realtime records
- Metrics service for throughput and efficiency
- Desktop UI for config preview/write, realtime data, system monitoring, and metrics

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

## Lint

```bash
uv run ruff check .
```

## Package on Ubuntu 22.04

```bash
bash scripts/build_linux.sh
bash scripts/package_deb.sh
```

## Deploy `.deb`

```bash
sudo dpkg -i dist-deb/single-piece-client_0.2.0_amd64.deb
```
