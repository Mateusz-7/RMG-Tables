import tkinter as tk

from configs.utils import Colors


class LoadingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg=Colors.BG_COLOR)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content_frame = tk.Frame(self, bg=Colors.BG_COLOR)
        content_frame.grid(row=0, column=0)
        
        label = tk.Label(
            content_frame,
            text="Loading...",
            font=("Runmageddon", 50),
            bg=Colors.BG_COLOR,
            fg=Colors.YELLOW)
        label.pack(pady=(0,20))
