from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum, auto
import math
import random
from src.combat_system.dimensional_combat import DimensionalLayer, Position, DimensionalEffect
from src.character.ability_system import AbilitySystem, Ability, AbilityType
from src.character.progression_system import ProgressionSystem, StatType
from src.world.terrain_generator import TerrainCell

class BehaviorType(Enum):
    AGGRESSIVE = auto()  # Actively seeks combat
    DEFENSIVE = auto()   # Prefers defensive positions
    CAUTIOUS = auto()    # Maintains distance, uses ranged attacks
    SUPPORT = auto()     # Focuses on buffing allies
    DIMENSIONAL = auto() # Specializes in dimensional manipulation
    ERRATIC = auto()     # Unpredictable behavior
    PASSIVE = auto()     # Non-hostile unless attacked

class TacticalRole(Enum):
    TANK = auto()        # High defense, crowd control
    DPS = auto()         # High damage output
    HEALER = auto()      # Support and healing
    CONTROLLER = auto()  # Crowd control and debuffs
    SHIFTER = auto()     # Dimensional manipulation

@dataclass
class CombatMemory:
    """Tracks combat-related memories for learning"""
    opponent_abilities: Set[str]
    successful_combos: List[List[str]]
    failed_attempts: List[List[str]]
    dimensional_shifts: Dict[DimensionalLayer, int]
    damage_taken: Dict[str, float]
    damage_dealt: Dict[str, float]

@dataclass
class TacticalState:
    """Current tactical state of the NPC"""
    health_percentage: float
    resource_percentages: Dict[str, float]
    current_position: Position
    nearby_allies: List[Position]
    nearby_enemies: List[Position]
    active_effects: Set[DimensionalEffect]
    current_terrain: TerrainCell
    available_abilities: Set[str]
    ability_cooldowns: Dict[str, float]

