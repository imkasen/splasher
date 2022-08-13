import json
import logging
from typing import Any

from PySide6.QtCore import QFile, QIODevice, QTextStream

from ..args import PATH
from . import lock


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
        lock.lockForRead()
        if settings_file.open(QIODevice.ReadOnly | QIODevice.Text | QIODevice.ExistingOnly):
            stream: QTextStream = QTextStream(settings_file)
            settings_dict: Any = json.loads(stream.readAll())
            try:
                res: tuple[bool, str] = (True, settings_dict[arg_key])
            except KeyError:
                logger.error("Key: %s does not exist in 'settings.json'", arg_key)
        else:
            logger.error("Failed to open 'settings.json'")
        settings_file.close()
        lock.unlock()
    else:
        logger.error("'settings.json' is not existed")
    return res
