from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDir
from .main_window import MainWindow
from .system_tray import SystemTray
from . import icons
from ..config import setup_env


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
        self.main_window: MainWindow = MainWindow()
        self.tray: SystemTray = SystemTray()
        setup_env()

    def display_widgets(self) -> None:
        """
        Display the main window and the system tray.
        """
        # ======== display the main window ========
        self.main_window.show()  # windows are hidden by default
        # -------------------------------------------------------------
        # ======== display the system tray ========
        if self.tray.isSystemTrayAvailable():
            self.setQuitOnLastWindowClosed(False)  # keep app running after closing all windows
            self.tray.show()
        else:
            self.main_window.status_bar.showMessage("The system tray can not be displayed!")
        # -------------------------------------------------------------

    @staticmethod
    def singleton_app_warning_msg() -> None:
        """
        Show a warning message if there is an app already.
        """
        err_msg: QMessageBox = QMessageBox()
        err_msg.setIcon(QMessageBox.Warning)
        err_msg.setWindowTitle("Error")
        err_msg.setText("The application is already running!")
        err_msg.exec()
