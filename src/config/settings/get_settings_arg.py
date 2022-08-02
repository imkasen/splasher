from PySide6.QtCore import QFile, QIODevice, QTextStream
from ..args import PATH
import logging
import json
from typing import Any


def get_settings_arg(arg_key: str) -> tuple[bool, str]:
    """
    Get the configuration in the settings based on the input string.
    :param arg_key: configuration key
    :return tuple: (bool, configuration value)
    """
    logger: logging.Logger = logging.getLogger(__name__)
    res: tuple[bool, str] = (False, "")
    settings_file: QFile = QFile(PATH["CONFIG"] + "settings.json")
    if settings_file.exists():
        if settings_file.open(QIODevice.ReadOnly | QIODevice.Text | QIODevice.ExistingOnly):
            stream: QTextStream = QTextStream(settings_file)
            settings_dict: Any = json.loads(stream.readAll())
            if arg_key in settings_dict:
                res: tuple[bool, str] = (True, settings_dict[arg_key])
            else:
                logger.error("Failed to get the argument because the key is not existed")
        else:
            logger.error("Failed to open 'settings.json' when trying to read an argument")
        settings_file.close()
    else:
        logger.error("'settings.json' is not existed when trying to read an argument")
    return res
