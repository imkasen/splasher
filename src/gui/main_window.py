from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel
)
from PySide6.QtGui import QPixmap, QIcon
from utils.global_variables import ICONS_PATH, CACHE_PATH


# The configuration of MainWindow
class MainWindow(QMainWindow):  # subclass 'QMainWindow' to customize the application's main window
    """
    The MainWindow class which contains following functions:
    1. display a wallpaper,
    2. refresh, choose and download the displayed wallpaper,
    3. go to the settings window
    """
    def __init__(self) -> None:
        """
        Set the layout of MainWindow,
        wallpaper display is on the top side and takes up most of the space,
        with all buttons displayed in a row at the bottom.

        ------------------ 800 -------------------
        |                                        |
        |                                        |
        |                                        |
        |               wallpaper               600
        |                                        |
        |                                        |
        | -------------------------------------- |
        | refresh | choose | download | settings |
        ------------------------------------------
        """
        # ======== main window attributes ========
        super(MainWindow, self).__init__()
        self.setWindowTitle("Unsplash Wallpapers for Linux")
        self.setFixedSize(QSize(800, 600))
        self.setWindowIcon(QIcon(ICONS_PATH + "logo.png"))
        # -------------------------------------------------------------
        # ======== layouts ========
        main_layout = QVBoxLayout()
        func_layout = QHBoxLayout()
        # -------------------------------------------------------------
        # ======== display the wallpaper ========
        img_label = QLabel()
        img = QPixmap(CACHE_PATH + "photo-1652889946318-9085b5a2d4e7.jpeg")
        img_label.setPixmap(img)
        img_label.setScaledContents(True)  # adjust the image size to fit the window
        img_label.setAlignment(Qt.AlignCenter)
        # -------------------------------------------------------------
        # ======== functional widgets ========
        # theme list
        # theme_box = QComboBox()
        # ...
        # refresh button
        btn_refresh = QPushButton("Refresh")
        btn_refresh.setToolTip("display a new picture")
        btn_refresh.setIcon(QIcon(ICONS_PATH + "buttons/refresh.png"))
        btn_refresh.clicked.connect(self.refresh)
        func_layout.addWidget(btn_refresh)
        # choose button
        btn_choose = QPushButton("Choose")
        btn_choose.setToolTip("set the current picture as desktop wallpaper")
        btn_choose.setIcon(QIcon(ICONS_PATH + "buttons/choose.png"))
        btn_choose.clicked.connect(self.choose)
        func_layout.addWidget(btn_choose)
        # download button
        btn_download = QPushButton("Download")
        btn_download.setToolTip("download the current picture")
        btn_download.setIcon(QIcon(ICONS_PATH + "buttons/download.png"))
        btn_download.clicked.connect(self.download)
        func_layout.addWidget(btn_download)
        # settings button
        btn_settings = QPushButton("Settings")
        btn_settings.setToolTip("open the settings window")
        btn_settings.setIcon(QIcon(ICONS_PATH + "buttons/settings.png"))
        btn_settings.clicked.connect(self.open_settings_window)
        func_layout.addWidget(btn_settings)
        # -------------------------------------------------------------
        # ======== main layout styles ========
        main_layout.addWidget(img_label)
        main_layout.addLayout(func_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # -------------------------------------------------------------
        # ======== main widget ========
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        # -------------------------------------------------------------

    @Slot()
    def refresh(self) -> None:
        print("Refresh the picture!")

    @Slot()
    def choose(self) -> None:
        print("Set the picture as wallpaper")

    @Slot()
    def download(self) -> None:
        print("Download the wallpaper!")

    @Slot()
    def open_settings_window(self) -> None:
        print("Open the window of Settings!")
