from PySide6.QtCore import QIODevice, QSaveFile, Slot
from PySide6.QtNetwork import QNetworkReply

from .downloader import Downloader


class WallpaperDownloader(Downloader):
    """
    The WallpaperDownloader class contains the following functions:
    1. Bind the reply to different handler functions.
    2. Save the image into the path specified by the user.
    """

    def download(self, reply: QNetworkReply, path: str) -> None:
        """
        Receive the network reply and bind the reply to the handler functions.
        :param reply: QNetworkReply
        :param path: the image saving path
        """
        super().run(reply)
        self.reply.finished.connect(lambda: self.on_finished(path))

    @Slot()
    def on_finished(self, path: str) -> None:
        """
        Read the reply data and save the image into the path.
        """
        if self.reply:
            if self.reply.error() == QNetworkReply.NoError:
                failed: bool = False
                file: QSaveFile = QSaveFile(path)
                if file.open(QIODevice.WriteOnly):
                    self.logger.info("Open and save the wallpaper: '%s'", path)
                    if file.write(self.reply.readAll()) == -1:
                        self.show_message("Failed to save a wallpaper.")
                        self.logger.error("Failed to save a wallpaper.")
                        failed: bool = True
                else:
                    self.show_message("Can not open file when trying to write a wallpaper.")
                    self.logger.error("Can not open file '%s' when trying to write a wallpaper: '%s'", path,
                                      file.errorString())
                    failed: bool = True
                if failed:
                    file.cancelWriting()
                if file.commit():
                    self.show_message("Download and save the wallpaper successfully.")
            self.reply.deleteLater()
