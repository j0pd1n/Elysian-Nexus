from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Any
from enum import Enum, auto
from datetime import datetime, timedelta
import json
import math

from .ability_system import ResourceType, AbilitySystem
from ..combat_system.dimensional_combat import DimensionalLayer, DimensionalEffect
from ..world.difficulty_scaling import PlayerProgression

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

class MasteryType(Enum):
    """Types of masteries a character can develop"""
    COMBAT = auto()         # Combat proficiency
    DIMENSIONAL = auto()    # Dimensional manipulation
    CRAFTING = auto()       # Item creation and enhancement
    EXPLORATION = auto()    # World discovery and navigation
    SOCIAL = auto()         # NPC interactions and influence
    STEALTH = auto()        # Stealth and subterfuge
    SURVIVAL = auto()       # Environmental adaptation

class Specialization(Enum):
    """Advanced specializations within progression paths"""
    # Warrior specializations
    BLADE_MASTER = auto()      # Sword combat mastery
    GUARDIAN = auto()          # Defensive specialist
    BERSERKER = auto()         # Rage-powered warrior
    
    # Mage specializations
    ELEMENTALIST = auto()      # Elemental magic mastery
    CHRONOMANCER = auto()      # Time manipulation
    RUNEWEAVER = auto()        # Rune-based spellcasting
    
    # Dimensionist specializations
    VOID_WALKER = auto()       # Void dimension mastery
    REALITY_SHAPER = auto()    # Reality manipulation
    PLANAR_WEAVER = auto()     # Multi-dimensional combat
    
    # Hybrid specializations
    SPELLBLADE = auto()        # Magic-enhanced combat
    DIMENSIONAL_KNIGHT = auto() # Physical-dimensional hybrid
    VOID_MAGE = auto()         # Void-magic specialist

@dataclass
class MasteryProgress:
    """Tracks progress in a mastery"""
    mastery_type: MasteryType
    level: int = 1
    experience: float = 0.0
    milestones_achieved: Set[str] = field(default_factory=set)
    
    def get_next_level_requirement(self) -> float:
        """Calculate experience needed for next level"""
        return 150.0 * (1.4 ** (self.level - 1))

@dataclass
class SpecializationNode:
    """Represents a node in a specialization tree"""
    name: str
    description: str
    specialization: Specialization
    tier: int
    requirements: Dict[str, Any]  # Flexible requirements
    bonuses: Dict[str, Any]       # Flexible bonuses
    is_unlocked: bool = False
    is_active: bool = False
    
    def meets_requirements(self, character_state: Dict[str, Any]) -> bool:
        """Check if node requirements are met"""
        for req_type, req_value in self.requirements.items():
            if req_type.startswith('stat_'):
                stat_name = req_type[5:]
                if character_state.get('stats', {}).get(stat_name, 0) < req_value:
                    return False
            elif req_type == 'level':
                if character_state.get('level', 1) < req_value:
                    return False
            elif req_type == 'mastery':
                mastery_name, mastery_level = req_value
                if character_state.get('masteries', {}).get(mastery_name, 0) < mastery_level:
                    return False
            elif req_type == 'ability':
                ability_name, ability_rank = req_value
                if character_state.get('abilities', {}).get(ability_name, 0) < ability_rank:
                    return False
        return True

