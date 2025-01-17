from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Callable
from enum import Enum, auto
import math
from src.combat_system.dimensional_combat import DimensionalLayer, DimensionalEffect
from src.world.difficulty_scaling import PlayerProgression

class AbilityType(Enum):
    PHYSICAL = auto()  # Physical combat abilities
    ETHEREAL = auto()  # Spirit/energy based abilities
    CELESTIAL = auto()  # Star/cosmic power abilities
    VOID = auto()  # Chaos/entropy abilities
    PRIMORDIAL = auto()  # Reality-warping abilities
    DIMENSIONAL = auto()  # Cross-dimensional abilities
    UTILITY = auto()  # Non-combat utility abilities

class AbilityTrigger(Enum):
    ON_CAST = auto()  # Activated manually
    ON_HIT = auto()  # Triggers when hitting
    ON_DODGE = auto()  # Triggers when dodging
    ON_DAMAGE = auto()  # Triggers when taking damage
    ON_KILL = auto()  # Triggers when defeating an enemy
    ON_DIMENSION_SHIFT = auto()  # Triggers when shifting dimensions
    PASSIVE = auto()  # Always active

class ResourceType(Enum):
    MANA = auto()
    STAMINA = auto()
    FOCUS = auto()
    DIMENSIONAL_ENERGY = auto()
    HEALTH = auto()

@dataclass
class AbilityCost:
    """Represents the cost of using an ability"""
    resource_type: ResourceType
    base_amount: float
    scaling_factor: float = 1.0
    
    def calculate_cost(self, power_level: float) -> float:
        """Calculate actual cost based on power level"""
        return self.base_amount * (1.0 + (power_level - 1.0) * self.scaling_factor)

@dataclass
class AbilityEffect:
    """Represents an effect caused by an ability"""
    effect_type: DimensionalEffect
    power: float
    duration: float
    radius: float = 0.0
    is_buff: bool = False

@dataclass
class Ability:
    """Represents a character ability"""
    name: str
    description: str
    ability_type: AbilityType
    trigger: AbilityTrigger
    base_power: float
    base_cooldown: float
    costs: List[AbilityCost]
    effects: List[AbilityEffect]
    requirements: Dict[str, float]  # Stat requirements
    dimension_requirements: Set[DimensionalLayer]
    scaling_stats: Dict[str, float]  # Stat scaling factors
    max_rank: int = 5
    current_rank: int = 1
    is_unlocked: bool = False
    
    def calculate_power(self, character_stats: Dict[str, float]) -> float:
        """Calculate ability power based on character stats"""
        power = self.base_power * (1.0 + 0.2 * (self.current_rank - 1))
        for stat, scale in self.scaling_stats.items():
            if stat in character_stats:
                power *= (1.0 + character_stats[stat] * scale)
        return power
    
    def meets_requirements(
        self,
        character_stats: Dict[str, float],
        available_dimensions: Set[DimensionalLayer]
    ) -> bool:
        """Check if character meets ability requirements"""
        # Check stat requirements
        for stat, req in self.requirements.items():
            if stat not in character_stats or character_stats[stat] < req:
                return False
        
        # Check dimension requirements
        if not self.dimension_requirements.issubset(available_dimensions):
            return False
            
        return True
    
    def can_rank_up(self, character_level: int) -> bool:
        """Check if ability can be ranked up"""
        return (
            self.current_rank < self.max_rank and
            character_level >= self.current_rank * 5
        )

