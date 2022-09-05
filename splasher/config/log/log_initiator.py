import json
import logging
import logging.config

from PySide6.QtCore import QDir, QFile, QFileInfo, QIODevice, QTextStream

from ..folders_creator import create_folder


def init_log(file_path: str = "log.json") -> None:
    """
    Read the logging configuration.
    :param file_path: the path of 'log.json' (/opt/splasher/log.json)
    """
    file: QFileInfo = QFileInfo(file_path)
    if not file.exists():
        file_path: str = "splasher/config/log/dev_log.json"  # the path of 'log.json' in dev mode
        create_folder(f"{QDir.currentPath()}/logs/")
    log_config: QFile = QFile(file_path)
    if log_config.open(QIODevice.ReadOnly | QIODevice.Text | QIODevice.ExistingOnly):
        stream: QTextStream = QTextStream(log_config)
        context: str = stream.readAll()
        logging.config.dictConfig(json.loads(context))
    else:
        fallback_config(f"Failed to open the configuration file: '{file_path}', using default configuration.")
    log_config.close()


def fallback_config(msg: str) -> None:
    """
    Default configuration when loading 'log.json' fails.
    :param msg:
    """
    logging.basicConfig(level=logging.WARNING,
                        datefmt="%Y/%m/%d %H:%M:%S",
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.error(msg, exc_info=True)
