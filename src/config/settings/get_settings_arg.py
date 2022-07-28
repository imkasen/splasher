from PySide6.QtCore import QFile, QIODevice, QTextStream
from ..args import PATH
import logging
import json


def get_settings_arg(arg_key: str) -> (bool, str):
    """
    Get the configuration in the settings based on the input string.
    :param arg_key: configuration key
    :return tuple: (bool, configuration value)
    """
    logger: logging.Logger = logging.getLogger(__name__)
    res: tuple = (False, "")
    settings_file: QFile = QFile(PATH["CONFIG"] + "settings.json")
    if settings_file.exists():
        if settings_file.open(QIODevice.ReadOnly | QIODevice.Text | QIODevice.ExistingOnly):
            stream: QTextStream = QTextStream(settings_file)
            val: str = json.loads(stream.readAll()).get(arg_key, "")
            if val:
                res = (True, val)
            else:
                logger.error("Fail to get the argument because the key is not existed")
        else:
            logger.error("Fail to open 'settings.json' when trying to read an argument")
    else:
        logger.error("'settings.json' is not existed when trying to read an argument")
    settings_file.close()
    return res
