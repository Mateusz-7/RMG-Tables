import logging
import os
import platform
import tkinter as tk

log = logging.getLogger(__name__)


class FinalFrame(tk.Frame):
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
            text="Wygenerowano Listę Przeszkód!",
            font=("Runmageddon", 30),
            bg="#232323",
            fg="#ffde00"
        )
        label.pack(pady=(0, 60))

        self.open_button = tk.Button(
            content_frame,
            text="OTWÓRZ",
            font=("Runmageddon", 20),
            bg="#ffde00",
            fg="#000000",
            activeforeground="#ffde00",
            activebackground="#232323",
            bd=5,
            width=15,
            command=self.open_file,
            cursor="hand2"
        )
        self.open_button.pack(pady=10)

        self.open_button.bind("<Enter>", self.on_enter)
        self.open_button.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.open_button.config(bg="#ffde00", fg="#565656")

    def on_leave(self, event):
        self.open_button.config(bg="#ffde00", fg="#000000")

    # noinspection PyUnusedLocal
    def open_file(self, event=None):
        obstacle_list_file = self.controller.obstacle_list_file
        if obstacle_list_file:
            log.debug("Opening file: %s", obstacle_list_file)
            if platform.system() == "Windows":
                os.startfile(obstacle_list_file)
            elif platform.system() == "Darwin":
                os.system("open '" + obstacle_list_file + "'")
            elif platform.system() == "Linux":
                os.system("xdg-open '" + obstacle_list_file + "'")
            else:
                log.error("Unsupported operating system")
            self.controller.quit_app()

    def bind_open_button(self):
        self.bind("<Return>", self.open_file)  # Add binding for main Enter key
        self.bind("<KP_Enter>", self.open_file)  # Add binding for numeric keypad Enter
        self.focus_set()
