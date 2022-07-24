from .init_log import init_log
from .create_folders import create_folders


def init_app() -> None:
    """
    Initialization, creating the environment configuration needed for the application.
    """
    create_folders()
    init_log()
