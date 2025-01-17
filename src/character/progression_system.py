from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional
from enum import Enum, auto
from src.combat_system.dimensional_combat import DimensionalLayer, DimensionalEffect
from src.character.ability_system import ResourceType, AbilitySystem
from src.world.difficulty_scaling import PlayerProgression

class StatType(Enum):
    # Core Stats
    STRENGTH = auto()
    AGILITY = auto()
    INTELLIGENCE = auto()
    VITALITY = auto()
    WILLPOWER = auto()
    
    # Combat Stats
    PHYSICAL_POWER = auto()
    MAGICAL_POWER = auto()
    DEFENSE = auto()
    SPEED = auto()
    CRITICAL_CHANCE = auto()
    
    # Dimensional Stats
    DIMENSIONAL_ATTUNEMENT = auto()
    STABILITY_CONTROL = auto()
    VOID_RESISTANCE = auto()
    REALITY_MANIPULATION = auto()
    DIMENSIONAL_AWARENESS = auto()

class ProgressionPath(Enum):
    WARRIOR = auto()  # Physical combat focus
    MAGE = auto()  # Magical combat focus
    DIMENSIONIST = auto()  # Dimensional manipulation focus
    VOIDWALKER = auto()  # Void/chaos focus
    PRIMORDIAL = auto()  # Reality manipulation focus

@dataclass
class StatAllocation:
    """Represents stat allocation for a level up"""
    base_stats: Dict[StatType, float]
    combat_stats: Dict[StatType, float]
    dimensional_stats: Dict[StatType, float]

@dataclass
class ProgressionNode:
    """Represents a node in the progression tree"""
    name: str
    description: str
    level_requirement: int
    stat_requirements: Dict[StatType, float]
    stat_bonuses: Dict[StatType, float]
    ability_unlock: Optional[str] = None
    dimension_unlock: Optional[DimensionalLayer] = None
    is_unlocked: bool = False
    
    def meets_requirements(
        self,
        character_level: int,
        character_stats: Dict[StatType, float]
    ) -> bool:
        """Check if requirements are met"""
        if character_level < self.level_requirement:
            return False
            
        for stat, req in self.stat_requirements.items():
            if stat not in character_stats or character_stats[stat] < req:
                return False
                
        return True

