#!/usr/bin/env bash
set -euo pipefail
uv sync
uv run pyinstaller packaging/pyinstaller_linux.spec --noconfirm
