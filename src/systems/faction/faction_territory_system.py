from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Tuple
import random
import math
import time
import logging
from collections import defaultdict

from weather_system import WeatherType, CelestialPattern
from economic_system import ResourceType, MarketEvent

class TerritoryType(Enum):
    MUNDANE = "mundane"
    MAGICAL = "magical"
    CELESTIAL = "celestial"
    VOID = "void"
    TEMPORAL = "temporal"
    PRIMAL = "primal"

class ResourceNodeType(Enum):
    MANA_WELL = "mana_well"
    CRYSTAL_VEIN = "crystal_vein"
    VOID_RIFT = "void_rift"
    CELESTIAL_ANCHOR = "celestial_anchor"
    TEMPORAL_NEXUS = "temporal_nexus"
    PRIMAL_SPRING = "primal_spring"
    ESSENCE_POOL = "essence_pool"

class InfluencePointType(Enum):
    FORTRESS = "fortress"
    RITUAL_CIRCLE = "ritual_circle"
    OBSERVATORY = "observatory"
    VOID_GATE = "void_gate"
    TIME_LOCK = "time_lock"
    PRIMAL_SHRINE = "primal_shrine"

@dataclass
class ResourceNode:
    """Represents a resource gathering point in territory"""
    node_type: ResourceNodeType
    base_yield: float
    current_yield: float
    quality: float  # 0.0 to 1.0
    depletion_rate: float
    regeneration_rate: float
    magical_resonance: float  # Affects yield during celestial events
    controlling_faction: Optional[str] = None
    last_harvest: float = time.time()

@dataclass
class InfluencePoint:
    """Represents a point of faction influence in territory"""
    point_type: InfluencePointType
    base_strength: float
    current_strength: float
    magical_attunement: float  # 0.0 to 1.0
    area_of_effect: float
    maintenance_cost: float
    special_abilities: List[str]
    controlling_faction: str
    linked_points: Set[str] = None
    last_update: float = time.time()

@dataclass
class Territory:
    """Represents a controllable territory"""
    name: str
    territory_type: TerritoryType
    controlling_faction: Optional[str]
    resource_nodes: Dict[str, ResourceNode]
    influence_points: Dict[str, InfluencePoint]
    strategic_value: float
    magical_stability: float
    celestial_alignment: float
    contested: bool = False
    last_control_change: float = time.time()

