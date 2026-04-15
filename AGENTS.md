# AGENTS

## Product goal
This repository contains a PyQt6 edge desktop client for single-piece separation stations.

## Development rules
- Keep UI logic inside `src/app/ui`
- Keep filesystem monitoring and OS integration inside `src/app/adapters`
- Keep business rules inside `src/app/services`
- New site-specific behavior should be profile-driven, not hard-coded with `if site == ...`
- Tests must be added for parser, metrics, and config rendering changes

## Packaging
- macOS is for development and GUI debugging
- Ubuntu 22.04 is the target packaging platform for Linux and `.deb`
