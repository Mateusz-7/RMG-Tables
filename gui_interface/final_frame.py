import logging
import tkinter as tk

from configs.utils import start_application, Colors

log = logging.getLogger(__name__)


class FinalFrame(tk.Frame):
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
            text="Wygenerowano Listę Przeszkód!",
            font=("Runmageddon", 30),
            bg=Colors.BG_COLOR,
            fg=Colors.YELLOW
        )
        label.pack(pady=(0, 60))

        self.open_button = tk.Button(
            content_frame,
            text="OTWÓRZ",
            font=("Runmageddon", 20),
            bg=Colors.YELLOW,
            fg=Colors.BLACK,
            activeforeground=Colors.YELLOW,
            activebackground=Colors.BG_COLOR,
            bd=5,
            width=15,
            command=self.open_file,
            cursor="hand2"
        )
        self.open_button.pack(pady=10)

        self.open_button.bind("<Enter>", self.on_enter)
        self.open_button.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.open_button.config(bg=Colors.YELLOW, fg=Colors.BG_VERY_LIGHT)

    def on_leave(self, event):
        self.open_button.config(bg=Colors.YELLOW, fg=Colors.BLACK)

    # noinspection PyUnusedLocal
    def open_file(self, event=None):
        obstacle_list_file = self.controller.obstacle_list_file
        if obstacle_list_file:
            start_application(obstacle_list_file)
            self.controller.destroy()

    def bind_open_button(self):
        self.bind("<Return>", self.open_file)  # Add binding for main Enter key
        self.bind("<KP_Enter>", self.open_file)  # Add binding for numeric keypad Enter
        self.focus_set()
