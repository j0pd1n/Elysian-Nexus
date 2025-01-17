from enum import Enum
from typing import Dict, Set, List, Tuple, Optional, Protocol
from dataclasses import dataclass

class TerrainType(Enum):
    PLAINS = "Plains"
    FOREST = "Forest"
    MOUNTAIN = "Mountain"
    DESERT = "Desert"
    WATER = "Water"
    CITY = "City"
    RUINS = "Ruins"
    CAVE = "Cave"

class LocationType(Enum):
    MAJOR_CITY = "Major City"
    DUNGEON = "Dungeon"
    QUEST_LOCATION = "Quest Location"
    POINT_OF_INTEREST = "Point of Interest"
    FAST_TRAVEL = "Fast Travel Point"
    RESOURCE_NODE = "Resource Node"
    HIDDEN = "Hidden Location"
    SAFE_HAVEN = "Safe Haven"

@dataclass
class Location:
    """Represents a named location in the game world"""
    name: str
    position: tuple[int, int]
    location_type: LocationType
    terrain_type: TerrainType
    description: str
    icon: str
    discovered: bool = False
    fast_travel_unlocked: bool = False
    quests: List[str] = None
    resources: List[str] = None
    danger_level: int = 0
    weather_effects: List[str] = None

    def __post_init__(self):
        self.quests = self.quests or []
        self.resources = self.resources or []
        self.weather_effects = self.weather_effects or []

class WorldMapProtocol(Protocol):
    """Protocol defining the interface for world maps"""
    locations: Dict[str, Location]
    terrain_map: Dict[Tuple[int, int], TerrainType]
    discovered_locations: Set[Tuple[int, int]]
    current_position: Tuple[int, int]
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    
    def _get_location_at_position(self, position: Tuple[int, int]) -> Optional[Location]:
        """Get location at a specific position"""
        ...
        
    def get_current_location_info(self) -> Dict[str, str]:
        """Get information about the current location"""
        ... 