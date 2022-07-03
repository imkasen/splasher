from PySide6.QtCore import QDir
from .args import PATH


def setup_env() -> None:
    """
    Initialize various environment settings:
    1. check if the cache folder exists, if not, create it. 
    2. check if the configuration folder exists, if not, create it.
    """
    # ======== check the cache dir ========
    cache_dir: QDir = QDir(PATH["cache"])
    if not cache_dir.exists():
        cache_dir.mkpath(PATH["cache"])
    # -------------------------------------------------------------
    # ======== check the configuration dir ========
    config_dir: QDir = QDir(PATH["config"])
    if not config_dir.exists():
        config_dir.mkpath(PATH["config"])
    # -------------------------------------------------------------
