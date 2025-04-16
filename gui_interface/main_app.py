import platform
import tkinter as tk
import threading
from GoogleMyMaps import GoogleMyMaps
from excel_tables.utils import resource_path
from .error_window import ErrorWindow
from .final_frame import FinalFrame

from .map_link_frame import MapLinkFrame
from .loading_frame import LoadingFrame
from excel_tables.obstacle_list import ObstacleList


class MainApp(tk.Tk):
    def __init__(self):
        print("Initializing application...")
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
        container = tk.Frame(self, bg="#232323")
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
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def process_map_link(self, map_link: str):
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
        print("Map loaded successfully")
        self.obstacle_list_file = ObstacleList.create_and_save(self.google_map)
        if self.obstacle_list_file is None:
            self.reopen_map_frame()
        else:
            self.frames["MapLinkFrame"].unbind_submit_button()
            self.frames["FinalFrame"].bind_open_button()
            self.show_frame("FinalFrame")

    def failed_to_load_map(self, error_message: str):
        print(f"*Failed to load map: {error_message}")
        ErrorWindow(self, error_message)
        self.reopen_map_frame()

    def reopen_map_frame(self):
        print("Please provide map link again")
        self.frames["MapLinkFrame"].entry.delete(0, tk.END)
        self.frames["MapLinkFrame"].bind_submit_button()
        self.show_frame("MapLinkFrame")

    def quit_app(self, event=None):
        print("Closing application...")
        self.destroy()
