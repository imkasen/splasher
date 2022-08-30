from PySide6.QtCore import QDir

from splasher.__version__ import __version__

# Some information about the application
APP: dict[str, str] = {
    "NAME": "Splasher",
    "VERSION": __version__,
    "AUTHOR": "Kasen",
    "ADDR": "https://github.com/imkasen/splasher",
    "DIR": "splasher/",
}

# PATH for storing file
PATH: dict[str, str] = {
    "APPLOCK": f"{QDir.tempPath()}/splasher.lock",
    "CONFIG": f"{QDir.homePath()}/.config/{APP['DIR']}",
    "CACHE": f"{QDir.homePath()}/.cache/{APP['DIR']}",
    "BACKGROUND": f"{QDir.homePath()}/Pictures/splasher_background/",
    "SUBFOLDER": "unsplash/",
}

# API for fetching Unsplash images
UNSPLASH: dict[str, str] = {
    "SOURCE": "https://source.unsplash.com/random/",
    "IMAGES": "https://images.unsplash.com/",
    "IMAGES-MIRROR": "https://dogefs.s3.ladydaily.com/~/source/unsplash/",
}
