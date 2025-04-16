import re
from typing import List, Optional

from shapely import Point, Polygon

from GoogleMyMaps.models import Map, Place


class Areas:
    def __init__(self, google_map: Map):
        self.areas = Areas._get_areas_from_map(google_map)
        self.polygons = Areas._get_polygons_from_areas(self.areas)

    @staticmethod
    def _get_areas_from_map(google_map: Map) -> List[Place]:
        for layer in google_map.layers:
            if "STREFY" in layer.name.upper():
                return layer.places
        return []

    @staticmethod
    def _get_polygons_from_areas(areas: List[Place]) -> List[Polygon]:
        return [Polygon(area.coords) for area in areas]
    
    @staticmethod
    def _get_point_from_obstacle(obstacle: Place) -> Optional[Point]:
        if obstacle.coords is None or len(obstacle.coords) < 2:
            return None
        else:
            return Point(obstacle.coords[0], obstacle.coords[1])
    
    @staticmethod
    def _get_area_number(area: Place) -> Optional[int]:
        match = re.search(r'STREFA\s+(\d+)', area.name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None
    
    def _get_obstacle_area(self, obstacle: Place) -> Optional[Place]:
        for area_index, polygon in enumerate(self.polygons):
            if polygon.contains(Areas._get_point_from_obstacle(obstacle)):
                return self.areas[area_index]
        return None
    
    def get_obstacle_area_number(self, obstacle: Place) -> Optional[int]:
        obstacle_area = self._get_obstacle_area(obstacle)
        return self._get_area_number(obstacle_area) if obstacle_area else None
