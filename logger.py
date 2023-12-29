import os
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    NOTSET,
    WARNING,
    Formatter,
    LogRecord,
    StreamHandler,
    getLogger,
)
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from common import settings

LEVELS = Literal['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


class DefaultLoggerSettings(BaseModel):
    """Дефолтные настройки логгера."""

    TO_FILE: bool = False
    TO_CONSOLE: bool = True
    LEVEL_DEV: LEVELS = 'INFO'
    LEVEL_PROD: LEVELS = 'ERROR'
    LOG_FILENAME: str = 'app.log'
    SAVE_PATH: Path = 'logs'
    MAX_FILE_SIZE: int = 1024 * 10  # 10 KB
    BACKUP_COUNT: int = 10
    FORMAT: str = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s'


COLOR = {
    NOTSET: '\x1b[38;20m',
    DEBUG: '\x1b[38;20m',
    INFO: '\x1b[38;20m',
    WARNING: '\x1b[33;20m',
    ERROR: '\x1b[31;20m',
    CRITICAL: '\x1b[31;1m',
    'RESET': '\x1b[0m',
}

# define in .env or in common.settings
DEBUG = os.environ.get('DEBUG') or getattr(settings, 'DEBUG', None) or True


class CustomFormatter(Formatter):
    def __init__(self, fmt: str):
        super().__init__()
        self.fmt = fmt

    def format(self, record: LogRecord) -> str:
        colored_fmt = COLOR.get(record.levelno) + self.fmt + COLOR.get('RESET')
        formatter = Formatter(colored_fmt)
        return formatter.format(record)


def make_logger():
    _logger = getLogger(__name__)
    _logger.propagate = False
    level = logger_settings.LEVEL_DEV if DEBUG else logger_settings.LEVEL_PROD
    _logger.setLevel(level)
    if logger_settings.TO_FILE:
        if not os.path.exists(logger_settings.SAVE_PATH):
            os.makedirs(logger_settings.SAVE_PATH)
        rotating_handler = RotatingFileHandler(
            os.path.join(logger_settings.SAVE_PATH, logger_settings.LOG_FILENAME),
            backupCount=logger_settings.BACKUP_COUNT,
            maxBytes=logger_settings.MAX_FILE_SIZE,
        )
        _logger.addHandler(rotating_handler)
    if logger_settings.TO_CONSOLE:
        _logger.addHandler(StreamHandler())
    for handler in _logger.handlers:
        formatter = (
            CustomFormatter(logger_settings.FORMAT)
            if isinstance(handler, StreamHandler)
            else Formatter(logger_settings.FORMAT)
        )
        handler.setFormatter(formatter)
        handler.setLevel(level)
    return _logger


logger_settings = DefaultLoggerSettings()
if LoggerSettings := getattr(settings, 'LoggerSettings', None):
    logger_settings = DefaultLoggerSettings().model_dump()
    logger_settings.update(**LoggerSettings().dict())  # pylint: disable=not-callable
    logger_settings = DefaultLoggerSettings(**logger_settings)

# simply import this instance
logger = make_logger()
