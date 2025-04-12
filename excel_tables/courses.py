import re
from typing import Optional

from GoogleMyMaps import *


class Courses:
    def __init__(self, google_map: Map):
        self.courses_list = [
            layer for layer in google_map.layers
            if layer.name.upper().startswith("TRASA")
        ]
        self._set_kids_as_last_course()

    def _set_kids_as_last_course(self):
        for course in self.courses_list:
            if "KIDS" in course.name.upper():
                self.courses_list.remove(course)
                self.courses_list.append(course)
                break

    @staticmethod
    def get_obstacle_number(obstacle: Place) -> Optional[int]:
        if obstacle.place_type == "Point" and obstacle.icon:
            match = re.search(r'&text=(\d+)', obstacle.icon)
            if match:
                return int(match.group(1))
        return None

    def get_course_obstacles_number(self, course: Layer) -> int:
        for obstacle in reversed(course.places):
            number = self.get_obstacle_number(obstacle)
            if number is not None:
                return number
        return 0

    def get_course_index(self, course: Layer) -> Optional[int]:
        return self.courses_list.index(course)
