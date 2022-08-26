import os
import re

from PySide6.QtCore import QFile, QIODevice, QProcess, QSaveFile, Slot
from PySide6.QtNetwork import QNetworkReply

from ..config import PATH
from .downloader import Downloader


class WallpaperSetter(Downloader):
    """
    The WallpaperSetter class contains the following functions:
    1. Bind the reply passed to different handler functions.
    2. Save the image back to the same file and set it as the desktop wallpaper.
    """

    def fetch_wallpaper(self, reply: QNetworkReply) -> None:
        """
        Receive the network reply and bind the reply to the handler functions.
        :param reply: QNetworkReply
        """
        super().run(reply)
        self.reply.finished.connect(self.on_finished)

    @Slot()
    def on_finished(self) -> None:
        """
        Read the replied image data and save the wallpaper back to the same file in the app cache folder,
        then set the image as the desktop wallpaper.
        """
        if self.reply:
            if self.reply.error() == QNetworkReply.NoError:
                # ======== variables ========
                img_id: str = re.findall(r"photo-[0-9]{13}-[0-9a-z]{12}", self.reply.request().url().path())[0]
                subfolder: str = PATH["SUBFOLDER"]
                img_fullpath: str = f"{PATH['CACHE']}{subfolder}{img_id}.jpg"
                failed: bool = False
                # ======== save the wallpaper ========
                file: QSaveFile = QSaveFile(img_fullpath)
                if file.open(QIODevice.WriteOnly):
                    self.logger.info("Open and write the wallpaper: '%s'", img_fullpath)
                    if file.write(self.reply.readAll()) == -1:  # if an error occurred
                        self.show_message("Failed to write a wallpaper back to its preview file.")
                        self.logger.error("Failed to write a wallpaper back to its preview file.")
                        failed: bool = True
                else:
                    self.show_message("Can not open file when trying to write a wallpaper.")
                    self.logger.error("Can not open file '%s' when trying to write a wallpaper: '%s'", img_fullpath,
                                      file.errorString())
                    failed: bool = True
                if failed:
                    file.cancelWriting()
                # ======== set as the desktop wallpaper ========
                if file.commit():
                    self.set_wallpaper(img_fullpath, f"{img_id}.jpg")
            self.reply.deleteLater()

    def set_wallpaper(self, img_fullpath: str, img_name: str) -> None:
        """
        Copy the image to a new folder, then set the wallpaper in different desktop environments.
        :param img_fullpath: the full path of the source image, the image name is included.
        :param img_name: the name of wallpaper.
        """
        dst_path: str = f"{PATH['BACKGROUND']}{img_name}"
        QFile.remove(dst_path)
        if QFile.copy(img_fullpath, dst_path):
            self.logger.info("Copy the wallpaper from '%s' to '%s'", img_fullpath, dst_path)

            # ======== detect KDE/GNOME/XFCE... ========
            env:str = os.getenv("XDG_CURRENT_DESKTOP")
            match env:
                case "KDE":
                    self.set_kde(dst_path)
                case "GNOME":
                    self.set_gnome(dst_path)
                case "XFCE":
                    self.set_xfce(dst_path)
                case _:
                    self.show_message("Unsupported desktop environment.")
                    self.logger.error("Detect an unsupported desktop environment: %s", env)
                    return
        else:
            self.show_message("Failed to copy the wallpaper")
            self.logger.error("Failed to copy the wallpaper from '%s' to '%s'", img_fullpath, dst_path)

    def set_kde(self, img_path: str) -> None:
        """
        Set the wallpaper on KDE.
        :param img_path: the new copied wallpaper path.

        Command Reference:
            https://www.reddit.com/r/linux4noobs/comments/emvwai/change_kde_background_image_through_terminal/
        """
        jscript: str = (
            f"var allDesktops = desktops();\n"
            f"for (i=0; i<allDesktops.length; i++) {{\n"
            f"    d = allDesktops[i];\n"
            f"    d.wallpaperPlugin = 'org.kde.image';\n"
            f"    d.currentConfigGroup = Array('Wallpaper','org.kde.image','General');\n"
            f"    d.writeConfig('Image', 'file://{img_path}');\n"
            f"}}"
        )
        return_code: int = QProcess.execute("qdbus", ["org.kde.plasmashell", "/PlasmaShell",
                                                      "org.kde.PlasmaShell.evaluateScript", jscript])
        if return_code == -2:
            self.logger.error("The process can not be started")
        elif return_code == -1:
            self.logger.error("The process crashed")
        else:
            self.logger.info("Set '%s' as the desktop wallpaper, return code: %s", img_path, return_code)

    def set_gnome(self, img_path: str) -> None:
        """
        Set the wallpaper in GNOME.
        :param img_path: the copied wallpaper path.
        """

    def set_xfce(self, img_path: str) -> None:
        """
        Set the wallpaper in XFCE.
        :param img_path: the copied wallpaper path.
        """
