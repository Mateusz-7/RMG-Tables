import tkinter as tk
from tkinter import ttk, font

from excel_tables.obstacle_list import ObstacleList


class NotFoundObstaclesWindow(tk.Tk):
    """Window displaying obstacles that couldn't be found"""

    def __init__(self, obstacle_list):
        super().__init__()
        self.obstacle_list = obstacle_list
        self.title("Nie znalezione przeszkody")
        self.geometry("600x400")
        self.resizable(True, True)
        
        # Set window icon if available
        try:
            self.iconbitmap("assets/icon.ico")  # Replace with your icon path if available
        except:
            pass
            
        # Configure the style
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use clam theme as base
        
        # Configure colors with stronger contrast
        bg_color = "#f5f5f5"
        header_bg = "#3a7ebf"
        header_fg = "white"
        row_odd = "#e0e9f5"  # More pronounced light blue-gray
        row_even = "white"
        hover_color = "#c4d9f7"  # Darker hover color

        self.configure(bg=bg_color)

        # Configure fonts
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=10)

        header_font = font.Font(family=default_font.cget("family"), size=11, weight="bold")

        # Configure treeview style
        self.style.configure("Treeview",
                             background=row_even,
                             fieldbackground=row_even,
                             foreground="black",
                             rowheight=25,
                             borderwidth=0)

        self.style.configure("Treeview.Heading",
                             background=header_bg,
                             foreground=header_fg,
                             font=header_font,
                             relief="flat",
                             borderwidth=0)

        self.style.map("Treeview",
                       background=[("selected", "#4a8fd8")],
                       foreground=[("selected", "white")])

        self.style.map("Treeview.Heading",
                       background=[("active", "#2a6eaf")],
                       relief=[("active", "flat")])

        # Create a main frame
        main_frame = ttk.Frame(self, padding=10, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title_label = ttk.Label(main_frame,
                               text="Lista przeszkód, których nie udało się znaleźć",
                               font=font.Font(family=default_font.cget("family"), size=12, weight="bold"),
                               padding=(0, 0, 0, 10))
        title_label.pack(fill=tk.X)

        # Create a frame for the list with border
        frame = ttk.Frame(main_frame, style="TreeFrame.TFrame")
        frame.pack(fill=tk.BOTH, expand=True)

        # Create scrollbar
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create columns
        columns = ("course_name", "obstacle_number", "obstacle_name")

        # Create treeview
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)

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

        # Add alternating row colors
        self.tree.tag_configure('odd', background=row_odd)
        self.tree.tag_configure('even', background=row_even)

        # Add hover effect
        self.tree.bind("<Motion>", self.on_tree_hover)
        self.tree.tag_configure('hover', background=hover_color)
        self._hover_item = None

        # Add obstacles to the list
        self.populate_tree()

        # Add close button with custom style
        self.style.configure("Close.TButton",
                            font=font.Font(family=default_font.cget("family"), size=10),
                            background="#3a7ebf",
                            foreground="white")

        self.style.map("Close.TButton",
                      background=[("active", "#2a6eaf")],
                      foreground=[("active", "white")])

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        close_button = ttk.Button(button_frame, 
                                 text="Zamknij", 
                                 command=self.destroy,
                                 style="Close.TButton",
                                 width=15)
        close_button.pack(side=tk.RIGHT)
        
        # Count label
        count_text = f"Znaleziono {len(self.obstacle_list.not_found_obstacles)} przeszkód"
        count_label = ttk.Label(button_frame, text=count_text)
        count_label.pack(side=tk.LEFT, padx=5)

    def on_tree_hover(self, event):
        """Handle hover effect on treeview"""
        item = self.tree.identify_row(event.y)
        if item != self._hover_item:
            if self._hover_item:
                tags = self.tree.item(self._hover_item, 'tags')
                if tags and 'hover' in tags:
                    new_tags = tuple(t for t in tags if t != 'hover')
                    self.tree.item(self._hover_item, tags=new_tags)
            
            if item:
                tags = self.tree.item(item, 'tags')
                if tags:
                    self.tree.item(item, tags=tags + ('hover',))
                else:
                    self.tree.item(item, tags=('hover',))
            
            self._hover_item = item

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