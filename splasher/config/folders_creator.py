import logging
import sys

from PySide6.QtCore import QDir

from .args import PATH


def create_folder(dir_path: str, subfolder_name: str = "") -> None:
    """
    Create a directory using QDir.
    :param dir: a directory path, e.g. "$HOME/.config/splasher/"
    :param subfolder_name: a subfolder name, e.g. "unsplash/"
    """
    directory: QDir = QDir(dir_path)
    if not directory.exists():
        if not directory.mkpath("."):
            logging.error("Failed to create folder: '%s'", directory.path())
            sys.exit(f"Failed to create folder: {directory.path()}")
        if subfolder_name and not directory.mkpath(f"./{subfolder_name}"):
            logging.error("Failed to create folder: '%s/%s'", directory.path(), subfolder_name)
            sys.exit(f"Failed to create folder: {directory.path()}/{subfolder_name}")


def create_folders() -> None:
    """
    Create multiple folders for the application:
    1. create a directory where cache is stored if it does not exist.(~/.cache/splasher/<source>)
    2. create a directory where configuration is stored if it does not exist.(~/.config/splasher/)
    3. create a directory where logs are stored if it does not exist.(<project>/logs/)
    4. create a directory where background images are stored if it does not exist. ($HOME/Pictures/splasher_background/)
    """
    create_folder(PATH["CACHE"], PATH["SUBFOLDER"])
    create_folder(PATH["CONFIG"])
    create_folder(PATH["BACKGROUND"])
