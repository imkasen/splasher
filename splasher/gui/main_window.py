import logging
import re
from math import ceil
from typing import Optional

from PySide6.QtCore import QDir, QFileInfo, Qt, QUrl, Slot
from PySide6.QtGui import QGuiApplication, QIcon, QPixmap, QScreen
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QMainWindow, QPushButton, QStatusBar, QVBoxLayout,
                               QWidget)

from splasher.config import APP, PATH, UNSPLASH, get_settings_arg
from splasher.downloader import AreaDetector, PreviewFetcher, WallpaperDownloader, WallpaperSetter

from . import icons_rc  # pylint: disable=unused-import


# The configuration of MainWindow
class MainWindow(QMainWindow):
    """
    The MainWindow class contains following functions:
    1. display a wallpaper,
    2. refresh, choose and download the displayed wallpaper,
    3. go to the settings window,
    4. show messages in the status bar.
    """

    def __init__(self) -> None:
        """
        Set the layout of MainWindow,
        wallpaper display is on the top side and takes up most of the space,
        with all buttons displayed in a row at the bottom.

                           960
        ------------------------------------------
        |                                        |
        |                                        |
        |                                        |
        |               wallpaper                |
        |                                        |  540
        |                                        |
        | -------------------------------------- |
        |    refresh   |  choose  |   download   | 24
        | -------------------------------------- |
        |              status bar                | 19
        ------------------------------------------
        """
        super().__init__()
        # ======== main window attributes ========
        self.setWindowTitle(APP["NAME"])
        self.setFixedSize(960, 540)
        self.logger: logging.Logger = logging.getLogger(__name__)
        # self.settings_window: Optional[SettingsWindow] = None
        self.manager: Optional[QNetworkAccessManager] = None
        # -------------------------------------------------------------
        # ======== draw ui ========
        self.draw_window_ui()
        self.set_preview()
        # -------------------------------------------------------------
        # ======== QNetWorkAccessManager ========
        self.init_manager()
        # -------------------------------------------------------------

    def draw_window_ui(self) -> None:
        """
        Draw the layouts, wallpaper, buttons and status bar.
        """
        # ======== layouts ========
        main_layout: QVBoxLayout = QVBoxLayout()
        # -------------------------------------------------------------
        # ======== display the wallpaper ========
        self.img_label: QLabel = QLabel()
        main_layout.addWidget(self.img_label)
        # -------------------------------------------------------------
        # ======== functional widgets ========
        self.func_layout: QHBoxLayout = QHBoxLayout()
        btns_h: int = self.draw_functional_bar()
        main_layout.addLayout(self.func_layout)
        # -------------------------------------------------------------
        # ======== status bar ========
        self.status_bar: QStatusBar = QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        main_layout.addWidget(self.status_bar)
        # -------------------------------------------------------------
        # ======== set QLabel size ========  # do not move the code
        img_label_h: int = self.height() - btns_h - self.status_bar.sizeHint().height()
        self.img_label.setFixedSize(self.width(), img_label_h)
        # -------------------------------------------------------------
        # ======== main layout styles ========
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # -------------------------------------------------------------
        # ======== main widget ========
        main_widget: QWidget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        # -------------------------------------------------------------

    def draw_functional_bar(self) -> int:
        """
        Draw some functional widgets.
        :return : buttons' height
        """
        # ======== refresh button ========
        refresh_btn: QPushButton = QPushButton("Refresh")
        refresh_btn.setToolTip("display a new picture")
        refresh_btn.setIcon(QIcon(":/buttons/refresh.png"))
        refresh_btn.clicked.connect(self.refresh)  # pylint: disable=no-member
        self.func_layout.addWidget(refresh_btn)
        # -------------------------------------------------------------
        # ======== choose button ========
        choose_btn: QPushButton = QPushButton("Choose")
        choose_btn.setToolTip("set the current picture as desktop wallpaper")
        choose_btn.setIcon(QIcon(":/buttons/choose.png"))
        choose_btn.clicked.connect(self.choose)  # pylint: disable=no-member
        self.func_layout.addWidget(choose_btn)
        # -------------------------------------------------------------
        # ======== download button ========
        download_btn: QPushButton = QPushButton("Download")
        download_btn.setToolTip("download the current picture")
        download_btn.setIcon(QIcon(":/buttons/download.png"))
        download_btn.clicked.connect(self.download)  # pylint: disable=no-member
        self.func_layout.addWidget(download_btn)
        # -------------------------------------------------------------
        # return buttons' height
        return refresh_btn.sizeHint().height()

    def set_preview(self) -> None:
        """
        Set a preivew image for QLabel and refresh.
        """
        res, img_subpath = get_settings_arg("PREVIEW")
        if res and img_subpath:
            img: QPixmap = QPixmap(f"{PATH['CACHE']}{img_subpath}.jpg")
            self.img_label.setPixmap(img)
            self.img_label.setScaledContents(True)  # adjust the image size to fit the window
            self.img_label.setAlignment(Qt.AlignCenter)
            self.img_label.repaint()
        elif not res:
            self.logger.error("Failed to get the value of 'PREVIEW' from 'settings.json'")

    def init_manager(self) -> None:
        """
        Init a QNetworkAccessManager to handle functions related to images.
        """
        self.manager: QNetworkAccessManager = QNetworkAccessManager(self)
        self.manager.setAutoDeleteReplies(True)
        self.manager.setTransferTimeout(5000)  # 5s
        # ======== detect area in order to use mirror site ========
        request: QNetworkRequest = QNetworkRequest(QUrl("https://www.google.com"))
        request.setTransferTimeout(500)  # 500ms
        AreaDetector(self).detect(self.manager.head(request))

    @Slot()
    def refresh(self) -> None:
        """
        Use 'PreviewFetcher' to load a previewed image.
        Create a network request and use 'get' function to precess the response.
        The image's resolution is based on the QLabel's size.
        """
        self.show_message("Attempt to fetch a new preview.")
        self.logger.info("The refresh button is clicked.")

        img_resolution: str = f"{self.img_label.size().width()}x{self.img_label.size().height()}"  # 960x497
        url: str = f"{UNSPLASH['SOURCE']}{img_resolution}"
        reply: QNetworkReply = self.manager.get(QNetworkRequest(QUrl(url)))
        PreviewFetcher(self).fetch_preview(reply)

    @Slot()
    def choose(self) -> None:
        """
        Set the current image as the desktop wallpaper.

        The image's resolution is based on the primary screen's resolution.
        Please refer to the documentation for the construction of the url path:
            https://unsplash.com/documentation#dynamically-resizable-images

        e.g. https://images.unsplash.com/photo-xxx?w=1920&h=1080&fit=crop&crop=faces,edges,entropy\
             &fm=jpg&q=95&dpr=1&cs=srgb
        CN mirror: https://dogefs.s3.ladydaily.com/~/source/unsplash/photo-xxx?...

        The request url args:
            w: image width
            h: image height
            fit: resize fit mode
            crop: crop mode
            fm: output format
            q: output quality
            dpr: device pixel ratio, based on device pixel ratio
            cs: color space
        """
        self.show_message("Attempt to set the current preview as desktop wallpaper.")
        self.logger.info("The choose button is clicked.")

        res, img_name = get_settings_arg("PREVIEW")
        _, is_cnm = get_settings_arg("CNM")
        if res and img_name:
            img_id: str = re.findall(r"photo-[0-9]{13}-[0-9a-z]{12}", img_name)[0]
            screen: QScreen = QGuiApplication.primaryScreen()
            screen_w: int = screen.size().width()
            screen_h: int = screen.size().height()
            ratio: int = ceil(screen.devicePixelRatio())  # default is 1 and the max is 5.
            api: str = UNSPLASH["IMAGES-MIRROR"] if is_cnm else UNSPLASH["IMAGES"]
            url: str = (f"{api}{img_id}?w={screen_w}&h={screen_h}&fit=crop&crop=faces,edges,entropy"
                        f"&fm=jpg&q=95&dpr={ratio}&cs=srgb")
            # ======== check the image's resolution ========
            subfolder: str = PATH["SUBFOLDER"]
            img_fullpath: str = f"{PATH['CACHE']}{subfolder}{img_id}.jpg"
            file_info: QFileInfo = QFileInfo(img_fullpath)
            if file_info.exists() and file_info.isFile():
                img: QPixmap = QPixmap(img_fullpath)
                img_w: int = img.size().width()
                img_h: int = img.size().height()
                if img_w != screen_w or img_h != screen_h:
                    # ======== send the request, download and set ========
                    reply: QNetworkReply = self.manager.get(QNetworkRequest(QUrl(url)))
                    WallpaperSetter(self).fetch_wallpaper(reply)
                else:
                    # ======== set the wallpaper only ========
                    WallpaperSetter(self).set_wallpaper(img_fullpath, f"{img_id}.jpg")
            else:
                self.logger.error("Failed to find the image file: '%s'", img_fullpath)
        else:
            self.logger.error("Failed to get the value of 'PREVIEW' from 'settings.json'")

    @Slot()
    def download(self) -> None:
        """
        Download the current image to the user-specified path.
        """
        self.show_message("Attempt to download the current preview.")
        self.logger.info("The download button is clicked.")

        res, img_name = get_settings_arg("PREVIEW")
        _, is_cnm = get_settings_arg("CNM")
        if res and img_name:
            img_id: str = re.findall(r"photo-[0-9]{13}-[0-9a-z]{12}", img_name)[0]
            img_path: str = QFileDialog.getSaveFileName(self,
                                                        "Save",
                                                        f"{QDir.homePath()}/{img_id}.jpg",
                                                        "Images (*.png *.jpg)",
                                                        options=QFileDialog.DontResolveSymlinks)[0]
            api: str = UNSPLASH["IMAGES-MIRROR"] if is_cnm else UNSPLASH["IMAGES"]
            url: str = f"{api}{img_id}"
            # ======== send the request and download ========
            if img_path:
                reply: QNetworkReply = self.manager.get(QNetworkRequest(QUrl(url)))
                WallpaperDownloader(self).download(reply, img_path)
        else:
            self.logger.error("Failed to get the value of 'PREVIEW' from 'settings.json'")

    def show_message(self, msg: str, timeout: int = 5000) -> None:
        """
        Show messages in the status bar.
        :param msg: message string.
        :param timeout: default timeout is 5000 ms.
        """
        self.status_bar.clearMessage()
        self.status_bar.showMessage(msg, timeout)
