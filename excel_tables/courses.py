import re
from typing import Optional

from GoogleMyMaps import *


class Courses:
    """
    A class to manage race courses from Google My Maps data.
    """
    
    def __init__(self, google_map: Map):
        """
        Initialize the Courses object with courses from a Google Map.
        
        Parameters:
            google_map (Map): A Google My Maps object containing course layers.
        """
        self.courses_list = [
            layer for layer in google_map.layers
            if layer.name.upper().startswith("TRASA")
        ]
        self._set_kids_as_last_course()

    def _set_kids_as_last_course(self):
        """
        Reorder courses to ensure the kids' course is always the last one in the list.
        """
        for course in self.courses_list:
            if "KIDS" in course.name.upper():
                self.courses_list.remove(course)
                self.courses_list.append(course)
                break

    @staticmethod
    def get_obstacle_number(obstacle: Place) -> Optional[int]:
        """
        Extract the obstacle number from a place's icon URL.
        
        Parameters:
            obstacle (Place): The place object representing an obstacle.
            
        Returns:
            Optional[int]: The extracted obstacle number if found, None otherwise.
        """
        if obstacle.place_type == "Point" and obstacle.icon:
            match = re.search(r'&text=(\d+)', obstacle.icon)
            if match:
                return int(match.group(1))
        return None

    @staticmethod
    def get_course_obstacles_number(course: Layer) -> int:
        """
        Get the total number of obstacles in a course.
        
        Parameters:
            course (Layer): The course layer to analyze.
            
        Returns:
            int: The highest obstacle number found in the course, or 0 if none found.
        """
        for obstacle in reversed(course.places):
            # number = self.get_obstacle_number(obstacle)
            number = Courses.get_obstacle_number(obstacle)
            if number is not None:
                return number
        return 0

    def get_course_index(self, course: Layer) -> Optional[int]:
        """
        Get the index of a course in the courses list.
        
        Parameters:
            course (Layer): The course layer to find.
            
        Returns:
            Optional[int]: The index of the course in the courses_list, or None if not found.
        """
        return self.courses_list.index(course)