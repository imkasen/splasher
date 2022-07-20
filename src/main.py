from PySide6.QtCore import QLockFile
from PySide6.QtWidgets import QMessageBox
from .gui import Application
from .config import PATH, init_app
import logging


def main() -> None:
    """
    The main function of the application.
    """
    init_app()
    # -------------------------------------------------------------
    logger: logging.Logger = logging.getLogger(__name__)
    logger.info("App starts.")
    applock: QLockFile = QLockFile(PATH["applock"])  # make sure only one program can run
    try:
        app: Application = Application()  # only one QApplication instance per application
        if applock.tryLock():
            app.display_widgets()
            app.exec()  # start the event loop
        else:
            QMessageBox.warning(None, "Error", "The application is already running!")
            logger.error("The application is already running!")
    except (RuntimeError, Exception, BaseException):
        logger.exception("Error when running the app.")
    finally:
        applock.unlock()
    logger.info("App quits.")
