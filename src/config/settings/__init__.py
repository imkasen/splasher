from PySide6.QtCore import QReadWriteLock

lock: QReadWriteLock = QReadWriteLock()

from .settings_arg_getter import get_settings_arg
from .settings_arg_setter import set_settings_arg
from .settings_creator import create_settings
