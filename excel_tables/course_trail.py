import logging
from math import radians, sin, cos, sqrt, atan2

import numpy as np

from GoogleMyMaps import Layer, Place
from configs.utils import are_strings_similar

log = logging.getLogger(__name__)


class CourseTrail:
    """
    A class that represents a course trail and provides methods for distance calculations.
    """

    def __init__(self, course: Layer):
        """
        Initialize a CourseTrail object with a course layer.

        Parameters:
            course (Layer): The course layer containing places and trail information.
        """
        self.trail = self._get_right_direction_trail(course)

    @staticmethod
    def _get_trail(course: Layer) -> list | None:
        """
        Extract the trail coordinates from a course layer.

        Searches for a place of type "Line" within the course that has a name matching
        or contained within the course name.

        Parameters:
            course (Layer): The course layer containing places to search through.

        Returns:
            list | None: A list of coordinate points forming the trail, or None if no matching trail is found.
        """
        line_counter = 0
        last_line = None
        for place in course.places:
            if place.place_type == "Line":
                line_counter += 1
                last_line = place
                if are_strings_similar(place.name, course.name):
                    return place.coords
        if line_counter == 1 and last_line is not None:
            return last_line.coords
        else:
            log.warning("Couldn't find trail in course: ", course.name)
            return None

    def _get_right_direction_trail(self, course: Layer) -> list | None:
        """
        Determines and returns the trail in the correct direction based on obstacle positions.

        Parameters:
            course (Layer): The course layer containing places and trail information.

        Returns:
            list | None: Trail coordinates in the correct direction, or None if invalid.
        """
        trail = self._get_trail(course)
        if not trail:
            return None

        distances = self._get_start_end_obstacle_distances(course.places, trail)
        if distances is None:
            return trail
        start_distance, end_distance = distances

        return trail[::-1] if start_distance > end_distance else trail

    def _get_start_end_obstacle_distances(self, places: list[Place], trail: list) -> tuple[float, float] | None:
        """
        Calculates distances to the first obstacles from both ends of the trail.

        Parameters:
            places (list[Place]): List of places in the course.
            trail (list): The trail coordinates.

        Returns:
            tuple[float, float] | None: Tuple of (start_distance, end_distance) or None if invalid.
        """
        first_obstacle = self._get_first_obstacle_in_course(places)
        last_obstacle = self._get_first_obstacle_in_course(places[::-1])

        if not (first_obstacle and last_obstacle):
            return None

        start_distance = self.get_obstacle_distance(first_obstacle, trail)
        end_distance = self.get_obstacle_distance(last_obstacle, trail)

        if not (start_distance and end_distance):
            return None

        return start_distance, end_distance

    @staticmethod
    def _get_first_obstacle_in_course(course_places: list[Place]) -> Place | None:
        """
        Determines the first obstacle in a given list of course places, where an obstacle
        is defined as a place with a type of "Point".

        :param course_places: A list of Place objects representing locations in the course.
        :return: The first Place object in the list with a place_type of "Point",
            or None if no such Place exists.
        """
        for obstacle in course_places:
            if obstacle.place_type == "Point":
                return obstacle
        return None

    def get_obstacle_distance(self, obstacle: Place, trail: list = None) -> float | None:
        """
        Calculate the distance from the start of the trail to a given obstacle.

        Parameters:
            obstacle (Place): The obstacle place object containing coordinates.
            trail (list, optional): The trail coordinates. If None, uses self.trail.

        Returns:
            float | None: Distance in meters from the start of the trail to the given obstacle,
                            or None if coordinates are missing.
        """
        if not obstacle.coords:
            log.warning("Obstacle cords is None")
            return None

        # Use self.trail if the trail parameter is not provided
        if trail is None:
            trail = self.trail

        if not trail:
            log.warning("Trail is None")
            return None

        segment_idx, distance_along, perpendicular_distance = CourseTrail._find_closest_line_segment(obstacle.coords, trail)

        return self._calculate_total_distance(segment_idx, distance_along, trail)

    @staticmethod
    def _calculate_total_distance(segment_idx, distance_along, trail):
        """
        Calculate distance between starting point and a specified point along the trail.

        Parameters:
            segment_idx (int): Index of the segment where the point is located.
            distance_along (float): Distance along the segment from its start point.
            trail (list): The trail coordinates.

        Returns:
            float: Total distance in meters from the start of the trail to the specified point.
        """
        total_distance = 0
        for i in range(segment_idx):
            total_distance += CourseTrail._haversine_distance(
                trail[i][0], trail[i][1],
                trail[i + 1][0], trail[i + 1][1]
            )

        total_distance += distance_along

        return total_distance

    @staticmethod
    def _haversine_distance(lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points on the earth.

        Parameters:
            lat1 (float): Latitude of the first point in decimal degrees.
            lon1 (float): Longitude of the first point in decimal degrees.
            lat2 (float): Latitude of the second point in decimal degrees.
            lon2 (float): Longitude of the second point in decimal degrees.

        Returns:
            float: Distance in meters between the two points.
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        r = 6371000  # Radius of earth in meters
        return r * c


    @staticmethod
    def _point_to_line_distance(point, line_start, line_end):
        """
        Calculate the minimum distance from a point to a line segment.

        Parameters:
            point (tuple): A tuple containing (lat, lon) of the point.
            line_start (tuple): A tuple containing (lat, lon) of the line segment start.
            line_end (tuple): A tuple containing (lat, lon) of the line segment end.

        Returns:
            tuple: A tuple containing:
                - distance (float): The perpendicular distance in meters from the point to the line segment.
                - along_line (float): The distance in meters along the line segment from the start point
                                     to the projection of the given point onto the segment.
        """
        # Convert to radians for calculations
        lat, lon = point
        lat1, lon1 = line_start
        lat2, lon2 = line_end

        # Calculate distances
        d_point_to_start = CourseTrail._haversine_distance(lat, lon, lat1, lon1)
        d_point_to_end = CourseTrail._haversine_distance(lat, lon, lat2, lon2)
        d_start_to_end = CourseTrail._haversine_distance(lat1, lon1, lat2, lon2)

        # If the line segment is very short, just return distance to either endpoint
        if d_start_to_end < 1:  # Less than 1 meter
            return min(d_point_to_start, d_point_to_end), 0 if d_point_to_start < d_point_to_end else d_start_to_end

        # Check if the closest point is one of the endpoints
        # Using the law of cosines to check if the point is outside the line segment
        if d_point_to_start == 0 or d_start_to_end == 0:
            return d_point_to_start, 0
        cos_angle = (d_point_to_start ** 2 + d_start_to_end ** 2 - d_point_to_end ** 2) / (
                    2 * d_point_to_start * d_start_to_end)

        # Handle floating point errors
        if cos_angle > 1:
            cos_angle = 1
        elif cos_angle < -1:
            cos_angle = -1

        angle = np.arccos(cos_angle)

        if angle > np.pi / 2:
            # The closest point is the start point
            return d_point_to_start, 0

        if d_point_to_end == 0 or d_start_to_end == 0:
            return d_point_to_end, d_start_to_end
        cos_angle = (d_point_to_end ** 2 + d_start_to_end ** 2 - d_point_to_start ** 2) / (
                    2 * d_point_to_end * d_point_to_start)

        # Handle floating point errors
        if cos_angle > 1:
            cos_angle = 1
        elif cos_angle < -1:
            cos_angle = -1

        angle = np.arccos(cos_angle)

        if angle > np.pi / 2:
            # The closest point is the end point
            return d_point_to_end, d_start_to_end

        # Calculate the perpendicular distance
        # Using the formula: area of triangle / base length
        # Area can be calculated using Heron's formula
        s = (d_point_to_start + d_point_to_end + d_start_to_end) / 2
        area = sqrt(s * (s - d_point_to_start) * (s - d_point_to_end) * (s - d_start_to_end))
        height = 2 * area / d_start_to_end

        # Calculate the distance along the line from start to the projection of the point
        # Using Pythagorean theorem
        d_along_line = sqrt(d_point_to_start ** 2 - height ** 2)

        return height, d_along_line


    @staticmethod
    def _find_closest_line_segment(point, line_points):
        """
        Find the line segment in a list of points that is closest to the given point.

        This function iterates through all line segments formed by consecutive points
        in the provided list and determines which segment is closest to the specified point.
        It uses the _point_to_line_distance method to calculate distances.

        Parameters:
            point (tuple): A tuple containing the latitude and longitude (lat, lon) of the point.
            line_points (list): A list of points (each as a lat, lon tuple) forming a polyline.

        Returns:
            tuple: A tuple containing three elements:
                - closest_segment_idx (int): The index of the first point of the closest line segment.
                - distance_along_line (float): The distance in meters along the closest segment from 
                  its starting point to the projection of the given point onto the segment.
                - min_distance (float): The perpendicular distance in meters from the point to 
                  the closest line segment.
        """
        min_distance = float('inf')
        closest_segment_idx = -1
        distance_along_line = 0

        for i in range(len(line_points) - 1):
            line_start = line_points[i]
            line_end = line_points[i + 1]

            distance, along_line = CourseTrail._point_to_line_distance(point, line_start, line_end)

            if distance < min_distance:
                min_distance = distance
                closest_segment_idx = i
                distance_along_line = along_line

        return closest_segment_idx, distance_along_line, min_distance
