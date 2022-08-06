from typing import Optional, Any
import logging
import json
from PySide6.QtCore import QFile, QIODevice, QTextStream
from ..args import PATH
from . import lock

logger: logging.Logger = logging.getLogger(__name__)


def set_settings_arg(arg_key: str, arg_value: str) -> bool:
    """
    Modify the configuration value in the settings based on the input key.
    :param arg_key: the configuration key that needs to be updated
    :param arg_value: the configuration value for update
    :return: bool
    """
    res: bool = False
    file: QFile = QFile(PATH["CONFIG"] + "settings.json")
    if file.exists():
        res, settings_dict = read_settings(file)
        if res and arg_key in settings_dict:
            settings_dict[arg_key] = arg_value
            res: bool = write_settings(file, settings_dict)
        else:
            logger.error("Key: %s does not exist in 'settings.json'", arg_key)
    else:
        logger.error("'settings.json' is not existed when trying to set an argument")
    return res


def read_settings(settings_file: QFile) -> tuple[bool, Optional[dict]]:
    """
    Read json from 'settings.json' and return it as dictionary.
    :param settings_file: QFile
    :return tuple: (bool, dictionary | None)
    """
    tup_res: tuple[bool, Optional[dict]] = (False, None)
    lock.lockForRead()
    if settings_file.open(QIODevice.ReadOnly | QIODevice.Text | QIODevice.ExistingOnly):
        stream: QTextStream = QTextStream(settings_file)
        settings_dict: Any = json.loads(stream.readAll())
        if settings_dict:
            tup_res: tuple[bool, dict] = (True, settings_dict)
        else:
            logger.warning("'settings.json' is empty")
    else:
        logger.error("Failed to open 'settings.json' when trying to set an argument")
    settings_file.close()
    lock.unlock()
    return tup_res


def write_settings(settings_file: QFile, settings_dict: dict) -> bool:
    """
    Write json back to 'settings.json'
    :param settings_file: QFile
    :param settings_dict: json dictionary
    :return: bool
    """
    res: bool = False
    lock.lockForWrite()
    if settings_file.open(QIODevice.WriteOnly | QIODevice.Text | QIODevice.ExistingOnly):
        stream: QTextStream = QTextStream(settings_file)
        stream << json.dumps(settings_dict, indent=2)  # pylint: disable=expression-not-assigned
        res: bool = True
    settings_file.close()
    lock.unlock()
    return res
