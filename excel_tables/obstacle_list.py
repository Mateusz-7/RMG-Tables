import re

import openpyxl as xl
from openpyxl.utils import get_column_letter

from GoogleMyMaps.models import *
from .excel_file import ExcelFile


class ObstacleList(ExcelFile):
    file_name = "LISTA PRZESZKÓD"
    file_path = f"WZORY/{file_name}.xlsx"

    # print_area = ['$A$1:$Y$201'] # Used in previous version

    def __init__(self, google_map: Map):
        super().__init__(self.file_path)
        self.google_map = google_map
        self.courses = [
            layer for layer in self.google_map.layers
            if layer.name.upper().startswith("TRASA")
        ]
        # TODO: Note that courses has to start with TRASA; KIDS last layer; first layer is the longest course / add visual options

    @staticmethod
    def _get_obstacle_number(obstacle: Place) -> int | None:
        if obstacle.place_type == "Point" and obstacle.icon:
            match = re.search(r'&text=(\d+)', obstacle.icon)
            if match:
                return int(match.group(1))
        return None

    def _get_course_obstacles_number(self, course: Layer) -> int:
        for obstacle in reversed(course.places):
            number = self._get_obstacle_number(obstacle)
            if number is not None:
                return number
        return 0

    def _save_headlines(self):
        for course in self.courses:
            cell_column = get_column_letter(self.courses.index(course) * 3 + 1)
            cell_line = '1'
            cell_value = course.name[6:]

            self.ws[cell_column + cell_line] = cell_value

    def _save_course_info(self, course: Layer):
        important_names = ["START", "META", "START KIDS", "META KIDS"]
        line_offset = self._get_course_obstacles_number(self.courses[0]) + 3 if "KIDS" in course.name.upper() else 2
        numbers_column_number = self.courses.index(course) * 3 + 1

        for obstacle in course.places:
            obstacle_number = self._get_obstacle_number(obstacle)
            if obstacle_number is None:
                continue
            cell_line = obstacle_number + line_offset

            self.ws[get_column_letter(numbers_column_number) + str(cell_line)] = obstacle_number
            # self.ws[get_column_letter(numbers_column_number + 1) + str(cell_line)] = # Area number
            # self.ws[get_column_letter(numbers_column_number + 2) + str(cell_line)] = # KM number

            self.ws["S" + str(cell_line)] = obstacle.name
            if obstacle.name in important_names:
                self.ws["S" + str(cell_line)].font = xl.styles.Font(bold=True, name="Calibri")

            if obstacle.data is None:
                continue
            self.ws["T" + str(cell_line)] = int(obstacle.data.get("WOLO", "")) if int(obstacle.data.get("WOLO", 0)) > 0 else ""
            self.ws["U" + str(cell_line)] = int(obstacle.data.get("SĘDZIA", "")) if int(obstacle.data.get("SĘDZIA", 0)) > 0 else ""
            self.ws["X" + str(cell_line)] = obstacle.data.get("OPIS", "")
            # TODO: Make sure of the data naming

            # self.ws["V" + str(cell_line)] = # Responsible person

    def _save_obstacles_numbers(self, course: Layer):
        numbers_column_number = self.courses.index(course) * 3 + 1
        line_offset = self._get_course_obstacles_number(self.courses[0]) + 4

        for obstacle in course.places:
            for main_obstacle in self.courses[0].places: # TODO: Counter for latest found obstacle
                if main_obstacle.name == obstacle.name:
                    cell_line = self._get_obstacle_number(main_obstacle) + 2

                    # TODO: Check if obstacle is not already numbered
                    self.ws[get_column_letter(numbers_column_number) + str(cell_line)] = self._get_obstacle_number(obstacle)
                    # self.ws[get_column_letter(numbers_column_number + 1) + str(cell_line)] = # Area number
                    # self.ws[get_column_letter(numbers_column_number + 2) + str(cell_line)] = # KM number

                    break
                # TODO: if obstacle not found -> look in kids -> if still not found -> visual indication

    def _sum_and_save_number_of_volunteers_and_judges(self):
        self.ws["T201"] = f"=SUM(T3:T200)"
        self.ws["U201"] = f"=SUM(U3:U200)"

    def hide_unnecessary_columns_and_rows(self):
        self.ws.column_dimensions.group(
            get_column_letter(len(self.courses) * 3 + 1),
            get_column_letter(18),
            hidden=True
        )
        self.ws.row_dimensions.group(
            self._get_course_obstacles_number(self.courses[0]) + self._get_course_obstacles_number(self.courses[-1]) + 4,
            200,
            hidden=True
        )

    def _save_data(self):
        self._save_headlines()
        self._save_course_info(self.courses[0])
        self._save_course_info(self.courses[-1])
        for course in self.courses[1:-1]:
            self._save_obstacles_numbers(course)
        self._sum_and_save_number_of_volunteers_and_judges()
        self.hide_unnecessary_columns_and_rows()
        self.save_file(self.google_map.name + " - LISTA PRZESZKÓD.xlsx")

    @classmethod
    def create_and_save(cls, google_map: Map):
        obstacle_list = cls(google_map)
        obstacle_list._save_data()
