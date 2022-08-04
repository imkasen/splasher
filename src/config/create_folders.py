import logging
from PySide6.QtCore import QDir
from .args import PATH


def create_folders() -> None:
    """
    Create multiple folders for the application:
    1. create a directory where cache is stored if it does not exist.(~/.cache/<dir>)
    2. create a directory where configuration is stored if it does not exist.(~/.config/<dir>)
    3. create a directory where logs are stored if it does not exist.(<project>/logs/)
    """
    # ======== create the cache dir ========
    cache_dir: QDir = QDir(PATH["CACHE"])
    if not cache_dir.exists():
        if not cache_dir.mkpath("."):
            logging.error("Failed to create folder: '%s'", PATH["CACHE"])
    # -------------------------------------------------------------
    # ======== create the cache dir ========
    config_dir: QDir = QDir(PATH["CONFIG"])
    if not config_dir.exists():
        if not config_dir.mkpath("."):
            logging.error("Failed to create folder: '%s'", PATH["CONFIG"])
    # -------------------------------------------------------------
    # ======== create the log dir ========
    log_dir: QDir = QDir("logs")
    if not log_dir.exists():
        if not log_dir.mkpath("."):
            logging.error("Failed to create folder: 'logs/'")
    # -------------------------------------------------------------
