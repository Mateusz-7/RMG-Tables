import enum
import logging
import os
import platform
import sys

log = logging.getLogger(__name__)


def resource_path(relative_path: str) -> str:
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def start_application(file_path: str) -> None:
    log.info("Opening file: %s", file_path)
    if platform.system() == "Windows":
        os.startfile(file_path)
    elif platform.system() == "Darwin":
        os.system("open '" + file_path + "'")
    elif platform.system() == "Linux":
        os.system("xdg-open '" + file_path + "'")
    else:
        log.error("Unsupported operating system: %s", platform.system())


def unify_string(string: str) -> str:
    """
    :param string: String to unify
    :return: String without spaces, new line characters, and with UPPER
    """
    return string.upper().replace("\n", "").replace(" ", "")

class Colors(str, enum.Enum):
    """Color constants used throughout the application"""
    # Dark theme colors
    BG_COLOR = "#232323"  # Dark background
    BG_LIGHTER = "#252525"  # Between background and lighter background
    BG_LIGHTEST = "#2a2a2a"  # Slightly lighter than background
    TEXT_COLOR = "#e0e0e0"  # Light gray text
    MAIN_YELLOW = "#ffde00"  # Yellow for buttons and highlights
    MAIN_DARKER = "#ddbc00"  # Yellow for scrollbar

    # def __str__(self):
    #     return str(self.value)
    #
    # def __repr__(self):
    #     return str(self.value)
