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
            font=tk.font.Font(size=12),
            bg="#cc0033",
            wraplength=300
        )
        error_message_label.pack()

        self.ok_button = tk.Button(
            error_frame,
            text="OK",
            font=("Runmageddon", 20),
            width=10,
            bg="#ffde00",
            fg="#000000",
            activeforeground="#ffde00",
            activebackground="#cc0033",
            bd=4,
            command=self.destroy,
            cursor="hand2"
        )
        self.ok_button.pack(pady=20)

        self.bind("<Return>", lambda event: self.destroy()) # Add binding for main Enter key
        self.bind("<KP_Enter>", lambda event: self.destroy())  # Add binding for numeric keypad Enter
        self.bind("<Escape>", lambda event: self.destroy())
        self.focus_set()
        self.grab_set()
        self.transient(parent)

        self.ok_button.bind("<Enter>", self.on_enter)
        self.ok_button.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.ok_button.config(bg="#ffde00", fg="#cc0033")

    def on_leave(self, event):
        self.ok_button.config(bg="#ffde00", fg="#000000")

    def center_window_on_parent(self, parent, width, height):
        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
