from __future__ import annotations

import logging
import sys
import traceback

from PyQt6.QtWidgets import QMessageBox


class ExceptionHandler:
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def install(self) -> None:
        sys.excepthook = self.handle_exception

    def handle_exception(self, exc_type, exc_value, exc_tb) -> None:
        text = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        self._logger.exception('Unhandled exception: %s', text)
        QMessageBox.critical(None, 'Unhandled Error', text)
