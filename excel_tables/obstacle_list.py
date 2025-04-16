import logging
from typing import Optional, Tuple, List

from openpyxl.utils import get_column_letter

from GoogleMyMaps.models import *
from .areas import Areas
from .course_trail import CourseTrail
from .courses import Courses
from .excel_file import ExcelFile

log = logging.getLogger(__name__)

# List to store obstacles that couldn't be found
not_found_obstacles: List[Tuple[Place, str]] = []

def addToList(obstacle: Place, course_name: str = ""):
    """Add obstacle to the list of obstacles that couldn't be found"""
    not_found_obstacles.append((obstacle, course_name))

class ObstacleList(ExcelFile):
    IMPORTANT_OBSTACLE_NAMES = ["START", "META", "START KIDS", "META KIDS"]
    COLUMN_LAST_COURSE = 18
    COLUMN_NAME = 19
    COLUMN_WOLO = 20
    COLUMN_JUDGE = 21
    # COLUMN_WORKER = 22
    COLUMN_INFO = 24
    ROW_HEADERS = 1
    ROW_OBSTACLES_OFFSET = 2
    ROW_MAX = 200

    file_name = "LISTA PRZESZKÓD"
    file_path = f"WZORY/{file_name}.xlsx"

    def __init__(self, google_map: Map):
        super().__init__(self.file_path)
        self.google_map = google_map
        self.courses = Courses(google_map)
        self.areas = Areas(google_map)

    def _write_headlines(self):
        for course in self.courses.courses_list:
            self._write_cell(self._get_course_column_number(course), self.ROW_HEADERS, course.name[6:])

    def _get_course_column_number(self, course: Layer) -> int:
        return self.courses.get_course_index(course) * 3 + 1

    def _write_obstacle_number_area_km(self, course_column: int, obstacle_row: int, obstacle_number: int,
                                       obstacle_area: int, obstacle_distance: Optional[float]) -> None:
        if obstacle_distance is not None:
            obstacle_distance = round(obstacle_distance / 1000, 1)
        self._write_cell(course_column, obstacle_row, obstacle_number)
        self._write_cell(course_column + 1, obstacle_row, obstacle_area)
        self._write_cell(course_column + 2, obstacle_row, obstacle_distance)

    def _write_obstacle_name_data(self, obstacle: Place, obstacle_row: int):
        self._write_cell(self.COLUMN_NAME, obstacle_row, obstacle.name)
        if obstacle.name.upper() in self.IMPORTANT_OBSTACLE_NAMES:
            self._bold_cell(self.COLUMN_NAME, obstacle_row)

        # self.ws["V" + str(cell_line)] = # Responsible person

        data = self._get_obstacle_data(obstacle)
        if data is None:
            return

        wolo, judge, description = data
        self._write_cell(self.COLUMN_WOLO, obstacle_row, wolo if wolo > 0 else None)
        self._write_cell(self.COLUMN_JUDGE, obstacle_row, judge if judge > 0 else None)
        self._write_cell(self.COLUMN_INFO, obstacle_row, description)

    def _get_obstacle_data(self, obstacle: Place) -> Optional[Tuple[int, int, str]]:
        if obstacle.data is None:
            return None
        normalized_data = {key[0].upper(): value for key, value in obstacle.data.items()}

        wolo = self._get_person_number(normalized_data, "W")  # WOLO
        judge = self._get_person_number(normalized_data, "S")  # SĘDZIA
        description = normalized_data.get("O", "")  # OPIS
        return wolo, judge, description

    @staticmethod
    def _get_person_number(data: dict, data_key: str) -> int:
        try:
            return int(data.get(data_key, 0))
        except ValueError:
            # TODO: info?
            log.warning("Invalid data type for %s: %s", data_key, type(data.get(data_key, 0)))
            return 0

    def _write_course_info(self, course: Layer):
        row_offset = self.courses.get_course_obstacles_number(self.courses.courses_list[
                                                                  0]) + self.ROW_OBSTACLES_OFFSET + 2 if "KIDS" in course.name.upper() else self.ROW_OBSTACLES_OFFSET

        for obstacle in course.places:
            if obstacle.place_type != "Point":
                continue

            self._write_single_obstacle_info(course, obstacle, row_offset)

    def _write_single_obstacle_info(self, course: Layer, obstacle: Place, row_offset: int):
        course_column = self._get_course_column_number(course)
        obstacle_number = self.courses.get_obstacle_number(obstacle)
        if obstacle_number is None:
            log.warning("Obstacle without number: %s, %s", obstacle.name, obstacle.icon)
            return
        obstacle_row = obstacle_number + row_offset
        obstacle_area_number = self.areas.get_obstacle_area_number(obstacle)
        obstacle_distance = CourseTrail(course).get_obstacle_distance(obstacle)
        self._write_obstacle_number_area_km(course_column, obstacle_row, obstacle_number, obstacle_area_number, obstacle_distance)
        self._write_obstacle_name_data(obstacle, obstacle_row)

    def _write_obstacles_numbers(self, course: Layer):
        obstacle_row_offset = self.ROW_OBSTACLES_OFFSET
        kids_obstacle_row_offset = self.courses.get_course_obstacles_number(
            self.courses.courses_list[0]) + self.ROW_OBSTACLES_OFFSET + 2

        last_found_obstacle_index = -1
        for analysed_obstacle in course.places:
            if analysed_obstacle.place_type != "Point":
                continue

            last_found_obstacle_index = self._process_obstacle(
                course,
                analysed_obstacle,
                obstacle_row_offset,
                kids_obstacle_row_offset,
                last_found_obstacle_index
            )

    def _process_obstacle(
            self,
            course: Layer,
            analysed_obstacle: Place,
            obstacle_row_offset: int,
            kids_obstacle_row_offset: int,
            last_found_obstacle_index: int
    ) -> int:
        found_obstacle_index = self._find_and_write_obstacle(
            analysed_obstacle,
            self.courses.courses_list[0].places[last_found_obstacle_index + 1:],
            course,
            obstacle_row_offset,
        )
        if found_obstacle_index is not None:
            return last_found_obstacle_index + found_obstacle_index + 1

        found_obstacle_index = self._find_and_write_obstacle(
            analysed_obstacle,
            self.courses.courses_list[0].places[last_found_obstacle_index + 1::-1],
            course,
            obstacle_row_offset,
        )
        if found_obstacle_index is not None:
            return last_found_obstacle_index + found_obstacle_index + 1

        found_obstacle_index = self._find_and_write_obstacle(
            analysed_obstacle,
            self.courses.courses_list[-1].places,
            course,
            kids_obstacle_row_offset,
        )
        if found_obstacle_index is None:
            log.warning("-Unable to find obstacle: %s from course: %s", analysed_obstacle.name, course.name)
            # Add to list with course name
            addToList(analysed_obstacle, course.name)

        return last_found_obstacle_index

    def _find_and_write_obstacle(self, analysed_obstacle: Place, obstacles, course: Layer, row_offset: int) -> \
            Optional[int]:
        for obstacle in obstacles:
            if analysed_obstacle.name.upper().strip("\n").strip() == obstacle.name.upper().strip("\n").strip():
                obstacle_number = self.courses.get_obstacle_number(obstacle)
                if obstacle_number is None:
                    log.warning("Obstacle without number: %s, %s", obstacle.name, obstacle.icon)
                    return
                obstacle_row = obstacle_number + row_offset
                course_column = self._get_course_column_number(course)
                if self._get_cell_value(course_column, obstacle_row) is not None:
                    continue

                analysed_obstacle_number = self.courses.get_obstacle_number(analysed_obstacle)
                obstacle_area_number = self.areas.get_obstacle_area_number(obstacle)
                obstacle_distance = CourseTrail(course).get_obstacle_distance(obstacle)
                self._write_obstacle_number_area_km(course_column, obstacle_row, analysed_obstacle_number,
                                                    obstacle_area_number, obstacle_distance)

                return obstacles.index(obstacle)
        return None

    def _sum_and_write_number_of_volunteers_and_judges(self):
        self._write_cell(
            self.COLUMN_WOLO,
            self.ROW_MAX + 1,
            f"=SUM({get_column_letter(self.COLUMN_WOLO)}{self.ROW_OBSTACLES_OFFSET + 1}:{get_column_letter(self.COLUMN_WOLO)}{self.ROW_MAX})"
        )
        self._write_cell(
            self.COLUMN_JUDGE,
            self.ROW_MAX + 1,
            f"=SUM({get_column_letter(self.COLUMN_JUDGE)}{self.ROW_OBSTACLES_OFFSET + 1}:{get_column_letter(self.COLUMN_JUDGE)}{self.ROW_MAX})"
        )

    def _hide_unnecessary_columns_and_rows(self):
        self._group_columns(
            self._get_course_column_number(self.courses.courses_list[-1]) + 3,
            self.COLUMN_LAST_COURSE,
            True
        )
        self._group_rows(
            self.courses.get_course_obstacles_number(self.courses.courses_list[0])
            + self.courses.get_course_obstacles_number(self.courses.courses_list[-1])
            + self.ROW_OBSTACLES_OFFSET + 2,
            self.ROW_MAX,
            True
        )

    def _save_data(self) -> Optional[str]:
        self._write_headlines()
        self._write_course_info(self.courses.courses_list[0])
        self._write_course_info(self.courses.courses_list[-1])
        for course in self.courses.courses_list[1:-1]:
            self._write_obstacles_numbers(course)
        self._sum_and_write_number_of_volunteers_and_judges()
        self._hide_unnecessary_columns_and_rows()
        return self.save_file(self.google_map.name + " - LISTA PRZESZKÓD.xlsx")

    @classmethod
    def create_and_save(cls, google_map: Map) -> Tuple[Optional[str], List[Tuple[Place, str]]]:
        obstacle_list = cls(google_map)
        file_path = obstacle_list._save_data()
        return file_path, not_found_obstacles