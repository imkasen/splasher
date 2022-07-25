from PySide6.QtCore import QFile, QIODevice, QTextStream
from ..args import PATH
import json
import logging


def create_settings() -> None:
    """
    Create 'settings.json' in the configuration folder.(~/.config/<dir>/settings.json)
    """
    # QJsonObject is missing in PySide 6.3.1, use dict and json to construct directly.
    settings: dict[str, str] = {
        "CACHE": PATH["CACHE"],
        "LOG": PATH["LOG"],
        "PREVIEW": ""
    }

    logger: logging.Logger = logging.getLogger(__name__)
    settings_file: QFile = QFile(PATH["CONFIG"] + "settings.json")
    if not settings_file.exists():
        if settings_file.open(QIODevice.WriteOnly | QIODevice.Text | QIODevice.NewOnly):
            stream: QTextStream = QTextStream(settings_file)
            stream << json.dumps(settings, indent=2)
            logger.info("Create 'settings.json'")
        else:
            logger.error("Fail to open 'settings.json' when trying to create it")
    settings_file.close()