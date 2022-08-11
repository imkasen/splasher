import logging
from typing import Optional
from PySide6.QtCore import QObject, Slot, QUrl, QFile, QIODevice
from PySide6.QtWidgets import QMainWindow
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from ..config import API, PATH, set_settings_arg


class ImageDownloader(QObject):
    """
    The ImgFetcher class which contains following functions:
    1. Send a request using API in order to get a low resolution image.
    2. Write the image to cache and update ui to show it.
    """

    def __init__(self, main_window: QMainWindow) -> None:
        """
        Init a network access manager.
        """
        super().__init__(parent=main_window)
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.manager: QNetworkAccessManager = QNetworkAccessManager(self)
        self.manager.setAutoDeleteReplies(True)
        self.manager.setTransferTimeout(10000)  # 10s
        self.reply: Optional[QNetworkReply] = None
        self.file: Optional[QFile] = None

    def fetch_image(self, url: str = API["SOURCE"]) -> None:
        """
        Init a network request and send the request to Unsplash api.
        :param url: Unsplash api url
        """
        self.reply: QNetworkReply = self.manager.get(QNetworkRequest(QUrl(url)))
        self.reply.downloadProgress.connect(self.on_progress)
        self.reply.requestSent.connect(self.on_request_sent)
        self.reply.finished.connect(self.on_finished)
        self.reply.errorOccurred.connect(self.on_error)

    @Slot()
    def on_request_sent(self) -> None:
        """
        Add a log to record the request url.
        """
        self.logger.info("Send a request to '%s' to get an image", self.reply.request().url().toString())

    @Slot()
    def on_finished(self) -> None:
        """
        Read the reply data and write the image to the cache folder.
            reply.url(): "https://images.unsplash.com/photo-123456789?xxx=xxx&xxx=..."
            reply.url().path(): "/photo-123456789"
            reply.readAll(): binary data
        """
        if self.reply and self.reply.error() == QNetworkReply.NoError:
            img_name: str = self.reply.url().path()[1:] + ".jpg"
            img_path: str = PATH["CACHE"] + img_name
            self.file: QFile = QFile(img_path)
            if self.file.open(QIODevice.WriteOnly | QIODevice.NewOnly):
                self.logger.info("Open and write an image file: '%s'", img_path)
                self.file.write(self.reply.readAll())

                if set_settings_arg("PREVIEW", img_name):  # write the image name into 'settings.json'
                    self.parent().set_image()  # refresh and update an image
                else:
                    self.logger.error("Failed to set the value of 'PREVIEW' from 'settings.json'")
            else:
                self.show_message("Can not open file when trying to write an image.")
                self.logger.error("Can not open file '%s' when trying to write an image: '%s'", img_path,
                                  self.file.errorString())
            self.file.close()
            self.reply.deleteLater()

    @Slot(QNetworkReply.NetworkError)
    def on_error(self, code: QNetworkReply.NetworkError) -> None:
        """
        Handle error message.
        :param code: QNetworkReply::NetworkError Code.
        """
        if self.reply:
            self.show_message("An error occured when fetching an image.", 0)
            self.logger.error("QNetworkReply NetworkError - Code: %s, Content: %s", code, self.reply.errorString())

    @Slot(int, int)
    def on_progress(self, bytes_received: int = 0, bytes_total: int = 0) -> None:
        """
        Display download progress in status bar when fetching an image.
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
        :param msg: message string.
        :param timeout: default timeout is 5000 ms.
        """
        self.parent().show_message(msg, timeout)
