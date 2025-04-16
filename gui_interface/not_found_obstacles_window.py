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
        
        # Configure colors with dark theme - matching MapLinkFrame
        bg_color = "#232323"  # Dark background matching MapLinkFrame
        header_bg = "#2c2c2c"  # Slightly lighter dark for header
        header_fg = "#e0e0e0"  # Light gray text for header
        row_odd = "#2a2a2a"    # Slightly lighter than background
        row_even = "#252525"   # Between bg_color and row_odd
        hover_color = "#3a3a3a"  # Lighter shade for hover
        text_color = "#e0e0e0"   # Light gray text
        button_bg = "#ffde00"    # Yellow for buttons (matching MapLinkFrame)
        button_fg = "#000000"    # Black text for buttons
        button_active_fg = "#565656"  # Gray text for active buttons
        
        # Set window background color
        self.configure(bg=bg_color)
        
        # Configure fonts
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=10)
        header_font = font.Font(family=default_font.cget("family"), size=11, weight="bold")
        title_font = font.Font(family=default_font.cget("family"), size=12, weight="bold")
        
        # Override the Treeview background globally to fix white areas
        self.option_add("*TCombobox*Listbox.background", bg_color)
        self.option_add("*TCombobox*Listbox.foreground", text_color)
        self.option_add("*Treeview.background", bg_color)
        self.option_add("*Treeview.fieldbackground", bg_color)
        
        # Create a main frame
        main_frame = tk.Frame(self, bg=bg_color, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title_label = tk.Label(
            main_frame,
            text="Lista przeszkód, których nie udało się znaleźć",
            font=title_font,
            bg=bg_color,
            fg=text_color,
            pady=10
        )
        title_label.pack(fill=tk.X)

        # Create a frame for the list
        frame = tk.Frame(main_frame, bg=bg_color, highlightthickness=0, bd=0)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create scrollbar with matching colors
        scrollbar = tk.Scrollbar(frame, 
                               bg=bg_color, 
                               troughcolor=row_odd, 
                               activebackground=hover_color,
                               highlightbackground=bg_color,
                               highlightcolor=bg_color)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create columns
        columns = ("course_name", "obstacle_number", "obstacle_name")

        # Create treeview with explicit background
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scrollbar.set, style="Treeview")
        self.tree.configure(style="Treeview")  # Ensure style is applied

        # Configure treeview style
        style = ttk.Style()
        style.theme_use("clam")  # Use clam theme as base
        
        # Fix for empty space in treeview
        style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ])
        
        # Set the background color for the entire Treeview widget
        style.configure("Treeview", 
                        background=bg_color,  # Use bg_color instead of row_even for the entire background
                        fieldbackground=bg_color,  # Use bg_color for the field background
                        foreground=text_color,
                        rowheight=25,
                        borderwidth=0)

        # Explicitly configure Treeview.Heading with dark background and light text
        style.configure("Treeview.Heading",
                        background=header_bg,
                        foreground=header_fg,
                        font=header_font,
                        relief="flat",
                        borderwidth=0)

        # Map Treeview.Heading for active state
        style.map("Treeview.Heading",
                  background=[("active", "#3c3c3c"), ("!active", header_bg)],
                  foreground=[("active", "white"), ("!active", header_fg)],
                  relief=[("active", "flat"), ("!active", "flat")])

        # Map Treeview for selected state
        style.map("Treeview",
                  background=[("selected", hover_color), ("!selected", row_even)],
                  foreground=[("selected", "white"), ("!selected", text_color)])

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
        self.tree.tag_configure('odd', background=row_odd, foreground=text_color)
        self.tree.tag_configure('even', background=row_even, foreground=text_color)

        # Add hover effect with explicit foreground
        self.tree.bind("<Motion>", self.on_tree_hover)
        self.tree.tag_configure('hover', background=hover_color, foreground=text_color)
        self._hover_item = None

        # Add obstacles to the list
        self.populate_tree()

        # Create button frame
        button_frame = tk.Frame(main_frame, bg=bg_color)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        # Count label
        count_text = f"Lista zawiera {len(self.obstacle_list.not_found_obstacles)} przeszkód"
        count_label = tk.Label(
            button_frame, 
            text=count_text,
            bg=bg_color,
            fg=text_color,
            font=default_font
        )
        count_label.pack(side=tk.LEFT, padx=5)
        
        # Create close button - matching style from MapLinkFrame
        close_button = tk.Button(
            button_frame, 
            text="Zamknij", 
            command=self.destroy,
            width=15,
            bg=button_bg,
            fg=button_fg,
            activeforeground=button_bg, # button_active_fg
            activebackground=bg_color,
            bd=3,
            font=default_font,
            cursor="hand2"
        )
        close_button.pack(side=tk.RIGHT)
        
        # Add hover effects to button
        close_button.bind("<Enter>", lambda e: close_button.config(fg=button_bg))
        close_button.bind("<Leave>", lambda e: close_button.config(fg=button_fg))

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
