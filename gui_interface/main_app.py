import logging
import threading
import tkinter as tk

from GoogleMyMaps import GoogleMyMaps
from configs.utils import resource_path, Colors
from excel_tables.obstacle_list import ObstacleList
from .error_window import ErrorWindow
from .final_frame import FinalFrame
from .loading_frame import LoadingFrame
from .map_link_frame import MapLinkFrame
from .not_found_obstacles_window import NotFoundObstaclesWindow

log = logging.getLogger(__name__)


class MainApp(tk.Tk):
    """
    Main application class for the RMG (Robot Mateusza Grzech) application.
    
    This class initializes the main application window, sets up the UI frames,
    and handles the core functionality of processing Google Maps data to create
    obstacle lists.
    """
    
    def __init__(self):
        """
        Initialize the main application window and set up the UI components.
        
        Sets up the application window with title, icon, and size, creates the
        frame container, initializes all UI frames, and sets up initial state
        variables for map processing.
        """
        log.debug("Initializing application...")
        super().__init__()
        self.title("RMG - Robot Mateusza Grzech")

        try:
            icon_image = tk.PhotoImage(file=resource_path("gui_interface/icon.png"))
            self.iconphoto(True, icon_image)
        except Exception as e:
            print(f"Could not set application icon: {e}")

        self.geometry("600x400")
        self.center_window(600, 400)

        self.frames = {}
        container = tk.Frame(self, bg=Colors.BG_COLOR)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (MapLinkFrame, LoadingFrame, FinalFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.gmm = GoogleMyMaps()
        self.google_map = None
        self.obstacle_list_file = None

        self.show_frame("MapLinkFrame")
        self.bind("<Escape>", self.quit_app)

    def center_window(self, width, height):
        """
        Center the application window on the screen.
        
        Parameters:
            width (int): The desired width of the window in pixels.
            height (int): The desired height of the window in pixels.
        
        Returns:
            None
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_frame(self, page_name):
        """
        Display the specified frame in the application window.
        
        Parameters:
            page_name (str): The name of the frame to display.
        
        Returns:
            None
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def process_map_link(self, map_link: str):
        """
        Process the provided Google Maps link in a separate thread.
        
        Creates a new thread to handle the map processing to prevent UI freezing.
        If successful, proceeds to process the map data; otherwise, displays an error.
        
        Parameters:
            map_link (str): The Google Maps URL to process.
        
        Returns:
            None
        """
        def process():
            try:
                self.google_map = self.gmm.create_map(map_link)
                self.after(0, self.process_map)
            except Exception as e:
                error_msg = str(e)
                self.after(0, lambda: self.failed_to_load_map(error_msg))

        thread = threading.Thread(target=process)
        thread.daemon = True
        thread.start()

    def process_map(self):
        """
        Process the loaded Google Map data to create an obstacle list.
        
        Creates an obstacle list from the loaded map data, handles any obstacles
        that couldn't be found, and updates the UI accordingly.
        
        Returns:
            None
        """
        log.info("Map loaded successfully")
        obstacle_list = ObstacleList(self.google_map)
        self.obstacle_list_file, not_found_obstacles = obstacle_list.create_and_save()
        if not_found_obstacles:
            NotFoundObstaclesWindow.show_not_found_obstacles(obstacle_list)
        if self.obstacle_list_file is None:
            self.reopen_map_frame()
        else:
            self.frames["MapLinkFrame"].unbind_submit_button()
            self.frames["FinalFrame"].bind_open_button()
            self.show_frame("FinalFrame")

    def failed_to_load_map(self, error_message: str):
        """
        Handle the case when map loading fails.
        
        Displays an error window with the provided error message and
        returns to the map link input frame.
        
        Parameters:
            error_message (str): The error message to display.
        
        Returns:
            None
        """
        log.error("Failed to load map: %s", error_message)
        ErrorWindow(self, error_message)
        self.reopen_map_frame()

    def reopen_map_frame(self):
        """
        Reset and display the map link input frame.
        
        Clears the previous map link input, rebinds the submit button,
        and displays the map link frame.
        
        Returns:
            None
        """
        log.info("Please provide map link again")
        self.frames["MapLinkFrame"].entry.delete(0, tk.END)
        self.frames["MapLinkFrame"].bind_submit_button()
        self.show_frame("MapLinkFrame")

    def quit_app(self, event=None):
        """
        Close the application.
        
        Parameters:
            event (Event, optional): The event that triggered this method, if any.
        
        Returns:
            None
        """
        log.info("Closing application...")
        self.destroy()
