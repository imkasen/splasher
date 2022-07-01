from PySide6.QtCore import QLockFile
from config import PATH
from gui import Application


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
            app.singleton_app_warning_msg()
    finally:
        applock.unlock()


if __name__ == "__main__":
    main()
