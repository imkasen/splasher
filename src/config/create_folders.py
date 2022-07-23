from PySide6.QtCore import QDir
from .args import PATH
import logging


def create_folders() -> None:
    """
    Create multiple folders for the application:
    1. create a single directory where app cache is stored if it does not exist.(~/.cache/<dir>)
    2. create a single directory where app logs are stored if it does not exist.(~/tmp/<dir>)
    """
    # ======== check the cache dir ========
    cache_dir: QDir = QDir(PATH["CACHE"])
    if not cache_dir.exists():
        if cache_dir.mkpath(PATH["CACHE"]) is not True:
            logging.error(f"Failed to create folder: '{PATH['CACHE']}'")
        else:
            logging.warning(f"Create folder: '{PATH['CACHE']}'")
    # -------------------------------------------------------------
    # ======== check the log dir ========
    log_dir: QDir = QDir(PATH["LOG"])
    if not log_dir.exists():
        if log_dir.mkpath(PATH["LOG"]) is not True:
            logging.error(f"Failed to create folder: '{PATH['LOG']}'")
        else:
            logging.warning(f"Create folder: '{PATH['LOG']}'")
    # -------------------------------------------------------------
