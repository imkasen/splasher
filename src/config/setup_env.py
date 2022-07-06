from PySide6.QtCore import QDir
from .args import PATH
import logging


def setup_env() -> None:
    """
    Initialize various environment settings:
    1. create a single directory where app cache is stored if it does not exist.(~/.cache/<dir>)
    2. create a single directory where app logs are stored if it does not exist.(~/tmp/<dir>)
    """
    # ======== check the cache dir ========
    cache_dir: QDir = QDir(PATH["cache"])
    if not cache_dir.exists():
        if cache_dir.mkpath(PATH["cache"]) is not True:
            logging.error(f"Failed to create folder: '{PATH['cache']}'")
        else:
            logging.warning(f"Create folder: '{PATH['cache']}'")
    # -------------------------------------------------------------
    # ======== check the log dir ========
    log_dir: QDir = QDir(PATH["log"])
    if not log_dir.exists():
        if log_dir.mkpath(PATH["log"]) is not True:
            logging.error(f"Failed to create folder: '{PATH['log']}'")
        else:
            logging.warning(f"Create folder: '{PATH['log']}'")
    # -------------------------------------------------------------
