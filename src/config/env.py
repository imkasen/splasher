from PySide6.QtCore import QDir

APP = {
    "name": "Unsplash Wallpapers for Linux",
    "version": "v0.1.4",
    "author": "Kasen",
    "addr": "https://github.com/imkasen/unsplash-wallpapers-for-linux",
    "dir": "unsplash_wallpapers/",
}

PATH = {
    "applock": QDir.tempPath() + "/unsplash_wallpapers.lock",
    "cache": QDir.homePath() + "/.cache/" + APP["dir"],
}
