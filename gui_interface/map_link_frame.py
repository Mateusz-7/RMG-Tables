import tkinter as tk
from tkinter import font


class MapLinkFrame(tk.Frame):
    def __init__(self, parent, controller):
        print("Please provide map link")
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#232323")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content_frame = tk.Frame(self, bg="#232323")
        content_frame.grid(row=0, column=0)

        label = tk.Label(
            content_frame,
            text="Podaj link do mapy:",
            font=("Runmageddon", 35),
            bg="#232323",
            fg="#ffde00"
        )
        label.pack(pady=(80, 50))

        self.entry = tk.Entry(content_frame, width=70, font=tk.font.Font(size=10))
        self.entry.pack(pady=10)
        self.bind_submit_button()
        self.entry.focus_set()

        # TODO: Delete after testing
        # self.entry.insert(0,"https://www.google.com/maps/d/u/0/edit?mid=1QU5ydDpF5bg_8jfQca3An2qJfqddpcY&ll=53.08931730768191%2C21.56582239999997&z=15")
        # self.entry.insert(0, "https://www.google.com/maps/d/u/1/edit?mid=134VUSLwnSE0LorF8FeYLEd3E6EhIYwc&usp=sharing")

        self.submit_button = tk.Button(
            content_frame,
            text="GENERUJ",
            font=("Runmageddon", 20),
            bg="#ffde00",
            fg="#000000",
            activeforeground="#ffde00",
            activebackground="#232323",
            bd=5,
            width=10,
            command=self.submit_link,
            cursor="hand2"
        )
        self.submit_button.pack(pady=(10, 80))

        disclaimer_label = tk.Label(
            content_frame,
            text='Mapa musi być udostępniona/widoczna poprzez link\n'
                 'Wszystkie nazwy dystansów muszą zaczynać się od "TRASA"\n'
                 'Warstwa najdłuższego dystansu musi być przed pozostałymi dystansami',
            font=("Runmageddon", 10),
            bg="#232323",
            fg="#ffffff"
        )
        disclaimer_label.pack()

        self.submit_button.bind("<Enter>", self.on_enter)
        self.submit_button.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.submit_button.config(bg="#ffde00", fg="#565656")

    def on_leave(self, event):
        self.submit_button.config(bg="#ffde00", fg="#000000")

    def submit_link(self):
        map_link = self.entry.get()
        if map_link:
            print("Map link provided:", map_link)
            self.controller.show_frame("LoadingFrame")
            self.controller.process_map_link(map_link)

    def bind_submit_button(self):
        self.entry.bind("<Return>", lambda event: self.submit_link())

    def unbind_submit_button(self):
        self.entry.unbind("<Return>")
