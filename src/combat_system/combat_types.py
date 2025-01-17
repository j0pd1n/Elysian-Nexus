from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
import math

class ActionType(Enum):
    """Combat action types"""
    BASIC_ATTACK = auto()
    CELESTIAL_ALIGNMENT = auto()
    CELESTIAL_BURST = auto()
    CREATE_VOID_RIFT = auto()
    VOID_STRIKE = auto()
    PRIMAL_FORCE = auto()
    PRIMAL_SURGE = auto()
    RITUAL_DEFENSE = auto()
    DIMENSIONAL_SHIFT = auto()

class DefenseFormation(Enum):
    """Defensive formation types"""
    CIRCLE = auto()
    TRIANGLE = auto()
    SQUARE = auto()
    DEFAULT = auto()

class EffectType(Enum):
    """Combat effect types"""
    DIMENSIONAL_DISTORTION = auto()
    FORMATION_BONUS = auto()
    CELESTIAL_CHARGE = auto()
    VOID_ESSENCE = auto()
    PRIMAL_ENERGY = auto()
    RITUAL_PROTECTION = auto()

@dataclass
class Position:
    """3D position in combat space"""
    x: float
    y: float
    z: float
    dimensional_layer: int = 0

    def distance_to(self, other: 'Position') -> float:
        """Calculate Euclidean distance to another position"""
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

@dataclass
class CombatAction:
    """Represents a combat action"""
    action_type: ActionType
    target: Optional[Position]
    power_level: float
    additional_effects: Dict[str, any] = None

@dataclass
class DimensionalRift:
    """Represents a dimensional rift in combat"""
    center: Position
    effect_radius: float
    pulse_duration: int
    distortion_level: float
    affected_layers: List[int]

@dataclass
class CombatEffect:
    """Represents an active combat effect"""
    effect_type: EffectType
    strength: float
    duration: Optional[int]
    source: Optional[str] = None 