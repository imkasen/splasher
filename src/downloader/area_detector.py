from PySide6.QtCore import Slot
from PySide6.QtNetwork import QNetworkReply

from ..config import set_settings_arg
from .downloader import Downloader


class AreaDetector(Downloader):
    """
    This class is used to check network area.
    """

    def detect(self, reply: QNetworkReply) -> None:
        """
        Detect whether user is in mainland China in order to use mirror site.
        :param reply: QNetworkReply
        """
        super().run(reply)
        self.reply.finished.connect(self.on_finished)
        self.reply.errorOccurred.connect(self.on_error)

    @Slot()
    def on_finished(self) -> None:
        """
        If user is in mainland China, then the error will be "Operation Canceled"
        """
        if self.reply:
            if self.reply.error() == QNetworkReply.OperationCanceledError:
                self.logger.error("Reply Error: '%s'", self.reply.errorString())
                self.logger.info("Prepare to use mirror, set 'CNM' to 'True' in settings.")
                set_settings_arg("CNM", True)
            elif self.reply.error() == QNetworkReply.NoError:
                self.logger.info("Prepare to use the orignal site, set 'CNM' to 'False'")
                set_settings_arg("CNM", False)
            else:
                self.logger.warning("Unhandled error: %s", self.reply.errorString())
            self.reply.deleteLater()

    @Slot(QNetworkReply.NetworkError)
    def on_error(self, code: QNetworkReply.NetworkError) -> None:
        """
        Override parent method, do not display any error messages
        """
