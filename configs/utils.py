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

    Parameters:
        file_path (str): The path to the file to be opened
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
    Each color is represented as a hexadecimal string value (#RRGGBB format).

    Inherits from:
        str: Allows the enum values to be used directly as strings
        enum.Enum: Provides enumeration functionality

    Usage:
        Colors.BG_COLOR # Returns "#232323"
    """
    # Base UI colors
    BG_COLOR = "#232323"  # Dark background
    BG_LIGHT = "#2a2a2a"  # Slightly lighter than the background
    BG_VERY_LIGHT = "#565656" # Highly lighter than the background
    TEXT_COLOR = "#e0e0e0"  # Light gray text

    # Accent colors
    YELLOW = "#ffde00"  # Yellow for buttons and highlights
    YELLOW_DARKER = "#ddbc00"  # Yellow for scrollbar
    ERROR_RED = "#cc0033" # Red for an error window

    # Basic colors
    BLACK = "#000000"
    WHITE = "#ffffff"