class AbilitySystem:
    """Manages character abilities and their progression"""
    
    def __init__(self):
        self.abilities: Dict[str, Ability] = {}
        self.active_abilities: Set[str] = set()
        self.passive_abilities: Set[str] = set()
        self.ability_cooldowns: Dict[str, float] = {}
        
    def register_ability(self, ability: Ability) -> None:
        """Register a new ability"""
        self.abilities[ability.name] = ability
        if ability.trigger == AbilityTrigger.PASSIVE:
            self.passive_abilities.add(ability.name)
        else:
            self.active_abilities.add(ability.name)
    
    def unlock_ability(
        self,
        ability_name: str,
        character_stats: Dict[str, float],
        available_dimensions: Set[DimensionalLayer]
    ) -> bool:
        """Attempt to unlock an ability"""
        if ability_name not in self.abilities:
            return False
            
        ability = self.abilities[ability_name]
        if ability.meets_requirements(character_stats, available_dimensions):
            ability.is_unlocked = True
            return True
        return False
    
    def rank_up_ability(
        self,
        ability_name: str,
        character_level: int
    ) -> bool:
        """Attempt to rank up an ability"""
        if ability_name not in self.abilities:
            return False
            
        ability = self.abilities[ability_name]
        if ability.can_rank_up(character_level):
            ability.current_rank += 1
            return True
        return False
    
    def get_available_abilities(
        self,
        character_stats: Dict[str, float],
        available_dimensions: Set[DimensionalLayer]
    ) -> List[Ability]:
        """Get list of abilities that can be unlocked"""
        return [
            ability for ability in self.abilities.values()
            if not ability.is_unlocked and
            ability.meets_requirements(character_stats, available_dimensions)
        ]
    
    def get_active_effects(
        self,
        character_stats: Dict[str, float]
    ) -> List[AbilityEffect]:
        """Get all active effects from passive abilities"""
        effects = []
        for ability_name in self.passive_abilities:
            ability = self.abilities[ability_name]
            if ability.is_unlocked:
                power = ability.calculate_power(character_stats)
                for effect in ability.effects:
                    scaled_effect = AbilityEffect(
                        effect_type=effect.effect_type,
                        power=effect.power * power,
                        duration=effect.duration,
                        radius=effect.radius,
                        is_buff=effect.is_buff
                    )
                    effects.append(scaled_effect)
        return effects
    
    def update_cooldowns(self, delta_time: float) -> None:
        """Update ability cooldowns"""
        for ability_name in list(self.ability_cooldowns.keys()):
            self.ability_cooldowns[ability_name] -= delta_time
            if self.ability_cooldowns[ability_name] <= 0:
                del self.ability_cooldowns[ability_name]
    
    def can_use_ability(
        self,
        ability_name: str,
        character_resources: Dict[ResourceType, float]
    ) -> bool:
        """Check if an ability can be used"""
        if ability_name not in self.abilities:
            return False
            
        ability = self.abilities[ability_name]
        if not ability.is_unlocked:
            return False
            
        if ability_name in self.ability_cooldowns:
            return False
            
        # Check resource costs
        for cost in ability.costs:
            if (
                cost.resource_type not in character_resources or
                character_resources[cost.resource_type] < cost.base_amount
            ):
                return False
                
        return True
    
    def use_ability(
        self,
        ability_name: str,
        character_stats: Dict[str, float],
        character_resources: Dict[ResourceType, float]
    ) -> Optional[List[AbilityEffect]]:
        """Use an ability and return its effects"""
        if not self.can_use_ability(ability_name, character_resources):
            return None
            
        ability = self.abilities[ability_name]
        
        # Apply costs
        for cost in ability.costs:
            character_resources[cost.resource_type] -= cost.calculate_cost(
                ability.calculate_power(character_stats)
            )
            
        # Set cooldown
        self.ability_cooldowns[ability_name] = ability.base_cooldown * (
            1.0 - 0.1 * (ability.current_rank - 1)
        )
        
        # Calculate effects
        power = ability.calculate_power(character_stats)
        effects = []
        for effect in ability.effects:
            scaled_effect = AbilityEffect(
                effect_type=effect.effect_type,
                power=effect.power * power,
                duration=effect.duration,
                radius=effect.radius,
                is_buff=effect.is_buff
            )
            effects.append(scaled_effect)
            
        return effects 