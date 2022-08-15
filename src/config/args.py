from PySide6.QtCore import QDir

# Some information about the application
APP: dict[str, str] = {
    "NAME": "Splasher",
    "VERSION": "v0.2.0",
    "AUTHOR": "Kasen",
    "ADDR": "https://github.com/imkasen/splasher",
    "DIR": "splasher/",
}

# PATH for storing file
PATH: dict[str, str] = {
    "APPLOCK": QDir.tempPath() + "/splasher.lock",
    "CONFIG": QDir.homePath() + "/.config/" + APP["DIR"],
    "CACHE": QDir.homePath() + "/.cache/" + APP["DIR"],
}

# API for fetching images of 'Lorem Picsum'
# https://picsum.photos/
PICSUM: str = "https://picsum.photos/"
