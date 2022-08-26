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
                set_settings_arg("CNM", True)
                self.logger.info("Prepare to use mirror, set 'CNM' to 'True' in settings.")
            elif self.reply.error() == QNetworkReply.NoError:
                set_settings_arg("CNM", False)
                self.logger.info("Prepare to use the orignal site, set 'CNM' to 'False'")
            else:
                self.logger.warning("Unhandled error: %s", self.reply.errorString())
            self.reply.deleteLater()

    @Slot(QNetworkReply.NetworkError)
    def on_error(self, code: QNetworkReply.NetworkError) -> None:
        """
        Override parent method.
        Handle error messages.
        :param code: QNetworkReply.NetworkError Code.
        """
        if self.reply:
            error_message: str = self.reply.errorString()
            self.logger.error("QNetworkReply NetworkError - Code: %s, Content: %s", code, error_message)
            self.reply.deleteLater()
