from typing import Optional

from GoogleMyMaps.models import *
from .courses import Courses
from .excel_file import ExcelFile


class ObstacleList(ExcelFile):
    file_name = "LISTA PRZESZKÓD"
    file_path = f"WZORY/{file_name}.xlsx"

    def __init__(self, google_map: Map):
        super().__init__(self.file_path)
        self.google_map = google_map
        self.course_map = Courses(google_map)
        # TODO: put here offsets, columns

    def _write_headlines(self):
        [self._write_cell(self._get_course_column_number(course), 1, course.name[6:]) for course in self.course_map.courses_list]

    def _get_course_column_number(self, course: Layer) -> int:
        return self.course_map.get_course_index(course) * 3 + 1

    def _save_course_info(self, course: Layer):
        important_names = ["START", "META", "START KIDS", "META KIDS"]
        obstacle_row_offset = self.course_map.get_course_obstacles_number(self.course_map.courses_list[0]) + 3 if "KIDS" in course.name.upper() else 2

        for obstacle in course.places:
            obstacle_number = self.course_map.get_obstacle_number(obstacle)
            if obstacle_number is None:
                continue
            cell_line = obstacle_number + obstacle_row_offset

            self._write_cell(self._get_course_column_number(course), cell_line, obstacle_number)
            # self.ws[get_column_letter(numbers_column_number + 1) + str(cell_line)] = # Area number
            # self.ws[get_column_letter(numbers_column_number + 2) + str(cell_line)] = # KM number

            self._write_cell(19, cell_line, obstacle.name)
            if obstacle.name in important_names:
                self._bold_cell(19, cell_line)

            if obstacle.data is None:
                continue
            self._write_cell(20, cell_line, int(obstacle.data.get("WOLO", "")) if int(obstacle.data.get("WOLO", 0)) > 0 else "")
            self._write_cell(21, cell_line, int(obstacle.data.get("SĘDZIA", "")) if int(obstacle.data.get("SĘDZIA", 0)) > 0 else "")
            self._write_cell(24, cell_line, obstacle.data.get("OPIS", ""))
            # TODO: Make sure of the data naming

            # self.ws["V" + str(cell_line)] = # Responsible person

    def _save_obstacles_numbers(self, course: Layer):
        course_column = self._get_course_column_number(course)
        obstacle_row_offset = 2
        kids_obstacle_row_offset = self.course_map.get_course_obstacles_number(self.course_map.courses_list[0]) + 4

        last_found_obstacle_index = -1
        for analysed_obstacle in course.places:
            if self.course_map.get_obstacle_number(analysed_obstacle) is None:
                continue

            found_obstacle_index = self._find_and_write_obstacle(
                analysed_obstacle,
                self.course_map.courses_list[0].places[last_found_obstacle_index + 1:],
                course_column,
                obstacle_row_offset,
            )
            if found_obstacle_index is not None:
                last_found_obstacle_index = found_obstacle_index
                continue

            found_obstacle_index = self._find_and_write_obstacle(
                analysed_obstacle,
                self.course_map.courses_list[0].places[last_found_obstacle_index + 1::-1],
                course_column,
                obstacle_row_offset,
            )
            if found_obstacle_index is not None:
                last_found_obstacle_index = found_obstacle_index
                continue

            found_obstacle_index = self._find_and_write_obstacle(
                analysed_obstacle,
                self.course_map.courses_list[-1].places,
                course_column,
                kids_obstacle_row_offset,
            )
            if found_obstacle_index is None:
                print(f"Unable to find obstacle: {analysed_obstacle.name} from course: {course.name}")
                # TODO: Show on the Final Frame or Error Window

    def _find_and_write_obstacle(self, analysed_obstacle: Place, obstacles, course_column: int, row_offset: int = 0) -> Optional[int]:
        for obstacle in obstacles:
            print(analysed_obstacle.name, obstacle.name)
            if analysed_obstacle.name == obstacle.name:
                obstacle_row = self.course_map.get_obstacle_number(obstacle) + row_offset

                if self._get_cell_value(course_column, obstacle_row) is not None:
                    continue
                self._write_cell(course_column, obstacle_row, self.course_map.get_obstacle_number(analysed_obstacle))
                # self.ws[get_column_letter(numbers_column_number + 1) + str(cell_line)] = # Area number
                # self.ws[get_column_letter(numbers_column_number + 2) + str(cell_line)] = # KM number

                return self.course_map.get_obstacle_number(obstacle)
        return None

    def _sum_and_save_number_of_volunteers_and_judges(self):
        self._write_cell(20, 201, "=SUM(T3:T200)")
        self._write_cell(21, 201, "=SUM(U3:U200)")

    def _hide_unnecessary_columns_and_rows(self):
        self._group_columns(
            self._get_course_column_number(self.course_map.courses_list[-1]) + 3,
            18,
            True
        )
        self._group_rows(
            self.course_map.get_course_obstacles_number(self.course_map.courses_list[0]) + self.course_map.get_course_obstacles_number(self.course_map.courses_list[-1]) + 4,
            200,
            True
        )

    def _save_data(self) -> Optional[str]:
        self._write_headlines()
        self._save_course_info(self.course_map.courses_list[0])
        self._save_course_info(self.course_map.courses_list[-1])
        for course in self.course_map.courses_list[1:-1]:
            self._save_obstacles_numbers(course)
        self._sum_and_save_number_of_volunteers_and_judges()
        self._hide_unnecessary_columns_and_rows()
        return self.save_file(self.google_map.name + " - LISTA PRZESZKÓD.xlsx")

    @classmethod
    def create_and_save(cls, google_map: Map) -> Optional[str]:
        obstacle_list = cls(google_map)
        return obstacle_list._save_data()
