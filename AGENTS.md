# AGENTS

## Product goal
This repository contains a PyQt6 edge desktop client for single-piece separation stations.

## Key architecture rules
- Separate stable client settings from algorithm-specific settings.
- Keep ingest channels decoupled from parsers.
- New algorithms should be added by registering parser types, not by editing UI logic.
- New site behavior should be configuration-driven.
- The main ingest path is: Channel -> RawMessage -> ParserRegistry -> RealtimeRecord -> Metrics/UI.
