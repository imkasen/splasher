from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStatusBar, QComboBox
)
from PySide6.QtGui import QPixmap, QIcon
from utils.global_variables import APP_NAME, ICONS_PATH, CACHE_PATH
from gui.settings_window import SettingsWindow


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
        self.settings_window = None
        self.setWindowTitle(APP_NAME)
        self.setFixedSize(960, 540)
        self.setWindowIcon(QIcon(ICONS_PATH + "logo.ico"))
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
        # theme lists
        theme_box = QComboBox()
        # ...
        func_layout.addWidget(theme_box)
        # refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setToolTip("display a new picture")
        refresh_btn.setIcon(QIcon(ICONS_PATH + "buttons/refresh.png"))
        refresh_btn.clicked.connect(self.refresh)
        func_layout.addWidget(refresh_btn)
        # choose button
        choose_btn = QPushButton("Choose")
        choose_btn.setToolTip("set the current picture as desktop wallpaper")
        choose_btn.setIcon(QIcon(ICONS_PATH + "buttons/choose.png"))
        choose_btn.clicked.connect(self.choose)
        func_layout.addWidget(choose_btn)
        # download button
        download_btn = QPushButton("Download")
        download_btn.setToolTip("download the current picture")
        download_btn.setIcon(QIcon(ICONS_PATH + "buttons/download.png"))
        download_btn.clicked.connect(self.download)
        func_layout.addWidget(download_btn)
        # settings button
        settings_btn = QPushButton("Settings")
        settings_btn.setToolTip("open the settings window")
        settings_btn.setIcon(QIcon(ICONS_PATH + "buttons/settings.png"))
        settings_btn.clicked.connect(self.open_settings_window)
        func_layout.addWidget(settings_btn)
        # -------------------------------------------------------------
        # ======== status bar ========
        self.status_bar = QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        # -------------------------------------------------------------
        # ======== main layout styles ========
        main_layout.addWidget(img_label)
        main_layout.addLayout(func_layout)
        main_layout.addWidget(self.status_bar)
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
        self.status_bar.showMessage("Refresh the picture!", 5000)

    @Slot()
    def choose(self) -> None:
        self.status_bar.showMessage("Set the picture as wallpaper!", 5000)

    @Slot()
    def download(self) -> None:
        self.status_bar.showMessage("Download the wallpaper!", 5000)

    @Slot()
    def open_settings_window(self) -> None:
        """
        Open the settings window if it does not exist.
        :return: None
        """
        if self.settings_window is None:
            self.settings_window = SettingsWindow()
        self.settings_window.show()
