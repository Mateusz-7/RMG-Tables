import logging
import os
import os.path
import tkinter as tk
from abc import ABC
from tkinter import filedialog
from typing import Tuple, Optional

import openpyxl as xl
from openpyxl.utils import get_column_letter
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from excel_tables.utils import resource_path


class ExcelFile(ABC):
    def __init__(self, file_path: str, worksheet_number: int = 0):
        self.file_path = resource_path(file_path)
        self.file_name = os.path.basename(file_path)
        self.wb, self.ws = ExcelFile.open_file(self.file_path, worksheet_number)

    @staticmethod
    def open_file(file_name: str, worksheet_number: int = 0) -> Tuple[Optional[Workbook], Optional[Worksheet]]:
        print("Opening file: ", file_name)
        if file_name:
            try:
                wb = xl.load_workbook(file_name)
                ws = wb.worksheets[worksheet_number] if worksheet_number < len(wb.worksheets) else None
                print("File opened successfully: ", file_name)
                return wb, ws
            except Exception as e:
                print(f"*Error opening file {file_name}: {e}")
                return None, None
        else:
            return None, None

    def save_file(self, new_file_name: str = None) -> Optional[str]:
        print("Saving file:", self.file_name)
        if self.wb is None:
            raise ValueError("Workbook is not initialized")

        root = tk.Tk()
        root.withdraw()
        new_file_name = filedialog.asksaveasfilename(
            initialdir=".",
            initialfile=new_file_name,
            defaultextension=".xlsx",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
        )
        root.destroy()

        if new_file_name:
            try:
                self.wb.save(new_file_name)
                print("File saved successfully: ", new_file_name)
                return new_file_name
            except Exception as e:
                print(f"*Error saving file {new_file_name}: {e}")
        else:
            print("File name not provided")
            return None

    def _write_cell(self, col: int, row: int, value) -> None:
        self.ws[f"{get_column_letter(col)}{row}"] = value

    def _get_cell_value(self, col: int, row: int) -> str:
        return self.ws[f"{get_column_letter(col)}{row}"].value

    def _group_rows(self, start_row: int, end_row: int, hidden: bool = False) -> None:
        self.ws.row_dimensions.group(start_row, end_row, hidden=hidden)

    def _group_columns(self, start_col: int, end_col: int, hidden: bool = False) -> None:
        if start_col <= end_col:
            self.ws.column_dimensions.group(get_column_letter(start_col), get_column_letter(end_col), hidden=hidden)

    def _bold_cell(self, col: int, row: int) -> None:
        self.ws[f"{get_column_letter(col)}{row}"].font = xl.styles.Font(bold=True, name="Calibri")
