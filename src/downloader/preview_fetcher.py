from PySide6.QtCore import QFile, QIODevice, Slot
from PySide6.QtNetwork import QNetworkReply

from ..config import PATH, set_settings_arg
from .downloader import Downloader


class PreviewFetcher(Downloader):
    """
    The PreviewFetcher class contains the following functions:
    1. Bind the reply to different handler functions.
    2. Save the preview to cache and show it by updating widgets.
    """

    def fetch_preview(self, reply: QNetworkReply) -> None:
        """
        Receive the network reply and bind the reply to the handler functions.
        :param reply: QNetworkReply
        """
        super().run(reply)
        self.reply.finished.connect(self.on_finished)

    @Slot()
    def on_finished(self) -> None:
        """
        Read the reply data and write the preview to the app cache folder.
        The 'PREVIEW' argument in 'settings.json' will be modified and the QLabel in 'MainWindow' will be repainted.

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
                file: QFile = QFile(img_fullpath)
                if file.open(QIODevice.WriteOnly | QIODevice.NewOnly):
                    self.logger.info("Open and write an preview: '%s'", img_fullpath)
                    if file.write(self.reply.readAll()) == -1:  # if an error occurred
                        self.show_message("Failed to write a preview")
                        self.logger.error("Failed to write a preview")
                        failed: bool = True
                else:
                    self.show_message("Can not open file when trying to write a preview.")
                    self.logger.error("Can not open file '%s' when trying to write a preview: '%s'", img_fullpath,
                                      file.errorString())
                    failed: bool = True
                file.close()
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
