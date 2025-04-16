import os
import platform
import sys


def resource_path(relative_path: str) -> str:
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def start_application(file_path: str) -> None:
    print("Opening file: ", file_path)
    if platform.system() == "Windows":
        os.startfile(file_path)
    elif platform.system() == "Darwin":
        os.system("open '" + file_path + "'")
    elif platform.system() == "Linux":
        os.system("xdg-open '" + file_path + "'")
    else:
        print("Unsupported operating system")
