# Single Piece Client

A PyQt6 desktop edge client for single-piece separation stations.

## What this client does

- Write algorithm config files based on stable client settings + algorithm settings
- Receive realtime data from file / TCP / HTTP / Unix socket / ZeroMQ
- Parse algorithm-specific payloads into unified realtime records
- Compute throughput and efficiency metrics
- Display station overview, realtime feed, system health, and logs

## Project structure

```text
src/app/app_context.py                # app composition root
src/app/config/                      # client settings + algorithm settings loaders
src/app/ingest/                      # ingest channel implementations
src/app/parsers/registry.py          # parser registry by parser_type
src/app/services/                    # config write / ingest pipeline / metrics
src/app/ui/main_window.py            # operator-facing industrial UI
profiles/client_settings.json        # stable client settings
profiles/algorithms/*.json           # algorithm-specific settings
```

## macOS run commands

### 1. Install uv

```bash
brew install uv
```

### 2. Enter the project

```bash
cd single_piece_client
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Run the desktop client

```bash
uv run python -m app.main
```

### 5. Or use the helper script

```bash
bash scripts/dev.sh
```

## Test commands

Run all tests:

```bash
uv run pytest
```

Or:

```bash
bash scripts/test.sh
```

## Lint commands

```bash
uv run ruff check .
```

## Build commands

### macOS local debug build

```bash
bash scripts/build_mac.sh
```

### Ubuntu 22.04 Linux build

```bash
bash scripts/build_linux.sh
```

### Build `.deb` on Ubuntu 22.04

```bash
bash scripts/package_deb.sh
```

## Runtime log location

The app uses a rotating file handler and writes logs to the platform app-data directory.
In the UI, you also see operator-facing runtime messages in the Logs / Alerts panel.

Typical macOS log path from Qt app data location will be under your user Library application data directory.

## Configuration files

### Stable client settings

```text
profiles/client_settings.json
```

This file controls:
- selected site/device
- enabled ingest channels
- channel endpoints / file paths
- monitor sampling interval

### Algorithm settings

```text
profiles/algorithms/default_algorithm.json
```

This file controls:
- algorithm type / algorithm name
- parser type
- config output dir
- algorithm-specific fields like threshold / speed

## Main data path

```text
Channel -> RawMessage -> ParserRegistry -> RealtimeRecord -> Metrics -> UI
```

When debugging, always follow this order.

## Integration examples

### 1. UI-only smoke test

Use the button:
- `Inject Sample Event`

This verifies:
- ingest callback binding
- parser registry
- realtime table update
- metrics update

### 2. File ingest example

Make sure file channel is enabled in `profiles/client_settings.json`, then append a JSONL line to the watched directory:

```bash
mkdir -p runtime/hz_demo/spc_01/realtime
printf '{"timestamp":"2026-04-15T12:00:00","item_id":"file-001","device_id":"spc_01","result":"success","process_time_ms":35}\n' >> runtime/hz_demo/spc_01/realtime/events.jsonl
```

Expected result:
- file channel log appears
- realtime table gets a new row
- throughput / efficiency updates

### 3. TCP ingest example (macOS)

With TCP enabled on `127.0.0.1:9101`:

```bash
printf '{"timestamp":"2026-04-15T12:01:00","item_id":"tcp-001","device_id":"spc_01","result":"success","process_time_ms":28}\n' | nc 127.0.0.1 9101
```

Expected result:
- TCP channel receives payload
- parser runs
- UI updates

### 4. HTTP ingest example (macOS)

With HTTP enabled on `127.0.0.1:9102/events`:

```bash
curl -X POST http://127.0.0.1:9102/events \
  -H 'Content-Type: application/json' \
  -d '{"timestamp":"2026-04-15T12:02:00","item_id":"http-001","device_id":"spc_01","result":"success","process_time_ms":31}'
```

Expected result:
- HTTP 200 OK
- UI gets one realtime row

### 5. Unix socket ingest example (Linux / Ubuntu)

```bash
printf '{"timestamp":"2026-04-15T12:03:00","item_id":"unix-001","device_id":"spc_01","result":"success","process_time_ms":22}' | socat - UNIX-CONNECT:/tmp/single_piece_algo.sock
```

### 6. ZeroMQ ingest example

Example sender in Python:

```python
import zmq
ctx = zmq.Context.instance()
sock = ctx.socket(zmq.PUSH)
sock.connect('tcp://127.0.0.1:5555')
sock.send_string('{"timestamp":"2026-04-15T12:04:00","item_id":"zmq-001","device_id":"spc_01","result":"success","process_time_ms":26}')
```

## Troubleshooting handbook

### Problem: the UI starts but no realtime data appears

Check in this order:
1. Is the correct channel enabled in `profiles/client_settings.json`?
2. Did the channel start successfully in logs?
3. Did the channel receive payload bytes/text?
4. Did the parser run with the expected `parser_type`?
5. Did the parser produce any `RealtimeRecord` objects?
6. Did metrics update?
7. Did the UI receive records?

### Problem: config write fails

Check:
1. `config_output_dir` exists or can be created
2. the current user has write permission
3. algorithm settings JSON is valid
4. override values in the UI are numeric where expected

### Problem: file channel does not react

Check:
1. `watch_mode` is correct
2. `path` points to the right file or directory
3. `file_pattern` matches the actual file name
4. the file actually changed after the client started
5. logs show `Read X chars from file ...`

### Problem: TCP channel does not receive messages

Check:
1. `host` and `port` match the sender
2. nothing else is occupying the port
3. your sender ends the payload with newline when using `line` mode
4. logs show `TCP payload received length=...`

### Problem: HTTP channel returns 404

Check:
1. the endpoint matches exactly, for example `/events`
2. request uses POST
3. host and port match the client settings

### Problem: Unix socket channel fails on macOS or Windows

Unix socket support is primarily for Linux/Ubuntu deployment.
Use TCP or HTTP for macOS local development unless you specifically need Unix sockets.

### Problem: ZeroMQ receives nothing

Check:
1. endpoint string is correct
2. sender/receiver modes match (`PUSH/PULL` or `PUB/SUB`)
3. topic is correct for `SUB` mode
4. no other process already bound the endpoint

## Suggested debug reading order

```text
1. src/app/app_context.py
2. src/app/config/config_loader.py
3. src/app/ingest/channel_manager.py
4. src/app/ingest/<channel>.py
5. src/app/services/ingest_pipeline_service.py
6. src/app/parsers/registry.py
7. src/app/ui/main_window.py
```
