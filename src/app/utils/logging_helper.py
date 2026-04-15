from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from app.utils.paths import app_log_dir


def configure_logging() -> None:
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        app_log_dir() / 'single_piece_client.log',
        maxBytes=2_000_000,
        backupCount=3,
        encoding='utf-8',
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root.addHandler(console)
    root.addHandler(file_handler)
    logging.getLogger(__name__).info('Logging configured. file_dir=%s', app_log_dir())
