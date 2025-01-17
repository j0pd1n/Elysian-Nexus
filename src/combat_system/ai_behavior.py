from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Set, Optional, Tuple, Any, Callable
from datetime import datetime
import math
import random

from .dimensional_combat import DimensionalLayer, DimensionalEffect, DimensionalAffinity
from .combat_types import Position, DamageType

class BehaviorType(Enum):
    """Types of AI behaviors"""
    AGGRESSIVE = auto()    # Focus on dealing damage
    DEFENSIVE = auto()     # Focus on survival
    TACTICAL = auto()      # Balance of offense and defense
    SUPPORT = auto()       # Focus on helping allies
    DISRUPTIVE = auto()    # Focus on hindering enemies
    DIMENSIONAL = auto()   # Focus on dimensional manipulation

class TacticalRole(Enum):
    """Combat roles for AI"""
    TANK = auto()          # Absorb damage
    DPS = auto()          # Deal damage
    HEALER = auto()       # Heal and support
    CONTROLLER = auto()    # Control battlefield
    ASSASSIN = auto()     # Target key enemies
    DIMENSIONIST = auto()  # Manipulate dimensions

class CombatPhase(Enum):
    """Different phases of combat"""
    OPENING = auto()       # Start of combat
    ADVANTAGE = auto()     # When winning
    DISADVANTAGE = auto()  # When losing
    CRITICAL = auto()      # Low health/resources
    FINISHING = auto()     # End of combat

@dataclass
class BehaviorPattern:
    """Defines a specific behavior pattern"""
    name: str
    behavior_type: BehaviorType
    tactical_role: TacticalRole
    priority: float
    conditions: Dict[str, Any]
    actions: List[str]
    cooldown: float = 0.0
    last_used: Optional[datetime] = None
    success_rate: float = 0.0
    usage_count: int = 0

@dataclass
class CombatMemory:
    """Stores combat experience for learning"""
    opponent_id: str
    timestamp: datetime
    behavior_used: str
    success: bool
    damage_dealt: float
    damage_taken: float
    duration: float
    dimensional_layers_used: Set[DimensionalLayer]
    effects_triggered: List[DimensionalEffect]

