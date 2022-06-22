from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStatusBar, QComboBox
)
from PySide6.QtGui import QPixmap, QIcon
from utils.env import APP_NAME, ICONS_PATH, CACHE_PATH
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
        self.__settings_window = None
        self.setWindowTitle(APP_NAME)
        self.setFixedSize(960, 540)
        self.setWindowIcon(QIcon(ICONS_PATH + "logo.ico"))
        # -------------------------------------------------------------
        # ======== layouts ========
        main_layout = QVBoxLayout()
        # -------------------------------------------------------------
        # ======== display the wallpaper ========
        self.__draw_wallpaper_ui(main_layout)
        # -------------------------------------------------------------
        # ======== functional widgets ========
        self.__draw_functional_bar(main_layout)
        # -------------------------------------------------------------
        # ======== status bar ========
        self.__status_bar = QStatusBar()
        self.__status_bar.setSizeGripEnabled(False)
        # -------------------------------------------------------------
        # ======== main layout styles ========
        main_layout.addWidget(self.__status_bar)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # -------------------------------------------------------------
        # ======== main widget ========
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        # -------------------------------------------------------------

    def __draw_wallpaper_ui(self, main_layout: QVBoxLayout) -> None:
        """
        Display the wallpaper.
        """
        img_label = QLabel()
        img = QPixmap(CACHE_PATH + "5f7563b1538140c5931ba0a773aac650.jpg")
        if img.isNull():  # if the image can not be found
            img_label.setFixedSize(960, 540)  # fix and keep the layouts the same
        img_label.setPixmap(img)
        img_label.setScaledContents(True)  # adjust the image size to fit the window
        img_label.setAlignment(Qt.AlignCenter)
        # add to main layout
        main_layout.addWidget(img_label)

    def __draw_functional_bar(self, main_layout: QVBoxLayout) -> None:
        """
        Functional widgets.
        """
        # layout
        func_layout = QHBoxLayout()
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
        settings_btn.clicked.connect(self.__open_settings_window)
        func_layout.addWidget(settings_btn)
        # add to main layout
        main_layout.addLayout(func_layout)

    @Slot()
    def refresh(self) -> None:
        self.__status_bar.showMessage("Refresh the picture!", 5000)

    @Slot()
    def choose(self) -> None:
        self.__status_bar.showMessage("Set the picture as wallpaper!", 5000)

    @Slot()
    def download(self) -> None:
        self.__status_bar.showMessage("Download the wallpaper!", 5000)

    @Slot()
    def __open_settings_window(self) -> None:
        """
        Open the settings window if it does not exist.
        """
        if self.__settings_window is None:
            self.__settings_window = SettingsWindow()
        self.__settings_window.show()
