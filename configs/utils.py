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
    BG_COLOR = "#232323"  # Dark background
    BG_LIGHT = "#2a2a2a"  # Slightly lighter than background
    BG_VERY_LIGHT = "#565656" # Highly lighter than background
    TEXT_COLOR = "#e0e0e0"  # Light gray text
    YELLOW = "#ffde00"  # Yellow for buttons and highlights
    YELLOW_DARKER = "#ddbc00"  # Yellow for scrollbar
    ERROR_RED = "#cc0033"
    BLACK = "#000000"
    WHITE = "#ffffff"
    RED = "#ff0000"
    GREEN = "#00ff00"
    BLUE = "#0000ff"

    # Modern UI colors
    PURPLE = "#8a2be2"  # Vibrant purple
    ORANGE = "#ff8c00"  # Dark orange
    CYAN = "#00ffff"  # Bright cyan
    MAGENTA = "#ff00ff"  # Bright magenta
    TEAL = "#008080"  # Teal
    LIME = "#32cd32"  # Lime green
    PINK = "#ff69b4"  # Hot pink
    INDIGO = "#4b0082"  # Deep indigo

    # Material design inspired colors
    MATERIAL_RED = "#f44336"
    MATERIAL_BLUE = "#2196f3"
    MATERIAL_GREEN = "#4caf50"
    MATERIAL_AMBER = "#ffc107"
    MATERIAL_PURPLE = "#9c27b0"

    # Dark mode friendly colors
    DARK_BLUE = "#1e3a8a"
    DARK_GREEN = "#166534"
    DARK_PURPLE = "#581c87"
    DARK_RED = "#991b1b"
    DARK_TEAL = "#115e59"

    # Pastel colors
    PASTEL_BLUE = "#a7c5eb"
    PASTEL_GREEN = "#b5e8b5"
    PASTEL_YELLOW = "#f6f6a3"
    PASTEL_PINK = "#ffb6c1"
    PASTEL_PURPLE = "#d8bfd8"

    # Gradient shades
    GRAY_100 = "#f3f4f6"
    GRAY_200 = "#e5e7eb"
    GRAY_300 = "#d1d5db"
    GRAY_400 = "#9ca3af"
    GRAY_500 = "#6b7280"
    GRAY_600 = "#4b5563"
    GRAY_700 = "#374151"
    GRAY_800 = "#1f2937"
    GRAY_900 = "#111827"
