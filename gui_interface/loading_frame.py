import tkinter as tk


class LoadingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#232323")

        label = tk.Label(self, text="Loading...", bg="#232323", fg="#ffde00")
        label.pack(pady=10)