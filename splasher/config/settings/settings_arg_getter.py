import json
import logging
from typing import Any

from PySide6.QtCore import QFile, QIODevice, QTextStream

from ..args import PATH
from . import lock


def get_settings_arg(arg_key: str, file_path: str = f"{PATH['CONFIG']}settings.json") -> tuple[bool, Any]:
    """
    Get the configuration in the settings based on the input string.
    :param arg_key: configuration key
    :return tuple: (bool, configuration value)
    """
    logger: logging.Logger = logging.getLogger(__name__)
    res: tuple[bool, Any] = (False, "")
    settings_file: QFile = QFile(file_path)

    lock.lockForRead()
    if settings_file.open(QIODevice.ReadOnly | QIODevice.Text | QIODevice.ExistingOnly):
        stream: QTextStream = QTextStream(settings_file)
        try:
            settings_dict: Any = json.loads(stream.readAll())
            res: tuple[bool, Any] = (True, settings_dict[arg_key])
        except json.JSONDecodeError:
            logger.warning("'%s' is empty", file_path)
        except KeyError:
            logger.error("Key: %s does not exist in '%s'", arg_key, file_path)
    else:
        logger.error("Failed to open '%s': %s", file_path, settings_file.errorString())
    settings_file.close()
    lock.unlock()

    return res
