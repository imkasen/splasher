from PySide6.QtCore import QDir

APP_DIR: str = "unsplash_wallpapers/"

ICONS_PATH: str = "resources/icons/"
LOCKFILE_PATH: str = QDir.tempPath() + "/unsplash_wallpapers.lock"
CACHE_PATH: str = QDir.homePath() + "/.cache/" + APP_DIR
