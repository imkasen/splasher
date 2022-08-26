import logging
from typing import Optional

from PySide6.QtCore import QIODevice, QObject, QSaveFile, Slot
from PySide6.QtNetwork import QNetworkReply
from PySide6.QtWidgets import QMainWindow


class WallpaperDownloader(QObject):
    """
    The WallpaperDownloader class contains the following functions:
    1. Bind the reply passed from MainWindow to different handler functions.
    2. Save the image into the path specified by the user.
    """

    def __init__(self, parent: QMainWindow) -> None:
        """
        Create some variables that will be used later and initialize them to none.
        :param parent: MainWindow
        """
        super().__init__(parent)
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.reply: Optional[QNetworkReply] = None

    def download(self, reply: QNetworkReply, path: str) -> None:
        """
        Receive the network reply and bind the reply to the handler functions.
        :param reply: QNetworkReply
        """
        self.reply: QNetworkReply = reply
        self.reply.downloadProgress.connect(self.on_progress)
        self.reply.requestSent.connect(self.on_request_sent)
        self.reply.finished.connect(lambda: self.on_finished(path))
        self.reply.errorOccurred.connect(self.on_error)

    @Slot()
    def on_request_sent(self) -> None:
        """
        Add a log to record the request url.
        The request will be send twice, because the url will be redirected.
        """
        self.logger.info("Send a request to '%s' to get a wallpaper", self.reply.request().url().toString())

    @Slot()
    def on_finished(self, path: str) -> None:
        """
        Read the reply data and save the image into disk.
        """
        if self.reply:
            if self.reply.error() == QNetworkReply.NoError:
                failed: bool = False
                file: QSaveFile = QSaveFile(path)
                if file.open(QIODevice.WriteOnly):
                    self.logger.info("Open and save the wallpaper: '%s'", path)
                    if file.write(self.reply.readAll()) == -1:
                        self.show_message("Failed to save a wallpaper.")
                        self.logger.error("Failed to save a wallpaper.")
                        failed: bool = True
                else:
                    self.show_message("Can not open file when trying to write a wallpaper.")
                    self.logger.error("Can not open file '%s' when trying to write a wallpaper: '%s'", path,
                                      file.errorString())
                    failed: bool = True
                if failed:
                    file.cancelWriting()
                if file.commit():
                    self.show_message("Download and save the wallpaper successfully.")
            self.reply.deleteLater()

    @Slot(QNetworkReply.NetworkError)
    def on_error(self, code: QNetworkReply.NetworkError) -> None:
        """
        Handle error messages.
        :param code: QNetworkReply.NetworkError Code.
        """
        if self.reply:
            error_message: str = self.reply.errorString()
            self.show_message(f"An error occured when fetching a wallpaper: '{error_message}'", 0)
            self.logger.error("QNetworkReply NetworkError - Code: %s, Content: %s", code, error_message)
            self.reply.deleteLater()

    @Slot(int, int)
    def on_progress(self, bytes_received: int, bytes_total: int) -> None:
        """
        Display the download progress in status bar when fetching a wallpaper.
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
        :param msg: message string.
        :param timeout: default timeout is 5000 ms.
        """
        self.parent().show_message(msg, timeout)
