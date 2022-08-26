import logging
from typing import Optional

from PySide6.QtCore import QObject, Slot
from PySide6.QtNetwork import QNetworkReply
from PySide6.QtWidgets import QMainWindow


class Downloader(QObject):
    """
    The basic downloader class.
    """

    def __init__(self, parent: QMainWindow) -> None:
        """
        Create some variables that will be used later and initialize them.
        :param parent: MainWindow
        """
        super().__init__(parent)
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.reply: Optional[QNetworkReply] = None

    def run(self, reply: QNetworkReply) -> None:
        """
        Receive the network reply and bind the reply to the handler functions.
        :param reply: QNetworkReply
        """
        self.reply: QNetworkReply = reply
        self.reply.downloadProgress.connect(self.on_progress)
        self.reply.requestSent.connect(self.on_request_sent)
        self.reply.errorOccurred.connect(self.on_error)

    @Slot()
    def on_request_sent(self) -> None:
        """
        Add a log to record the request url.
        The request may be send twice if the url needs to be redirected.
        """
        self.logger.info("Send a request to '%s'", self.reply.request().url().toString())

    @Slot(QNetworkReply.NetworkError)
    def on_error(self, code: QNetworkReply.NetworkError) -> None:
        """
        Handle error messages.
        :param code: QNetworkReply.NetworkError Code.
        """
        if self.reply:
            error_message: str = self.reply.errorString()
            self.show_message(f"An error occured: '{error_message}'", 0)
            self.logger.error("QNetworkReply NetworkError - Code: %s, Content: %s", code, error_message)
            self.reply.deleteLater()

    @Slot(int, int)
    def on_progress(self, bytes_received: int, bytes_total: int) -> None:
        """
        Display the download progress in status bar.
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

    def show_message(self, msg: str, timeout: int = 5000) -> None:
        """
        Show some messages in the status bar of 'MainWindow' using its show_message() function.
        :param msg: message string.
        :param timeout: default timeout is 5000 ms.
        """
        self.parent().show_message(msg, timeout)
