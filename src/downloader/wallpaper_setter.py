import logging
import re
from typing import Optional

from PySide6.QtCore import QIODevice, QObject, QSaveFile, Slot
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
        Set the image as the desktop wallpaper using 'gsettings' command.
        """
        if self.reply:
            if self.reply.error() == QNetworkReply.NoError:
                # ======== variables ========
                reply_path: str = self.reply.url().path()
                img_id: str = re.findall(r"^/id/(\d+)/", reply_path)[0]  # get the image id
                subfolder: str = "picsum/"
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
                    self.set_wallpaper(img_fullpath)
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
    def on_progress(self, bytes_received: int = 0, bytes_total: int = 0) -> None:
        """
        Display the download progress in status bar when fetching an wallpaper.
        :param bytes_received: default value is 0.
        :param bytes_total: default value is 0 to prevent exception when network error occurs.
        """
        if bytes_total != 0:
            if bytes_received == bytes_total:
                self.show_message(
                    f"Download progress: {bytes_received}/{bytes_total} - {round(bytes_received / bytes_total * 100)}%",
                )
            else:
                self.show_message(
                    f"Download progress: {bytes_received}/{bytes_total} - {round(bytes_received / bytes_total * 100)}%",
                    0)

    def show_message(self, msg: str, timeout: int = 5000) -> None:
        """
        Show some messages in the status bar of 'MainWindow' using its show_message() function.
        :param msg: message string
        :param timeout: default time is 5000 ms.
        """
        self.parent().show_message(msg, timeout)

    def set_wallpaper(self, img_path: str) -> None:
        """
        Set the wallpaper using 'gsettings' command
        :param img_path: the location of wallpaper.
        """
        self.logger.info("Set '%s' as the desktop wallpaper", img_path)
