from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDir
from gui.main_window import MainWindow
from gui.system_tray import SystemTray
import gui.icons
from config.env import CACHE_PATH


# The configuration of Application
class Application(QApplication):
    """
    The Application class which contains following functions:
    1. draw the main window
    2. draw the system tray
    """
    def __init__(self) -> None:
        """
        Draw the main window and the system tray.
        """
        super(Application, self).__init__([])  # no command line arguments
        self.setWindowIcon(QIcon(":/logo.png"))  # QResource system
        self.main_window = None
        self.tray = None
        self.__init_env()

    @staticmethod
    def __init_env():
        """
        Initialize various environment settings:
        1. check if the cache folder exists, if not, create it.
        """
        # ======== check the cache dir ========
        cache_dir = QDir(CACHE_PATH)
        if not cache_dir.exists():
            cache_dir.mkpath(CACHE_PATH)
        # -------------------------------------------------------------

    def draw_main_window(self) -> None:
        """
        Display the main window.
        """
        if self.main_window is None:
            self.main_window = MainWindow()
            self.main_window.show()  # windows are hidden by default

    def draw_system_tray(self) -> None:
        """
        Display the system tray.
        """
        if self.tray is None:
            self.tray = SystemTray()
            if self.tray.isSystemTrayAvailable():
                self.setQuitOnLastWindowClosed(False)  # keep app running after closing all windows
                self.tray.show()
            else:
                self.main_window.status_bar.showMessage("The system tray can not be displayed!")

    @staticmethod
    def singleton_app_warning_msg() -> None:
        """
        Show a warning message if there is an app already.
        """
        err_msg = QMessageBox()
        err_msg.setIcon(QMessageBox.Warning)
        err_msg.setWindowTitle("Error")
        err_msg.setText("The application is already running!")
        err_msg.exec()
