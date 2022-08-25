import logging
from typing import Optional

from PySide6.QtCore import QObject, Slot
from PySide6.QtNetwork import QNetworkReply
from PySide6.QtWidgets import QMainWindow

from ..config import set_settings_arg


class AreaDetector(QObject):
    """
    This class is used to check network area.
    """

    def __init__(self, parent: QMainWindow) -> None:
        """
        Create some variables that will be used later and initialize them to none.
        :param parent: MainWindow
        """
        super().__init__(parent)
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.reply: Optional[QNetworkReply] = None

    def detect(self, reply: QNetworkReply) -> None:
        """
        Detect whether user is in mainland China in order to use mirror site.
        :param reply: QNetworkReply
        """
        self.reply: QNetworkReply = reply
        self.reply.finished.connect(self.on_finished)

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
