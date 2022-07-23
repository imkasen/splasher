from PySide6.QtCore import QDir
from .args import PATH
import logging


def create_folders() -> None:
    """
    Create multiple folders for the application:
    1. create a directory where cache is stored if it does not exist.(~/.cache/<dir>)
    2. create a directory where configuration is stored if it does not exist.(~/.config/<dir>)
    3. create a directory where logs are stored if it does not exist.(~/tmp/<dir>)
    """
    # ======== create the cache dir ========
    cache_dir: QDir = QDir(PATH["CACHE"])
    if not cache_dir.exists():
        if cache_dir.mkpath(PATH["CACHE"]) is not True:
            logging.error(f"Fail to create folder: '{PATH['CACHE']}'")
    # -------------------------------------------------------------
    # ======== create the cache dir ========
    config_dir: QDir = QDir(PATH["CONFIG"])
    if not config_dir.exists():
        if config_dir.mkpath(PATH["CONFIG"]) is not True:
            logging.error(f"Fail to create folder: '{PATH['CONFIG']}'")
    # -------------------------------------------------------------
    # ======== create the log dir ========
    log_dir: QDir = QDir(PATH["LOG"])
    if not log_dir.exists():
        if log_dir.mkpath(PATH["LOG"]) is not True:
            logging.error(f"Fail to create folder: '{PATH['LOG']}'")
    # -------------------------------------------------------------
