from typing import Any
from .args import PATH
import logging
import logging.config
import os
import json


def init_log(file_path: str = PATH["logfile"]) -> None:
    """
    Read the logging configuration.
    :param file_path: the path of 'log.json'
    """
    if os.path.exists(path=file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                file_config: Any = json.load(file)
                logging.config.dictConfig(file_config)
            except (IOError, Exception, BaseException):
                fallback_config("Error in loading configuration, using default configuration.")
    else:
        fallback_config(f"Failed to load configuration file: '{file_path}', using default configuration.")


def fallback_config(msg: str) -> None:
    """
    Default configuration when loading 'log.json' fails.
    :param msg:
    """
    logging.basicConfig(level=logging.WARNING,
                        datefmt="%Y/%m/%d %H:%M:%S",
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.error(msg, exc_info=True)
