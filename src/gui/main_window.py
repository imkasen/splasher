from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStatusBar, QComboBox
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
        self.__logger: logging.Logger = logging.getLogger(__name__)
        self.__downloader: ImgDownloader = ImgDownloader()
        # ======== main window attributes ========
        self.__settings_window: SettingsWindow | None = None
        self.setWindowTitle(APP["name"])
        self.setFixedSize(960, 540)
        # -------------------------------------------------------------
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
        self.status_bar: QStatusBar = QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        main_layout.addWidget(self.status_bar)
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
        Display the wallpaper.
        """
        img_label: QLabel = QLabel()
        img: QPixmap = QPixmap(PATH["cache"] + "5f7563b1538140c5931ba0a773aac650.jpg")
        if img.isNull():  # if the image can not be found
            img_label.setFixedSize(960, 540)  # fix and keep the layouts the same
        img_label.setPixmap(img)
        img_label.setScaledContents(True)  # adjust the image size to fit the window
        img_label.setAlignment(Qt.AlignCenter)
        # return label
        return img_label

    def __draw_functional_bar(self) -> QHBoxLayout:
        """
        Functional widgets.
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
        self.status_bar.showMessage("Fetch a new wallpaper.", 5000)
        self.__logger.info("Fetch a new wallpaper.")
        self.__downloader.send_request()

    @Slot()
    def choose(self) -> None:
        self.status_bar.showMessage("Set the picture as wallpaper!", 5000)
        self.__logger.info("Set the picture as wallpaper.")

    @Slot()
    def download(self) -> None:
        self.status_bar.showMessage("Download the wallpaper!", 5000)
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
