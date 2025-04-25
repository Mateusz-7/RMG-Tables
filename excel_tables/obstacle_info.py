from abc import ABC, abstractmethod

from configs.utils import are_strings_similar
from excel_tables.excel_file import ExcelFile


class ObstacleInfo(ExcelFile, ABC):
    """
    Abstract class for handling obstacle information in Excel files.

    Attributes:
        file_name (str): The name of the Excel file containing obstacle information.
        file_path (str): The path to the Excel file.
        WORKSHEET_NUMBER (int): The worksheet number to be used in the Excel file.
        COLUMN_NAME (int): The column number for obstacle names.
        COLUMN_WORKER (int): The column number for worker names.
        ROW_FIRST_OBSTACLE (int): The row number where the first obstacle is located.
    """
    file_name = "PRZESZKODY - SZEF TRASY"
    file_path = f"WZORY/{file_name}.xlsx"

    WORKSHEET_NUMBER: int
    COLUMN_NAME: int
    COLUMN_WORKER: int
    ROW_FIRST_OBSTACLE: int

    def __init__(self):
        """
        Initializes the ObstacleInfo instance with the specified worksheet number.
        """
        super().__init__(self.file_path, self.WORKSHEET_NUMBER)

    def get_worker(self, obstacle_name: str) -> str | None:
        """
        Get the worker responsible for the obstacle.

        Args:
            obstacle_name (str): The name of the obstacle.

        Returns:
            str | None: The name of the worker responsible for the obstacle, or None if not found.
        """
        for row in range(self.ROW_FIRST_OBSTACLE, self.ws.max_row + 1):
            if are_strings_similar(self._get_cell_value(self.COLUMN_NAME, row), obstacle_name):
                return self._get_cell_value(self.COLUMN_WORKER, row)
        return None
