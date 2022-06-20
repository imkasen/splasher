from PySide6.QtCore import QDir

APP_NAME = "Unsplash Wallpapers for Linux"
APP_VERSION = "v0.1.0"
APP_AUTHOR = "Kasen"
APP_ADDR = "https://github.com/imkasen/unsplash-wallpapers-for-linux"
APP_DIR: str = "unsplash_wallpapers/"

ICONS_PATH: str = "resources/icons/"
LOCKFILE_PATH: str = QDir.tempPath() + "/unsplash_wallpapers.lock"
CACHE_PATH: str = QDir.homePath() + "/.cache/" + APP_DIR
