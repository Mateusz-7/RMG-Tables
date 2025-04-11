import tkinter as tk


class LoadingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#232323")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content_frame = tk.Frame(self, bg="#232323")
        content_frame.grid(row=0, column=0)
        
        label = tk.Label(
            content_frame,
            text="Loading...",
            font=("Runmageddon", 50),
            bg="#232323",
            fg="#ffde00")
        label.pack(pady=(0,20))