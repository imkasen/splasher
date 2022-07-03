from PySide6.QtCore import QDir

APP: dict[str, str] = {
    "name": "Unsplash Wallpapers for Linux",
    "version": "v0.1.4",
    "author": "Kasen",
    "addr": "https://github.com/imkasen/unsplash-wallpapers-for-linux",
    "dir": "unsplash_wallpapers/",
}

PATH: dict[str, str] = {
    "applock": QDir.tempPath() + "/unsplash_wallpapers.lock",
    "cache": QDir.homePath() + "/.cache/" + APP["dir"],
    "config": QDir.homePath() + "/.config/" + APP["dir"],
}