class ProgressionSystem:
    """Manages character progression and stats"""
    
    def __init__(self, ability_system: AbilitySystem):
        self.ability_system = ability_system
        self.level = 1
        self.experience = 0.0
        self.progression_path: Optional[ProgressionPath] = None
        
        # Enhanced stats system
        self.base_stats: Dict[StatType, float] = {
            stat: 10.0 for stat in StatType
        }
        self.stat_modifiers: Dict[StatType, Dict[str, float]] = {
            stat: {} for stat in StatType
        }
        
        # Mastery system
        self.masteries: Dict[MasteryType, MasteryProgress] = {
            mastery: MasteryProgress(mastery) for mastery in MasteryType
        }
        
        # Specialization system
        self.specializations: Dict[Specialization, List[SpecializationNode]] = {}
        self.active_specializations: Set[Specialization] = set()
        self.specialization_points = 0
        
        # Dynamic scaling system
        self.combat_multipliers: Dict[str, float] = {
            'damage': 1.0,
            'defense': 1.0,
            'healing': 1.0,
            'resource_regen': 1.0
        }
        
        # Achievement and milestone system
        self.achievements: Set[str] = set()
        self.milestones: Dict[str, datetime] = {}
        
        self._initialize_specialization_trees()
        
    def _initialize_specialization_trees(self) -> None:
        """Initialize all specialization trees"""
        # Warrior specializations
        self._init_blade_master_tree()
        self._init_guardian_tree()
        self._init_berserker_tree()
        
        # Mage specializations
        self._init_elementalist_tree()
        self._init_chronomancer_tree()
        self._init_runeweaver_tree()
        
        # Dimensionist specializations
        self._init_void_walker_tree()
        self._init_reality_shaper_tree()
        self._init_planar_weaver_tree()
        
        # Hybrid specializations
        self._init_spellblade_tree()
        self._init_dimensional_knight_tree()
        self._init_void_mage_tree()

    def _init_blade_master_tree(self) -> None:
        """Initialize Blade Master specialization tree"""
        nodes = [
            SpecializationNode(
                name="Way of the Blade",
                description="Begin your journey as a Blade Master",
                specialization=Specialization.BLADE_MASTER,
                tier=1,
                requirements={'level': 10, 'stat_strength': 15},
                bonuses={'critical_chance': 0.05, 'physical_power': 10}
            ),
            SpecializationNode(
                name="Perfect Form",
                description="Master advanced sword techniques",
                specialization=Specialization.BLADE_MASTER,
                tier=2,
                requirements={
                    'level': 20,
                    'mastery': ('COMBAT', 3),
                    'ability': ('basic_slash', 3)
                },
                bonuses={'attack_speed': 0.1, 'combo_efficiency': 0.15}
            ),
            # Add more nodes...
        ]
        self.specializations[Specialization.BLADE_MASTER] = nodes

    def gain_mastery_experience(
        self,
        mastery_type: MasteryType,
        amount: float,
        source: str
    ) -> bool:
        """Gain experience in a mastery type"""
        mastery = self.masteries[mastery_type]
        mastery.experience += amount
        
        leveled_up = False
        while mastery.experience >= mastery.get_next_level_requirement():
            mastery.experience -= mastery.get_next_level_requirement()
            mastery.level += 1
            leveled_up = True
            
            # Check for milestones
            milestone_key = f"{mastery_type.name}_level_{mastery.level}"
            if milestone_key not in mastery.milestones_achieved:
                mastery.milestones_achieved.add(milestone_key)
                self.milestones[milestone_key] = datetime.now()
        
        return leveled_up

    def unlock_specialization_node(
        self,
        specialization: Specialization,
        node_name: str
    ) -> bool:
        """Attempt to unlock a specialization node"""
        if specialization not in self.specializations:
            return False
            
        # Find the node
        node = next(
            (n for n in self.specializations[specialization] if n.name == node_name),
            None
        )
        if not node or node.is_unlocked:
            return False
            
        # Check requirements
        character_state = self.get_character_state()
        if not node.meets_requirements(character_state):
            return False
            
        # Check if we have points available
        if self.specialization_points <= 0:
            return False
            
        # Unlock the node
        node.is_unlocked = True
        node.is_active = True
        self.specialization_points -= 1
        
        # Apply bonuses
        self._apply_specialization_bonuses(node)
        
        return True

    def _apply_specialization_bonuses(self, node: SpecializationNode) -> None:
        """Apply bonuses from a specialization node"""
        for bonus_type, value in node.bonuses.items():
            if bonus_type in self.combat_multipliers:
                self.combat_multipliers[bonus_type] *= (1 + value)
            elif bonus_type.startswith('stat_'):
                stat_name = bonus_type[5:]
                if stat_name in self.stat_modifiers:
                    self.stat_modifiers[stat_name][f"spec_{node.name}"] = value

    def get_character_state(self) -> Dict[str, Any]:
        """Get current character state for requirement checking"""
        return {
            'level': self.level,
            'stats': self.get_effective_stats(),
            'masteries': {m.mastery_type.name: m.level for m in self.masteries.values()},
            'abilities': {
                name: ability.current_rank
                for name, ability in self.ability_system.abilities.items()
                if ability.is_unlocked
            },
            'achievements': self.achievements,
            'milestones': self.milestones
        }

    def get_effective_stats(self) -> Dict[StatType, float]:
        """Calculate effective stats with all modifiers"""
        effective_stats = self.base_stats.copy()
        
        # Apply stat modifiers
        for stat, modifiers in self.stat_modifiers.items():
            for modifier in modifiers.values():
                effective_stats[stat] *= (1 + modifier)
        
        # Apply mastery bonuses
        for mastery in self.masteries.values():
            if mastery.mastery_type == MasteryType.COMBAT:
                effective_stats[StatType.PHYSICAL_POWER] *= (1 + 0.05 * mastery.level)
                effective_stats[StatType.DEFENSE] *= (1 + 0.03 * mastery.level)
            elif mastery.mastery_type == MasteryType.DIMENSIONAL:
                effective_stats[StatType.DIMENSIONAL_ATTUNEMENT] *= (1 + 0.05 * mastery.level)
                effective_stats[StatType.STABILITY_CONTROL] *= (1 + 0.04 * mastery.level)
        
        return effective_stats

    def get_combat_multiplier(self, multiplier_type: str) -> float:
        """Get the current value of a combat multiplier"""
        return self.combat_multipliers.get(multiplier_type, 1.0)

    def reset_specialization(self, specialization: Specialization) -> bool:
        """Reset a specialization tree and refund points"""
        if specialization not in self.specializations:
            return False
            
        refunded_points = 0
        for node in self.specializations[specialization]:
            if node.is_unlocked:
                node.is_unlocked = False
                node.is_active = False
                refunded_points += 1
                
        self.specialization_points += refunded_points
        return True

    def save_progression(self) -> Dict[str, Any]:
        """Save progression data"""
        return {
            'level': self.level,
            'experience': self.experience,
            'progression_path': self.progression_path.name if self.progression_path else None,
            'base_stats': {str(k): v for k, v in self.base_stats.items()},
            'masteries': {
                mastery.mastery_type.name: {
                    'level': mastery.level,
                    'experience': mastery.experience,
                    'milestones': list(mastery.milestones_achieved)
                }
                for mastery in self.masteries.values()
            },
            'specializations': {
                spec.name: [
                    {
                        'name': node.name,
                        'is_unlocked': node.is_unlocked,
                        'is_active': node.is_active
                    }
                    for node in nodes
                ]
                for spec, nodes in self.specializations.items()
            },
            'achievements': list(self.achievements),
            'milestones': {
                k: v.isoformat() for k, v in self.milestones.items()
            }
        }

    def load_progression(self, data: Dict[str, Any]) -> None:
        """Load progression data"""
        self.level = data['level']
        self.experience = data['experience']
        self.progression_path = (
            ProgressionPath[data['progression_path']]
            if data['progression_path'] else None
        )
        
        # Load stats
        for stat_name, value in data['base_stats'].items():
            self.base_stats[StatType[stat_name]] = value
            
        # Load masteries
        for mastery_name, mastery_data in data['masteries'].items():
            mastery_type = MasteryType[mastery_name]
            self.masteries[mastery_type].level = mastery_data['level']
            self.masteries[mastery_type].experience = mastery_data['experience']
            self.masteries[mastery_type].milestones_achieved = set(mastery_data['milestones'])
            
        # Load specializations
        for spec_name, nodes_data in data['specializations'].items():
            spec = Specialization[spec_name]
            for node_data, node in zip(nodes_data, self.specializations[spec]):
                node.is_unlocked = node_data['is_unlocked']
                node.is_active = node_data['is_active']
                
        # Load achievements and milestones
        self.achievements = set(data['achievements'])
        self.milestones = {
            k: datetime.fromisoformat(v)
            for k, v in data['milestones'].items()
        }

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