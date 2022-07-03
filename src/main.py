from PySide6.QtCore import QLockFile
from PySide6.QtWidgets import QMessageBox
from .gui import Application
from .config import PATH


def main() -> None:
    """
    The entry function of the application.
    """
    applock: QLockFile = QLockFile(PATH["applock"])  # make sure only one program can run
    try:
        app: Application = Application()  # only one QApplication instance per application
        if applock.tryLock():
            app.display_widgets()
            app.exec()  # start the event loop
        else:
            QMessageBox.warning(None, "Error", "The application is already running!")
    finally:
        applock.unlock()
