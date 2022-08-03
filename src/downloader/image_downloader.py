from PySide6.QtCore import QObject, Slot, QUrl, QFile, QIODevice
from PySide6.QtWidgets import QMainWindow
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from ..config import API, PATH, set_settings_arg
import logging


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
        super(ImgDownloader, self).__init__(parent=main_window)
        self.__logger: logging.Logger = logging.getLogger(__name__)
        self.__mgr: QNetworkAccessManager = QNetworkAccessManager()
        self.__mgr.setAutoDeleteReplies(True)
        self.__mgr.setTransferTimeout(10000)  # 10s

    def send_request(self, api: str = API["SOURCE"]) -> None:
        """
        Init a network request and send the request to Unsplash api.
        :param api: Unsplash api url
        """
        req: QNetworkRequest = QNetworkRequest(QUrl(api))
        self.__mgr.finished.connect(self.handle_response)
        self.__mgr.get(req)

    @Slot()
    def handle_response(self, reply: QNetworkReply) -> None:
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
        img_name: str = reply.url().path()[1:] + ".jpg"
        img_path: str = PATH["CACHE"] + img_name
        img_file: QFile = QFile(img_path)
        if img_file.open(QIODevice.WriteOnly | QIODevice.NewOnly):
            img_file.write(reply.readAll())
            if set_settings_arg("PREVIEW", img_name):
                self.parent().set_image()  # refresh and update the image
            else:
                self.__logger.error("Failed to set the value of 'PREVIEW' from 'settings.json'")
            self.__logger.info(f"Write an image to: '{img_path}'")
        else:
            self.__show_message("Failed to write a previewed image to cache.")
            self.__logger.error(f"Failed to write an image to: '{img_path}'")
        img_file.close()

    def __show_message(self, msg: str) -> None:
        """
        Show some messages in the status bar of 'MainWindow' using its show_message() function.
        :param msg: message string.
        """
        self.parent().show_message(msg)
