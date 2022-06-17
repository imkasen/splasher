from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QAction
from utils.global_variables import ICONS_PATH


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
        # -------------------------------------------------------------
        # ======== menu list ========
        self.menu = QMenu()
        self.setContextMenu(self.menu)  # add the menu to the tray
        # refresh and set a picture as the desktop wallpaper
        self.refresh_set_opt = QAction("Refresh and Set")
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

    def refresh_set(self) -> None:
        """
        Refresh and set a picture as the desktop wallpaper
        :return: None
        """
        pass

    def show_app(self) -> None:
        """
        Display the main window if it does not exist.
        :return: None
        """
        if self.app.main_window.isVisible() is False:
            self.app.main_window.show()
        else:
            self.app.main_window.status_bar.showMessage("The main window already exists!", 5000)

    def quit_app(self) -> None:
        """
        Exit the app.
        :return: None
        """
        self.app.quit()
