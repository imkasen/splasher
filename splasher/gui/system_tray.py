from typing import Optional

from PySide6.QtCore import QCoreApplication, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from splasher.config import APP

from . import icons_rc  # pylint: disable=unused-import
from .main_window import MainWindow
from .settings_window import SettingsWindow


# The configuration of SystemTray
class SystemTray(QSystemTrayIcon):
    """
    The SystemTray class contains following functions:
    1. show the app
    2. quit the app
    """

    def __init__(self) -> None:
        """
        Set the content of system tray, add multiple functions into the menu.
        :return: None
        """
        super().__init__()
        self.app: Optional[QCoreApplication] = QCoreApplication.instance()  # get the current QApplication instance
        if self.app is not None:
            self.main_window: MainWindow = self.app.main_window
            self.settings_window: Optional[SettingsWindow] = self.app.settings_window
        # ======== tray attributes ========
        self.setIcon(QIcon(":/logo.png"))
        self.setToolTip(APP["NAME"])
        self.activated.connect(self.handle_mouse_click)  # pylint: disable=no-member
        # -------------------------------------------------------------
        # ======== menu list ========
        menu: QMenu = QMenu()
        self.setContextMenu(menu)  # add the menu to the system tray
        # show the main window
        show_act: QAction = QAction("Show", parent=menu)
        show_act.triggered.connect(self.show_app)  # pylint: disable=no-member
        menu.addAction(show_act)
        # show the settings window
        set_act: QAction = QAction("Set", parent=menu)
        set_act.triggered.connect(self.set_app)  # pylint: disable=no-member
        menu.addAction(set_act)
        # quit the app
        quit_act: QAction = QAction("Quit", parent=menu)
        quit_act.triggered.connect(self.quit_app)  # pylint: disable=no-member
        menu.addAction(quit_act)
        # -------------------------------------------------------------

    @Slot(QSystemTrayIcon.ActivationReason)
    def handle_mouse_click(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """
        Handle the mouse click, left click to open the main window;
        right click to open the menu, which is the default behavior.
        :param reason: mouse click behavior.
        """
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # left click
            self.show_app()

    @Slot()
    def show_app(self) -> None:
        """
        Display the main window if it does not exist, otherwise show the main window on the top.
        """
        if not self.main_window.isVisible():
            self.main_window.show()
        elif self.main_window.isMinimized():
            self.main_window.showNormal()
        elif not self.main_window.isActiveWindow():  # put the settings window on the top
            self.main_window.activateWindow()
            self.main_window.raise_()

    @Slot()
    def set_app(self) -> None:
        """
        Open the settings window if it does not exist.
        """
        if self.settings_window is None \
                or not self.settings_window.isVisible():
            self.settings_window = SettingsWindow()
            self.settings_window.show()
        elif self.settings_window.isMinimized():
            self.settings_window.showNormal()

    @Slot()
    def quit_app(self) -> None:
        """
        Exit the app.
        """
        self.app.quit()
