from PySide6.QtCore import QSize
from PySide6.QtWidgets import QTabWidget


# The configuration of SettingsWindow
class SettingsWindow(QTabWidget):
    """
    The SettingsWindow class which contains following functions:
    1. display and set the file save path,
    2. update wallpapers regularly and set the resolution of the preview image,
    3. display the app info,
    """
    def __init__(self) -> None:
        """
        Set the layout of SettingsWindow
        """
        # ======== settings window attributes ========
        super(SettingsWindow, self).__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(QSize(480, 270))
        # -------------------------------------------------------------
