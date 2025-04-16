import tkinter as tk
from tkinter import ttk
from typing import List, Tuple

from GoogleMyMaps.models import Place
from excel_tables.obstacle_list import not_found_obstacles


class NotFoundObstaclesWindow(tk.Toplevel):
    """Window displaying obstacles that couldn't be found"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Not Found Obstacles")
        self.geometry("600x400")
        self.resizable(True, True)

        # Create a frame for the list
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create scrollbar
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create columns
        columns = ("obstacle_name", "course_name")

        # Create treeview
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)

        # Define headings
        self.tree.heading("obstacle_name", text="Obstacle Name")
        self.tree.heading("course_name", text="Course Name")

        # Define columns width
        self.tree.column("obstacle_name", width=300)
        self.tree.column("course_name", width=200)

        # Pack treeview
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configure scrollbar
        scrollbar.config(command=self.tree.yview)

        # Add obstacles to the list
        self.populate_tree()

        # Add close button
        close_button = ttk.Button(self, text="Close", command=self.destroy)
        close_button.pack(pady=10)

    def populate_tree(self):
        """Populate the tree with obstacles"""
        for i, (obstacle, course_name) in enumerate(not_found_obstacles):
            self.tree.insert("", tk.END, values=(obstacle.name, course_name))


def show_not_found_obstacles(parent):
    """Show window with obstacles that couldn't be found"""
    if not not_found_obstacles:
        return

    window = NotFoundObstaclesWindow(parent)
    window.focus_set()
    window.grab_set()  # Make window modal
    return window
