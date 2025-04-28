import enum
import logging
import os
import platform
import subprocess
import sys

log = logging.getLogger(__name__)


def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource, works for both development and PyInstaller frozen applications.

    This function handles path resolution differently depending on whether the application
    is running in a development environment or as a PyInstaller frozen executable.

    Parameters:
        relative_path (str): The relative path to the resource file or directory

    Returns:
        str: The absolute path to the resource
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def start_application(file_path: str) -> None:
    """
    Open a file with the default application based on the operating system.

    This function detects the current operating system and uses the appropriate
    method to open the specified file with its associated default application.
    Supports Windows, macOS (Darwin), and Linux.

    Parameters:
        file_path (str): The path to the file to be opened

    Returns:
        None

    Raises:
        Logs an error if the operating system is not supported
    """
    log.info("Opening file: %s", file_path)
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", file_path], check=True)
        elif platform.system() == "Linux":
            subprocess.run(["xdg-open", file_path], check=True)
        else:
            log.error("Unsupported operating system: %s", platform.system())
    except Exception as e:
        log.error("Failed to open file %s: %s", file_path, str(e))

def unify_string(string: str) -> str | None:
    """
    Standardize a string by removing whitespace and converting to uppercase.

    Parameters:
        string (str): String to unify

    Returns:
        str: String without spaces, new line characters, and with UPPER
    """
    if string is None:
        return None
    return string.upper().replace("\n", "").replace(" ", "")

def are_strings_similar(string1: str, string2: str) -> bool:
    """
    Compare two strings to determine if they are similar.

    This function checks if two strings are similar by:
    1. Converting both to uppercase and removing spaces and newlines
    2. Checking if they are equal
    3. Checking if one is a substring of the other

    Parameters:
        string1 (str): First string to compare
        string2 (str): Second string to compare

    Returns:
        bool: True if the strings are considered similar, False otherwise
    """
    if string1 is None or string2 is None:
        return False
    unified_str1 = unify_string(string1)
    unified_str2 = unify_string(string2)
    if (
            unified_str1 == unified_str2 or
            unified_str1 in unified_str2 or
            unified_str2 in unified_str1
    ):
        return True
    return False


class Colors(str, enum.Enum):
    """
    Color constants used throughout the application.

    This enumeration provides a centralized collection of color hex codes organized by categories:
    - Base UI colors (background, text, highlights)
    - Basic colors (black, white, primary colors)
    - Modern UI color palette
    - Material design inspired colors
    - Dark mode friendly colors
    - Pastel colors
    - Grayscale gradient shades

    Each color is represented as a hexadecimal string value (#RRGGBB format).

    Inherits from:
        str: Allows the enum values to be used directly as strings
        enum.Enum: Provides enumeration functionality

    Usage:
        Colors.BG_COLOR  # Returns "#232323"
    """
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
