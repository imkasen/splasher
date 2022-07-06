from typing import Any
import logging
import logging.config
import os
import yaml


def init_log(file_path: str = "src/config/log.yaml") -> None:
    """
    Read the logging configuration.
    :param file_path: the path of 'log.yaml'
    """
    if os.path.exists(path=file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                file_config: Any = yaml.safe_load(file)
                logging.config.dictConfig(file_config)
            except (IOError, Exception, BaseException):
                fallback_config("Error in loading configuration, using default configuration.")
    else:
        fallback_config(f"Failed to load configuration file: '{file_path}', using default configuration.")


def fallback_config(msg: str) -> None:
    """
    Default configuration when loading 'log.yaml' fails.
    :param msg:
    """
    logging.basicConfig(level=logging.WARNING,
                        datefmt="%Y/%m/%d %H:%M:%S",
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.error(msg, exc_info=True)
