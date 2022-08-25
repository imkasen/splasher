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
            logging.error("Failed to create folder: '%s'", cache_dir.path())
        if not cache_dir.mkpath(f"./{PATH['SUBFOLDER']}"):
            logging.error("Failed to create folder: '%s%s'", cache_dir.path(), PATH["SUBFOLDER"])
    # -------------------------------------------------------------
    # ======== create the configuration dir ========
    config_dir: QDir = QDir(PATH["CONFIG"])
    if not config_dir.exists():
        if not config_dir.mkpath("."):
            logging.error("Failed to create folder: '%s'", config_dir.path())
    # -------------------------------------------------------------
    # ======== create the log dir ========
    log_dir: QDir = QDir("logs")
    if not log_dir.exists():
        if not log_dir.mkpath("."):
            logging.error("Failed to create folder: '%s%s'", QDir.currentPath(), "/logs/")
    # -------------------------------------------------------------
    # ======== create the background dir ========
    backgound_dir: QDir = QDir(PATH["BACKGROUND"])
    if not backgound_dir.exists():
        if not backgound_dir.mkpath("."):
            logging.error("Failed to create folder: '%s'", backgound_dir.path())
    # -------------------------------------------------------------
