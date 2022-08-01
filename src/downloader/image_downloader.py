from PySide6.QtCore import QObject, Slot, QUrl, QFile, QIODevice
from PySide6.QtWidgets import QMainWindow
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from ..config import API, PATH
from typing import NoReturn
import logging


class ImgDownloader(QObject):
    """
    The ImgFetcher class which contains following functions:
    1. Fetch a preview image and write to the cache folder.
    """

    def __init__(self, main_window: QMainWindow) -> NoReturn:
        """
        Init a network access manager.
        """
        super(ImgDownloader, self).__init__(parent=main_window)
        self.__logger: logging.Logger = logging.getLogger(__name__)
        self.__mgr: QNetworkAccessManager = QNetworkAccessManager()
        self.__mgr.setAutoDeleteReplies(True)
        self.__mgr.setTransferTimeout()

    def send_request(self, api: str = API["SOURCE"] + "960x540") -> NoReturn:
        """
        Init a network request and send the request to Unsplash api.
        :param api: Unsplash api url
        """
        req: QNetworkRequest = QNetworkRequest(QUrl(api))
        self.__mgr.finished.connect(self.handle_response)
        self.__mgr.get(req)

    @Slot()
    def handle_response(self, reply: QNetworkReply) -> NoReturn:
        """
        Read the reply data and write the image to the cache folder.
        :param reply: download contents and headers.
            reply.url(): "https://images.unsplash.com/photo-123456789?xxx=xxx&xxx=..."
            reply.url().path(): "/photo-123456789"
            reply.readAll(): binary data
        """
        if reply.error() != QNetworkReply.NoError:
            self.__show_message("Failed to fetch a previewed image.")
            self.__logger.error("QNetworkReply Error: " + reply.errorString())
            return
        img_path: str = PATH["CACHE"] + reply.url().path()[1:] + ".jpg"
        img_file: QFile = QFile(img_path)
        if img_file.open(QIODevice.WriteOnly | QIODevice.NewOnly):
            img_file.write(reply.readAll())
            self.__logger.info(f"Write an image to: '{img_path}'")
        else:
            self.__show_message("Failed to write a previewed image to cache.")
            self.__logger.error(f"Failed to write an image to: '{img_path}'")
        img_file.close()

    def __show_message(self, msg: str) -> NoReturn:
        """
        Show some messages in the status bar of 'MainWindow' using its show_message() function.
        :param msg: message string.
        """
        self.parent().show_message(msg)
