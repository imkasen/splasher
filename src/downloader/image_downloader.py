from PySide6.QtCore import QObject, Slot, QUrl, QFile, QIODevice
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from ..config import URL, PATH
import logging


class ImgDownloader(QObject):
    """
    The ImgFetcher class which contains following functions:
    1. Fetch a preview image and write to the cache folder.
    """

    def __init__(self) -> None:
        """
        Init a network access manager.
        """
        super(ImgDownloader, self).__init__()
        self.__logger: logging.Logger = logging.getLogger(__name__)
        self.__mgr: QNetworkAccessManager = QNetworkAccessManager()
        self.__mgr.setAutoDeleteReplies(True)
        self.__mgr.setTransferTimeout()

    def send_request(self, api: str = URL["source"]) -> None:
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
            self.__logger.error("QNetworkReply Error: " + reply.errorString())
            return
        img_path: str = PATH["cache"] + reply.url().path()[1:] + ".jpg"
        img_file: QFile = QFile(img_path)
        if img_file.open(QIODevice.WriteOnly):
            img_file.write(reply.readAll())
            self.__logger.info(f"Write an image to: '{img_path}'")
        else:
            self.__logger.error(f"Fail to write an image to: '{img_path}'")
