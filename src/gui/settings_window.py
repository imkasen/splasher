from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QWidget, QTabWidget, QLabel
)
from PySide6.QtGui import QPixmap, QIcon
from config.env import (
    APP_NAME, APP_VERSION, APP_AUTHOR, APP_ADDR,
)
import gui.icons


# The configuration of SettingsWindow
class SettingsWindow(QTabWidget):
    """
    The SettingsWindow class which contains following functions:
    1. display and set the file path,
    2. update wallpapers regularly and set the resolution of the preview image,
    3. display the app info.
    """
    def __init__(self) -> None:
        """
        Set the layout of SettingsWindow.
        """
        # ======== settings window attributes ========
        super(SettingsWindow, self).__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(480, 270)
        # -------------------------------------------------------------
        # ======== tabs design ========
        self.__draw_path_tab()
        self.__draw_update_tab()
        self.__draw_info_tab()
        # -------------------------------------------------------------

    def __draw_path_tab(self) -> None:
        """
        Set the path tab layout,
        here the paths to files are displayed and can be modified.
        """
        # ======== declaration and add the tab ========
        path_tab = QWidget()
        self.addTab(path_tab, QIcon(":/tabs/path.png"), "Path")
        # -------------------------------------------------------------

    def __draw_update_tab(self) -> None:
        """
        Set the update tab layout,
        here users can set the update frequency and the preview resolution.
        """
        # ======== declaration and add the tab ========
        update_tab = QWidget()
        self.addTab(update_tab, QIcon(":/tabs/update.png"), "Update")
        # -------------------------------------------------------------

    def __draw_info_tab(self) -> None:
        """
        Set the info tab layout,
        here shows the app's information.
        """
        # ======== declaration and add the tab ========
        info_tab = QWidget()
        self.addTab(info_tab, QIcon(":/tabs/info.png"), "About")
        # -------------------------------------------------------------
        # ======== layout ========
        layout = QVBoxLayout()
        ico_layout = QHBoxLayout()
        layout.setSpacing(10)
        info_tab.setLayout(layout)
        # -------------------------------------------------------------
        # ======== widgets ========
        # icon
        ico_label = QLabel()
        ico_label.setPixmap(QPixmap(":/logo.png"))
        ico_label.setFixedSize(50, 50)
        ico_label.setScaledContents(True)
        ico_label.setAlignment(Qt.AlignCenter)
        # app name
        name_label = QLabel(APP_NAME)
        name_label.setScaledContents(True)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-weight: bold")
        name_label.setFixedHeight(name_label.fontMetrics().height())
        # version
        ver_label = QLabel("Version: " + APP_VERSION)
        ver_label.setScaledContents(True)
        ver_label.setAlignment(Qt.AlignCenter)
        ver_label.setFixedHeight(name_label.fontMetrics().height())
        # author
        author_label = QLabel("Author: " + APP_AUTHOR)
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setFixedHeight(name_label.fontMetrics().height())
        # web address
        addr_label = QLabel()
        addr_label.setText(f"<a href='{APP_ADDR}'>GitHub</a>")
        addr_label.setOpenExternalLinks(True)
        addr_label.setAlignment(Qt.AlignCenter)
        addr_label.setFixedHeight(addr_label.fontMetrics().height())
        # add widgets into the layout
        layout.addStretch()
        ico_layout.addStretch()
        ico_layout.addWidget(ico_label)
        ico_layout.addStretch()
        layout.addLayout(ico_layout)
        layout.addWidget(name_label)
        layout.addWidget(ver_label)
        layout.addWidget(author_label)
        layout.addWidget(addr_label)
        layout.addStretch()
        # -------------------------------------------------------------


