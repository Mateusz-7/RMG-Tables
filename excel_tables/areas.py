import re
from typing import List, Optional

from shapely import Point, Polygon

from GoogleMyMaps.models import Map, Place


class Areas:
    """
    A class for managing and analyzing geographical areas from Google Maps.
    """
    
    def __init__(self, google_map: Map):
        """
        Initialize the Areas object with areas and polygons from a Google Map.
        
        Parameters:
            google_map (Map): A Google Map object containing layers and places.
        """
        self.areas = Areas._get_areas_from_map(google_map)
        self.polygons = Areas._get_polygons_from_areas(self.areas)

    @staticmethod
    def _get_areas_from_map(google_map: Map) -> List[Place]:
        """
        Extract area places from a Google Map by finding layers with 'STREFY' in their name.
        
        Parameters:
            google_map (Map): A Google Map object to extract areas from.
            
        Returns:
            List[Place]: A list of Place objects representing areas, or an empty list if no matching layer is found.
        """
        for layer in google_map.layers:
            if "STREFY" in layer.name.upper():
                return layer.places
        return []

    @staticmethod
    def _get_polygons_from_areas(areas: List[Place]) -> List[Polygon]:
        """
        Convert a list of Place objects to Shapely Polygon objects.
        
        Parameters:
            areas (List[Place]): A list of Place objects with coordinate data.
            
        Returns:
            List[Polygon]: A list of Shapely Polygon objects created from the coordinates of each Place.
        """
        return [Polygon(area.coords) for area in areas]
    
    @staticmethod
    def _get_point_from_obstacle(obstacle: Place) -> Optional[Point]:
        """
        Convert an obstacle Place to a Shapely Point object.
        
        Parameters:
            obstacle (Place): A Place object representing an obstacle.
            
        Returns:
            Optional[Point]: A Shapely Point object created from the first two coordinates of the obstacle,
                            or None if the obstacle has insufficient coordinates.
        """
        if obstacle.coords is None or len(obstacle.coords) < 2:
            return None
        else:
            return Point(obstacle.coords[0], obstacle.coords[1])
    
    @staticmethod
    def _get_area_number(area: Place) -> Optional[int]:
        """
        Extract the area number from an area's name using regex.
        
        Parameters:
            area (Place): A Place object representing an area.
            
        Returns:
            Optional[int]: The extracted area number as an integer, or None if no number is found.
        """
        match = re.search(r'STREFA\s+(\d+)', area.name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None
    
    def _get_obstacle_area(self, obstacle: Place) -> Optional[Place]:
        """
        Find the area that contains a given obstacle.
        
        Parameters:
            obstacle (Place): A Place object representing an obstacle.
            
        Returns:
            Optional[Place]: The area Place object that contains the obstacle, or None if no containing area is found.
        """
        for area_index, polygon in enumerate(self.polygons):
            if polygon.contains(Areas._get_point_from_obstacle(obstacle)):
                return self.areas[area_index]
        return None
    
    def get_obstacle_area_number(self, obstacle: Place) -> Optional[int]:
        """
        Get the area number for the area containing a given obstacle.
        
        Parameters:
            obstacle (Place): A Place object representing an obstacle.
            
        Returns:
            Optional[int]: The area number as an integer for the area containing the obstacle,
                          or None if the obstacle is not in any area or the area has no number.
        """
        obstacle_area = self._get_obstacle_area(obstacle)
        return self._get_area_number(obstacle_area) if obstacle_area else None