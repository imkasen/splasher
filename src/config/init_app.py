from .log import init_log
from .create_folders import create_folders


def init_app() -> None:
    create_folders()
    init_log()
