import logging
from typing import Optional

from PySide6.QtCore import QFile, QIODevice, QObject, Slot
from PySide6.QtNetwork import QNetworkReply
from PySide6.QtWidgets import QMainWindow

from ..config import PATH, set_settings_arg


class PreviewFetcher(QObject):
    """
    The ImgFetcher class contains the following functions:
    1. Bind the reply passed from MainWindow to different handler functions.
    2. Write the preview to cache and update ui to show it.
    """

    def __init__(self, parent: QMainWindow) -> None:
        """
        Create some variables that will be used later and initialize them to none.
        :param parent: MainWindow
        """
        super().__init__(parent)
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.reply: Optional[QNetworkReply] = None
        self.file: Optional[QFile] = None

    def fetch_preview(self, reply: QNetworkReply) -> None:
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
        self.logger.info("Send a request to '%s' to get a preview", self.reply.request().url().toString())

    @Slot()
    def on_finished(self) -> None:
        """
        Read the reply data and write the preview to the cache folder.('~/.cache/splasher/unsplash/')
        The 'settings.json' will be modified and the QLabel in 'MainWindow' will be repainted.

        reply.url(): "https://images.unsplash.com/photo-123456789?xxx=xxx&xxx=..."
        reply.url().path(): "/photo-123456789"
        reply.readAll(): binary data
        """
        if self.reply:
            if self.reply.error() == QNetworkReply.NoError:
                # ======== variables ========
                img_id: str = self.reply.url().path()[1:]
                subfolder: str = PATH["SUBFOLDER"]
                img_fullpath: str = f"{PATH['CACHE']}{subfolder}{img_id}.jpg"
                failed: bool = False
                # ======== save the image ========
                self.file: QFile = QFile(img_fullpath)
                if self.file.open(QIODevice.WriteOnly | QIODevice.NewOnly):
                    self.logger.info("Open and write an preview: '%s'", img_fullpath)
                    if self.file.write(self.reply.readAll()) == -1:  # if an error occurred
                        self.show_message("Failed to write a preview")
                        self.logger.error("Failed to write a preview")
                        failed: bool = True
                else:
                    self.show_message("Can not open file when trying to write a preview.")
                    self.logger.error("Can not open file '%s' when trying to write a preview: '%s'", img_fullpath,
                                      self.file.errorString())
                    failed: bool = True
                self.file.close()
                # ======== modify 'settings.json' ========
                if not failed:
                    if set_settings_arg("PREVIEW",
                                        f"{subfolder}{img_id}"):  # write the preview name into 'settings.json'
                        self.parent().set_preview()  # refresh and update an previw
                    else:
                        self.logger.error("Failed to set the value of 'PREVIEW' from 'settings.json'")
                else:
                    self.logger.warning("Remove file: %s", img_fullpath)
                    QFile.remove(img_fullpath)
            self.reply.deleteLater()

    @Slot(QNetworkReply.NetworkError)
    def on_error(self, code: QNetworkReply.NetworkError) -> None:
        """
        Handle error messages.
        :param code: QNetworkReply.NetworkError Code.
        """
        if self.reply:
            error_message: str = self.reply.errorString()
            self.show_message(f"An error occured when fetching a preview: '{error_message}'", 0)
            self.logger.error("QNetworkReply NetworkError - Code: %s, Content: %s", code, error_message)
            self.reply.deleteLater()

    @Slot(int, int)
    def on_progress(self, bytes_received: int, bytes_total: int) -> None:
        """
        Display the download progress in status bar when fetching a preview.
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
