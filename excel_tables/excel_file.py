from abc import ABC
from typing import Tuple, Optional
import os.path

import openpyxl as xl
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet


class ExcelFile(ABC):
    def __init__(self, file_path: str, worksheet_number: int = 0):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.wb, self.ws = ExcelFile.open_file(file_path, worksheet_number)

    @staticmethod
    def open_file(file_name: str, worksheet_number: int = 0) -> Tuple[Optional[Workbook], Optional[Worksheet]]:
        if file_name:
            try:
                wb = xl.load_workbook(file_name)
                ws = wb.worksheets[worksheet_number] if worksheet_number < len(wb.worksheets) else None
                print(f'File "{file_name}" opened successfully')
                return wb, ws
            except Exception as e:
                print(f"Error opening file {file_name}: {e}")
                return None, None
        else:
            return None, None

    def save_file(self, new_file_name: str = None) -> None:
        if self.wb is None:
            raise ValueError("Workbook is not initialized")
            
        new_file_name = new_file_name if new_file_name else self.file_name
        try:
            self.wb.save(new_file_name)
            print(f'File "{new_file_name}" saved successfully')
        except Exception as e:
            print(f"Error saving file {new_file_name}: {e}")

    # # Used in previous version
    # def change_print_area(self, print_area: List[str]) -> None:
    #     if self.ws is None:
    #         raise ValueError("Worksheet is not initialized")
    #
    #     print_area = print_area if print_area else self.ws.print_area
    #     self.ws.print_area = print_area
