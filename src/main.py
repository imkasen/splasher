from PySide6.QtCore import QLockFile
from config.env import PATH
from gui.application import Application


def main() -> None:
    """
    The entry function of the application.
    """
    applock = QLockFile(PATH["applock"])  # make sure only one program can run
    try:
        app = Application()  # only one QApplication instance per application
        if applock.tryLock():
            app.draw_main_window()
            app.draw_system_tray()
            app.exec()  # start the event loop
        else:
            app.singleton_app_warning_msg()
    finally:
        applock.unlock()


if __name__ == "__main__":
    main()
