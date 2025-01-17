from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from unified_map_system import UnifiedWorldMap, Location, TerrainType, Path
import heapq

@dataclass
class RouteSegment:
    """Represents a segment of a route between two points"""
    start: Location
    end: Location
    terrain: TerrainType
    distance: float
    difficulty: float
    estimated_time: float  # in minutes
    
    def __post_init__(self):
        # Calculate difficulty based on terrain
        terrain_difficulty = {
            TerrainType.PLAINS: 1.0,
            TerrainType.FOREST: 1.2,
            TerrainType.MOUNTAIN: 2.0,
            TerrainType.DESERT: 1.5,
            TerrainType.WATER: 3.0,
            TerrainType.CITY: 1.0,
            TerrainType.RUINS: 1.3,
            TerrainType.CAVE: 1.4
        }
        self.difficulty = terrain_difficulty.get(self.terrain, 1.0)
        
        # Calculate estimated time (base speed: 3 units per minute)
        base_speed = 3.0  # units per minute
        self.estimated_time = (self.distance * self.difficulty) / base_speed

@dataclass
class Route:
    """Represents a complete route with multiple segments"""
    segments: List[RouteSegment]
    total_distance: float
    total_time: float
    difficulty_rating: float
    required_level: int
    warnings: List[str]
    
    @property
    def start_location(self) -> Location:
        return self.segments[0].start
    
    @property
    def end_location(self) -> Location:
        return self.segments[-1].end
    
    def get_waypoints(self) -> List[Location]:
        """Get list of all locations along the route"""
        waypoints = [self.start_location]
        for segment in self.segments:
            waypoints.append(segment.end)
        return waypoints

class RouteCalculator:
    def __init__(self, world_map: UnifiedWorldMap):
        self.world_map = world_map
        
    def find_route(
        self,
        start_location: str,
        end_location: str,
        player_level: int = 1,
        avoid_terrain: List[TerrainType] = None,
        prefer_safe: bool = False
    ) -> Optional[Route]:
        """Find the optimal route between two locations"""
        start = self.world_map.get_location_by_name(start_location)
        end = self.world_map.get_location_by_name(end_location)
        
        if not start or not end:
            return None
            
        # Initialize pathfinding
        distances = {start: 0}
        previous = {start: None}
        segments = {start: None}
        queue = [(0, start)]
        avoid_terrain = avoid_terrain or []
        
        while queue:
            current_distance, current = heapq.heappop(queue)
            
            if current == end:
                break
                
            # Get all possible next locations
            neighbors = self._get_neighbors(current)
            
            for next_loc, terrain in neighbors:
                # Skip if terrain should be avoided
                if terrain in avoid_terrain:
                    continue
                    
                # Calculate segment
                segment = RouteSegment(
                    start=current,
                    end=next_loc,
                    terrain=terrain,
                    distance=self._calculate_distance(current, next_loc),
                    difficulty=1.0,  # Will be calculated in post_init
                    estimated_time=0.0  # Will be calculated in post_init
                )
                
                # Calculate new distance including difficulty
                new_distance = (
                    distances[current] + 
                    segment.distance * segment.difficulty
                )
                
                # Add danger level penalty if preferring safe routes
                if prefer_safe:
                    new_distance += next_loc.danger_level * 10
                
                if (next_loc not in distances or 
                    new_distance < distances[next_loc]):
                    distances[next_loc] = new_distance
                    previous[next_loc] = current
                    segments[next_loc] = segment
                    heapq.heappush(queue, (new_distance, next_loc))
        
        # Build route from path
        if end not in previous:
            return None
            
        route_segments = []
        current = end
        warnings = []
        max_danger = 0
        
        while current != start:
            segment = segments[current]
            route_segments.append(segment)
            max_danger = max(max_danger, current.danger_level)
            
            # Add warnings for dangerous areas
            if current.danger_level > player_level + 2:
                warnings.append(
                    f"Warning: {current.name} (Danger Level {current.danger_level}) "
                    f"may be too dangerous for your level ({player_level})"
                )
            
            current = previous[current]
            
        route_segments.reverse()
        
        # Calculate route statistics
        total_distance = sum(seg.distance for seg in route_segments)
        total_time = sum(seg.estimated_time for seg in route_segments)
        avg_difficulty = sum(seg.difficulty for seg in route_segments) / len(route_segments)
        required_level = max(1, max_danger - 2)
        
        return Route(
            segments=route_segments,
            total_distance=total_distance,
            total_time=total_time,
            difficulty_rating=avg_difficulty,
            required_level=required_level,
            warnings=warnings
        )
    
    def _get_neighbors(self, location: Location) -> List[Tuple[Location, TerrainType]]:
        """Get all accessible locations from current location"""
        neighbors = []
        
        # Add directly connected paths
        for path in self.world_map.paths:
            if path.discovered:
                if path.start == location:
                    neighbors.append((path.end, path.terrain_type))
                elif path.end == location:
                    neighbors.append((path.start, path.terrain_type))
        
        # Add nearby discovered locations
        nearby = self.world_map.get_nearby_locations(radius=1)
        for loc in nearby:
            if loc != location and loc.discovered:
                terrain = self.world_map.terrain_map.get(
                    loc.position,
                    TerrainType.PLAINS
                )
                neighbors.append((loc, terrain))
        
        return neighbors
    
    def _calculate_distance(self, start: Location, end: Location) -> float:
        """Calculate distance between two locations"""
        x1, y1 = start.position
        x2, y2 = end.position
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
    def get_route_description(self, route: Route) -> str:
        """Generate a human-readable description of the route"""
        description = [
            f"Route from {route.start_location.name} to {route.end_location.name}",
            f"Total Distance: {route.total_distance:.1f} units",
            f"Estimated Time: {route.total_time:.1f} minutes",
            f"Difficulty Rating: {route.difficulty_rating:.1f}",
            f"Recommended Level: {route.required_level}",
            "\nWaypoints:"
        ]
        
        for i, segment in enumerate(route.segments, 1):
            description.append(
                f"{i}. {segment.start.name} → {segment.end.name} "
                f"({segment.terrain.value}, {segment.estimated_time:.1f} min)"
            )
        
        if route.warnings:
            description.extend(["\nWarnings:", *route.warnings])
            
        return "\n".join(description)

def main():
    """Example usage"""
    # Create a world map
    world_map = UnifiedWorldMap()
    
    # Create route calculator
    calculator = RouteCalculator(world_map)
    
    # Find route between two locations
    route = calculator.find_route(
        "Crystal Spire Plaza",
        "Academy Gates",
        player_level=1,
        prefer_safe=True
    )
    
    if route:
        print(calculator.get_route_description(route))
    else:
        print("No route found!")

if __name__ == "__main__":
    main() 