import logging

from configs.logger_config import setup_logger
from gui_interface.main_app import MainApp

import pyfiglet


def main():
    """
    Initialize and run the main application for the RMG (Robot Mateusza Grzech) system.
    
    This function serves as the entry point for the entire application. It performs the following operations:
    
    1. Sets up the logging system with DEBUG level to capture detailed information about the application's
       execution flow, which is crucial for debugging and monitoring the application's behavior.
    
    2. Creates an instance of the MainApp class, which is the primary GUI container for the application.
       The MainApp instance initializes all necessary UI components, including frames for map link input,
       loading indicators, and result displays.
    
    3. Starts the application's main event loop by calling mainloop() on the MainApp instance.
       This begins the Tkinter event processing, which handles user interactions, window updates,
       and all other GUI-related operations. The application will continue running until this
       event loop is terminated (typically when the user closes the main window).
    
    The function is designed to be called directly when the script is executed as the main module,
    as indicated by the `if __name__ == '__main__'` check at the bottom of the file.
    
    Technical Details:
    - Logging is configured through the setup_logger function imported from configs.logger_config
    - The DEBUG level provides maximum verbosity for development and troubleshooting
    - The MainApp class is imported from gui_interface.main_app and handles all UI components
    - The Tkinter mainloop() method blocks execution until the application window is closed
    
    Application Flow:
    1. Display the RMG banner using pyfiglet for visual identification
    2. Configure logging system for application monitoring
    3. Initialize the main application window and UI components
    4. Enter the event loop to process user interactions
    5. Process Google Maps data and generate Excel tables based on user input
    
    Error Handling:
    - Font rendering errors are gracefully handled with fallbacks to ensure the application
      continues to run even if the ASCII art banner cannot be displayed properly
    - The application uses a comprehensive logging system to track errors and application state
    - GUI components include error handling and user feedback mechanisms
    - Exceptions in the main thread are caught to prevent application crashes
    
    Example Usage:
    ```
    python main.py
    ```
    
    Dependencies:
    - Python's built-in logging module
    - configs.logger_config.setup_logger function
    - gui_interface.main_app.MainApp class
    - Tkinter (implicitly used through MainApp)
    - pyfiglet for ASCII art banner generation
    - Google Maps API integration through GoogleMyMaps module
    - Excel processing capabilities through excel_tables module
    
    System Requirements:
    - Python 3.10 or higher
    - Tkinter library (usually included with Python installations)
    - Internet connection for Google Maps API access
    - Sufficient permissions to read/write files in the application directory
    
    Returns:
        None: This function does not return any value. The application runs until the
              user terminates it by closing the main window or through another exit mechanism.
    
    Notes:
        - The application must be run in an environment where Tkinter is available.
        - Proper exception handling is managed within the MainApp class.
        - Future enhancements may include command-line arguments for different logging levels
          or other configuration options.
        - The application processes Google Maps data to extract course information and
          generates formatted Excel tables for further analysis.
        - Performance may vary based on the complexity of the Google Maps data being processed.
    """
    try:
        result = pyfiglet.figlet_format("RMG", font="ansi_shadow")
        print(f"\033[94m{result}")
    except pyfiglet.FontNotFound:
        try:
            result = pyfiglet.figlet_format("default")
            print(f"\033[94m{result}")
        except Exception as e:
            print(f"\033[94m=== RMG ===")
            print(f"Font error: {str(e)}")

    setup_logger(logging.DEBUG)

    app = MainApp()
    app.mainloop()

if __name__ == '__main__':
    main()

    # TODO:
    # - rozdzielenie last found obstacle na doroslych i kids (lepsze numerowanie family)
    # - najpierw dokładne sprawdzenie, później podobne

    # - poprawa odpowiedzialnej osoby
    # - wolo, sędzia, tabliczki, palety, materace

    # - dodanie czcionki