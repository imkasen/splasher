from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel
)
from PySide6.QtGui import QPixmap


# The configuration of MainWindow
class MainWindow(QMainWindow):  # subclass QMainWindow to customize the application's main window
    """
    the MainWindow class which contains following functions:
    1. display a wallpaper,
    2. refresh, choose and download the displayed wallpaper,
    3. go to the settings window
    """
    def __init__(self) -> None:
        """
        set the layout of MainWindow
        """
        super(MainWindow, self).__init__()
        self.setWindowTitle("Unsplash Wallpaper")
        self.setFixedSize(QSize(800, 600))

        # ======== layouts ========
        main_layout = QVBoxLayout()
        func_layout = QHBoxLayout()
        # -------------------------------------------------------------
        # ======== display the wallpaper ========
        img_label = QLabel()
        img = QPixmap("/home/kasen/Downloads/benoit-deschasaux-JjmUwcy7HUM-unsplash.jpg")
        img_label.setPixmap(img)
        img_label.setScaledContents(True)  # fit the window
        img_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(img_label)
        # -------------------------------------------------------------
        # ======== functional widgets ========
        # theme list
        # theme_box = QComboBox()
        # ...
        # refresh button
        btn_refresh = QPushButton("Refresh")
        btn_refresh.setToolTip("Show a new picture.")
        btn_refresh.clicked.connect(self.refresh)
        func_layout.addWidget(btn_refresh)
        # choose button
        btn_choose = QPushButton("Choose")
        btn_choose.setToolTip("Set the current picture as the desktop wallpaper.")
        btn_choose.clicked.connect(self.choose)
        func_layout.addWidget(btn_choose)
        # download button
        btn_download = QPushButton("Download")
        btn_download.setToolTip("Download the current picture.")
        btn_download.clicked.connect(self.download)
        func_layout.addWidget(btn_download)
        # settings button
        btn_settings = QPushButton("Settings")
        btn_settings.setToolTip("Open the settings window.")
        btn_settings.clicked.connect(self.open_settings_window)
        func_layout.addWidget(btn_settings)
        # -------------------------------------------------------------
        # ======== main layout styles ========
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