class NPCAI:
    """Manages NPC AI behavior and decision making"""
    
    def __init__(
        self,
        behavior_type: BehaviorType,
        tactical_role: TacticalRole,
        ability_system: AbilitySystem,
        progression_system: ProgressionSystem
    ):
        self.behavior_type = behavior_type
        self.tactical_role = tactical_role
        self.ability_system = ability_system
        self.progression_system = progression_system
        
        self.combat_memory = CombatMemory(
            opponent_abilities=set(),
            successful_combos=[],
            failed_attempts=[],
            dimensional_shifts={},
            damage_taken={},
            damage_dealt={}
        )
        
        self.behavior_weights = self._initialize_behavior_weights()
        self.ability_preferences = self._initialize_ability_preferences()
        self.tactical_preferences = self._initialize_tactical_preferences()
        
    def _initialize_behavior_weights(self) -> Dict[str, float]:
        """Initialize behavior weights based on type"""
        weights = {
            "aggression": 0.5,
            "defense": 0.5,
            "ranged_preference": 0.5,
            "dimensional_usage": 0.5,
            "ally_support": 0.5,
            "risk_taking": 0.5
        }
        
        if self.behavior_type == BehaviorType.AGGRESSIVE:
            weights.update({
                "aggression": 0.9,
                "defense": 0.2,
                "risk_taking": 0.8
            })
        elif self.behavior_type == BehaviorType.DEFENSIVE:
            weights.update({
                "aggression": 0.2,
                "defense": 0.9,
                "risk_taking": 0.3
            })
        # Add other behavior type adjustments...
        
        return weights
        
    def _initialize_ability_preferences(self) -> Dict[AbilityType, float]:
        """Initialize ability type preferences based on role"""
        preferences = {ability_type: 0.5 for ability_type in AbilityType}
        
        if self.tactical_role == TacticalRole.TANK:
            preferences.update({
                AbilityType.PHYSICAL: 0.8,
                AbilityType.UTILITY: 0.7,
                AbilityType.DIMENSIONAL: 0.4
            })
        elif self.tactical_role == TacticalRole.SHIFTER:
            preferences.update({
                AbilityType.DIMENSIONAL: 0.9,
                AbilityType.VOID: 0.7,
                AbilityType.PRIMORDIAL: 0.6
            })
        # Add other role preferences...
        
        return preferences
        
    def _initialize_tactical_preferences(self) -> Dict[str, float]:
        """Initialize tactical preferences based on role"""
        preferences = {
            "optimal_range": 5.0,
            "ally_proximity": 5.0,
            "enemy_proximity": 5.0,
            "terrain_preference": 0.5,
            "dimensional_stability": 0.5
        }
        
        if self.tactical_role == TacticalRole.DPS:
            preferences.update({
                "optimal_range": 3.0,
                "enemy_proximity": 3.0
            })
        elif self.tactical_role == TacticalRole.HEALER:
            preferences.update({
                "ally_proximity": 3.0,
                "enemy_proximity": 8.0
            })
        # Add other role preferences...
        
        return preferences
        
    def update_combat_memory(
        self,
        ability_used: str,
        target_position: Position,
        damage_dealt: float,
        damage_taken: float,
        was_successful: bool
    ) -> None:
        """Update combat memory with results"""
        # Record damage
        self.combat_memory.damage_dealt[ability_used] = (
            self.combat_memory.damage_dealt.get(ability_used, 0) + damage_dealt
        )
        if damage_taken > 0:
            self.combat_memory.damage_taken[ability_used] = (
                self.combat_memory.damage_taken.get(ability_used, 0) + damage_taken
            )
            
        # Update combo tracking
        if len(self.combat_memory.successful_combos) > 0:
            current_combo = self.combat_memory.successful_combos[-1]
            if was_successful:
                current_combo.append(ability_used)
                if len(current_combo) >= 3:  # Complete combo
                    self.combat_memory.successful_combos.append([])
            else:
                if len(current_combo) > 0:
                    self.combat_memory.failed_attempts.append(current_combo)
                self.combat_memory.successful_combos.append([])
                
    def evaluate_tactical_position(
        self,
        state: TacticalState
    ) -> Dict[Position, float]:
        """Evaluate possible tactical positions"""
        position_scores = {}
        
        # Get possible positions (simplified for example)
        possible_positions = self._get_nearby_positions(state.current_position)
        
        for position in possible_positions:
            score = 0.0
            
            # Distance to allies
            for ally_pos in state.nearby_allies:
                distance = self._calculate_distance(position, ally_pos)
                score += self._score_ally_distance(distance)
                
            # Distance to enemies
            for enemy_pos in state.nearby_enemies:
                distance = self._calculate_distance(position, enemy_pos)
                score += self._score_enemy_distance(distance)
                
            # Terrain evaluation
            terrain_score = self._evaluate_terrain(state.current_terrain)
            score += terrain_score
            
            # Dimensional stability
            stability_score = self._evaluate_stability(
                state.active_effects,
                state.current_terrain
            )
            score += stability_score
            
            position_scores[position] = score
            
        return position_scores
        
    def choose_ability(
        self,
        state: TacticalState,
        target_position: Position
    ) -> Optional[str]:
        """Choose the best ability for the current situation"""
        available_abilities = {
            name: self.ability_system.abilities[name]
            for name in state.available_abilities
            if name not in state.ability_cooldowns
        }
        
        if not available_abilities:
            return None
            
        ability_scores = {}
        for name, ability in available_abilities.items():
            score = self._score_ability(
                ability,
                state,
                target_position
            )
            ability_scores[name] = score
            
        if ability_scores:
            return max(ability_scores.items(), key=lambda x: x[1])[0]
        return None
        
    def _score_ability(
        self,
        ability: Ability,
        state: TacticalState,
        target_position: Position
    ) -> float:
        """Score an ability based on current situation"""
        score = 0.0
        
        # Base score from preferences
        score += self.ability_preferences[ability.ability_type]
        
        # Distance consideration
        distance = self._calculate_distance(
            state.current_position,
            target_position
        )
        score += self._score_ability_range(ability, distance)
        
        # Resource consideration
        score += self._score_resource_cost(ability, state.resource_percentages)
        
        # Tactical consideration
        score += self._score_tactical_value(ability, state)
        
        # Success history
        score += self._score_historical_success(ability.name)
        
        return score
        
    def _score_ability_range(
        self,
        ability: Ability,
        distance: float
    ) -> float:
        """Score ability based on range to target"""
        optimal_range = self.tactical_preferences["optimal_range"]
        range_difference = abs(distance - optimal_range)
        return max(0.0, 1.0 - range_difference / optimal_range)
        
    def _score_resource_cost(
        self,
        ability: Ability,
        resource_percentages: Dict[str, float]
    ) -> float:
        """Score ability based on resource cost"""
        score = 0.0
        for cost in ability.costs:
            if str(cost.resource_type) in resource_percentages:
                resource_percent = resource_percentages[str(cost.resource_type)]
                if resource_percent < cost.base_amount:
                    return -1000.0  # Cannot use
                score += resource_percent - cost.base_amount
        return score / len(ability.costs) if ability.costs else 0.0
        
    def _score_tactical_value(
        self,
        ability: Ability,
        state: TacticalState
    ) -> float:
        """Score ability based on tactical situation"""
        score = 0.0
        
        # Health consideration
        if state.health_percentage < 0.3:
            # Favor defensive abilities when low on health
            if any(effect.is_buff for effect in ability.effects):
                score += 2.0
                
        # Enemy proximity
        if len(state.nearby_enemies) > 2:
            # Favor AOE abilities when multiple enemies are nearby
            if any(effect.radius > 0 for effect in ability.effects):
                score += 1.5
                
        # Dimensional considerations
        if any(effect.effect_type == DimensionalEffect.WARPING 
               for effect in state.active_effects):
            # Favor stabilizing abilities when dimensional warping is active
            if any(effect.effect_type == DimensionalEffect.STABILIZING 
                   for effect in ability.effects):
                score += 1.0
                
        return score
        
    def _score_historical_success(self, ability_name: str) -> float:
        """Score ability based on historical success"""
        damage_dealt = self.combat_memory.damage_dealt.get(ability_name, 0)
        damage_taken = self.combat_memory.damage_taken.get(ability_name, 0)
        
        if damage_dealt + damage_taken == 0:
            return 0.0
            
        success_ratio = damage_dealt / (damage_dealt + damage_taken)
        return success_ratio * 2.0 - 1.0  # Scale to [-1.0, 1.0]
        
    def _calculate_distance(self, pos1: Position, pos2: Position) -> float:
        """Calculate distance between positions"""
        return math.sqrt(
            (pos1.x - pos2.x)**2 +
            (pos1.y - pos2.y)**2
        )
        
    def _get_nearby_positions(self, position: Position) -> List[Position]:
        """Get list of nearby positions (simplified)"""
        nearby = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nearby.append(Position(
                    x=position.x + dx,
                    y=position.y + dy,
                    z=position.z,
                    dimensional_layer=position.dimensional_layer
                ))
        return nearby
        
    def _score_ally_distance(self, distance: float) -> float:
        """Score distance to ally based on preferences"""
        optimal = self.tactical_preferences["ally_proximity"]
        difference = abs(distance - optimal)
        return max(0.0, 1.0 - difference / optimal)
        
    def _score_enemy_distance(self, distance: float) -> float:
        """Score distance to enemy based on preferences"""
        optimal = self.tactical_preferences["enemy_proximity"]
        difference = abs(distance - optimal)
        return max(0.0, 1.0 - difference / optimal)
        
    def _evaluate_terrain(self, terrain: TerrainCell) -> float:
        """Evaluate terrain suitability"""
        if not terrain.traversable:
            return -1000.0
            
        score = 0.0
        
        # Height advantage
        score += terrain.height * 0.5
        
        # Hazard consideration
        score -= terrain.hazard_level * 0.8
        
        # Stability consideration
        score += terrain.stability_modifier * 0.3
        
        return score
        
    def _evaluate_stability(
        self,
        active_effects: Set[DimensionalEffect],
        terrain: TerrainCell
    ) -> float:
        """Evaluate dimensional stability"""
        score = terrain.stability_modifier
        
        # Consider active effects
        for effect in active_effects:
            if effect == DimensionalEffect.STABILIZING:
                score += 0.2
            elif effect == DimensionalEffect.WARPING:
                score -= 0.3
            elif effect == DimensionalEffect.DISTORTION:
                score -= 0.2
                
        return score * self.tactical_preferences["dimensional_stability"] 