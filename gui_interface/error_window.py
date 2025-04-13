import tkinter as tk

class ErrorWindow(tk.Toplevel):
    def __init__(self, parent, error_message):
        super().__init__(parent)
        self.title("Error")
        self.geometry("300x200")
        self.center_window_on_parent(parent, 300, 200)

        error_frame = tk.Frame(self, bg="#cc0033")
        error_frame.pack(fill="both", expand=True)
        error_label = tk.Label(
            error_frame,
            text="COŚ POSZŁO NIE TAK:",
            font=("Runmageddon", 25),
            bg="#cc0033"
        )
        error_label.pack(pady=(20, 0))

        error_message_label = tk.Label(
            error_frame,
            text=error_message,
            font=("Arial", 12),
            bg="#cc0033",
            wraplength=300
        )
        error_message_label.pack()

        ok_button = tk.Button(
            error_frame,
            text="OK",
            font=("Runmageddon", 20),
            width=10,
            bg="#000000",
            fg="#ffffff",
            bd=4,
            command=self.destroy
        )
        ok_button.pack(pady=20)

        self.bind("<Return>", lambda event: self.destroy())
        self.bind("<Escape>", lambda event: self.destroy())
        self.focus_set()
        self.grab_set()
        self.transient(parent)

    def center_window_on_parent(self, parent, width, height):
        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
