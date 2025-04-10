import tkinter as tk


class MapLinkFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#232323")

        label = tk.Label(self, text="Podaj link do mapy:", bg="#232323", fg="#ffde00")
        label.pack(pady=10)

        self.entry = tk.Entry(self, width=50)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.submit_link())

        submit_button = tk.Button(self, text="GENERUJ", command=self.submit_link, bg="#ffde00", fg="#000000", activeforeground="#ffde00", activebackground="#232323")
        submit_button.pack(pady=20)

    def submit_link(self):
        map_link = self.entry.get()
        if map_link:
            self.controller.show_frame("LoadingFrame")