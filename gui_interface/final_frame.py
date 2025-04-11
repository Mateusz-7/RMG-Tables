import os
import tkinter as tk


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
            command=self.open_file
        )
        self.open_button.pack(pady=10)

    def open_file(self):
        obstacle_list_file = self.controller.obstacle_list_file
        if obstacle_list_file:
            print("Opening file: ", obstacle_list_file)
            os.startfile(obstacle_list_file)
            self.controller.quit_app()

    def bind_open_button(self):
        self.bind("<Return>", lambda event: self.open_file())
        self.focus_set()
