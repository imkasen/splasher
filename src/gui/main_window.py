from typing import Optional
import logging
from PySide6.QtCore import Qt, Slot, QUrl
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStatusBar
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from .settings_window import SettingsWindow
from ..downloader import PreviewFetcher
from . import icons_rc  # pylint: disable=unused-import
from ..config import APP, PATH, UNSPLASH, get_settings_arg


# The configuration of MainWindow
class MainWindow(QMainWindow):
    """
    The MainWindow class which contains following functions:
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
        | refresh | choose | download | settings | 24
        | -------------------------------------- |
        |              status bar                | 19
        ------------------------------------------
        """
        super().__init__()
        # ======== main window attributes ========
        self.setWindowTitle(APP["NAME"])
        self.setFixedSize(960, 540)
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.settings_window: Optional[SettingsWindow] = None
        self.manager: Optional[QNetworkAccessManager] = None
        # -------------------------------------------------------------
        # ======== draw ui ========
        self.draw_window_ui()
        self.set_image()
        # -------------------------------------------------------------
        # ======== network ========
        self.init_network()
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
        # ======== set QLabel size ========
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
        # ======== settings button ========
        settings_btn: QPushButton = QPushButton("Settings")
        settings_btn.setToolTip("open the settings window")
        settings_btn.setIcon(QIcon(":/buttons/settings.png"))
        settings_btn.clicked.connect(self.open_settings_window)  # pylint: disable=no-member
        self.func_layout.addWidget(settings_btn)
        # -------------------------------------------------------------
        # return buttons' height
        return settings_btn.sizeHint().height()

    def set_image(self) -> None:
        """
        Set a preivew image for QLabel and refresh.
        """
        res: bool = False
        img_name: str = ""
        res, img_name = get_settings_arg("PREVIEW")
        if not res:
            self.logger.error("Failed to get the value of 'PREVIEW' from 'settings.json'")
        img: QPixmap = QPixmap(PATH["CACHE"] + img_name)
        self.img_label.setPixmap(img)
        self.img_label.setScaledContents(True)  # adjust the image size to fit the window
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.repaint()

    def init_network(self) -> None:
        """
        Init a QNetworkAccessManager to handle functions related to images.
        """
        self.manager: QNetworkAccessManager = QNetworkAccessManager(self)
        self.manager.setAutoDeleteReplies(True)
        self.manager.setTransferTimeout(10000)  # 10s

    @Slot()
    def refresh(self) -> None:
        """
        Use 'ImgDownloader' to load a previewed image.
        """
        self.show_message("Attempt to fetch a new image.")
        self.logger.info("The refresh button is clicked.")
        img_resolution: str = str(self.img_label.size().width()) + "x" + str(self.img_label.size().height())
        fetcher: PreviewFetcher = PreviewFetcher(self)
        reply: QNetworkReply = self.manager.get(QNetworkRequest(QUrl(UNSPLASH["SOURCE"] + img_resolution)))
        fetcher.fetch_image(reply)

    @Slot()
    def choose(self) -> None:
        """
        Set the current image as the desktop wallpaper.
        """
        self.show_message("Attempt to set the current preview as desktop wallpaper.")
        self.logger.info("The choose button is clicked.")

    @Slot()
    def download(self) -> None:
        """
        Download the current image to the user-specified path.
        """
        self.show_message("Download the wallpaper!")
        self.logger.info("Download the wallpaper.")

    @Slot()
    def open_settings_window(self) -> None:
        """
        Open the settings window if it does not exist.
        """
        if self.settings_window is None \
                or not self.settings_window.isVisible():
            self.settings_window = SettingsWindow()
            self.settings_window.show()
        elif self.settings_window.isMinimized():
            self.settings_window.showNormal()

    def show_message(self, msg: str, timeout: int = 5000) -> None:
        """
        Show messages in the status bar.
        :param msg: message string.
        :param timeout: default timeout is 5000 ms.
        """
        self.status_bar.clearMessage()
        self.status_bar.showMessage(msg, timeout)
