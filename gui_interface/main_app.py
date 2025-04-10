import tkinter as tk

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

        for F in (MapLinkFrame, LoadingFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

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
