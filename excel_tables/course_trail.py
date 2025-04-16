import logging
from math import radians, sin, cos, sqrt, atan2
from typing import Optional

import numpy as np

from GoogleMyMaps import Layer, Place

log = logging.getLogger(__name__)



class CourseTrail:
    def __init__(self, course: Layer):
        self.trail = self._get_trail(course)

    @staticmethod
    def _get_trail(course) -> Optional[list]:
        for place in course.places:
            if place.place_type == "Line" and place.name.strip() in course.name.strip():
                return place.coords

    def get_obstacle_distance(self, obstacle: Place) -> Optional[float]:
        """

        :param obstacle: Place
        :return: Distance in meters from start to given point
        """

        if obstacle.coords is None:
            log.warning("Obstacle cords is none")
            return None

        if self.trail is None:
            log.warning("Trail is none")
            return None

        segment_idx, distance_along, perpendicular_distance = CourseTrail._find_closest_line_segment(obstacle.coords, self.trail)

        return self._calculate_total_distance(segment_idx, distance_along)


    def _calculate_total_distance(self, segment_idx, distance_along):
        """
        Calculate distance between starting point, and specified point.
        Returns distance in meters
        """
        total_distance = 0
        for i in range(segment_idx):
            total_distance += CourseTrail._haversine_distance(
                self.trail[i][0], self.trail[i][1],
                self.trail[i + 1][0], self.trail[i + 1][1]
            )

        total_distance += distance_along

        return total_distance

    @staticmethod
    def _haversine_distance(lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        Returns distance in meters
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
        Calculate the minimum distance from a point to a line segment defined by two points.
        All points are in (lat, lon) format.
        Returns distance in meters
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
            # Closest point is the start point
            return d_point_to_start, 0

        if d_point_to_end == 0 or d_start_to_end == 0:
            return d_point_to_end, d_start_to_end
        cos_angle = (d_point_to_end ** 2 + d_start_to_end ** 2 - d_point_to_start ** 2) / (
                    2 * d_point_to_end * d_start_to_end)

        # Handle floating point errors
        if cos_angle > 1:
            cos_angle = 1
        elif cos_angle < -1:
            cos_angle = -1

        angle = np.arccos(cos_angle)

        if angle > np.pi / 2:
            # Closest point is the end point
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
        Returns the index of the first point of the segment and the distance along that segment.
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
