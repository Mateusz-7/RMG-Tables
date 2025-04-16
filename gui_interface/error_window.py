import tkinter as tk

from configs.utils import Colors


class ErrorWindow(tk.Toplevel):
    """
    A modal dialog window that displays an error message to the user.
    
    This window appears centered on the parent window and requires user acknowledgment
    before continuing with the application.
    """
    
    def __init__(self, parent, error_message):
        """
        Initialize the error window with the specified parent and error message.
        
        Parameters:
            parent (tk.Widget): The parent widget for this window. The error window
                                will be centered on this widget.
            error_message (str): The error message to display to the user.
        """
        super().__init__(parent)
        self.title("Error")
        self.geometry("300x200")
        self.center_window_on_parent(parent, 300, 200)

        error_frame = tk.Frame(self, bg=Colors.ERROR_RED)
        error_frame.pack(fill="both", expand=True)
        error_label = tk.Label(
            error_frame,
            text="COŚ POSZŁO NIE TAK:",
            font=("Runmageddon", 25),
            bg=Colors.ERROR_RED
        )
        error_label.pack(pady=(20, 0))

        error_message_label = tk.Label(
            error_frame,
            text=error_message,
            font=tk.font.Font(size=12),
            bg=Colors.ERROR_RED,
            wraplength=300
        )
        error_message_label.pack()

        self.ok_button = tk.Button(
            error_frame,
            text="OK",
            font=("Runmageddon", 20),
            width=10,
            bg=Colors.YELLOW,
            fg=Colors.BLACK,
            activeforeground=Colors.YELLOW,
            activebackground=Colors.ERROR_RED,
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
        """
        Handle mouse enter event for the OK button by changing its colors.
        
        Parameters:
            event (tk.Event): The event object containing information about the event.
        """
        self.ok_button.config(bg=Colors.YELLOW, fg=Colors.ERROR_RED)

    def on_leave(self, event):
        """
        Handle mouse leave event for the OK button by restoring its original colors.
        
        Parameters:
            event (tk.Event): The event object containing information about the event.
        """
        self.ok_button.config(bg=Colors.YELLOW, fg=Colors.BLACK)

    def center_window_on_parent(self, parent, width, height):
        """
        Center this window on its parent window.
        
        Calculates the position coordinates to place this window centered
        on the parent window based on the specified dimensions.
        
        Parameters:
            parent (tk.Widget): The parent widget to center on.
            width (int): The width of this window in pixels.
            height (int): The height of this window in pixels.
        """
        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