class AIBehaviorSystem:
    """Manages AI behavior in combat"""
    
    def __init__(self):
        self.behavior_patterns: Dict[str, BehaviorPattern] = {}
        self.combat_memories: List[CombatMemory] = []
        self.current_phase: CombatPhase = CombatPhase.OPENING
        self.learning_rate: float = 0.1
        self.exploration_rate: float = 0.2
        
        self._initialize_behavior_patterns()
        
    def _initialize_behavior_patterns(self) -> None:
        """Initialize default behavior patterns"""
        # Aggressive patterns
        self._add_aggressive_patterns()
        
        # Defensive patterns
        self._add_defensive_patterns()
        
        # Tactical patterns
        self._add_tactical_patterns()
        
        # Dimensional patterns
        self._add_dimensional_patterns()
        
    def _add_aggressive_patterns(self) -> None:
        """Add aggressive behavior patterns"""
        patterns = [
            BehaviorPattern(
                name="all_out_attack",
                behavior_type=BehaviorType.AGGRESSIVE,
                tactical_role=TacticalRole.DPS,
                priority=1.0,
                conditions={
                    'health_threshold': 0.7,
                    'target_distance': 'close',
                    'resource_threshold': 0.5
                },
                actions=['close_distance', 'heavy_attack', 'combo_attack']
            ),
            BehaviorPattern(
                name="dimensional_assault",
                behavior_type=BehaviorType.AGGRESSIVE,
                tactical_role=TacticalRole.DIMENSIONIST,
                priority=0.8,
                conditions={
                    'dimensional_energy': 0.6,
                    'target_vulnerable': True
                },
                actions=['dimension_shift', 'dimensional_strike', 'return_shift']
            ),
            # New aggressive patterns
            BehaviorPattern(
                name="berserker_frenzy",
                behavior_type=BehaviorType.AGGRESSIVE,
                tactical_role=TacticalRole.DPS,
                priority=0.9,
                conditions={
                    'health_threshold': 0.4,
                    'target_health_threshold': 0.6,
                    'adrenaline_charged': True
                },
                actions=['activate_frenzy', 'rapid_strikes', 'finishing_blow']
            ),
            BehaviorPattern(
                name="void_hunter",
                behavior_type=BehaviorType.AGGRESSIVE,
                tactical_role=TacticalRole.ASSASSIN,
                priority=0.85,
                conditions={
                    'void_energy': 0.7,
                    'target_isolated': True,
                    'stealth_available': True
                },
                actions=['void_step', 'mark_target', 'void_strike', 'execute']
            ),
            BehaviorPattern(
                name="reality_breaker",
                behavior_type=BehaviorType.AGGRESSIVE,
                tactical_role=TacticalRole.DIMENSIONIST,
                priority=0.95,
                conditions={
                    'reality_unstable': True,
                    'dimensional_power': 0.8,
                    'target_dimensional_shift': False
                },
                actions=['reality_shatter', 'dimensional_cascade', 'power_surge']
            )
        ]
        
        for pattern in patterns:
            self.behavior_patterns[pattern.name] = pattern
            
    def _add_defensive_patterns(self) -> None:
        """Add defensive behavior patterns"""
        patterns = [
            BehaviorPattern(
                name="tactical_retreat",
                behavior_type=BehaviorType.DEFENSIVE,
                tactical_role=TacticalRole.TANK,
                priority=0.9,
                conditions={
                    'health_threshold': 0.3,
                    'has_escape_route': True
                },
                actions=['create_distance', 'defensive_stance', 'heal']
            ),
            BehaviorPattern(
                name="dimensional_defense",
                behavior_type=BehaviorType.DEFENSIVE,
                tactical_role=TacticalRole.DIMENSIONIST,
                priority=0.85,
                conditions={
                    'under_pressure': True,
                    'dimensional_energy': 0.4
                },
                actions=['dimension_shift', 'stabilize_dimension', 'defensive_barrier']
            ),
            # New defensive patterns
            BehaviorPattern(
                name="celestial_guardian",
                behavior_type=BehaviorType.DEFENSIVE,
                tactical_role=TacticalRole.TANK,
                priority=0.95,
                conditions={
                    'allies_nearby': True,
                    'celestial_energy': 0.6,
                    'incoming_damage_high': True
                },
                actions=['celestial_shield', 'protection_aura', 'healing_burst', 'divine_intervention']
            ),
            BehaviorPattern(
                name="void_absorption",
                behavior_type=BehaviorType.DEFENSIVE,
                tactical_role=TacticalRole.TANK,
                priority=0.88,
                conditions={
                    'void_presence': True,
                    'corruption_level': 0.5,
                    'health_threshold': 0.4
                },
                actions=['void_embrace', 'absorb_damage', 'corruption_pulse', 'void_regeneration']
            ),
            BehaviorPattern(
                name="reality_anchor",
                behavior_type=BehaviorType.DEFENSIVE,
                tactical_role=TacticalRole.CONTROLLER,
                priority=0.92,
                conditions={
                    'dimensional_instability': 0.7,
                    'allies_in_danger': True,
                    'reality_anchor_available': True
                },
                actions=['deploy_anchor', 'stabilize_reality', 'dimensional_barrier', 'reality_restoration']
            )
        ]
        
        for pattern in patterns:
            self.behavior_patterns[pattern.name] = pattern
            
    def _add_tactical_patterns(self) -> None:
        """Add tactical behavior patterns"""
        patterns = [
            BehaviorPattern(
                name="flanking_maneuver",
                behavior_type=BehaviorType.TACTICAL,
                tactical_role=TacticalRole.ASSASSIN,
                priority=0.75,
                conditions={
                    'target_exposed': True,
                    'has_positioning': True
                },
                actions=['stealth_approach', 'surprise_attack', 'quick_retreat']
            ),
            BehaviorPattern(
                name="control_zone",
                behavior_type=BehaviorType.TACTICAL,
                tactical_role=TacticalRole.CONTROLLER,
                priority=0.7,
                conditions={
                    'in_control_zone': True,
                    'allies_nearby': True
                },
                actions=['area_control', 'support_allies', 'counter_attack']
            ),
            # New tactical patterns
            BehaviorPattern(
                name="dimensional_strategist",
                behavior_type=BehaviorType.TACTICAL,
                tactical_role=TacticalRole.CONTROLLER,
                priority=0.85,
                conditions={
                    'dimensional_mastery': 0.7,
                    'tactical_advantage': True,
                    'multiple_dimensions_active': True
                },
                actions=['analyze_dimensions', 'coordinate_shifts', 'exploit_weakness', 'dimensional_combo']
            ),
            BehaviorPattern(
                name="void_tactician",
                behavior_type=BehaviorType.TACTICAL,
                tactical_role=TacticalRole.CONTROLLER,
                priority=0.82,
                conditions={
                    'void_presence': True,
                    'tactical_insight': 0.6,
                    'enemy_pattern_recognized': True
                },
                actions=['void_analysis', 'predict_movement', 'tactical_void_step', 'counter_strategy']
            ),
            BehaviorPattern(
                name="reality_manipulator",
                behavior_type=BehaviorType.TACTICAL,
                tactical_role=TacticalRole.DIMENSIONIST,
                priority=0.88,
                conditions={
                    'reality_flux': True,
                    'dimensional_control': 0.7,
                    'environment_manipulatable': True
                },
                actions=['analyze_reality', 'manipulate_terrain', 'create_advantage', 'reality_trap']
            )
        ]
        
        for pattern in patterns:
            self.behavior_patterns[pattern.name] = pattern
            
    def _add_dimensional_patterns(self) -> None:
        """Add dimension-focused behavior patterns"""
        patterns = [
            BehaviorPattern(
                name="reality_warp",
                behavior_type=BehaviorType.DIMENSIONAL,
                tactical_role=TacticalRole.DIMENSIONIST,
                priority=0.9,
                conditions={
                    'dimensional_energy': 0.8,
                    'reality_unstable': True
                },
                actions=['destabilize_dimension', 'dimensional_surge', 'reality_anchor']
            ),
            BehaviorPattern(
                name="void_manipulation",
                behavior_type=BehaviorType.DIMENSIONAL,
                tactical_role=TacticalRole.CONTROLLER,
                priority=0.85,
                conditions={
                    'void_presence': True,
                    'corruption_level': 0.5
                },
                actions=['void_channel', 'corrupt_reality', 'void_step']
            ),
            # New dimensional patterns
            BehaviorPattern(
                name="dimension_weaver",
                behavior_type=BehaviorType.DIMENSIONAL,
                tactical_role=TacticalRole.DIMENSIONIST,
                priority=0.95,
                conditions={
                    'dimensional_mastery': 0.9,
                    'reality_threads_visible': True,
                    'dimensional_convergence': True
                },
                actions=['analyze_threads', 'weave_dimensions', 'reality_reshape', 'dimensional_lock']
            ),
            BehaviorPattern(
                name="void_sovereign",
                behavior_type=BehaviorType.DIMENSIONAL,
                tactical_role=TacticalRole.CONTROLLER,
                priority=0.92,
                conditions={
                    'void_dominion': 0.8,
                    'reality_corruption': 0.7,
                    'dimensional_weakness': True
                },
                actions=['void_dominance', 'reality_corrupt', 'dimensional_collapse', 'void_empowerment']
            ),
            BehaviorPattern(
                name="reality_architect",
                behavior_type=BehaviorType.DIMENSIONAL,
                tactical_role=TacticalRole.DIMENSIONIST,
                priority=0.88,
                conditions={
                    'reality_mastery': 0.8,
                    'dimensional_stability': 0.3,
                    'architecture_possible': True
                },
                actions=['analyze_structure', 'reality_blueprint', 'dimensional_construct', 'reality_fortify']
            )
        ]
        
        for pattern in patterns:
            self.behavior_patterns[pattern.name] = pattern

    def select_behavior(self, 
                       combat_state: Dict[str, Any],
                       available_actions: Set[str]) -> Optional[List[str]]:
        """Select the most appropriate behavior pattern"""
        valid_patterns = []
        
        # Update current phase
        self._update_combat_phase(combat_state)
        
        # Filter patterns by conditions and available actions
        for pattern in self.behavior_patterns.values():
            if self._check_pattern_conditions(pattern, combat_state):
                if all(action in available_actions for action in pattern.actions):
                    if not pattern.last_used or \
                       (datetime.now() - pattern.last_used).total_seconds() > pattern.cooldown:
                        valid_patterns.append(pattern)
        
        if not valid_patterns:
            return None
            
        # Exploration vs exploitation
        if random.random() < self.exploration_rate:
            # Explore: Choose random valid pattern
            chosen_pattern = random.choice(valid_patterns)
        else:
            # Exploit: Choose highest priority pattern considering success rate
            chosen_pattern = max(
                valid_patterns,
                key=lambda p: p.priority * (0.5 + 0.5 * p.success_rate)
            )
            
        chosen_pattern.last_used = datetime.now()
        chosen_pattern.usage_count += 1
        return chosen_pattern.actions

    def _check_pattern_conditions(self,
                                pattern: BehaviorPattern,
                                combat_state: Dict[str, Any]) -> bool:
        """Check if conditions for a pattern are met"""
        for condition, value in pattern.conditions.items():
            if condition not in combat_state:
                return False
                
            if isinstance(value, bool):
                if combat_state[condition] != value:
                    return False
            elif isinstance(value, (int, float)):
                if combat_state[condition] < value:
                    return False
            elif isinstance(value, str):
                if combat_state[condition] != value:
                    return False
                    
        return True

    def _update_combat_phase(self, combat_state: Dict[str, Any]) -> None:
        """Update the current combat phase"""
        if combat_state.get('combat_time', 0) < 10:
            self.current_phase = CombatPhase.OPENING
        elif combat_state.get('health', 1.0) < 0.3:
            self.current_phase = CombatPhase.CRITICAL
        elif combat_state.get('advantage_score', 0) > 0.6:
            self.current_phase = CombatPhase.ADVANTAGE
        elif combat_state.get('advantage_score', 0) < 0.4:
            self.current_phase = CombatPhase.DISADVANTAGE
        elif combat_state.get('target_health', 1.0) < 0.2:
            self.current_phase = CombatPhase.FINISHING

    def record_combat_memory(self,
                           opponent_id: str,
                           behavior_used: str,
                           combat_result: Dict[str, Any]) -> None:
        """Record the result of using a behavior"""
        memory = CombatMemory(
            opponent_id=opponent_id,
            timestamp=datetime.now(),
            behavior_used=behavior_used,
            success=combat_result['success'],
            damage_dealt=combat_result['damage_dealt'],
            damage_taken=combat_result['damage_taken'],
            duration=combat_result['duration'],
            dimensional_layers_used=set(combat_result['dimensions_used']),
            effects_triggered=combat_result['effects_triggered']
        )
        
        self.combat_memories.append(memory)
        self._update_behavior_stats(memory)
        
        # Trim old memories if needed
        if len(self.combat_memories) > 1000:
            self.combat_memories = self.combat_memories[-1000:]

    def _update_behavior_stats(self, memory: CombatMemory) -> None:
        """Update behavior pattern statistics"""
        if memory.behavior_used in self.behavior_patterns:
            pattern = self.behavior_patterns[memory.behavior_used]
            
            # Update success rate with learning rate
            new_success = 1.0 if memory.success else 0.0
            pattern.success_rate = (
                (1 - self.learning_rate) * pattern.success_rate +
                self.learning_rate * new_success
            )
            
            # Adjust priority based on performance
            effectiveness = (
                memory.damage_dealt / (memory.damage_taken + 1.0) *
                (1.0 if memory.success else 0.5)
            )
            pattern.priority = max(0.1, min(1.0,
                pattern.priority * (1.0 + 0.1 * (effectiveness - 0.5))
            ))

    def get_behavior_analytics(self) -> Dict[str, Any]:
        """Get analytics about behavior patterns"""
        analytics = {
            'pattern_usage': {},
            'success_rates': {},
            'phase_distribution': {},
            'dimensional_preferences': {},
            'average_effectiveness': {}
        }
        
        # Calculate pattern usage and success rates
        total_usage = sum(p.usage_count for p in self.behavior_patterns.values())
        if total_usage > 0:
            for name, pattern in self.behavior_patterns.items():
                analytics['pattern_usage'][name] = pattern.usage_count / total_usage
                analytics['success_rates'][name] = pattern.success_rate
                
        # Calculate phase distribution
        phase_counts = {}
        for memory in self.combat_memories:
            phase = self._get_phase_for_memory(memory)
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
        total_phases = sum(phase_counts.values())
        if total_phases > 0:
            analytics['phase_distribution'] = {
                phase.name: count/total_phases
                for phase, count in phase_counts.items()
            }
            
        # Calculate dimensional preferences
        dimension_usage = {}
        for memory in self.combat_memories:
            for dim in memory.dimensional_layers_used:
                dimension_usage[dim] = dimension_usage.get(dim, 0) + 1
        total_dims = sum(dimension_usage.values())
        if total_dims > 0:
            analytics['dimensional_preferences'] = {
                dim.name: count/total_dims
                for dim, count in dimension_usage.items()
            }
            
        # Calculate average effectiveness
        for name, pattern in self.behavior_patterns.items():
            relevant_memories = [
                m for m in self.combat_memories
                if m.behavior_used == name
            ]
            if relevant_memories:
                avg_damage_ratio = sum(
                    m.damage_dealt / (m.damage_taken + 1.0)
                    for m in relevant_memories
                ) / len(relevant_memories)
                analytics['average_effectiveness'][name] = avg_damage_ratio
                
        return analytics

    def _get_phase_for_memory(self, memory: CombatMemory) -> CombatPhase:
        """Determine the combat phase for a memory"""
        if memory.damage_taken == 0:
            return CombatPhase.ADVANTAGE
        damage_ratio = memory.damage_dealt / memory.damage_taken
        
        if damage_ratio > 2.0:
            return CombatPhase.ADVANTAGE
        elif damage_ratio < 0.5:
            return CombatPhase.DISADVANTAGE
        else:
            return CombatPhase.TACTICAL

    def adapt_behavior(self, opponent_id: str) -> None:
        """Adapt behavior patterns based on combat history"""
        # Get relevant memories
        relevant_memories = [
            m for m in self.combat_memories
            if m.opponent_id == opponent_id
        ]
        
        if not relevant_memories:
            return
            
        # Analyze successful patterns
        successful_patterns = {}
        for memory in relevant_memories:
            if memory.success:
                successful_patterns[memory.behavior_used] = \
                    successful_patterns.get(memory.behavior_used, 0) + 1
                    
        # Adjust pattern priorities
        total_successes = sum(successful_patterns.values())
        if total_successes > 0:
            for pattern_name, successes in successful_patterns.items():
                if pattern_name in self.behavior_patterns:
                    pattern = self.behavior_patterns[pattern_name]
                    success_ratio = successes / total_successes
                    pattern.priority = max(0.1, min(1.0,
                        pattern.priority * (1.0 + 0.2 * (success_ratio - 0.5))
                    ))
                    
        # Adjust exploration rate based on success
        overall_success_rate = sum(
            1 for m in relevant_memories if m.success
        ) / len(relevant_memories)
        
        self.exploration_rate = max(0.1, min(0.5,
            0.3 * (1.0 - overall_success_rate)
        )) 