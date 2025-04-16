import logging
import tkinter as tk

from configs.utils import start_application, Colors

log = logging.getLogger(__name__)


class FinalFrame(tk.Frame):
    """
    A frame that displays a success message after generating an obstacle list.
    
    This frame provides a button to open the generated file and automatically
    closes the application after opening the file.
    
    Attributes:
        controller: The parent controller that manages this frame
        open_button: Button widget that opens the generated file
    """
    
    def __init__(self, parent, controller):
        """
        Initialize the FinalFrame with success message and open button.
        
        Parameters:
            parent (tk.Widget): The parent widget that will contain this frame
            controller: The controller object that manages navigation and data between frames
        """
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
        """
        Handle mouse enter event for the open button.
        
        Parameters:
            event: The event object containing information about the event
        """
        self.open_button.config(bg=Colors.YELLOW, fg=Colors.BG_VERY_LIGHT)

    def on_leave(self, event):
        """
        Handle mouse leave event for the open button.
        
        Parameters:
            event: The event object containing information about the event
        """
        self.open_button.config(bg=Colors.YELLOW, fg=Colors.BLACK)

    # noinspection PyUnusedLocal
    def open_file(self, event=None):
        """
        Open the generated obstacle list file and close the application.
        
        This method retrieves the file path from the controller, opens the file
        using the system's default application, and then closes the current application.
        
        Parameters:
            event: Optional event parameter for binding to keyboard events (not used)
        """
        obstacle_list_file = self.controller.obstacle_list_file
        if obstacle_list_file:
            start_application(obstacle_list_file)
            self.controller.destroy()

    def bind_open_button(self):
        """
        Bind keyboard Enter keys to the open_file method.
        
        This method sets up keyboard shortcuts (Enter key and numeric keypad Enter)
        to trigger the open_file method, and sets focus to this frame.
        """
        self.bind("<Return>", self.open_file)  # Add binding for main Enter key
        self.bind("<KP_Enter>", self.open_file)  # Add binding for numeric keypad Enter
        self.focus_set()