class ProgressionSystem:
    """Manages character progression and stats"""
    
    def __init__(self, ability_system: AbilitySystem):
        self.ability_system = ability_system
        self.level = 1
        self.experience = 0.0
        self.progression_path: Optional[ProgressionPath] = None
        
        # Initialize stats
        self.stats: Dict[StatType, float] = {
            stat: 10.0 for stat in StatType
        }
        
        # Initialize resources
        self.resources: Dict[ResourceType, float] = {
            ResourceType.HEALTH: 100.0,
            ResourceType.MANA: 100.0,
            ResourceType.STAMINA: 100.0,
            ResourceType.FOCUS: 100.0,
            ResourceType.DIMENSIONAL_ENERGY: 50.0
        }
        
        # Initialize resource max values
        self.max_resources: Dict[ResourceType, float] = self.resources.copy()
        
        # Initialize progression trees
        self.progression_trees: Dict[ProgressionPath, List[ProgressionNode]] = {}
        self._initialize_progression_trees()
        
        # Initialize available dimensions
        self.available_dimensions: Set[DimensionalLayer] = {DimensionalLayer.PHYSICAL}
        
    def _initialize_progression_trees(self) -> None:
        """Initialize progression trees for each path"""
        # Warrior progression
        self.progression_trees[ProgressionPath.WARRIOR] = [
            ProgressionNode(
                name="Warrior's Path",
                description="Begin your journey as a warrior",
                level_requirement=1,
                stat_requirements={},
                stat_bonuses={
                    StatType.STRENGTH: 5.0,
                    StatType.VITALITY: 3.0
                }
            ),
            # Add more nodes...
        ]
        
        # Mage progression
        self.progression_trees[ProgressionPath.MAGE] = [
            ProgressionNode(
                name="Arcane Initiate",
                description="Begin your journey as a mage",
                level_requirement=1,
                stat_requirements={},
                stat_bonuses={
                    StatType.INTELLIGENCE: 5.0,
                    StatType.WILLPOWER: 3.0
                }
            ),
            # Add more nodes...
        ]
        
        # Dimensionist progression
        self.progression_trees[ProgressionPath.DIMENSIONIST] = [
            ProgressionNode(
                name="Dimensional Awakening",
                description="Begin your journey as a dimensionist",
                level_requirement=1,
                stat_requirements={},
                stat_bonuses={
                    StatType.DIMENSIONAL_ATTUNEMENT: 5.0,
                    StatType.STABILITY_CONTROL: 3.0
                },
                dimension_unlock=DimensionalLayer.ETHEREAL
            ),
            # Add more nodes...
        ]
        
        # Add other progression trees...
        
    def get_experience_requirement(self) -> float:
        """Get experience required for next level"""
        return 100.0 * (1.5 ** (self.level - 1))
        
    def gain_experience(self, amount: float) -> bool:
        """Gain experience and handle level ups"""
        self.experience += amount
        level_up = False
        
        while self.experience >= self.get_experience_requirement():
            self.experience -= self.get_experience_requirement()
            self.level += 1
            level_up = True
            
        return level_up
        
    def choose_progression_path(self, path: ProgressionPath) -> bool:
        """Choose a progression path"""
        if self.progression_path is not None:
            return False
            
        self.progression_path = path
        starting_node = self.progression_trees[path][0]
        
        # Apply starting bonuses
        for stat, bonus in starting_node.stat_bonuses.items():
            self.stats[stat] += bonus
            
        starting_node.is_unlocked = True
        
        # Unlock starting dimension if applicable
        if starting_node.dimension_unlock:
            self.available_dimensions.add(starting_node.dimension_unlock)
            
        return True
        
    def unlock_progression_node(self, node: ProgressionNode) -> bool:
        """Attempt to unlock a progression node"""
        if node.is_unlocked:
            return False
            
        if not node.meets_requirements(self.level, self.stats):
            return False
            
        # Apply stat bonuses
        for stat, bonus in node.stat_bonuses.items():
            self.stats[stat] += bonus
            
        # Unlock ability if applicable
        if node.ability_unlock:
            self.ability_system.unlock_ability(
                node.ability_unlock,
                {str(k): v for k, v in self.stats.items()},
                self.available_dimensions
            )
            
        # Unlock dimension if applicable
        if node.dimension_unlock:
            self.available_dimensions.add(node.dimension_unlock)
            
        node.is_unlocked = True
        return True
        
    def allocate_stats(self, allocation: StatAllocation) -> None:
        """Allocate stats from level up"""
        for stat_type, value in allocation.base_stats.items():
            self.stats[stat_type] += value
            
        for stat_type, value in allocation.combat_stats.items():
            self.stats[stat_type] += value
            
        for stat_type, value in allocation.dimensional_stats.items():
            self.stats[stat_type] += value
            
        self._update_derived_stats()
        
    def _update_derived_stats(self) -> None:
        """Update stats derived from base stats"""
        # Update resource maximums
        self.max_resources[ResourceType.HEALTH] = (
            100.0 + self.stats[StatType.VITALITY] * 10.0
        )
        self.max_resources[ResourceType.MANA] = (
            100.0 + self.stats[StatType.INTELLIGENCE] * 8.0
        )
        self.max_resources[ResourceType.STAMINA] = (
            100.0 + self.stats[StatType.VITALITY] * 5.0
        )
        self.max_resources[ResourceType.FOCUS] = (
            100.0 + self.stats[StatType.WILLPOWER] * 8.0
        )
        self.max_resources[ResourceType.DIMENSIONAL_ENERGY] = (
            50.0 + self.stats[StatType.DIMENSIONAL_ATTUNEMENT] * 10.0
        )
        
        # Update combat stats
        self.stats[StatType.PHYSICAL_POWER] = (
            self.stats[StatType.STRENGTH] * 1.5
        )
        self.stats[StatType.MAGICAL_POWER] = (
            self.stats[StatType.INTELLIGENCE] * 1.5
        )
        self.stats[StatType.DEFENSE] = (
            self.stats[StatType.VITALITY] * 1.2
        )
        self.stats[StatType.SPEED] = (
            self.stats[StatType.AGILITY] * 1.0
        )
        self.stats[StatType.CRITICAL_CHANCE] = (
            self.stats[StatType.AGILITY] * 0.2
        )
        
    def get_player_progression(self) -> PlayerProgression:
        """Get current player progression metrics"""
        return PlayerProgression(
            dimensional_mastery={
                dim: self.stats[StatType.DIMENSIONAL_ATTUNEMENT] / 100.0
                for dim in self.available_dimensions
            },
            combat_proficiency=(
                (self.stats[StatType.PHYSICAL_POWER] +
                 self.stats[StatType.MAGICAL_POWER]) / 200.0
            ),
            stability_control=self.stats[StatType.STABILITY_CONTROL] / 100.0,
            artifact_collection=0.0,  # TODO: Implement artifact system
            quest_completion=0.0  # TODO: Implement quest system
        )
        
    def regenerate_resources(self, delta_time: float) -> None:
        """Regenerate resources over time"""
        regen_rates = {
            ResourceType.HEALTH: self.stats[StatType.VITALITY] * 0.1,
            ResourceType.MANA: self.stats[StatType.WILLPOWER] * 0.2,
            ResourceType.STAMINA: self.stats[StatType.VITALITY] * 0.3,
            ResourceType.FOCUS: self.stats[StatType.WILLPOWER] * 0.2,
            ResourceType.DIMENSIONAL_ENERGY: (
                self.stats[StatType.DIMENSIONAL_ATTUNEMENT] * 0.1
            )
        }
        
        for resource_type, rate in regen_rates.items():
            self.resources[resource_type] = min(
                self.max_resources[resource_type],
                self.resources[resource_type] + rate * delta_time
            ) 