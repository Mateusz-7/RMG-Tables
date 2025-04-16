import tkinter as tk
from tkinter import ttk

from excel_tables.obstacle_list import ObstacleList


class NotFoundObstaclesWindow(tk.Tk):
    """Window displaying obstacles that couldn't be found"""

    def __init__(self, obstacle_list):
        super().__init__()
        self.obstacle_list = obstacle_list
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
        columns = ( "course_name", "obstacle_number", "obstacle_name")

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

        # Add obstacles to the list
        self.populate_tree()

        # Add close button
        close_button = ttk.Button(self, text="Close", command=self.destroy)
        close_button.pack(pady=10)

    def populate_tree(self):
        """Populate the tree with obstacles"""
        for i, (course, number, obstacle) in enumerate(self.obstacle_list.not_found_obstacles):
            self.tree.insert("", tk.END, values=(course.name, number, obstacle.name))


    @staticmethod
    def show_not_found_obstacles(obstacle_list: ObstacleList):
        """Show window with obstacles that couldn't be found"""
        if not obstacle_list.not_found_obstacles:
            return

        window = NotFoundObstaclesWindow(obstacle_list)
        return window
