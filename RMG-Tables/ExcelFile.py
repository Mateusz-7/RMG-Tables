from abc import ABC

import openpyxl as xl


class ExcelFile(ABC):
    def __init__(self, file_name: str, worksheet_number: int = 0):
        self.wb, self.ws = ExcelFile.open_file(file_name, worksheet_number)

    @staticmethod
    def open_file(file_name: str, worksheet_number: int = 0):
        if file_name:
            wb = xl.load_workbook(file_name)
            ws = wb.worksheets[worksheet_number] if worksheet_number < len(wb.worksheets) else None
            return wb, ws
        else:
            return None, None

    def change_print_area(self, print_area: list[str]):
        print_area = print_area if print_area else self.ws.print_area
        self.ws.print_area = print_area

    def save_file(self, new_file_name: str = None):
        new_file_name = new_file_name if new_file_name else self.wb.filename
        self.wb.save(new_file_name)