class FactionTerritorySystem:
    def __init__(self):
        self.territories: Dict[str, Territory] = {}
        self.faction_influence: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.territory_conflicts: Dict[str, List[str]] = defaultdict(list)
        self.logger = self._setup_logger()
        
        # Magical influence tracking
        self.magical_resonance = defaultdict(float)
        self.celestial_effects: List[Tuple[str, CelestialPattern, float]] = []
        self.ritual_networks: Dict[str, Set[str]] = defaultdict(set)

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("FactionTerritorySystem")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def create_territory(
        self,
        name: str,
        territory_type: TerritoryType,
        controlling_faction: Optional[str] = None,
        strategic_value: float = 1.0
    ) -> Territory:
        """Create a new territory"""
        territory = Territory(
            name=name,
            territory_type=territory_type,
            controlling_faction=controlling_faction,
            resource_nodes={},
            influence_points={},
            strategic_value=strategic_value,
            magical_stability=random.uniform(0.7, 1.0),
            celestial_alignment=random.uniform(0.0, 1.0)
        )
        
        self.territories[name] = territory
        if controlling_faction:
            self.faction_influence[controlling_faction][name] = 100.0
            
        self.logger.info(
            f"Created territory: {name}, Type: {territory_type.value}, "
            f"Controlling Faction: {controlling_faction}"
        )
        return territory

    def add_resource_node(
        self,
        territory_name: str,
        node_name: str,
        node_type: ResourceNodeType,
        base_yield: float,
        quality: float = 1.0
    ) -> Optional[ResourceNode]:
        """Add a resource node to territory"""
        if territory_name not in self.territories:
            return None
            
        node = ResourceNode(
            node_type=node_type,
            base_yield=base_yield,
            current_yield=base_yield,
            quality=quality,
            depletion_rate=0.1,
            regeneration_rate=0.05,
            magical_resonance=random.uniform(0.5, 1.5)
        )
        
        self.territories[territory_name].resource_nodes[node_name] = node
        return node

    def create_influence_point(
        self,
        territory_name: str,
        point_name: str,
        point_type: InfluencePointType,
        controlling_faction: str,
        base_strength: float = 100.0
    ) -> Optional[InfluencePoint]:
        """Create an influence point in territory"""
        if territory_name not in self.territories:
            return None
            
        point = InfluencePoint(
            point_type=point_type,
            base_strength=base_strength,
            current_strength=base_strength,
            magical_attunement=random.uniform(0.6, 1.0),
            area_of_effect=50.0,
            maintenance_cost=base_strength * 0.1,
            special_abilities=self._generate_point_abilities(point_type),
            controlling_faction=controlling_faction,
            linked_points=set()
        )
        
        self.territories[territory_name].influence_points[point_name] = point
        return point

    def _generate_point_abilities(self, point_type: InfluencePointType) -> List[str]:
        """Generate special abilities for influence point type"""
        abilities = {
            InfluencePointType.FORTRESS: [
                "reinforced_defense",
                "troop_training",
                "resource_storage"
            ],
            InfluencePointType.RITUAL_CIRCLE: [
                "mana_amplification",
                "ritual_enhancement",
                "magical_barrier"
            ],
            InfluencePointType.OBSERVATORY: [
                "celestial_scrying",
                "weather_prediction",
                "planar_sight"
            ],
            InfluencePointType.VOID_GATE: [
                "void_channeling",
                "reality_anchor",
                "dimensional_seal"
            ],
            InfluencePointType.TIME_LOCK: [
                "temporal_stasis",
                "time_dilation",
                "age_manipulation"
            ],
            InfluencePointType.PRIMAL_SHRINE: [
                "elemental_attunement",
                "nature_communion",
                "primal_surge"
            ]
        }
        return abilities.get(point_type, [])

    def update_territory_control(self, territory_name: str):
        """Update territory control based on influence"""
        if territory_name not in self.territories:
            return
            
        territory = self.territories[territory_name]
        faction_influences = self.faction_influence[territory_name]
        
        # Find faction with highest influence
        max_influence = 0
        controlling_faction = None
        
        for faction, influence in faction_influences.items():
            if influence > max_influence:
                max_influence = influence
                controlling_faction = faction
                
        # Check if control should change
        if controlling_faction != territory.controlling_faction:
            old_faction = territory.controlling_faction
            territory.controlling_faction = controlling_faction
            territory.last_control_change = time.time()
            territory.contested = False
            
            self.logger.info(
                f"Territory control changed: {territory_name} from {old_faction} "
                f"to {controlling_faction}"
            )
            
            # Transfer resource node control
            for node in territory.resource_nodes.values():
                node.controlling_faction = controlling_faction

    def process_celestial_effect(
        self,
        territory_name: str,
        pattern: CelestialPattern
    ):
        """Process celestial pattern effects on territory"""
        if territory_name not in self.territories:
            return
            
        territory = self.territories[territory_name]
        
        # Update magical stability
        stability_change = 0.1 * pattern.intensity
        if pattern.alignment == territory.territory_type:
            stability_change *= 1.5
            
        territory.magical_stability = max(
            0.1,
            min(1.0, territory.magical_stability + stability_change)
        )
        
        # Affect resource nodes
        for node in territory.resource_nodes.values():
            if pattern.alignment == territory.territory_type:
                node.current_yield = node.base_yield * (1 + node.magical_resonance * pattern.intensity)
            else:
                node.current_yield = node.base_yield * (1 - 0.2 * pattern.intensity)
                
        # Affect influence points
        for point in territory.influence_points.values():
            if pattern.alignment == territory.territory_type:
                point.current_strength = point.base_strength * (1 + point.magical_attunement * pattern.intensity)
            else:
                point.current_strength = point.base_strength * (1 - 0.1 * pattern.intensity)
                
        self.celestial_effects.append((territory_name, pattern, time.time()))

    def create_ritual_network(
        self,
        territory_name: str,
        point_names: List[str]
    ) -> bool:
        """Create a network of linked ritual points"""
        if territory_name not in self.territories:
            return False
            
        territory = self.territories[territory_name]
        points = territory.influence_points
        
        # Verify all points exist and are ritual circles
        for name in point_names:
            if (name not in points or
                points[name].point_type != InfluencePointType.RITUAL_CIRCLE):
                return False
                
        # Link points
        for name in point_names:
            points[name].linked_points.update(
                set(point_names) - {name}
            )
            
        self.ritual_networks[territory_name].update(point_names)
        return True

    def calculate_ritual_power(
        self,
        territory_name: str,
        ritual_points: List[str]
    ) -> float:
        """Calculate combined power of ritual network"""
        if territory_name not in self.territories:
            return 0.0
            
        territory = self.territories[territory_name]
        total_power = 0.0
        
        # Base power from points
        for point_name in ritual_points:
            if point_name in territory.influence_points:
                point = territory.influence_points[point_name]
                if point.point_type == InfluencePointType.RITUAL_CIRCLE:
                    point_power = point.current_strength * point.magical_attunement
                    total_power += point_power
                    
        # Network bonus
        if len(ritual_points) > 1:
            network_bonus = math.log(len(ritual_points)) * 0.2
            total_power *= (1 + network_bonus)
            
        # Territory modifiers
        total_power *= territory.magical_stability
        
        return total_power

    def get_territory_status(self, territory_name: str) -> Dict[str, any]:
        """Get current status of territory"""
        if territory_name not in self.territories:
            return {"error": "Territory not found"}
            
        territory = self.territories[territory_name]
        
        return {
            "name": territory.name,
            "type": territory.territory_type.value,
            "controlling_faction": territory.controlling_faction,
            "strategic_value": territory.strategic_value,
            "magical_stability": territory.magical_stability,
            "celestial_alignment": territory.celestial_alignment,
            "contested": territory.contested,
            "resource_nodes": [
                {
                    "name": name,
                    "type": node.node_type.value,
                    "current_yield": node.current_yield,
                    "quality": node.quality,
                    "controlling_faction": node.controlling_faction
                }
                for name, node in territory.resource_nodes.items()
            ],
            "influence_points": [
                {
                    "name": name,
                    "type": point.point_type.value,
                    "current_strength": point.current_strength,
                    "controlling_faction": point.controlling_faction,
                    "special_abilities": point.special_abilities
                }
                for name, point in territory.influence_points.items()
            ],
            "active_effects": [
                {
                    "type": pattern.pattern_type,
                    "intensity": pattern.intensity,
                    "duration": time.time() - effect_time
                }
                for t_name, pattern, effect_time in self.celestial_effects
                if t_name == territory_name
            ]
        } 