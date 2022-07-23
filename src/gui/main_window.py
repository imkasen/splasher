from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStatusBar
from PySide6.QtGui import QPixmap, QIcon
from .settings_window import SettingsWindow
from ..downloader import ImgDownloader
from . import icons_rc
from ..config import APP, PATH
import logging


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

        ------------------ 960 -------------------
        |                                        |
        |                                        |
        |                                        |
        |               wallpaper                |
        |                                       540
        |                                        |
        | -------------------------------------- |
        | refresh | choose | download | settings |
        | -------------------------------------- |
        |              status bar                |
        ------------------------------------------
        """
        super(MainWindow, self).__init__()
        # ======== main window attributes ========
        self.setWindowTitle(APP["NAME"])
        self.setFixedSize(960, 540)
        self.__logger: logging.Logger = logging.getLogger(__name__)
        self.__downloader: ImgDownloader = ImgDownloader(self)
        self.__settings_window: SettingsWindow | None = None
        # -------------------------------------------------------------
        # ======== draw ui ========
        self.__draw_window_ui()
        # -------------------------------------------------------------

    def __draw_window_ui(self) -> None:
        """
        Draw the layouts, wallpaper, buttons and status bar.
        """
        # ======== layouts ========
        main_layout: QVBoxLayout = QVBoxLayout()
        # -------------------------------------------------------------
        # ======== display the wallpaper ========
        main_layout.addWidget(self.__draw_wallpaper_ui())
        # -------------------------------------------------------------
        # ======== functional widgets ========
        main_layout.addLayout(self.__draw_functional_bar())
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

    def __draw_wallpaper_ui(self) -> QLabel:
        """
        Display a wallpaper.
        :return: QLabel
        """
        img_label: QLabel = QLabel()
        img: QPixmap = QPixmap(PATH["CACHE"] + "5f7563b1538140c5931ba0a773aac650.jpg")
        if img.isNull():  # if the image can not be found
            img_label.setFixedSize(960, 540)  # fix and keep the layouts the same
        img_label.setPixmap(img)
        img_label.setScaledContents(True)  # adjust the image size to fit the window
        img_label.setAlignment(Qt.AlignCenter)
        # return label
        return img_label

    def __draw_functional_bar(self) -> QHBoxLayout:
        """
        Draw some functional widgets.
        :return: QHBoxLayout
        """
        # layout
        func_layout: QHBoxLayout = QHBoxLayout()
        # refresh button
        refresh_btn: QPushButton = QPushButton("Refresh")
        refresh_btn.setToolTip("display a new picture")
        refresh_btn.setIcon(QIcon(":/buttons/refresh.png"))
        refresh_btn.clicked.connect(self.refresh)
        func_layout.addWidget(refresh_btn)
        # choose button
        choose_btn: QPushButton = QPushButton("Choose")
        choose_btn.setToolTip("set the current picture as desktop wallpaper")
        choose_btn.setIcon(QIcon(":/buttons/choose.png"))
        choose_btn.clicked.connect(self.choose)
        func_layout.addWidget(choose_btn)
        # download button
        download_btn: QPushButton = QPushButton("Download")
        download_btn.setToolTip("download the current picture")
        download_btn.setIcon(QIcon(":/buttons/download.png"))
        download_btn.clicked.connect(self.download)
        func_layout.addWidget(download_btn)
        # settings button
        settings_btn: QPushButton = QPushButton("Settings")
        settings_btn.setToolTip("open the settings window")
        settings_btn.setIcon(QIcon(":/buttons/settings.png"))
        settings_btn.clicked.connect(self.__open_settings_window)
        func_layout.addWidget(settings_btn)
        # return layout
        return func_layout

    @Slot()
    def refresh(self) -> None:
        """
        Use 'ImgDownloader' to load a preview image.
        """
        self.show_message("Attempt to fetch a new preview wallpaper.")
        self.__logger.info("Attempt to fetch a new preview wallpaper.")
        self.__downloader.send_request()

    @Slot()
    def choose(self) -> None:
        self.show_message("Set the picture as wallpaper!")
        self.__logger.info("Set the picture as wallpaper.")

    @Slot()
    def download(self) -> None:
        self.show_message("Download the wallpaper!")
        self.__logger.info("Download the wallpaper.")

    @Slot()
    def __open_settings_window(self) -> None:
        """
        Open the settings window if it does not exist.
        """
        if self.__settings_window is None \
                or self.__settings_window.isVisible() is False:
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
