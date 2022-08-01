from PySide6.QtCore import QFile, QIODevice, QTextStream
from typing import NoReturn
import logging
import logging.config
import json


def init_log(file_path: str = "src/config/log/log.json") -> NoReturn:
    """
    Read the logging configuration.
    :param file_path: the path of 'log.json'
    """
    log_file: QFile = QFile(file_path)
    if log_file.exists():
        if log_file.open(QIODevice.ReadOnly | QIODevice.Text | QIODevice.ExistingOnly):
            stream: QTextStream = QTextStream(log_file)
            context: str = stream.readAll()
            logging.config.dictConfig(json.loads(context))
        else:
            fallback_config(f"Fail to open the configuration file: '{file_path}', using default configuration.")
    else:
        fallback_config(f"Fail to find the configuration file: '{file_path}', using default configuration.")
    log_file.close()


def fallback_config(msg: str) -> NoReturn:
    """
    Default configuration when loading 'log.json' fails.
    :param msg:
    """
    logging.basicConfig(level=logging.WARNING,
                        datefmt="%Y/%m/%d %H:%M:%S",
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.error(msg, exc_info=True)
