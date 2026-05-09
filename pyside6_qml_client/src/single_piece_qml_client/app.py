from __future__ import annotations

import logging
import os
import sys

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from single_piece_qml_client.controllers.application_controller import ApplicationController
from single_piece_qml_client.core.app_config import ConfigLoadError, load_config
from single_piece_qml_client.core.database import Database, migrate
from single_piece_qml_client.core.logging_config import configure_logging
from single_piece_qml_client.core.paths import resolve_paths
from single_piece_qml_client.services.log_service import LogService
from single_piece_qml_client.services.state_service import StateService

logger = logging.getLogger(__name__)


def run() -> int:
    """Production entrypoint with explicit startup phases."""

    paths = resolve_paths()
    configure_logging(paths.log_dir)

    try:
        config = load_config(paths.config_dir)
    except ConfigLoadError:
        logger.exception("Failed to load production configuration")
        return 2

    logger.info("Starting %s profile=%s db=%s", config.ui.title, config.profile, paths.database_path)

    try:
        database = Database(paths.database_path, config.storage)
        with database.session() as conn:
            migrate(conn)
    except Exception:
        logger.exception("Database migration failed")
        return 3

    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
    os.environ["SPC_CLIENT_DB"] = str(paths.database_path)

    app = QGuiApplication(sys.argv)
    log_service = LogService(database, config.storage)
    state_service = StateService(database)
    backend = ApplicationController(config, log_service, state_service)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("backend", backend)
    engine.load(QUrl.fromLocalFile(str(paths.qml_main)))

    if not engine.rootObjects():
        logger.error("QML root object creation failed: %s", paths.qml_main)
        return 4

    exit_code = app.exec()
    logger.info("Application exited code=%s", exit_code)
    return exit_code
