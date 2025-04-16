import logging


class ColorFormatter(logging.Formatter):
    """Custom logging formatter to add colors based on log levels.
    
    This formatter enhances log readability by applying ANSI color codes to different
    log components based on their severity level. The format includes timestamp,
    logger name, line number, thread name, log level, and the actual message.
    """

    # Define colors for each log level
    COLOR_CODES = {
        logging.DEBUG: "\033[94m",  # Blue
        logging.INFO: "\033[92m",  # Green
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[95m",  # Magenta
    }

    RESET_CODE = "\033[0m"

    def format(self, record):
        """Format the log record with color-coded components.
        
        This method applies ANSI color codes to different parts of the log message
        to enhance readability. It creates a custom format string with colored
        components and then uses the standard logging.Formatter to apply it.
        
        Parameters
        ----------
        record : logging.LogRecord
            The log record to format, containing all the information about the log event.
            
        Returns
        -------
        str
            The formatted log message with color codes applied.
        """
        # Get the color based on the log level
        color = self.COLOR_CODES.get(record.levelno, self.RESET_CODE)
        white = "\033[97m"  # White
        grey = "\033[90m"  # Grey
        cyan = "\033[36m"  # Cyan"]"
        # cyan = "\033[96m"  # Cyan"]"
        magenta = "\033[95m"  # Magenta"]"
        bold = "\033[1m"  # Bold"]"

        # Add filename to the message format
        log_fmt = (f"{grey}%(asctime)s {white}- "
                   f"{cyan}%(name)s:%(lineno)d {white}- ["
                   f"{magenta}%(threadName)s{white}] {white}- "
                   f"{color}{bold}%(levelname)s{self.RESET_CODE}"
                   f"{white} - %(message)s{self.RESET_CODE}")

        # Set the format and use the parent `Formatter` to apply it
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Set up the root logger configuration
def setup_logger(log_level=logging.DEBUG):
    """Set up and configure the root logger with colored console output.
    
    This function configures the root logger with a console handler that uses
    the ColorFormatter for enhanced readability. It ensures that handlers are
    not duplicated if the function is called multiple times.
    
    Parameters
    ----------
    log_level : int, optional
        The minimum logging level to display. Messages below this level will be ignored.
        Default is logging.DEBUG, which shows all log messages.
        
    Returns
    -------
    logging.Logger
        The configured root logger instance that can be used for logging throughout
        the application.
    """
    # Configure the root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Prevent duplicate handlers if this is called multiple times
    if not logger.hasHandlers():
        # Create console handler
        console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.INFO)  # Setting console log level
        console_handler.setFormatter(ColorFormatter())

        # Add the console handler to the root logger
        logger.addHandler(console_handler)
