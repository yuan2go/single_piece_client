# Single Piece Client

A PyQt6 desktop edge client for single-piece separation stations.

## Features

- Fill in station and algorithm settings, then render and write config files to a target directory
- Watch algorithm output files and show real-time records in the desktop client
- Monitor CPU, memory, disk, and key process-level OS health
- Compute throughput and efficiency metrics from event streams
- Support multi-site and multi-device profiles through profile-driven configuration

## Architecture

- `ui/`: desktop pages and dialogs
- `services/`: business workflows
- `adapters/`: filesystem watch, parsers, and OS integration
- `domain/`: typed models
- `profiles/`: site and device specific templates

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
sudo dpkg -i dist-deb/single-piece-client_0.1.0_amd64.deb
```
