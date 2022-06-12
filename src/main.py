from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QLockFile
from gui.main_window import MainWindow
from utils.global_variables import LOCKFILE_PATH


def main() -> None:
    """
    The entry function of the application
    :return: None
    """
    lock_file = QLockFile(LOCKFILE_PATH)  # make sure only one program can run
    try:
        app = QApplication([])  # only one QApplication instance per application, no command line arguments
        if lock_file.tryLock():
            window = MainWindow()
            window.show()  # windows are hidden by default
            app.exec()  # start the event loop
        else:
            err_msg = QMessageBox()
            err_msg.setIcon(QMessageBox.Warning)
            err_msg.setWindowTitle("Error")
            err_msg.setText("The application is already running!")
            err_msg.setStandardButtons(QMessageBox.Ok)
            err_msg.exec()
    finally:
        lock_file.unlock()


if __name__ == "__main__":
    main()
