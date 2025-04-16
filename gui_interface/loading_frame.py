import tkinter as tk

from configs.utils import Colors


class LoadingFrame(tk.Frame):
    """
    A frame that displays a loading message to the user.
    
    This frame is typically shown during operations that require waiting,
    such as data processing or initialization tasks. It displays a centered
    "Loading..." text with the Runmageddon font.
    
    Parameters
    ----------
    parent : tk.Widget
        The parent widget in which this frame will be placed.
    controller : object
        The controller object that manages navigation between frames
        and contains application logic.
    
    Returns
    -------
    None
    """
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
