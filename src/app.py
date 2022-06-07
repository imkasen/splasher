from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main() -> None:
    """
    the entry function of the application
    :return: None
    """
    app = QApplication([])  # only one QApplication instance per application, no command line arguments

    window = MainWindow()
    window.show()  # windows are hidden by default

    app.exec()  # start the event loop


if __name__ == "__main__":
    main()
