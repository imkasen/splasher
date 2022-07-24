from PySide6.QtCore import QFile, QIODevice, QTextStream
from ..args import PATH
import json
import logging


def create_settings() -> None:
    """
    Create 'settings.json' in the configuration folder.(~/.config/<dir>/settings.json)
    :return:
    """
    settings: dict[str, str] = {
        "CACHE": PATH["CACHE"],
        "CONFIG": PATH["CONFIG"],
        "LOG": PATH["LOG"],
        "PREVIEW_IMAGE": ""
    }

    settings_file: QFile = QFile(PATH["CONFIG"] + "settings.json")
    if not settings_file.exists():
        if settings_file.open(QIODevice.WriteOnly | QIODevice.Text | QIODevice.NewOnly):
            stream: QTextStream = QTextStream(settings_file)
            stream << json.dumps(settings, indent=2)
        else:
            logging.getLogger(__name__).error("Fail to write 'settings.json'")
    settings_file.close()
