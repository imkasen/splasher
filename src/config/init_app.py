from .log import init_log
from .create_folders import create_folders
from .settings import create_settings


def init_app() -> None:
    """
    Initialization, creating the environment configuration needed for the application.
    """
    create_folders()
    init_log()
    create_settings()
