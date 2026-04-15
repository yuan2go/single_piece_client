#!/usr/bin/env bash
set -euo pipefail
APP_NAME="single-piece-client"
VERSION="0.3.0"
ARCH="amd64"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist/$APP_NAME"
PKG_DIR="$ROOT_DIR/dist-deb/${APP_NAME}_${VERSION}_${ARCH}"
rm -rf "$PKG_DIR"
mkdir -p "$PKG_DIR/DEBIAN" "$PKG_DIR/opt/$APP_NAME" "$PKG_DIR/usr/share/applications" "$PKG_DIR/usr/share/icons/hicolor/scalable/apps"
cp -r "$DIST_DIR"/* "$PKG_DIR/opt/$APP_NAME/"
cp "$ROOT_DIR/packaging/${APP_NAME}.desktop" "$PKG_DIR/usr/share/applications/"
cp "$ROOT_DIR/packaging/${APP_NAME}.svg" "$PKG_DIR/usr/share/icons/hicolor/scalable/apps/"
cat > "$PKG_DIR/DEBIAN/control" <<EOF
Package: $APP_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: yuan2go
Description: Single piece separation desktop edge client
EOF
dpkg-deb --build "$PKG_DIR"
