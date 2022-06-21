from PySide6.QtCore import Slot
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QAction
from utils.global_variables import APP_NAME, ICONS_PATH


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
        self.app = QApplication.instance()  # get the current QApplication instance
        # ======== tray attributes ========
        self.setIcon(QIcon(ICONS_PATH + "logo.ico"))
        self.setToolTip(APP_NAME)
        self.activated.connect(self.handle_mouse_click)
        # -------------------------------------------------------------
        # ======== menu list ========
        self.menu = QMenu()
        self.setContextMenu(self.menu)  # add the menu to the tray
        # refresh and set a picture as the desktop wallpaper
        self.refresh_set_opt = QAction("Refresh and Set")
        self.refresh_set_opt.triggered.connect(self.refresh_and_set)
        self.menu.addAction(self.refresh_set_opt)
        # show the main window
        self.show_opt = QAction("Show")
        self.show_opt.triggered.connect(self.show_app)
        self.menu.addAction(self.show_opt)
        # quit the app
        self.quit_opt = QAction("Quit")
        self.quit_opt.triggered.connect(self.quit_app)
        self.menu.addAction(self.quit_opt)
        # -------------------------------------------------------------

    @Slot()
    def handle_mouse_click(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """
        Handle the mouse click, left click to open the main window;
        right click to open the menu, which is the default behavior.
        :param reason: mouse click behavior.
        """
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # left click
            self.show_app()

    @Slot()
    def refresh_and_set(self) -> None:
        """
        Refresh and set a picture as the desktop wallpaper
        :return: None
        """
        pass

    @Slot()
    def show_app(self) -> None:
        """
        Display the main window if it does not exist.
        :return: None
        """
        if self.app.main_window.isVisible() is False:
            self.app.main_window.show()
        else:
            self.app.main_window.status_bar.showMessage("The main window already exists!", 5000)

    @Slot()
    def quit_app(self) -> None:
        """
        Exit the app.
        :return: None
        """
        self.app.quit()
