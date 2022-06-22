from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QLockFile
from gui.main_window import MainWindow
from gui.system_tray import SystemTray
from utils.env import LOCKFILE_PATH


def main() -> None:
    """
    The entry function of the application.
    """
    lock_file = QLockFile(LOCKFILE_PATH)  # make sure only one program can run
    try:
        app = QApplication([])  # only one QApplication instance per application, no command line arguments
        if lock_file.tryLock():
            # ======== display the main window ========
            app.main_window = MainWindow()
            app.main_window.show()  # windows are hidden by default
            # -------------------------------------------------------------
            # ======== display the system tray ========
            app.tray = SystemTray()
            # display
            if app.tray.isSystemTrayAvailable():
                app.setQuitOnLastWindowClosed(False)  # keep app running after closing all windows
                app.tray.show()
            else:
                app.main_window.status_bar.showMessage("The system tray can not be displayed!")
            # -------------------------------------------------------------
            app.exec()  # start the event loop
        else:
            # ======== show a warning message ========
            err_msg = QMessageBox()
            err_msg.setIcon(QMessageBox.Warning)
            err_msg.setWindowTitle("Error")
            err_msg.setText("The application is already running!")
            err_msg.setStandardButtons(QMessageBox.Ok)
            err_msg.exec()
            # -------------------------------------------------------------
    finally:
        lock_file.unlock()


if __name__ == "__main__":
    main()
