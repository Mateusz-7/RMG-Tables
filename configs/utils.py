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

class Colors(enum.Enum):
    """Color constants used throughout the application"""
    # Dark theme colors
    BG_COLOR = "#232323"  # Dark background
    ROW_ODD = "#2a2a2a"  # Slightly lighter than background
    ROW_EVEN = "#252525"  # Between bg_color and row_odd
    TEXT_COLOR = "#e0e0e0"  # Light gray text
    SCROLLBAR_BG = "#ddbc00"  # Yellow for scrollbar
    MAIN_YELLOW = "#ffde00"  # Yellow for buttons and highlights
