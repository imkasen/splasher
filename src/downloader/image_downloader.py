import logging
from typing import Optional
from PySide6.QtCore import QObject, Slot, QUrl, QFile, QIODevice
from PySide6.QtWidgets import QMainWindow
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from ..config import API, PATH, set_settings_arg


class ImgDownloader(QObject):
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
        self.__logger: logging.Logger = logging.getLogger(__name__)
        self.__mgr: QNetworkAccessManager = QNetworkAccessManager(self)
        self.__reply: Optional[QNetworkReply] = None
        self.__mgr.setAutoDeleteReplies(True)
        self.__mgr.setTransferTimeout(10000)  # 10s

    def send_request(self, url: str = API["SOURCE"]) -> None:
        """
        Init a network request and send the request to Unsplash api.
        :param url: Unsplash api url
        """
        req: QNetworkRequest = QNetworkRequest(QUrl(url))
        self.__reply: QNetworkReply = self.__mgr.get(req)
        self.__reply.finished.connect(self.handle_response)  # pylint: disable=no-member
        self.__logger.info("Send a request to '%s' to get an image", url)

    @Slot()
    def handle_response(self) -> None:
        """
        Read the reply data and write the image to the cache folder.
        reply.url(): "https://images.unsplash.com/photo-123456789?xxx=xxx&xxx=..."
        reply.url().path(): "/photo-123456789"
        reply.readAll(): binary data
        """
        if self.__reply.error() != QNetworkReply.NoError:
            self.__show_message("Failed to fetch an image.", 0)
            self.__logger.error("QNetworkReply Error: %s", self.__reply.errorString())
            return

        img_name: str = self.__reply.url().path()[1:] + ".jpg"
        img_path: str = PATH["CACHE"] + img_name
        img_file: QFile = QFile(img_path)
        if img_file.open(QIODevice.WriteOnly | QIODevice.NewOnly):
            img_file.write(self.__reply.readAll())
            self.__logger.info("Write an image to: '%s'", img_path)
            if set_settings_arg("PREVIEW", img_name):  # write the image name into 'settings.json'
                self.parent().set_image()  # refresh and update an image
                self.__show_message("")  # clear messages
            else:
                self.__logger.error("Failed to set the value of 'PREVIEW' from 'settings.json'")
        else:
            self.__show_message("Failed to write an image to cache.")
            self.__logger.error("Failed to write an image to: '%s'", img_path)
        img_file.close()

    def __show_message(self, msg: str, timeout: int = 5000) -> None:
        """
        Show some messages in the status bar of 'MainWindow' using its show_message() function.
        :param msg: message string.
        :param timeout: default timeout is 5000 ms.
        """
        self.parent().show_message(msg, timeout)
