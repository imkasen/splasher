from PySide6.QtCore import Slot, QCoreApplication
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QAction
from config.env import APP
import gui.icons


# The configuration of SystemTray
class SystemTray(QSystemTrayIcon):
    """
    The SystemTray class which contains following functions:
    1. refresh and set a wallpaper
    2. show the app
    3. quit the app
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
        # refresh and set a picture as the desktop wallpaper
        refresh_set_act: QAction = QAction("Refresh and Set", parent=menu)
        refresh_set_act.triggered.connect(self.__refresh_and_set)
        menu.addAction(refresh_set_act)
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
    def __refresh_and_set(self) -> None:
        """
        Refresh and set a picture as the desktop wallpaper.
        """
        pass

    @Slot()
    def __show_app(self) -> None:
        """
        Display the main window if it does not exist, otherwise show the main window on the top.
        """
        if self.__app.main_window.isVisible() is False:
            self.__app.main_window.show()
        else:
            self.__app.main_window.activateWindow()
            self.__app.main_window.raise_()

    @Slot()
    def __quit_app(self) -> None:
        """
        Exit the app.
        """
        self.__app.quit()
