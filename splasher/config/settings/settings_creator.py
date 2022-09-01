import json  # QJsonObject is missing in PySide 6.3.1, use dict and json to construct directly.
import logging
import sys

from PySide6.QtCore import QFile, QIODevice, QTextStream

from ..args import PATH, SETTINGS
from . import lock


def create_settings() -> None:
    """
    Create 'settings.json' in the configuration folder.(~/.config/splasher/settings.json)
    """
    logger: logging.Logger = logging.getLogger(__name__)
    file_path: str = f"{PATH['CONFIG']}settings.json"
    settings_file: QFile = QFile(file_path)
    if not settings_file.exists():
        lock.lockForWrite()
        try:
            if settings_file.open(QIODevice.WriteOnly | QIODevice.Text | QIODevice.NewOnly):
                stream: QTextStream = QTextStream(settings_file)
                stream << json.dumps(SETTINGS, indent=2)  # pylint: disable=expression-not-assigned
                logger.info("Create '%s'", file_path)
            else:
                raise IOError
        except IOError:
            logger.error("Failed to open '%s'", file_path)
            sys.exit(f"Fail to open {file_path} when trying to create it")
        finally:
            settings_file.close()
            lock.unlock()
