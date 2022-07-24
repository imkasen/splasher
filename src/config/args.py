from PySide6.QtCore import QDir

# Some information about the application
APP: dict[str, str] = {
    "NAME": "Unsplash Wallpapers for Linux",
    "VERSION": "v0.1.0",
    "AUTHOR": "Kasen",
    "ADDR": "https://github.com/imkasen/unsplash-wallpapers-for-linux",
    "DIR": "unsplash_wallpapers/",
}

# PATH for storing file
PATH: dict[str, str] = {
    "APPLOCK": QDir.tempPath() + "/unsplash_wallpapers.lock",
    "CACHE": QDir.homePath() + "/.cache/" + APP["DIR"],
    "CONFIG": QDir.homePath() + "/.config/" + APP["DIR"],
    "LOG": QDir.tempPath() + "/" + APP["DIR"],
}

# API for fetching images
API: dict[str, str] = {
    "SOURCE": "https://source.unsplash.com/random/",
}
