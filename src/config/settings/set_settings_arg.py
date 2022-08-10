from typing import Optional, Any
import logging
import json
from PySide6.QtCore import QFile, QSaveFile, QIODevice, QTextStream
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
    file_path = PATH["CONFIG"] + "settings.json"
    res, settings_dict = read_settings(file_path)
    if res:
        try:
            settings_dict[arg_key] = arg_value
            res: bool = write_settings(file_path, settings_dict)
        except KeyError:
            logger.error("Key: %s does not exist in 'settings.json'", arg_key)
    return res


def read_settings(path: str) -> tuple[bool, Optional[dict]]:
    """
    Read json from 'settings.json' and return it as dictionary.
    :param path: file path of 'settings.json'
    :return tuple: (bool, dictionary | None)
    """
    tup_res: tuple[bool, Optional[dict]] = (False, None)
    lock.lockForRead()
    file: QFile = QFile(path)
    if file.exists():
        if file.open(QIODevice.ReadOnly | QIODevice.Text | QIODevice.ExistingOnly):
            stream: QTextStream = QTextStream(file)
            settings_dict: Any = json.loads(stream.readAll())
            if settings_dict:
                tup_res: tuple[bool, dict] = (True, settings_dict)
            else:
                logger.warning("'settings.json' is empty")
        else:
            logger.error("Failed to open 'settings.json'")
    else:
        logger.error("'settings.json' is not existed")
    file.close()
    lock.unlock()
    return tup_res


def write_settings(path: str, settings_dict: dict) -> bool:
    """
    Write json back to 'settings.json'
    :param path: file path of 'settings.json'
    :param settings_dict: json dictionary
    :return: bool
    """
    res: bool = False
    lock.lockForWrite()
    file: QSaveFile = QSaveFile(path)
    if file.open(QIODevice.WriteOnly | QIODevice.Text):
        stream: QTextStream = QTextStream(file)
        stream << json.dumps(settings_dict, indent=2)  # pylint: disable=expression-not-assigned
        res: bool = True
    else:
        file.cancelWriting()
        logger.error("Failed to open 'settings.json'")
    file.commit()
    lock.unlock()
    return res
