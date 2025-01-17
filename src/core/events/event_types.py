from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, Optional, Set, List
from ...combat_system.dimensional_combat import DimensionalLayer, DimensionalEffect

class EventPriority(Enum):
    """Priority levels for event handling."""
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()
    CRITICAL = auto()

class EventCategory(Enum):
    """Categories of game events."""
    COMBAT = auto()
    QUEST = auto()
    INVENTORY = auto()
    CHARACTER = auto()
    WORLD = auto()
    FACTION = auto()
    SYSTEM = auto()
    ENVIRONMENTAL = auto()

@dataclass
class GameEvent:
    """Base class for all game events."""
    event_id: str
    timestamp: datetime
    category: EventCategory
    priority: EventPriority
    source: str
    data: Dict[str, Any]
    handled: bool = False

@dataclass
class CombatEvent(GameEvent):
    """Events related to combat interactions."""
    damage_dealt: float = 0.0
    damage_received: float = 0.0
    combat_type: str = "normal"
    enemy_level: int = 1
    critical_hit: bool = False
    source_dimension: Optional[DimensionalLayer] = None
    target_dimension: Optional[DimensionalLayer] = None
    dimensional_effects: Set[DimensionalEffect] = None
    dimensional_stability_change: float = 0.0
    
    def __post_init__(self):
        if self.dimensional_effects is None:
            self.dimensional_effects = set()

@dataclass
class QuestEvent(GameEvent):
    """Events related to quest progression."""
    quest_id: str
    quest_status: str
    rewards: Dict[str, Any]
    requirements_met: bool = False

@dataclass
class InventoryEvent(GameEvent):
    """Events related to inventory changes."""
    item_id: str
    quantity: int
    action: str  # "add", "remove", "use", "equip", "unequip"
    item_rarity: str = "common"

@dataclass
class CharacterEvent(GameEvent):
    """Events related to character progression."""
    level: int
    experience_gained: int
    skills_unlocked: list[str]
    attributes_changed: Dict[str, int]

@dataclass
class WorldEvent(GameEvent):
    """Events related to world state changes."""
    location: str
    event_type: str  # "discovery", "change", "interaction"
    affected_npcs: list[str]
    permanent_change: bool = False

@dataclass
class FactionEvent(GameEvent):
    """Events related to faction interactions."""
    faction_id: str
    reputation_change: int
    interaction_type: str
    territory_affected: Optional[str] = None

@dataclass
class SystemEvent(GameEvent):
    """Events related to system operations."""
    operation: str
    success: bool
    error_message: Optional[str] = None
    performance_metrics: Optional[Dict[str, float]] = None

@dataclass
class EnvironmentalEvent(GameEvent):
    """Events related to environmental changes."""
    weather_type: str
    time_of_day: int
    hazard_level: float
    affects_gameplay: bool = True 

@dataclass
class DimensionalEvent(GameEvent):
    """Events related to dimensional changes and effects."""
    source_dimension: DimensionalLayer
    target_dimension: Optional[DimensionalLayer] = None
    effect_type: Optional[DimensionalEffect] = None
    stability_change: float = 0.0
    distortion_level: float = 0.0
    affected_positions: List[Position] = None
    
    def __post_init__(self):
        if self.affected_positions is None:
            self.affected_positions = [] 