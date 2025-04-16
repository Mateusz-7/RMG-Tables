import tkinter as tk
from tkinter import ttk, font

from excel_tables.obstacle_list import ObstacleList
from configs.utils import Colors


class NotFoundObstaclesWindow(tk.Tk):
    """Window displaying obstacles that couldn't be found"""

    def __init__(self, obstacle_list):
        super().__init__()
        self.obstacle_list = obstacle_list
        self.title("RMG - Robot Mateusza Grzech")
        self.geometry("600x400")
        self.resizable(True, True)

        # Set window background color
        self.configure(bg=Colors.BG_COLOR)

        # Configure fonts
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=10)
        title_font = font.Font(family=default_font.cget("family"), size=12, weight="bold")

        # Create a main frame
        main_frame = tk.Frame(self, bg=Colors.BG_COLOR, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title_label = tk.Label(
            main_frame,
            text="Lista przeszkód, których nie udało się znaleźć",
            font=title_font,
            bg=Colors.BG_COLOR,
            fg=Colors.MAIN_YELLOW,
            pady=10
        )
        title_label.pack(fill=tk.X)

        # Create a frame for the list
        frame = tk.Frame(main_frame, bg=Colors.BG_COLOR, highlightthickness=0, bd=0)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create scrollbar with matching colors
        scrollbar = tk.Scrollbar(frame,
                                 bg=Colors.MAIN_YELLOW,
                                 troughcolor=Colors.MAIN_DARKER,
                                 activebackground=Colors.MAIN_YELLOW)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create columns
        columns = ("course_name", "obstacle_number", "obstacle_name")

        # Create treeview with explicit background
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scrollbar.set,
                                 style="Treeview")
        self.tree.configure(style="Treeview")  # Ensure style is applied

        # Define headings
        self.tree.heading("course_name", text="Formuła")
        self.tree.heading("obstacle_number", text="Numer")
        self.tree.heading("obstacle_name", text="Nazwa Przeszkody")

        # Define columns width
        self.tree.column("course_name", width=175)
        self.tree.column("obstacle_number", width=40, anchor=tk.E)
        self.tree.column("obstacle_name", width=285)

        # Pack treeview
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configure scrollbar
        scrollbar.config(command=self.tree.yview)

        # Add alternating row colors with explicit foreground
        self.tree.tag_configure('odd', background=Colors.BG_COLOR, foreground=Colors.TEXT_COLOR)
        self.tree.tag_configure('even', background=Colors.BG_LIGHTER, foreground=Colors.TEXT_COLOR)

        # Add obstacles to the list
        self.populate_tree()

        # Create button frame
        button_frame = tk.Frame(main_frame, bg=Colors.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        # Count label
        count_text = f"Lista zawiera {len(self.obstacle_list.not_found_obstacles)} przeszkód"
        count_label = tk.Label(
            button_frame,
            text=count_text,
            bg=Colors.BG_COLOR,
            fg=Colors.MAIN_YELLOW,
            font=default_font
        )
        count_label.pack(side=tk.LEFT, padx=5)

    def populate_tree(self):
        """Populate the tree with obstacles"""
        for i, (course, number, obstacle) in enumerate(self.obstacle_list.not_found_obstacles):
            tag = 'odd' if i % 2 else 'even'
            self.tree.insert("", tk.END, values=(course.name, number, obstacle.name), tags=(tag,))

    @staticmethod
    def show_not_found_obstacles(obstacle_list: ObstacleList):
        """Show window with obstacles that couldn't be found"""
        if not obstacle_list.not_found_obstacles:
            return

        window = NotFoundObstaclesWindow(obstacle_list)
        window.focus_force()  # Force focus on this window
        return window
