import json  # QJsonObject is missing in PySide 6.3.1, use dict and json to construct directly.
import logging
from PySide6.QtCore import QFile, QIODevice, QTextStream
from ..args import PATH
from . import lock


def create_settings() -> None:
    """
    Create 'settings.json' in the configuration folder.(~/.config/<dir>/settings.json)
    """
    settings: dict[str, str] = {"PREVIEW": ""}

    logger: logging.Logger = logging.getLogger(__name__)
    settings_file: QFile = QFile(PATH["CONFIG"] + "settings.json")
    if not settings_file.exists():
        lock.lockForWrite()
        if settings_file.open(QIODevice.WriteOnly | QIODevice.Text | QIODevice.NewOnly):
            stream: QTextStream = QTextStream(settings_file)
            stream << json.dumps(settings, indent=2)  # pylint: disable=expression-not-assigned
            logger.info("Create 'settings.json'")
        else:
            logger.error("Failed to open 'settings.json' when trying to create it")
        settings_file.close()
        lock.unlock()
