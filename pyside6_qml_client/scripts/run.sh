#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uv run python -c 'from single_piece_qml_client.app import run; raise SystemExit(run())'
