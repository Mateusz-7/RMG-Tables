import logging

from configs.logger_config import setup_logger
from gui_interface.main_app import MainApp


def main():
    setup_logger(logging.DEBUG)

    app = MainApp()
    app.mainloop()

if __name__ == '__main__':
    main()

    # TODO:
    # - logging
    # - lista nie znalezionych przeszkód

    # - dodanie kilometrów
    # - dodanie odpowiedzialnej osoby

    # - docstrings
    # - usuwanie wierszy/kolumn?
