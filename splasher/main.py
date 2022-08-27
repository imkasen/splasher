import logging

from PySide6.QtCore import QLockFile
from PySide6.QtWidgets import QMessageBox

from splasher.config import PATH, init_app
from splasher.gui import Application


def main() -> None:
    """
    The main function of the application.
    """
    init_app()
    # -------------------------------------------------------------
    logger: logging.Logger = logging.getLogger(__name__)
    applock: QLockFile = QLockFile(PATH["APPLOCK"])  # make sure only one program can run
    try:
        app: Application = Application()  # only one QApplication instance per application
        logger.info("App starts.")
        if applock.tryLock():
            app.display_widgets()
            app.exec()  # start the event loop
        else:
            QMessageBox.warning(None, "Error", "The application is already running!")
            logger.error("The application is already running!")
    except (SystemError, RuntimeError, Exception):  # pylint: disable=broad-except
        logger.exception("Error when running the app.")
    finally:
        applock.unlock()
        logger.info("App quits.")


if __name__ == "__main__":
    main()
