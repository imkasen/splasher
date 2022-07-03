from PySide6.QtCore import Slot, QCoreApplication
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QAction
from . import icons_rc
from ..config import APP


# The configuration of SystemTray
class SystemTray(QSystemTrayIcon):
    """
    The SystemTray class which contains following functions:
    1. show the app
    2. quit the app
    """

    def __init__(self) -> None:
        """
        Set the content of system tray, add multiple functions into the menu.
        :return: None
        """
        super(SystemTray, self).__init__()
        self.__app: QCoreApplication | None = QApplication.instance()  # get the current QApplication instance
        # ======== tray attributes ========
        self.setIcon(QIcon(":/logo.png"))
        self.setToolTip(APP["name"])
        self.activated.connect(self.__handle_mouse_click)
        # -------------------------------------------------------------
        # ======== menu list ========
        menu: QMenu = QMenu()
        self.setContextMenu(menu)  # add the menu to the system tray
        # show the main window
        show_act: QAction = QAction("Show", parent=menu)
        show_act.triggered.connect(self.__show_app)
        menu.addAction(show_act)
        # quit the app
        quit_act: QAction = QAction("Quit", parent=menu)
        quit_act.triggered.connect(self.__quit_app)
        menu.addAction(quit_act)
        # -------------------------------------------------------------

    @Slot()
    def __handle_mouse_click(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """
        Handle the mouse click, left click to open the main window;
        right click to open the menu, which is the default behavior.
        :param reason: mouse click behavior.
        """
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # left click
            self.__show_app()

    @Slot()
    def __show_app(self) -> None:
        """
        Display the main window if it does not exist, otherwise show the main window on the top.
        """
        if self.__app.main_window.isVisible() is False:
            self.__app.main_window.show()
        elif self.__app.main_window.isMinimized():
            self.__app.main_window.showNormal()
        else:
            self.__app.main_window.activateWindow()
            self.__app.main_window.raise_()

    @Slot()
    def __quit_app(self) -> None:
        """
        Exit the app.
        """
        self.__app.quit()
