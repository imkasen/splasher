from PySide6.QtCore import QDir

APP_TITLE: str = "Unsplash Wallpapers for Linux"
APP_DIR: str = "unsplash_wallpapers/"

LOCKFILE_PATH: str = QDir.tempPath() + "/unsplash_wallpapers.lock"
CACHE_PATH: str = QDir.homePath() + "/.cache/" + APP_DIR
