import logging
import os
from typing import Optional

from PySide6.QtCore import QFile, QIODevice, QObject, QProcess, QSaveFile, Slot
from PySide6.QtNetwork import QNetworkReply
from PySide6.QtWidgets import QMainWindow

from ..config import PATH


class WallpaperSetter(QObject):
    """
    The WallpaperSetter class contains the following functions:
    1. Bind the reply passed from MainWindow to different handler functions.
    2. Write the image back to the same file and set it as the desktop wallpaper.
    """

    def __init__(self, parent: QMainWindow) -> None:
        """
        Create some variables that will be used later and initialize them to none.
        :param parent: MainWindow
        """
        super().__init__(parent)
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.reply: Optional[QNetworkReply] = None
        self.file: Optional[QSaveFile] = None

    def fetch_wallpaper(self, reply: QNetworkReply) -> None:
        """
        Receive the network reply and bind the reply to the handler functions.
        :param reply: QNetworkReply
        """
        self.reply: QNetworkReply = reply
        self.reply.downloadProgress.connect(self.on_progress)
        self.reply.requestSent.connect(self.on_request_sent)
        self.reply.finished.connect(self.on_finished)
        self.reply.errorOccurred.connect(self.on_error)

    @Slot()
    def on_request_sent(self) -> None:
        """
        Add a log to record the request url.
        The request will be send twice, because the url will be redirected.
        """
        self.logger.info("Send a request to '%s' to get an image", self.reply.request().url().toString())

    @Slot()
    def on_finished(self) -> None:
        """
        Read the reply data and write the wallpaper to the same file in cache folder.
        Set the image as the desktop wallpaper.
        """
        if self.reply:
            if self.reply.error() == QNetworkReply.NoError:
                # ======== variables ========
                img_id: str = self.reply.request().url().path()[1:]
                subfolder: str = PATH["SUBFOLDER"]
                img_fullpath: str = f"{PATH['CACHE']}{subfolder}{img_id}.jpg"
                failed: bool = False
                # ======== save the wallpaper ========
                self.file: QSaveFile = QSaveFile(img_fullpath)
                if self.file.open(QIODevice.WriteOnly):
                    self.logger.info("Open and write the wallpaper: '%s'", img_fullpath)
                    if self.file.write(self.reply.readAll()) == -1:  # if an error occurred
                        self.show_message("Failed to write a wallpaper back to its preview file.")
                        self.logger.error("Failed to write a wallpaper back to its preview file.")
                        failed: bool = True
                else:
                    self.show_message("Can not open file when trying to write a wallpaper.")
                    self.logger.error("Can not open file '%s' when trying to write a wallpaper: '%s'", img_fullpath,
                                      self.file.errorString())
                    failed: bool = True
                if failed:
                    self.file.cancelWriting()
                # ======== set as the desktop wallpaper ========
                if self.file.commit():
                    self.set_wallpaper(img_fullpath, f"{img_id}.jpg")
            self.reply.deleteLater()

    @Slot(QNetworkReply.NetworkError)
    def on_error(self, code: QNetworkReply.NetworkError) -> None:
        """
        Handle error messages.
        :param code: QNetworkReply.NetworkError Code
        """
        if self.reply:
            error_message: str = self.reply.errorString()
            self.show_message(f"An error occured when fetching an image: '{error_message}'", 0)
            self.logger.error("QNetworkReply NetworkError - Code: %s, Content: %s", code, error_message)

    @Slot(int, int)
    def on_progress(self, bytes_received: int, bytes_total: int) -> None:
        """
        Display the download progress in status bar when fetching an wallpaper.
        :param bytes_received: 0 means no download.
        :param bytes_total: 0 means no download, -1 means the number of bytes is unknown.
        """
        if bytes_total not in (-1, 0):
            if bytes_received == bytes_total:
                self.show_message(
                    f"Download progress: {bytes_received}/{bytes_total} - {round(bytes_received / bytes_total * 100)}%",
                )
            else:
                self.show_message(
                    f"Download progress: {bytes_received}/{bytes_total} - {round(bytes_received / bytes_total * 100)}%",
                    0)
        elif bytes_total == -1:
            self.show_message(f"Download progress: {bytes_received}/Unknown", 0)
        elif bytes_total == 0:
            self.show_message(f"Download progress: {bytes_received}/{bytes_total}", 0)

    def show_message(self, msg: str, timeout: int = 5000) -> None:
        """
        Show some messages in the status bar of 'MainWindow' using its show_message() function.
        :param msg: message string
        :param timeout: default time is 5000 ms.
        """
        self.parent().show_message(msg, timeout)

    def set_wallpaper(self, img_fullpath: str, img_name: str) -> None:
        """
        Set the wallpaper base on the desktop environment.
        :param img_fullpath: the source full path of wallpaper, the image name is included.
        :param img_name: the name of wallpaper.
        """
        dst_path: str = f"{PATH['BACKGROUND']}{img_name}"
        QFile.remove(dst_path)
        if QFile.copy(img_fullpath, dst_path):
            self.logger.info("Copy the wallpaper from '%s' to '%s'", img_fullpath, dst_path)

            # ======== detect KDE/GNOME/XFCE... ========
            env:str = os.getenv("XDG_CURRENT_DESKTOP")
            match env:
                case "KDE":
                    self.set_wallpaper_kde(dst_path)
                case "GNOME":
                    self.set_wallpaper_gnome(dst_path)
                case "XFCE":
                    self.set_wallpaper_xfce(dst_path)
                case _:
                    self.show_message("Unsupported desktop environment.")
                    self.logger.error("Detect an unsupported desktop environment: %s", env)
                    return
        else:
            self.show_message("Failed to copy the wallpaper")
            self.logger.error("Failed to copy the wallpaper from '%s' to '%s'", img_fullpath, dst_path)

    def set_wallpaper_kde(self, img_path: str) -> None:
        """
        Set the wallpaper on KDE.
        :param img_path: the copied wallpaper path.
        Ref: https://www.reddit.com/r/linux4noobs/comments/emvwai/change_kde_background_image_through_terminal/
        """
        jscript: str = (
            f"var allDesktops = desktops();\n"
            f"for (i=0; i<allDesktops.length; i++) {{\n"
            f"    d = allDesktops[i];\n"
            f"    d.wallpaperPlugin = 'org.kde.image';\n"
            f"    d.currentConfigGroup = Array('Wallpaper','org.kde.image','General');\n"
            f"    d.writeConfig('Image', 'file://{img_path}');\n"
            f"}}"
        )
        return_code: int = QProcess.execute("qdbus", ["org.kde.plasmashell", "/PlasmaShell",
                                                      "org.kde.PlasmaShell.evaluateScript", jscript])
        if return_code == -2:
            self.logger.error("The process can not be started")
        elif return_code ==-1:
            self.logger.error("The process crashed")
        else:
            self.logger.info("Set '%s' as the desktop wallpaper, return code: %s", img_path, return_code)

    def set_wallpaper_gnome(self, img_path: str) -> None:
        """
        Set the wallpaper on GNOME.
        :param img_path: the copied wallpaper path.
        """

    def set_wallpaper_xfce(self, img_path: str) -> None:
        """
        Set the wallpaper on XFCE.
        :param img_path: the copied wallpaper path.
        """
