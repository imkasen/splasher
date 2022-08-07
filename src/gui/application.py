import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from .main_window import MainWindow
from .system_tray import SystemTray
from . import icons_rc  # pylint: disable=unused-import


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
        super().__init__([])  # no command line arguments
        self.setWindowIcon(QIcon(":/logo.png"))  # QResource system
        self.main_window: MainWindow = MainWindow()
        self.tray: SystemTray = SystemTray()

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
            self.main_window.show_message("The system tray can not be displayed!", 0)
            logging.getLogger(__name__).critical("The system tray can not be displayed!")
        # -------------------------------------------------------------
