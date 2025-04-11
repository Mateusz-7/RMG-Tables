import tkinter as tk
import threading
from GoogleMyMaps import GoogleMyMaps
from .error_window import ErrorWindow

from .map_link_frame import MapLinkFrame
from .loading_frame import LoadingFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RMG - Robot Mateusza Grzech")
        self.geometry("600x400")
        self.center_window(600, 400)

        self.frames = {}
        container = tk.Frame(self, bg="#232323")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (MapLinkFrame, LoadingFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.gmm = GoogleMyMaps()
        self.google_map = None

        self.show_frame("MapLinkFrame")

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


    def failed_to_load_map(self, error_message: str):
        print(f"Failed to load map: {error_message}")
        ErrorWindow(self, error_message)

        self.frames["MapLinkFrame"].entry.delete(0, tk.END)
        self.show_frame("MapLinkFrame")