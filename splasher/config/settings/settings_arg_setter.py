import json
import logging
from typing import Any, Optional

from PySide6.QtCore import QFile, QIODevice, QSaveFile, QTextStream

from ..args import PATH
from . import lock

logger: logging.Logger = logging.getLogger(__name__)


def set_settings_arg(arg_key: str, arg_value: Any, file_path: str = f"{PATH['CONFIG']}settings.json") -> bool:
    """
    Modify the configuration value in the settings based on the input key.
    Creating a new pair of key and value is not allowed.
    :param arg_key: the configuration key that needs to be updated
    :param arg_value: the configuration value for update
    :return: bool
    """
    res: bool = False
    settings_dict: Optional[dict[str, Any]] = None
    res, settings_dict = read_settings(file_path)
    if res and settings_dict is not None:
        res: bool = False
        try:
            if not arg_key in settings_dict:
                raise KeyError
            settings_dict[arg_key] = arg_value
            res: bool = write_settings(file_path, settings_dict)
        except KeyError:
            logger.error("Key: %s does not exist in '%s'", arg_key, file_path)
    return res


def read_settings(path: str) -> tuple[bool, Optional[dict[str, Any]]]:
    """
    Read json from 'settings.json' and return it as dictionary.
    :param path: file path of 'settings.json'
    :return tuple: (bool, dictionary | None)
    """
    tup_res: tuple[bool, Optional[dict[str, Any]]] = (False, None)
    lock.lockForRead()
    file: QFile = QFile(path)

    if file.open(QIODevice.ReadOnly | QIODevice.Text | QIODevice.ExistingOnly):
        stream: QTextStream = QTextStream(file)
        try:
            settings_dict: Any = json.loads(stream.readAll())
            tup_res: tuple[bool, dict[str, Any]] = (True, settings_dict)
        except json.JSONDecodeError:
            logger.warning("'%s' is empty", path)
    else:
        logger.error("Failed to open '%s': %s", path, file.errorString())

    file.close()
    lock.unlock()
    return tup_res


def write_settings(path: str, settings_dict: dict[str, Any]) -> bool:
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
        logger.error("Failed to open '%s'", path)
    file.commit()
    lock.unlock()
    return res
