from typing import Optional
import logging
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStatusBar
from PySide6.QtGui import QPixmap, QIcon
from .settings_window import SettingsWindow
from ..downloader import ImgDownloader
from . import icons_rc  # pylint: disable=unused-import
from ..config import APP, PATH, get_settings_arg


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
        super(MainWindow, self).__init__()
        # ======== main window attributes ========
        self.setWindowTitle(APP["NAME"])
        self.setFixedSize(960, 540)
        self.__logger: logging.Logger = logging.getLogger(__name__)
        self.__downloader: ImgDownloader = ImgDownloader(self)
        self.__settings_window: Optional[SettingsWindow] = None
        self.img_label: QLabel = QLabel()
        # -------------------------------------------------------------
        # ======== draw ui ========
        self.__draw_window_ui()
        self.set_image()
        # -------------------------------------------------------------

    def __draw_window_ui(self) -> None:
        """
        Draw the layouts, wallpaper, buttons and status bar.
        """
        # ======== layouts ========
        main_layout: QVBoxLayout = QVBoxLayout()
        # -------------------------------------------------------------
        # ======== display the wallpaper ========
        main_layout.addWidget(self.img_label)
        # -------------------------------------------------------------
        # ======== functional widgets ========
        self.__func_layout: QHBoxLayout = QHBoxLayout()
        self.__draw_functional_bar()
        main_layout.addLayout(self.__func_layout)
        # -------------------------------------------------------------
        # ======== status bar ========
        self.__status_bar: QStatusBar = QStatusBar()
        self.__status_bar.setSizeGripEnabled(False)
        main_layout.addWidget(self.__status_bar)
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

    def set_image(self) -> None:
        """
        Set a preivew image for QLabel and refresh.
        """
        res: bool = False
        img_name: str = ""
        res, img_name = get_settings_arg("PREVIEW")
        if not res:
            self.__logger.error("Failed to get the value of 'PREVIEW' from 'settings.json'")
        img: QPixmap = QPixmap(PATH["CACHE"] + img_name)
        if img.isNull():  # if the image can not be found
            img_h: int = self.height() - self.__func_layout.sizeHint().height() - self.__status_bar.sizeHint().height()
            self.img_label.setFixedSize(self.width(), img_h)  # fix and keep the layouts the same
        self.img_label.setPixmap(img)
        self.img_label.setScaledContents(True)  # adjust the image size to fit the window
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.repaint()

    def __draw_functional_bar(self) -> None:
        """
        Draw some functional widgets.
        """
        # refresh button
        refresh_btn: QPushButton = QPushButton("Refresh")
        refresh_btn.setToolTip("display a new picture")
        refresh_btn.setIcon(QIcon(":/buttons/refresh.png"))
        refresh_btn.clicked.connect(self.refresh)  # pylint: disable=no-member
        self.__func_layout.addWidget(refresh_btn)
        # choose button
        choose_btn: QPushButton = QPushButton("Choose")
        choose_btn.setToolTip("set the current picture as desktop wallpaper")
        choose_btn.setIcon(QIcon(":/buttons/choose.png"))
        choose_btn.clicked.connect(self.choose)  # pylint: disable=no-member
        self.__func_layout.addWidget(choose_btn)
        # download button
        download_btn: QPushButton = QPushButton("Download")
        download_btn.setToolTip("download the current picture")
        download_btn.setIcon(QIcon(":/buttons/download.png"))
        download_btn.clicked.connect(self.download)  # pylint: disable=no-member
        self.__func_layout.addWidget(download_btn)
        # settings button
        settings_btn: QPushButton = QPushButton("Settings")
        settings_btn.setToolTip("open the settings window")
        settings_btn.setIcon(QIcon(":/buttons/settings.png"))
        settings_btn.clicked.connect(self.__open_settings_window)  # pylint: disable=no-member
        self.__func_layout.addWidget(settings_btn)

    @Slot()
    def refresh(self) -> None:
        """
        Use 'ImgDownloader' to load a previewed image.
        """
        self.show_message("Attempt to fetch a new previewed image.", 0)
        self.__logger.info("Attempt to fetch a new previewed image.")
        self.__downloader.send_request()

    @Slot()
    def choose(self) -> None:
        """
        Set the current image as the desktop wallpaper.
        """
        self.show_message("Set the picture as wallpaper!")
        self.__logger.info("Set the picture as wallpaper.")

    @Slot()
    def download(self) -> None:
        """
        Download the current image to the user-specified path.
        """
        self.show_message("Download the wallpaper!")
        self.__logger.info("Download the wallpaper.")

    @Slot()
    def __open_settings_window(self) -> None:
        """
        Open the settings window if it does not exist.
        """
        if self.__settings_window is None \
                or not self.__settings_window.isVisible():
            self.__settings_window = SettingsWindow()
            self.__settings_window.show()
        elif self.__settings_window.isMinimized():
            self.__settings_window.showNormal()

    def show_message(self, msg: str, timeout: int = 5000) -> None:
        """
        Show some messages in the status bar.
        :param msg: message string.
        :param timeout: default timeout is 5000 ms.
        """
        self.__status_bar.showMessage(msg, timeout)
