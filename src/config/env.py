from PySide6.QtCore import QDir

APP_NAME = "Unsplash Wallpapers for Linux"
APP_VERSION = "v0.1.4"
APP_AUTHOR = "Kasen"
APP_ADDR = "https://github.com/imkasen/unsplash-wallpapers-for-linux"
APP_DIR = "unsplash_wallpapers/"

LOCKFILE_PATH = QDir.tempPath() + "/unsplash_wallpapers.lock"
CACHE_PATH = QDir.homePath() + "/.cache/" + APP_DIR
