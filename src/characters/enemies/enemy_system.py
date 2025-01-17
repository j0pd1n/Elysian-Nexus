from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random
import math
import time

class EnemyType(Enum):
    """Core enemy types with clear progression paths"""
    NORMAL = "Normal"          # 👤 Basic enemies
    ELITE = "Elite"           # 💪 Stronger variants
    BOSS = "Boss"             # 👑 Area/quest bosses
    LEGENDARY = "Legendary"    # ⭐ Unique named enemies
    MYTHICAL = "Mythical"      # 🌟 Story-critical bosses
    COSMIC = "Cosmic"          # 🌌 Reality-altering entities
    CORRUPTED = "Corrupted"    # 💀 Twisted variants
    ASCENDED = "Ascended"      # 🌠 Evolved forms
    PRIMORDIAL = "Primordial"  # 🌋 Ancient powers

class CombatState(Enum):
    """Enemy combat states"""
    IDLE = "Idle"
    AGGRESSIVE = "Aggressive"
    DEFENSIVE = "Defensive"
    FLEEING = "Fleeing"
    STUNNED = "Stunned"
    CASTING = "Casting"
    CHARGING = "Charging"
    RECOVERING = "Recovering"

@dataclass
class EnemyCore:
    """Core enemy attributes and identity"""
    id: str
    name: str
    type: EnemyType
    level: int
    rank: str
    faction: Optional[str] = None
    lore: Optional[Dict[str, str]] = None
    evolution_stage: int = 0
    variant_type: Optional[str] = None

@dataclass
class EnemyStats:
    """Core stats for enemies"""
    level: int
    health: float
    max_health: float
    mana: float
    max_mana: float
    stamina: float
    max_stamina: float
    attack: float
    defense: float
    magic_attack: float
    magic_defense: float
    speed: float
    critical_rate: float
    critical_damage: float
    dodge_chance: float
    accuracy: float
    resistance: Dict[str, float]  # Different types of damage resistance
    weakness: Dict[str, float]    # Different types of weakness

@dataclass
class CombatAbilities:
    """Combat abilities and skills"""
    basic_attacks: List[Dict[str, Any]]
    special_moves: List[Dict[str, Any]]
    ultimate_ability: Dict[str, Any]
    passive_effects: List[Dict[str, Any]]
    cooldowns: Dict[str, float]
    energy_costs: Dict[str, float]

@dataclass
class BehaviorSystem:
    """Advanced AI behavior system"""
    aggression: float
    intelligence: float
    caution: float
    cooperation: float
    patterns: List[Dict[str, Any]]
    triggers: Dict[str, Dict[str, Any]]
    responses: Dict[str, List[str]]
    current_pattern: Optional[Dict[str, Any]] = None
    aggression_level: float = None
    intelligence_level: float = None
    cooperation_level: float = None
    caution_level: float = None
    current_state: CombatState = CombatState.IDLE
    behavior_patterns: Dict[str, Any] = None
    memory: List[Dict[str, Any]] = None
    last_action: Optional[str] = None
    action_success_rate: Dict[str, float] = None

@dataclass
class PhaseSystem:
    """Combat phase management"""
    phases: List[str]
    transitions: List[Dict[str, Any]]
    abilities_per_phase: Dict[str, List[str]]
    phase_durations: Dict[str, Optional[float]]
    phase_conditions: Dict[str, Dict[str, float]]
    current_phase: str = "normal"
    phase_start_time: float = 0.0
    phase_triggers: Dict[str, Any] = None
    phase_abilities: Dict[str, List[str]] = None
    phase_modifiers: Dict[str, Dict[str, float]] = None
    phase_duration: Dict[str, float] = None
    phase_cooldowns: Dict[str, float] = None

@dataclass
class ScalingSystem:
    """Dynamic scaling and progression"""
    base_multiplier: float
    level_scaling: Dict[str, float]
    difficulty_scaling: Dict[str, float]
    progression_rate: float
    power_curve: Dict[str, float]

@dataclass
class InteractionSystem:
    """World and environment interaction"""
    faction_relations: Dict[str, float]
    environment_reactions: Dict[str, Dict[str, Any]]
    event_responses: Dict[str, List[str]]
    dialogue_options: Dict[str, List[str]]

@dataclass
class Enemy:
    """Main enemy class with integrated systems"""
    def __init__(
        self,
        core: EnemyCore,
        stats: EnemyStats,
        abilities: CombatAbilities,
        behavior: BehaviorSystem,
        phases: Optional[PhaseSystem] = None,
        scaling: Optional[ScalingSystem] = None,
        interaction: Optional[InteractionSystem] = None
    ):
        self.core = core
        self.stats = stats
        self.abilities = abilities
        self.behavior = behavior
        self.phases = phases or PhaseSystem([], {}, {}, {}, {})
        self.scaling = scaling or ScalingSystem()
        self.interaction = interaction or InteractionSystem()
        
        # Runtime state
        self.current_phase = None
        self.combat_state = {}
        self.interaction_state = {}
        self.memory = []

    def update(self, context: Dict[str, any]) -> Dict[str, any]:
        """Update enemy state based on context"""
        self._update_combat_state(context)
        self._process_behavior(context)
        self._check_phase_transition(context)
        self._apply_scaling(context)
        return self._get_current_state()

    def _update_combat_state(self, context: Dict[str, any]):
        """Update combat-related state"""
        self.combat_state.update({
            'health_ratio': self.stats.health / self.get_max_health(),
            'phase': self.current_phase,
            'active_effects': self._get_active_effects(),
            'available_moves': self._get_available_moves(context)
        })

    def _process_behavior(self, context: Dict[str, any]):
        """Process AI behavior"""
        threat_level = self._assess_threat(context)
        optimal_action = self._determine_optimal_action(context, threat_level)
        self._update_memory(context, optimal_action)
        self._adjust_behavior(context)

    def _check_phase_transition(self, context: Dict[str, any]):
        """Check and handle phase transitions"""
        if not self.phases.phases:
            return
            
        for phase, conditions in self.phases.phase_conditions.items():
            if self._should_transition_to_phase(phase, conditions, context):
                self._transition_to_phase(phase, context)
                break

    def _apply_scaling(self, context: Dict[str, any]):
        """Apply dynamic scaling"""
        if not self.scaling:
            return
            
        level_factor = self._calculate_level_scaling(context)
        difficulty_factor = self._calculate_difficulty_scaling(context)
        progression_factor = self._calculate_progression_scaling(context)
        
        self._apply_scaling_factors(level_factor, difficulty_factor, progression_factor)

    def get_max_health(self) -> float:
        """Get maximum health with all modifiers"""
        base = self.stats.health
        level_mod = self.scaling.level_scaling.get('health', 1.0)
        difficulty_mod = self.scaling.difficulty_scaling.get('health', 1.0)
        return base * level_mod * difficulty_mod * self.scaling.base_multiplier

    def _get_active_effects(self) -> List[str]:
        """Get currently active effects"""
        return [effect for effect, duration in self.combat_state.get('effects', {}).items() if duration > 0]

    def _get_available_moves(self, context: Dict[str, any]) -> List[str]:
        """Get available moves in current context"""
        available = self.abilities.basic_attacks.copy()
        
        # Add special moves if conditions are met
        if self._can_use_special_moves(context):
            available.extend(self.abilities.special_moves)
            
        # Add ultimate if available
        if self.abilities.ultimate_ability and self._can_use_ultimate(context):
            available.append(self.abilities.ultimate_ability)
            
        # Add phase-specific abilities
        if self.current_phase:
            available.extend(self.phases.abilities_per_phase.get(self.current_phase, []))
            
        return available

    def _assess_threat(self, context: Dict[str, any]) -> float:
        """Assess current threat level"""
        player_power = context.get('player_power', 1.0)
        health_ratio = self.combat_state['health_ratio']
        environmental_threat = self._calculate_environmental_threat(context)
        
        return (player_power * 0.5 + (1 - health_ratio) * 0.3 + environmental_threat * 0.2)

    def _determine_optimal_action(self, context: Dict[str, any], threat_level: float) -> str:
        """Determine best action based on context and threat"""
        available_moves = self._get_available_moves(context)
        move_scores = {}
        
        for move in available_moves:
            score = self._evaluate_move(move, context, threat_level)
            move_scores[move] = score
            
        return max(move_scores.items(), key=lambda x: x[1])[0]

    def _evaluate_move(self, move: str, context: Dict[str, any], threat_level: float) -> float:
        """Evaluate a move's effectiveness"""
        base_score = self._get_move_base_score(move)
        context_modifier = self._get_context_modifier(move, context)
        threat_modifier = self._get_threat_modifier(move, threat_level)
        memory_modifier = self._get_memory_modifier(move)
        
        return base_score * context_modifier * threat_modifier * memory_modifier

    def _update_memory(self, context: Dict[str, any], action: str):
        """Update combat memory"""
        self.memory.append({
            'action': action,
            'context': self._get_relevant_context(context),
            'outcome': self._get_action_outcome(action, context)
        })
        
        if len(self.memory) > self.behavior.memory_capacity:
            self.memory.pop(0)

    def _get_current_state(self) -> Dict[str, any]:
        """Get current enemy state"""
        return {
            'core': self.core.__dict__,
            'combat': self.combat_state,
            'interaction': self.interaction_state,
            'phase': self.current_phase,
            'memory': self.memory
        }

    def _can_use_special_moves(self, context: Dict[str, any]) -> bool:
        """Determine if special moves can be used"""
        # Check energy/resource requirements
        energy = self.combat_state.get('energy', 0)
        required_energy = 30  # Base energy requirement
        
        # Check cooldowns
        special_cooldowns = self.combat_state.get('cooldowns', {})
        has_available_special = any(cd <= 0 for cd in special_cooldowns.values())
        
        # Check conditions
        health_threshold = 0.3
        health_ratio = self.combat_state['health_ratio']
        in_combat = context.get('in_combat', False)
        
        return (
            energy >= required_energy and
            has_available_special and
            (health_ratio <= health_threshold or in_combat)
        )

    def _can_use_ultimate(self, context: Dict[str, any]) -> bool:
        """Determine if ultimate ability can be used"""
        # Check ultimate charge
        ultimate_charge = self.combat_state.get('ultimate_charge', 0)
        required_charge = 100
        
        # Check conditions
        health_threshold = 0.5
        health_ratio = self.combat_state['health_ratio']
        threat_level = self._assess_threat(context)
        
        # Check strategic value
        strategic_value = self._calculate_ultimate_value(context)
        
        return (
            ultimate_charge >= required_charge and
            (health_ratio <= health_threshold or threat_level >= 0.7) and
            strategic_value >= 0.8
        )

    def _calculate_environmental_threat(self, context: Dict[str, any]) -> float:
        """Calculate threat from environmental factors"""
        environment = context.get('environment', {})
        weather = environment.get('weather', 'normal')
        time = environment.get('time', 'day')
        terrain = environment.get('terrain', 'normal')
        
        # Base threat values
        weather_threat = {
            'storm': 0.3,
            'fog': 0.2,
            'rain': 0.1,
            'normal': 0.0
        }.get(weather, 0.0)
        
        time_threat = {
            'night': 0.2,
            'dusk': 0.1,
            'dawn': 0.1,
            'day': 0.0
        }.get(time, 0.0)
        
        terrain_threat = {
            'hazardous': 0.3,
            'difficult': 0.2,
            'normal': 0.0
        }.get(terrain, 0.0)
        
        return weather_threat + time_threat + terrain_threat

    def _get_move_base_score(self, move: str) -> float:
        """Get base effectiveness score for a move"""
        if move in self.abilities.basic_attacks:
            return 1.0
        elif move in self.abilities.special_moves:
            return 1.5
        elif move == self.abilities.ultimate_ability:
            return 2.0
        else:
            return 0.5

    def _get_context_modifier(self, move: str, context: Dict[str, any]) -> float:
        """Get context-based modifier for move effectiveness"""
        modifiers = []
        
        # Environmental modifiers
        environment = context.get('environment', {})
        if self._move_suits_environment(move, environment):
            modifiers.append(1.2)
        
        # Target vulnerability
        target = context.get('target', {})
        if self._move_exploits_vulnerability(move, target):
            modifiers.append(1.3)
        
        # Tactical advantage
        position = context.get('position', {})
        if self._move_has_tactical_advantage(move, position):
            modifiers.append(1.1)
        
        return sum(modifiers) / len(modifiers) if modifiers else 1.0

    def _get_threat_modifier(self, move: str, threat_level: float) -> float:
        """Get threat-based modifier for move effectiveness"""
        if threat_level >= 0.8:  # High threat
            if move == self.abilities.ultimate_ability:
                return 1.5
            elif move in self.abilities.special_moves:
                return 1.3
        elif threat_level >= 0.5:  # Medium threat
            if move in self.abilities.special_moves:
                return 1.2
        
        return 1.0

    def _get_memory_modifier(self, move: str) -> float:
        """Get memory-based modifier for move effectiveness"""
        if not self.memory:
            return 1.0
        
        # Check move success history
        move_history = [m for m in self.memory if m['action'] == move]
        if not move_history:
            return 1.0
        
        success_rate = sum(1 for m in move_history if m['outcome']['success']) / len(move_history)
        return 1.0 + (success_rate - 0.5)  # Bonus for moves that worked well

    def _get_relevant_context(self, context: Dict[str, any]) -> Dict[str, any]:
        """Extract relevant context information for memory"""
        return {
            'player_state': context.get('player_state', {}),
            'environment': context.get('environment', {}),
            'combat_state': context.get('combat_state', {}),
            'threat_level': self._assess_threat(context)
        }

    def _get_action_outcome(self, action: str, context: Dict[str, any]) -> Dict[str, any]:
        """Get outcome of an action"""
        # This would be updated by the combat system after action execution
        return {
            'success': True,  # Placeholder
            'damage_dealt': 0,
            'effects_applied': [],
            'reactions_triggered': []
        }

    def _calculate_ultimate_value(self, context: Dict[str, any]) -> float:
        """Calculate strategic value of using ultimate ability"""
        if not self.abilities.ultimate_ability:
            return 0.0
        
        # Base value factors
        health_factor = 1.0 - self.combat_state['health_ratio']  # Lower health = higher value
        threat_factor = self._assess_threat(context)
        
        # Strategic factors
        allies_nearby = len(context.get('nearby_allies', []))
        enemies_nearby = len(context.get('nearby_enemies', []))
        strategic_position = self._evaluate_position(context)
        
        # Calculate final value
        value = (
            health_factor * 0.3 +
            threat_factor * 0.3 +
            (allies_nearby / (enemies_nearby + 1)) * 0.2 +
            strategic_position * 0.2
        )
        
        return min(1.0, value)

    def _evaluate_position(self, context: Dict[str, any]) -> float:
        """Evaluate strategic value of current position"""
        position = context.get('position', {})
        
        # Position factors
        elevation = position.get('elevation', 0) / 10  # Normalize to 0-1
        cover = position.get('cover', 0)  # 0-1
        mobility = position.get('mobility', 0)  # 0-1
        
        # Calculate position value
        return (elevation * 0.3 + cover * 0.4 + mobility * 0.3)

    def _move_suits_environment(self, move: str, environment: Dict[str, any]) -> bool:
        """Check if move is well-suited to environment"""
        # Example implementation - would need to be customized based on move properties
        weather = environment.get('weather', 'normal')
        terrain = environment.get('terrain', 'normal')
        
        # Move-specific checks would go here
        return True  # Placeholder

    def _move_exploits_vulnerability(self, move: str, target: Dict[str, any]) -> bool:
        """Check if move exploits target vulnerability"""
        # Example implementation - would need to be customized based on move properties
        vulnerabilities = target.get('vulnerabilities', [])
        resistances = target.get('resistances', [])
        
        # Move-specific checks would go here
        return True  # Placeholder

    def _move_has_tactical_advantage(self, move: str, position: Dict[str, any]) -> bool:
        """Check if move has tactical advantage from position"""
        # Example implementation - would need to be customized based on move properties
        elevation = position.get('elevation', 0)
        cover = position.get('cover', 0)
        
        # Move-specific checks would go here
        return True  # Placeholder

    def _transition_to_phase(self, enemy: Enemy, new_phase: str):
        """Handle enemy phase transition"""
        if new_phase not in enemy.phases.phases:
            return
        
        # Find transition
        transition = None
        for t in enemy.phases.transitions:
            if t['from'] == enemy.phases.current_phase and t['to'] == new_phase:
                transition = t
                break
        
        if not transition:
            return
        
        # Apply transition effects
        if 'effects' in transition:
            self._apply_transition_effects(enemy, transition['effects'])
        
        # Update phase
        enemy.phases.current_phase = new_phase
        enemy.phases.phase_start_time = time.time()
        
        # Update available abilities
        enemy.phases.current_abilities = enemy.phases.abilities_per_phase[new_phase]

    def _check_pattern_conditions(self, conditions: Dict[str, Any], enemy: Enemy, context: Dict[str, Any]) -> bool:
        """Check if pattern conditions are met"""
        for condition, value in conditions.items():
            if condition == 'health_above':
                if enemy.stats.health / enemy.stats.max_health <= value:
                    return False
            elif condition == 'health_below':
                if enemy.stats.health / enemy.stats.max_health >= value:
                    return False
            elif condition == 'allies_nearby':
                if not self._check_allies_nearby(enemy, context):
                    return False
            elif condition == 'enemies_nearby':
                if not self._check_enemies_nearby(enemy, value, context):
                    return False
            elif condition == 'has_status':
                if value not in enemy.current_status_effects:
                    return False
            elif condition == 'in_range':
                if not self._check_target_in_range(enemy, value, context):
                    return False
        return True

    def _check_trigger_conditions(self, conditions: Dict[str, Any], enemy: Enemy, context: Dict[str, Any]) -> bool:
        """Check if trigger conditions are met"""
        for condition, value in conditions.items():
            if condition == 'health_below':
                if enemy.stats.health / enemy.stats.max_health >= value:
                    return False
            elif condition == 'ally_health_below':
                if not self._check_ally_health_below(enemy, value, context):
                    return False
            elif condition == 'enemies_nearby':
                if not self._check_enemies_nearby(enemy, value, context):
                    return False
            elif condition == 'enemy_vulnerable':
                if not self._check_enemy_vulnerable(enemy, context):
                    return False
            elif condition == 'cooldown_ready':
                if not self._check_cooldown_ready(enemy, value):
                    return False
            elif condition == 'resource_available':
                if not self._check_resource_available(enemy, value):
                    return False
        return True

    def _process_trigger_response(self, enemy: Enemy, trigger: str, responses: List[str]):
        """Process trigger responses"""
        for response in responses:
            if response == 'use_healing_item':
                self._use_healing_item(enemy)
            elif response == 'retreat':
                self._initiate_retreat(enemy)
            elif response == 'protect_ally':
                self._protect_nearest_ally(enemy)
            elif response == 'heal_ally':
                self._heal_nearest_ally(enemy)
            elif response == 'area_attack':
                self._use_area_attack(enemy)
            elif response == 'escape':
                self._attempt_escape(enemy)
            elif response == 'use_special_move':
                self._use_special_move(enemy)
            elif response == 'coordinate_attack':
                self._coordinate_attack(enemy)
            elif response == 'enter_defensive_stance':
                self._enter_defensive_stance(enemy)
            elif response == 'call_for_reinforcements':
                self._call_for_reinforcements(enemy)

    def _apply_transition_effects(self, enemy: Enemy, effects: Dict[str, Any]):
        """Apply phase transition effects"""
        # Apply animation effect
        if 'animation' in effects:
            self.animation_system.play_animation(enemy.id, effects['animation'])
        
        # Play sound effect
        if 'sound' in effects:
            self.sound_system.play_sound(effects['sound'])
        
        # Create particle effect
        if 'particle_effect' in effects:
            self.particle_system.create_effect(enemy.position, effects['particle_effect'])
        
        # Apply stat modifiers
        if 'stat_modifiers' in effects:
            for stat, modifier in effects['stat_modifiers'].items():
                current_value = getattr(enemy.stats, stat)
                setattr(enemy.stats, stat, current_value * modifier)
        
        # Apply status effects
        if 'status_effects' in effects:
            for status in effects['status_effects']:
                self._apply_status_effect(enemy, status)
        
        # Trigger special abilities
        if 'trigger_ability' in effects:
            self._use_ability(enemy, effects['trigger_ability'])

    def _check_allies_nearby(self, enemy: Enemy, context: Dict[str, Any]) -> bool:
        """Check if allies are nearby"""
        allies = context.get('nearby_allies', [])
        return len(allies) > 0

    def _check_enemies_nearby(self, enemy: Enemy, count: int, context: Dict[str, Any]) -> bool:
        """Check if enough enemies are nearby"""
        enemies = context.get('nearby_enemies', [])
        return len(enemies) >= count

    def _check_ally_health_below(self, enemy: Enemy, threshold: float, context: Dict[str, Any]) -> bool:
        """Check if any ally's health is below threshold"""
        allies = context.get('nearby_allies', [])
        for ally in allies:
            if ally.stats.health / ally.stats.max_health < threshold:
                return True
        return False

    def _check_enemy_vulnerable(self, enemy: Enemy, context: Dict[str, Any]) -> bool:
        """Check if target enemy is vulnerable"""
        target = context.get('current_target')
        if not target:
            return False
        
        # Check for vulnerable status effects
        if hasattr(target, 'current_status_effects'):
            vulnerable_states = {'stunned', 'frozen', 'paralyzed', 'weakened'}
            if any(status in vulnerable_states for status in target.current_status_effects):
                return True
        
        # Check for low health
        if target.stats.health / target.stats.max_health < 0.2:
            return True
        
        # Check for defensive ability cooldowns
        if hasattr(target, 'ability_cooldowns'):
            defensive_abilities = {'shield', 'dodge', 'block', 'parry'}
            if all(target.ability_cooldowns.get(ability, 0) > 0 for ability in defensive_abilities):
                return True
        
        return False

    def _check_cooldown_ready(self, enemy: Enemy, ability: str) -> bool:
        """Check if an ability's cooldown is ready"""
        return enemy.ability_cooldowns.get(ability, 0) <= 0

    def _check_resource_available(self, enemy: Enemy, requirement: Dict[str, Any]) -> bool:
        """Check if required resources are available"""
        resource_type = requirement.get('type', 'energy')
        amount = requirement.get('amount', 0)
        
        current_amount = getattr(enemy.resources, resource_type, 0)
        return current_amount >= amount

    def _check_target_in_range(self, enemy: Enemy, range_requirement: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if target is within required range"""
        target = context.get('current_target')
        if not target:
            return False
        
        distance = self._calculate_distance(enemy.position, target.position)
        min_range = range_requirement.get('min', 0)
        max_range = range_requirement.get('max', float('inf'))
        
        return min_range <= distance <= max_range

    def _use_healing_item(self, enemy: Enemy):
        """Use a healing item"""
        if not hasattr(enemy, 'inventory') or not enemy.inventory.has_item('healing_potion'):
            return
        
        heal_amount = enemy.stats.max_health * 0.3
        enemy.stats.health = min(enemy.stats.max_health, enemy.stats.health + heal_amount)
        enemy.inventory.remove_item('healing_potion')
        
        # Create healing effect
        self.particle_system.create_effect(enemy.position, 'healing_sparkles')
        self.sound_system.play_sound('healing_chime')

    def _initiate_retreat(self, enemy: Enemy):
        """Initiate a tactical retreat"""
        # Find retreat position
        retreat_pos = self._find_safe_position(enemy)
        if not retreat_pos:
            return
        
        # Set movement target
        enemy.movement_target = retreat_pos
        enemy.current_action = 'retreating'
        
        # Apply retreat effects
        enemy.stats.speed *= 1.2  # Temporary speed boost
        self.particle_system.create_effect(enemy.position, 'dust_trail')

    def _protect_nearest_ally(self, enemy: Enemy):
        """Move to protect nearest ally"""
        ally = self._find_nearest_ally(enemy)
        if not ally:
            return
        
        # Calculate protection position
        protect_pos = self._calculate_protection_position(enemy, ally)
        
        # Move to position
        enemy.movement_target = protect_pos
        enemy.current_action = 'protecting'
        
        # Apply protection stance
        enemy.stats.defense *= 1.5
        self.particle_system.create_effect(enemy.position, 'protection_aura')

    def _heal_nearest_ally(self, enemy: Enemy):
        """Heal nearest ally"""
        ally = self._find_nearest_ally(enemy)
        if not ally or not hasattr(enemy, 'healing_power'):
            return
        
        heal_amount = enemy.healing_power * (1 + enemy.stats.intelligence * 0.2)
        ally.stats.health = min(ally.stats.max_health, ally.stats.health + heal_amount)
        
        # Create healing effects
        self.particle_system.create_effect(ally.position, 'healing_light')
        self.sound_system.play_sound('healing_spell')

    def _use_area_attack(self, enemy: Enemy):
        """Use area attack ability"""
        if not self._can_use_special_moves(enemy):
            return
        
        # Get nearby targets
        targets = self._get_nearby_targets(enemy, range=3)
        if not targets:
            return
        
        # Calculate damage
        base_damage = enemy.stats.damage * 0.8
        for target in targets:
            actual_damage = self._calculate_damage(enemy, target, base_damage)
            self._apply_damage(target, actual_damage)
        
        # Create attack effects
        self.particle_system.create_effect(enemy.position, 'area_attack_wave')
        self.sound_system.play_sound('area_attack')
        
        # Apply cooldown
        enemy.ability_cooldowns['area_attack'] = 3

    def _attempt_escape(self, enemy: Enemy):
        """Attempt to escape from combat"""
        if enemy.stats.health / enemy.stats.max_health < 0.2:
            escape_chance = 0.8
        else:
            escape_chance = 0.4
        
        if random.random() < escape_chance:
            enemy.current_action = 'escaped'
            self.particle_system.create_effect(enemy.position, 'smoke_screen')
            self.sound_system.play_sound('escape_poof')
            return True
        return False

    def _use_special_move(self, enemy: Enemy):
        """Use special move"""
        if not self._can_use_special_moves(enemy):
            return
        
        # Select best special move
        move = self._select_best_special_move(enemy)
        if not move:
            return
        
        # Use the move
        self._execute_special_move(enemy, move)

    def _coordinate_attack(self, enemy: Enemy):
        """Coordinate attack with allies"""
        allies = self._get_nearby_allies(enemy, range=5)
        if not allies:
            return
        
        # Signal attack
        for ally in allies:
            ally.combat_signals.append({
                'type': 'coordinate_attack',
                'target': enemy.current_target,
                'initiator': enemy.id
            })
        
        # Apply coordination bonus
        coordination_bonus = min(0.3, len(allies) * 0.1)
        for ally in allies + [enemy]:
            ally.stats.damage *= (1 + coordination_bonus)
        
        # Create coordination effect
        self.particle_system.create_effect(enemy.position, 'coordination_links', targets=[a.position for a in allies])

    def _enter_defensive_stance(self, enemy: Enemy):
        """Enter defensive stance"""
        enemy.current_stance = 'defensive'
        enemy.stats.defense *= 1.5
        enemy.stats.speed *= 0.8
        
        # Create defensive effect
        self.particle_system.create_effect(enemy.position, 'defense_shield')
        self.sound_system.play_sound('shield_up')

    def _call_for_reinforcements(self, enemy: Enemy):
        """Call for reinforcements"""
        if not hasattr(enemy, 'reinforcement_charges') or enemy.reinforcement_charges <= 0:
            return
        
        # Calculate spawn positions
        spawn_positions = self._find_reinforcement_positions(enemy)
        if not spawn_positions:
            return
        
        # Spawn reinforcements
        for pos in spawn_positions:
            reinforcement = self.spawn_enemy(
                enemy.core.faction + '_reinforcement',
                enemy.core.level - 2,
                {'position': pos}
            )
            reinforcement.loyalty_target = enemy.id
        
        enemy.reinforcement_charges -= 1
        
        # Create summoning effect
        self.particle_system.create_effect(enemy.position, 'summoning_circle')
        self.sound_system.play_sound('summoning_horn')

    def _execute_special_move(self, enemy: Enemy, move: str):
        """Execute a special move"""
        # Get move data
        move_data = enemy.abilities.special_moves_data[move]
        
        # Check requirements
        if not self._check_move_requirements(enemy, move_data):
            return
        
        # Apply costs
        self._apply_move_costs(enemy, move_data)
        
        # Execute move effects
        if move_data['type'] == 'attack':
            self._execute_attack_move(enemy, move_data)
        elif move_data['type'] == 'buff':
            self._execute_buff_move(enemy, move_data)
        elif move_data['type'] == 'debuff':
            self._execute_debuff_move(enemy, move_data)
        elif move_data['type'] == 'utility':
            self._execute_utility_move(enemy, move_data)
        
        # Apply cooldown
        enemy.ability_cooldowns[move] = move_data['cooldown']
        
        # Create move effects
        self.particle_system.create_effect(enemy.position, move_data['effect'])
        self.sound_system.play_sound(move_data['sound'])

    def _select_best_special_move(self, enemy: Enemy) -> Optional[str]:
        """Select the best special move to use"""
        available_moves = [
            move for move in enemy.abilities.special_moves
            if self._can_use_move(enemy, move)
        ]
        
        if not available_moves:
            return None
        
        # Score each move
        move_scores = {}
        for move in available_moves:
            base_score = self._get_move_base_score(move)
            context_mod = self._get_context_modifier(enemy, move)
            threat_mod = self._get_threat_modifier(enemy, move)
            memory_mod = self._get_memory_modifier(enemy, move)
            
            move_scores[move] = base_score * context_mod * threat_mod * memory_mod
        
        # Select highest scoring move
        return max(move_scores.items(), key=lambda x: x[1])[0]

    def _can_use_move(self, enemy: Enemy, move: str) -> bool:
        """Check if a move can be used"""
        # Check cooldown
        if enemy.ability_cooldowns.get(move, 0) > 0:
            return False
        
        # Check resources
        move_data = enemy.abilities.special_moves_data[move]
        if not self._check_resource_available(enemy, move_data['cost']):
            return False
        
        # Check conditions
        if move in enemy.abilities.conditional_moves:
            conditions = enemy.abilities.conditional_moves[move]
            if not self._check_move_conditions(enemy, conditions):
                return False
        
        return True

    def _check_move_conditions(self, enemy: Enemy, conditions: Dict[str, Any]) -> bool:
        """Check if move conditions are met"""
        for condition, value in conditions.items():
            if condition == 'min_health':
                if enemy.stats.health / enemy.stats.max_health < value:
                    return False
            elif condition == 'max_health':
                if enemy.stats.health / enemy.stats.max_health > value:
                    return False
            elif condition == 'min_targets':
                if len(self._get_nearby_targets(enemy)) < value:
                    return False
            elif condition == 'max_range':
                if not self._check_target_in_range(enemy, {'max': value}):
                    return False
        return True

    def _apply_move_costs(self, enemy: Enemy, move_data: Dict[str, Any]):
        """Apply move resource costs"""
        cost = move_data['cost']
        resource_type = cost.get('type', 'energy')
        amount = cost.get('amount', 0)
        
        current = getattr(enemy.resources, resource_type)
        setattr(enemy.resources, resource_type, current - amount)

    def _execute_attack_move(self, enemy: Enemy, move_data: Dict[str, Any]):
        """Execute an attack move"""
        targets = self._get_move_targets(enemy, move_data)
        
        for target in targets:
            base_damage = move_data['damage'] * enemy.stats.damage
            actual_damage = self._calculate_damage(enemy, target, base_damage)
            self._apply_damage(target, actual_damage)
            
            # Apply additional effects
            if 'effects' in move_data:
                for effect in move_data['effects']:
                    self._apply_status_effect(target, effect)

    def _execute_buff_move(self, enemy: Enemy, move_data: Dict[str, Any]):
        """Execute a buff move"""
        targets = self._get_move_targets(enemy, move_data)
        
        for target in targets:
            for stat, modifier in move_data['modifiers'].items():
                current = getattr(target.stats, stat)
                setattr(target.stats, stat, current * modifier)
            
            if 'duration' in move_data:
                target.active_buffs.append({
                    'move': move_data['id'],
                    'duration': move_data['duration'],
                    'modifiers': move_data['modifiers']
                })

    def _execute_debuff_move(self, enemy: Enemy, move_data: Dict[str, Any]):
        """Execute a debuff move"""
        targets = self._get_move_targets(enemy, move_data)
        
        for target in targets:
            if random.random() > target.stats.status_resistance:
                for stat, modifier in move_data['modifiers'].items():
                    current = getattr(target.stats, stat)
                    setattr(target.stats, stat, current * modifier)
                
                if 'duration' in move_data:
                    target.active_debuffs.append({
                        'move': move_data['id'],
                        'duration': move_data['duration'],
                        'modifiers': move_data['modifiers']
                    })

    def _execute_utility_move(self, enemy: Enemy, move_data: Dict[str, Any]):
        """Execute a utility move"""
        if move_data['utility_type'] == 'teleport':
            new_pos = self._calculate_teleport_position(enemy, move_data)
            if new_pos:
                enemy.position = new_pos
        elif move_data['utility_type'] == 'summon':
            self._execute_summon(enemy, move_data)
        elif move_data['utility_type'] == 'terrain':
            self._modify_terrain(enemy, move_data)
        elif move_data['utility_type'] == 'stealth':
            self._apply_stealth(enemy, move_data)

    def _find_safe_position(self, enemy: Enemy) -> Optional[tuple]:
        """Find a safe position to retreat to"""
        current_pos = enemy.position
        threats = self._get_nearby_threats(enemy)
        
        if not threats:
            return None
        
        # Calculate average threat position
        threat_x = sum(t.position[0] for t in threats) / len(threats)
        threat_y = sum(t.position[1] for t in threats) / len(threats)
        
        # Calculate direction away from threats
        dx = current_pos[0] - threat_x
        dy = current_pos[1] - threat_y
        
        # Normalize direction
        length = (dx * dx + dy * dy) ** 0.5
        if length == 0:
            return None
        
        dx /= length
        dy /= length
        
        # Try positions at increasing distances
        for distance in range(3, 8):
            new_x = int(current_pos[0] + dx * distance)
            new_y = int(current_pos[1] + dy * distance)
            
            if self._is_valid_position((new_x, new_y)):
                return (new_x, new_y)
        
        return None

    def _find_nearest_ally(self, enemy: Enemy) -> Optional[Enemy]:
        """Find the nearest ally"""
        allies = self._get_nearby_allies(enemy)
        if not allies:
            return None
        
        return min(allies, key=lambda a: self._calculate_distance(enemy.position, a.position))

    def _calculate_protection_position(self, enemy: 'Enemy', ally: 'Enemy') -> tuple:
        """Calculate best position to protect an ally"""
        ally_pos = ally.position
        threats = self._get_nearby_threats(ally)
        
        if not threats:
            # If no threats, stay close to ally
            return (ally_pos[0] + 1, ally_pos[1])
        
        # Calculate average threat position
        threat_x = sum(t.position[0] for t in threats) / len(threats)
        threat_y = sum(t.position[1] for t in threats) / len(threats)
        
        # Position between ally and threats
        dx = ally_pos[0] - threat_x
        dy = ally_pos[1] - threat_y
        
        # Normalize direction
        length = (dx * dx + dy * dy) ** 0.5
        if length == 0:
            return (ally_pos[0] + 1, ally_pos[1])
        
        dx /= length
        dy /= length
        
        # Position slightly in front of ally
        new_x = int(ally_pos[0] - dx * 2)
        new_y = int(ally_pos[1] - dy * 2)
        
        if self._is_valid_position((new_x, new_y)):
            return (new_x, new_y)
        else:
            return (ally_pos[0] + 1, ally_pos[1])

    def _find_reinforcement_positions(self, enemy: Enemy) -> List[tuple]:
        """Find positions to spawn reinforcements"""
        positions = []
        center = enemy.position
        
        # Try positions in a circle around the enemy
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            dx = int(math.cos(rad) * 3)
            dy = int(math.sin(rad) * 3)
            
            pos = (center[0] + dx, center[1] + dy)
            if self._is_valid_position(pos):
                positions.append(pos)
        
        return positions[:3]  # Limit to 3 reinforcements

    def _calculate_teleport_position(self, enemy: Enemy, move_data: Dict[str, Any]) -> Optional[tuple]:
        """Calculate position to teleport to"""
        if move_data.get('teleport_type') == 'retreat':
            return self._find_safe_position(enemy)
        elif move_data.get('teleport_type') == 'aggressive':
            target = enemy.current_target
            if not target:
                return None
            
            # Try to teleport behind target
            target_pos = target.position
            facing = target.facing if hasattr(target, 'facing') else (0, 1)
            
            new_x = target_pos[0] - facing[0] * 2
            new_y = target_pos[1] - facing[1] * 2
            
            if self._is_valid_position((new_x, new_y)):
                return (new_x, new_y)
        
        return None

    def _get_move_targets(self, enemy: Enemy, move_data: Dict[str, Any]) -> List[Enemy]:
        """Get valid targets for a move"""
        target_type = move_data.get('target_type', 'enemy')
        max_targets = move_data.get('max_targets', 1)
        range_val = move_data.get('range', 1)
        
        if target_type == 'enemy':
            targets = self._get_nearby_targets(enemy, range=range_val)
        elif target_type == 'ally':
            targets = self._get_nearby_allies(enemy, range=range_val)
        elif target_type == 'self':
            return [enemy]
        else:
            return []
        
        # Sort by priority if specified
        if 'target_priority' in move_data:
            targets = self._sort_targets_by_priority(targets, move_data['target_priority'])
        
        return targets[:max_targets]

    def _sort_targets_by_priority(self, targets: List[Enemy], priority: str) -> List[Enemy]:
        """Sort targets based on priority"""
        if priority == 'lowest_health':
            return sorted(targets, key=lambda t: t.stats.health / t.stats.max_health)
        elif priority == 'highest_health':
            return sorted(targets, key=lambda t: t.stats.health / t.stats.max_health, reverse=True)
        elif priority == 'lowest_defense':
            return sorted(targets, key=lambda t: t.stats.defense)
        elif priority == 'highest_threat':
            return sorted(targets, key=lambda t: self._calculate_threat_level(t), reverse=True)
        elif priority == 'nearest':
            return sorted(targets, key=lambda t: self._calculate_distance(t.position, targets[0].position))
        else:
            return targets

    def _calculate_threat_level(self, target: Enemy) -> float:
        """Calculate threat level of a target"""
        # Base threat from stats
        stat_threat = (
            target.stats.damage * 0.4 +
            target.stats.health / target.stats.max_health * 0.3 +
            target.stats.speed * 0.2 +
            target.stats.defense * 0.1
        )
        
        # Additional threat from abilities
        ability_threat = len(target.abilities.special_moves) * 0.1
        if target.abilities.ultimate_ability:
            ability_threat += 0.2
        
        # Threat from behavior
        behavior_threat = (
            target.behavior.aggression * 0.4 +
            target.behavior.intelligence * 0.4 +
            target.behavior.cooperation * 0.2
        )
        
        return stat_threat + ability_threat + behavior_threat

    def _calculate_distance(self, pos1: tuple, pos2: tuple) -> float:
        """Calculate distance between two positions"""
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def _is_valid_position(self, position: tuple) -> bool:
        """Check if a position is valid"""
        x, y = position
        
        # Check map boundaries
        if not (0 <= x < self.map_width and 0 <= y < self.map_height):
            return False
        
        # Check terrain
        terrain = self.world_system.get_terrain_at(position)
        if terrain in {'wall', 'water', 'lava'}:
            return False
        
        # Check for other entities
        if self.world_system.is_position_occupied(position):
            return False
        
        return True

    def _get_nearby_threats(self, enemy: Enemy, range: int = 5) -> List[Enemy]:
        """Get nearby threats"""
        threats = []
        
        for other in self.world_system.get_nearby_entities(enemy.position, range):
            if (isinstance(other, Enemy) and 
                other.core.faction != enemy.core.faction and
                self._calculate_threat_level(other) > 0):
                threats.append(other)
        
        return threats

    def _get_nearby_allies(self, enemy: Enemy, range: int = 5) -> List[Enemy]:
        """Get nearby allies"""
        allies = []
        
        for other in self.world_system.get_nearby_entities(enemy.position, range):
            if (isinstance(other, Enemy) and 
                other.core.faction == enemy.core.faction and
                other != enemy):
                allies.append(other)
        
        return allies

    def _get_nearby_targets(self, enemy: Enemy, range: int = 5) -> List[Enemy]:
        """Get nearby valid targets"""
        targets = []
        
        for other in self.world_system.get_nearby_entities(enemy.position, range):
            if (isinstance(other, Enemy) and 
                other.core.faction != enemy.core.faction and
                not other.current_action == 'escaped'):
                targets.append(other)
        
        return targets

    def _calculate_damage(self, attacker: Enemy, target: Enemy, base_damage: float) -> float:
        """Calculate actual damage after modifiers"""
        # Apply attacker's modifiers
        damage = base_damage * (1 + attacker.stats.damage_modifier if hasattr(attacker.stats, 'damage_modifier') else 1.0)
        
        # Critical hit
        if random.random() < attacker.stats.critical_rate:
            damage *= 2
        
        # Apply target's defense
        damage *= (100 / (100 + target.stats.defense))
        
        # Apply resistance
        damage *= (1 - target.stats.resistance)
        
        # Random variation (±10%)
        damage *= random.uniform(0.9, 1.1)
        
        return max(1, damage)  # Minimum 1 damage

    def _apply_damage(self, target: Enemy, damage: float):
        """Apply damage to target"""
        # Check for dodge
        if random.random() < target.stats.dodge_chance:
            self.particle_system.create_effect(target.position, 'dodge')
            self.sound_system.play_sound('dodge')
            return
        
        # Apply damage
        target.stats.health -= damage
        
        # Create hit effect
        self.particle_system.create_effect(target.position, 'hit')
        self.sound_system.play_sound('hit')
        
        # Check for defeat
        if target.stats.health <= 0:
            self._handle_defeat(target)

    def _handle_defeat(self, enemy: Enemy):
        """Handle enemy defeat"""
        enemy.current_action = 'defeated'
        
        # Create defeat effect
        self.particle_system.create_effect(enemy.position, 'defeat')
        self.sound_system.play_sound('defeat')
        
        # Drop loot if applicable
        if hasattr(enemy, 'loot_table'):
            self._generate_loot(enemy)
        
        # Trigger defeat responses
        self._trigger_defeat_responses(enemy)
        
        # Remove from world
        self.world_system.remove_entity(enemy)

    def _generate_loot(self, enemy: Enemy):
        """Generate and drop loot"""
        if not enemy.loot_table:
            return
        
        # Calculate loot quality modifier
        quality_mod = 1.0
        if enemy.core.type == EnemyType.ELITE:
            quality_mod = 1.5
        elif enemy.core.type == EnemyType.BOSS:
            quality_mod = 2.0
        
        # Roll for each loot entry
        dropped_items = []
        for entry in enemy.loot_table:
            if random.random() < entry['chance']:
                item = self._generate_loot_item(entry, quality_mod)
                if item:
                    dropped_items.append(item)
        
        # Create loot container
        if dropped_items:
            self.world_system.create_loot_container(enemy.position, dropped_items)

    def _generate_loot_item(self, loot_entry: Dict[str, Any], quality_mod: float) -> Optional[Dict[str, Any]]:
        """Generate a specific loot item"""
        item_type = loot_entry['type']
        
        if item_type == 'weapon':
            return self._generate_weapon(loot_entry, quality_mod)
        elif item_type == 'armor':
            return self._generate_armor(loot_entry, quality_mod)
        elif item_type == 'consumable':
            return self._generate_consumable(loot_entry, quality_mod)
        elif item_type == 'material':
            return self._generate_material(loot_entry, quality_mod)
        
        return None

    def _generate_weapon(self, loot_entry: Dict[str, Any], quality_mod: float) -> Dict[str, Any]:
        """Generate a weapon item"""
        weapon_type = loot_entry.get('weapon_type', random.choice(['sword', 'axe', 'spear', 'bow']))
        rarity = self._determine_rarity(loot_entry, quality_mod)
        
        # Base stats
        base_stats = {
            'sword': {'damage': 10, 'speed': 1.2, 'critical_rate': 0.1},
            'axe': {'damage': 15, 'speed': 0.8, 'critical_rate': 0.05},
            'spear': {'damage': 12, 'speed': 1.0, 'critical_rate': 0.08},
            'bow': {'damage': 8, 'speed': 1.5, 'critical_rate': 0.15}
        }[weapon_type]
        
        # Apply rarity modifiers
        rarity_mods = {
            'common': 1.0,
            'uncommon': 1.2,
            'rare': 1.5,
            'epic': 2.0,
            'legendary': 3.0
        }
        
        stats = {
            stat: value * rarity_mods[rarity] * quality_mod
            for stat, value in base_stats.items()
        }
        
        return {
            'type': 'weapon',
            'weapon_type': weapon_type,
            'name': f"{rarity.capitalize()} {weapon_type.capitalize()}",
            'rarity': rarity,
            'stats': stats,
            'level': loot_entry.get('level', 1)
        }

    def _generate_armor(self, loot_entry: Dict[str, Any], quality_mod: float) -> Dict[str, Any]:
        """Generate an armor item"""
        armor_type = loot_entry.get('armor_type', random.choice(['light', 'medium', 'heavy']))
        rarity = self._determine_rarity(loot_entry, quality_mod)
        
        # Base stats
        base_stats = {
            'light': {'defense': 5, 'resistance': 8, 'speed_mod': 1.1},
            'medium': {'defense': 8, 'resistance': 5, 'speed_mod': 1.0},
            'heavy': {'defense': 12, 'resistance': 3, 'speed_mod': 0.9}
        }[armor_type]
        
        # Apply rarity modifiers
        rarity_mods = {
            'common': 1.0,
            'uncommon': 1.2,
            'rare': 1.5,
            'epic': 2.0,
            'legendary': 3.0
        }
        
        stats = {
            stat: value * rarity_mods[rarity] * quality_mod
            for stat, value in base_stats.items()
        }
        
        return {
            'type': 'armor',
            'armor_type': armor_type,
            'name': f"{rarity.capitalize()} {armor_type.capitalize()} Armor",
            'rarity': rarity,
            'stats': stats,
            'level': loot_entry.get('level', 1)
        }

    def _generate_consumable(self, loot_entry: Dict[str, Any], quality_mod: float) -> Dict[str, Any]:
        """Generate a consumable item"""
        consumable_type = loot_entry.get('consumable_type', random.choice(['potion', 'scroll', 'food']))
        rarity = self._determine_rarity(loot_entry, quality_mod)
        
        # Base effects
        base_effects = {
            'potion': {'type': 'heal', 'value': 50},
            'scroll': {'type': 'buff', 'stat': 'damage', 'value': 1.5, 'duration': 60},
            'food': {'type': 'heal_over_time', 'value': 5, 'duration': 10}
        }[consumable_type]
        
        # Apply rarity modifier
        rarity_mods = {
            'common': 1.0,
            'uncommon': 1.2,
            'rare': 1.5,
            'epic': 2.0,
            'legendary': 3.0
        }
        
        effect = base_effects.copy()
        if 'value' in effect:
            effect['value'] *= rarity_mods[rarity] * quality_mod
        
        return {
            'type': 'consumable',
            'consumable_type': consumable_type,
            'name': f"{rarity.capitalize()} {consumable_type.capitalize()}",
            'rarity': rarity,
            'effect': effect,
            'stack_size': loot_entry.get('stack_size', 1)
        }

    def _generate_material(self, loot_entry: Dict[str, Any], quality_mod: float) -> Dict[str, Any]:
        """Generate a material item"""
        material_type = loot_entry.get('material_type', random.choice(['ore', 'herb', 'crystal']))
        rarity = self._determine_rarity(loot_entry, quality_mod)
        
        # Base properties
        base_properties = {
            'ore': {'crafting_value': 10, 'uses': ['weapon', 'armor']},
            'herb': {'crafting_value': 8, 'uses': ['potion', 'food']},
            'crystal': {'crafting_value': 15, 'uses': ['scroll', 'enchanting']}
        }[material_type]
        
        # Apply rarity modifier
        rarity_mods = {
            'common': 1.0,
            'uncommon': 1.2,
            'rare': 1.5,
            'epic': 2.0,
            'legendary': 3.0
        }
        
        properties = base_properties.copy()
        properties['crafting_value'] *= rarity_mods[rarity] * quality_mod
        
        return {
            'type': 'material',
            'material_type': material_type,
            'name': f"{rarity.capitalize()} {material_type.capitalize()}",
            'rarity': rarity,
            'properties': properties,
            'stack_size': loot_entry.get('stack_size', 1)
        }

    def _determine_rarity(self, loot_entry: Dict[str, Any], quality_mod: float) -> str:
        """Determine item rarity"""
        base_chances = {
            'legendary': 0.01,
            'epic': 0.05,
            'rare': 0.15,
            'uncommon': 0.30,
            'common': 0.49
        }
        
        # Apply quality modifier
        chances = {
            rarity: chance * quality_mod
            for rarity, chance in base_chances.items()
        }
        
        # Normalize chances
        total = sum(chances.values())
        chances = {
            rarity: chance / total
            for rarity, chance in chances.items()
        }
        
        # Roll for rarity
        roll = random.random()
        cumulative = 0
        
        for rarity, chance in chances.items():
            cumulative += chance
            if roll <= cumulative:
                return rarity
        
        return 'common'  # Fallback

    def _generate_weapon_effects(self, weapon_type: str, rarity: str) -> List[Dict[str, Any]]:
        """Generate weapon special effects"""
        effects = []
        effect_count = {
            'common': 0,
            'uncommon': 1,
            'rare': 2,
            'epic': 3,
            'legendary': 4
        }[rarity]
        
        possible_effects = {
            'sword': [
                {'type': 'bleed', 'chance': 0.2, 'damage': 5, 'duration': 3},
                {'type': 'critical_boost', 'value': 1.2},
                {'type': 'speed_boost', 'value': 1.1},
                {'type': 'lifesteal', 'value': 0.05}
            ],
            'axe': [
                {'type': 'stun', 'chance': 0.1, 'duration': 1},
                {'type': 'armor_break', 'value': 0.9},
                {'type': 'cleave', 'damage_ratio': 0.5},
                {'type': 'execution', 'threshold': 0.2}
            ],
            'spear': [
                {'type': 'pierce', 'value': 0.2},
                {'type': 'reach', 'value': 1},
                {'type': 'cripple', 'chance': 0.15, 'slow': 0.3},
                {'type': 'combo_boost', 'value': 1.2}
            ],
            'bow': [
                {'type': 'headshot', 'chance': 0.1, 'multiplier': 2.0},
                {'type': 'mark', 'duration': 5, 'bonus': 1.3},
                {'type': 'multishot', 'count': 2, 'damage_ratio': 0.7},
                {'type': 'range_boost', 'value': 2}
            ]
        }[weapon_type]
        
        selected = random.sample(possible_effects, min(effect_count, len(possible_effects)))
        for effect in selected:
            effects.append(effect)
        
        return effects

    def _generate_armor_effects(self, armor_type: str, rarity: str) -> List[Dict[str, Any]]:
        """Generate armor special effects"""
        effects = []
        effect_count = {
            'common': 0,
            'uncommon': 1,
            'rare': 2,
            'epic': 3,
            'legendary': 4
        }[rarity]
        
        possible_effects = {
            'light': [
                {'type': 'dodge_boost', 'value': 0.1},
                {'type': 'speed_boost', 'value': 1.1},
                {'type': 'stealth_boost', 'value': 1.2},
                {'type': 'energy_regen', 'value': 2}
            ],
            'medium': [
                {'type': 'balanced_protection', 'value': 1.15},
                {'type': 'status_resistance', 'value': 0.2},
                {'type': 'stamina_boost', 'value': 1.2},
                {'type': 'versatility', 'value': 1.1}
            ],
            'heavy': [
                {'type': 'damage_reduction', 'value': 0.15},
                {'type': 'stun_resistance', 'value': 0.3},
                {'type': 'thorns', 'value': 0.1},
                {'type': 'health_boost', 'value': 1.2}
            ]
        }[armor_type]
        
        selected = random.sample(possible_effects, min(effect_count, len(possible_effects)))
        for effect in selected:
            effects.append(effect)
        
        return effects

    def _generate_consumable_effects(self, consumable_type: str, rarity: str) -> Dict[str, Any]:
        """Generate consumable effects"""
        base_effects = {
            'potion': {
                'health': {'type': 'heal', 'value': 50},
                'mana': {'type': 'restore_mana', 'value': 50},
                'strength': {'type': 'buff', 'stat': 'damage', 'value': 1.5, 'duration': 60}
            },
            'scroll': {
                'teleport': {'type': 'teleport', 'range': 10},
                'shield': {'type': 'buff', 'stat': 'defense', 'value': 2.0, 'duration': 30},
                'fireball': {'type': 'damage', 'value': 100, 'area': 3}
            },
            'food': {
                'bread': {'type': 'heal', 'value': 20, 'duration': 10},
                'meat': {'type': 'buff', 'stat': 'health_regen', 'value': 2, 'duration': 300},
                'fruit': {'type': 'buff', 'stat': 'energy_regen', 'value': 2, 'duration': 300}
            }
        }[consumable_type]
        
        # Select random effect type
        effect_type = random.choice(list(base_effects.keys()))
        effect = base_effects[effect_type].copy()
        
        # Apply rarity modifiers
        rarity_mods = {
            'common': 1.0,
            'uncommon': 1.2,
            'rare': 1.5,
            'epic': 2.0,
            'legendary': 3.0
        }
        
        if 'value' in effect:
            effect['value'] *= rarity_mods[rarity]
        if 'duration' in effect:
            effect['duration'] = int(effect['duration'] * rarity_mods[rarity])
        
        return effect

    def _generate_material_properties(self, material_type: str, rarity: str) -> Dict[str, Any]:
        """Generate material properties"""
        base_properties = {
            'ore': {
                'crafting_value': 10,
                'uses': ['weapon', 'armor'],
                'quality': 1.0,
                'special_properties': []
            },
            'herb': {
                'crafting_value': 8,
                'uses': ['potion', 'food'],
                'quality': 1.0,
                'special_properties': []
            },
            'crystal': {
                'crafting_value': 15,
                'uses': ['scroll', 'enchanting'],
                'quality': 1.0,
                'special_properties': []
            }
        }[material_type]
        
        # Apply rarity modifiers
        rarity_mods = {
            'common': 1.0,
            'uncommon': 1.2,
            'rare': 1.5,
            'epic': 2.0,
            'legendary': 3.0
        }
        
        properties = base_properties.copy()
        properties['crafting_value'] *= rarity_mods[rarity]
        properties['quality'] *= rarity_mods[rarity]
        
        # Add special properties based on rarity
        special_properties = {
            'ore': ['pure', 'magnetic', 'lightweight', 'durable'],
            'herb': ['potent', 'preserved', 'aromatic', 'magical'],
            'crystal': ['resonating', 'clear', 'energized', 'perfect']
        }[material_type]
        
        num_properties = {
            'common': 0,
            'uncommon': 1,
            'rare': 2,
            'epic': 3,
            'legendary': 4
        }[rarity]
        
        if num_properties > 0:
            properties['special_properties'] = random.sample(special_properties, min(num_properties, len(special_properties)))
        
        return properties

class SystemIntegrationHandlers:
    """Handles integration between enemy system and other core systems"""
    def __init__(self, enemy_system: 'EnemySystem'):
        self.enemy_system = enemy_system
        self.event_handlers = {}
        self.combat_handlers = {}
        self.world_handlers = {}
        self.faction_handlers = {}
        self._initialize_handlers()

    def _initialize_handlers(self):
        """Initialize all system integration handlers"""
        self._setup_event_handlers()
        self._setup_combat_handlers()
        self._setup_world_handlers()
        self._setup_faction_handlers()

    def _setup_event_handlers(self):
        """Setup event system integration"""
        self.event_handlers.update({
            'on_enemy_spawn': self._handle_enemy_spawn_event,
            'on_enemy_defeat': self._handle_enemy_defeat_event,
            'on_enemy_phase_change': self._handle_enemy_phase_change,
            'on_enemy_status_change': self._handle_enemy_status_change,
            'on_enemy_ability_use': self._handle_enemy_ability_use
        })

    def _setup_combat_handlers(self):
        """Setup combat system integration"""
        self.combat_handlers.update({
            'calculate_damage': self._handle_damage_calculation,
            'process_ability': self._handle_ability_processing,
            'apply_status_effect': self._handle_status_effect,
            'check_combat_conditions': self._handle_combat_conditions,
            'update_combat_state': self._handle_combat_state_update
        })

    def _setup_world_handlers(self):
        """Setup world system integration"""
        self.world_handlers.update({
            'check_position': self._handle_position_check,
            'update_environment': self._handle_environment_update,
            'spawn_loot': self._handle_loot_spawn,
            'process_interaction': self._handle_world_interaction,
            'update_visibility': self._handle_visibility_update
        })

    def _setup_faction_handlers(self):
        """Setup faction system integration"""
        self.faction_handlers.update({
            'check_relations': self._handle_faction_relations,
            'update_standing': self._handle_faction_standing,
            'process_faction_event': self._handle_faction_event,
            'get_faction_modifiers': self._handle_faction_modifiers,
            'apply_faction_effects': self._handle_faction_effects
        })

    # Event System Handlers
    def _handle_enemy_spawn_event(self, enemy: Enemy, context: Dict[str, Any]):
        """Handle enemy spawn event"""
        if self.enemy_system.event_system:
            event_data = {
                'event_type': 'enemy_spawn',
                'enemy_id': enemy.core.id,
                'enemy_type': enemy.core.type.value,
                'location': context.get('location'),
                'level': enemy.core.level,
                'faction': enemy.core.faction
            }
            self.enemy_system.event_system.trigger_event(event_data)

    def _handle_enemy_defeat_event(self, enemy: Enemy, context: Dict[str, Any]):
        """Handle enemy defeat event"""
        if self.enemy_system.event_system:
            event_data = {
                'event_type': 'enemy_defeat',
                'enemy_id': enemy.core.id,
                'location': context.get('location'),
                'defeat_type': context.get('defeat_type', 'normal'),
                'rewards': self._calculate_defeat_rewards(enemy)
            }
            self.enemy_system.event_system.trigger_event(event_data)

    def _handle_enemy_phase_change(self, enemy: Enemy, new_phase: str):
        """Handle enemy phase change event"""
        if self.enemy_system.event_system:
            event_data = {
                'event_type': 'phase_change',
                'enemy_id': enemy.core.id,
                'old_phase': enemy.phases.current_phase,
                'new_phase': new_phase,
                'trigger_conditions': enemy.phases.phase_conditions.get(new_phase, {})
            }
            self.enemy_system.event_system.trigger_event(event_data)

    # Combat System Handlers
    def _handle_damage_calculation(self, attacker: Enemy, target: Any, base_damage: float) -> float:
        """Handle damage calculation through combat system"""
        if self.enemy_system.combat_system:
            return self.enemy_system.combat_system.calculate_damage(
                attacker=attacker,
                target=target,
                base_damage=base_damage,
                damage_type='enemy',
                modifiers=self._get_damage_modifiers(attacker)
            )
        return base_damage

    def _handle_ability_processing(self, enemy: Enemy, ability: Dict[str, Any], targets: List[Any]):
        """Handle ability processing through combat system"""
        if self.enemy_system.combat_system:
            return self.enemy_system.combat_system.process_ability(
                source=enemy,
                ability=ability,
                targets=targets,
                context=self._get_ability_context(enemy, ability)
            )

    def _handle_status_effect(self, target: Any, effect: Dict[str, Any], source: Enemy):
        """Handle status effect application through combat system"""
        if self.enemy_system.combat_system:
            return self.enemy_system.combat_system.apply_status_effect(
                target=target,
                effect=effect,
                source=source,
                duration=effect.get('duration', 0)
            )

    # World System Handlers
    def _handle_position_check(self, position: tuple) -> bool:
        """Handle position validation through world system"""
        if self.enemy_system.world_system:
            return self.enemy_system.world_system.is_valid_position(
                position=position,
                entity_type='enemy',
                check_collision=True
            )
        return True

    def _handle_environment_update(self, enemy: Enemy, context: Dict[str, Any]):
        """Handle environment updates through world system"""
        if self.enemy_system.world_system:
            environment_data = self.enemy_system.world_system.get_environment_data(
                position=enemy.position,
                entity_type='enemy'
            )
            self._apply_environment_effects(enemy, environment_data)

    def _handle_loot_spawn(self, position: tuple, loot: List[Dict[str, Any]]):
        """Handle loot spawning through world system"""
        if self.enemy_system.world_system:
            self.enemy_system.world_system.spawn_loot(
                position=position,
                loot=loot,
                source_type='enemy'
            )

    # Faction System Handlers
    def _handle_faction_relations(self, enemy: Enemy, target_faction: str) -> float:
        """Handle faction relation checks"""
        if self.enemy_system.faction_system:
            return self.enemy_system.faction_system.get_faction_relation(
                faction1=enemy.core.faction,
                faction2=target_faction
            )
        return 0.0

    def _handle_faction_standing(self, enemy: Enemy, action: str, target_faction: str):
        """Handle faction standing updates"""
        if self.enemy_system.faction_system:
            self.enemy_system.faction_system.update_faction_standing(
                faction=enemy.core.faction,
                action=action,
                target_faction=target_faction,
                context={'enemy_type': enemy.core.type.value}
            )

    def _handle_faction_modifiers(self, enemy: Enemy) -> Dict[str, float]:
        """Get faction-based modifiers"""
        if self.enemy_system.faction_system:
            return self.enemy_system.faction_system.get_faction_modifiers(
                faction=enemy.core.faction,
                context={'enemy_type': enemy.core.type.value}
            )
        return {}

    # Helper Methods
    def _calculate_defeat_rewards(self, enemy: Enemy) -> Dict[str, Any]:
        """Calculate rewards for defeating an enemy"""
        return {
            'experience': self._calculate_experience_reward(enemy),
            'loot': self._generate_loot_table(enemy),
            'faction_reputation': self._calculate_faction_reputation(enemy)
        }

    def _get_damage_modifiers(self, enemy: Enemy) -> Dict[str, float]:
        """Get all applicable damage modifiers"""
        modifiers = {
            'base': 1.0,
            'level': 1.0 + (enemy.core.level * 0.1),
            'type': self._get_type_modifier(enemy)
        }
        
        # Add faction modifiers
        faction_mods = self._handle_faction_modifiers(enemy)
        modifiers.update(faction_mods)
        
        return modifiers

    def _get_ability_context(self, enemy: Enemy, ability: Dict[str, Any]) -> Dict[str, Any]:
        """Get context for ability processing"""
        return {
            'source_type': 'enemy',
            'enemy_level': enemy.core.level,
            'enemy_type': enemy.core.type.value,
            'ability_type': ability.get('type', 'normal'),
            'modifiers': self._get_damage_modifiers(enemy)
        }

    def _apply_environment_effects(self, enemy: Enemy, environment_data: Dict[str, Any]):
        """Apply environment effects to enemy"""
        for effect, value in environment_data.items():
            if effect == 'damage_modifier':
                enemy.stats.damage *= value
            elif effect == 'defense_modifier':
                enemy.stats.defense *= value
            elif effect == 'speed_modifier':
                enemy.stats.speed *= value

    def _get_type_modifier(self, enemy: Enemy) -> float:
        """Get damage modifier based on enemy type"""
        type_modifiers = {
            'NORMAL': 1.0,
            'ELITE': 1.2,
            'BOSS': 1.5,
            'LEGENDARY': 2.0,
            'MYTHICAL': 2.5,
            'COSMIC': 3.0
        }
        return type_modifiers.get(enemy.core.type.value, 1.0)

class EnemySystem:
    """Main system for managing enemies"""
    def __init__(
        self,
        combat_system: 'CombatSystem',
        world_system: 'WorldSystem',
        event_system: 'EventSystem',
        faction_system: 'FactionSystem'
    ):
        self.combat_system = combat_system
        self.world_system = world_system
        self.event_system = event_system
        self.faction_system = faction_system
        
        self.enemies: Dict[str, Enemy] = {}
        self.templates: Dict[str, Dict[str, any]] = {}
        self.spawn_rules: Dict[str, Dict[str, any]] = {}
        self.balance_metrics: Dict[str, Dict[str, float]] = {}
        
        # Initialize system integration handlers
        self.system_handlers = SystemIntegrationHandlers(self)
        self._initialize_systems()

    def _initialize_systems(self):
        """Initialize core systems"""
        self._load_templates()
        self._setup_spawn_rules()
        self._initialize_balance_metrics()
        self._setup_event_handlers()

    def create_enemy(self, template_id: str, level: int, context: Dict[str, Any] = None) -> Enemy:
        """Create a new enemy instance"""
        if context is None:
            context = {}
        
        # Get template
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Unknown enemy template: {template_id}")
        
        # Add level to context
        context['level'] = level
        
        # Create enemy components
        core = self._create_core(template, level)
        stats = self._create_stats(template, context)
        abilities = self._create_abilities(template, context)
        behavior = self._create_behavior(template, context)
        phases = self._create_phases(template)
        scaling = self._create_scaling(template, context)
        interaction = self._create_interaction(template, context)
        
        # Create enemy instance
        enemy = Enemy(
            core=core,
            stats=stats,
            abilities=abilities,
            behavior=behavior,
            phases=phases,
            scaling=scaling,
            interaction=interaction
        )
        
        # Calculate initial metrics
        metrics = {
            'power_rating': self._calculate_power_rating(enemy),
            'challenge_rating': self._calculate_challenge_rating(enemy, context),
            'engagement_score': self._calculate_engagement_score(enemy, context),
            'fairness_rating': self._calculate_fairness_rating(enemy, context)
        }
        
        # Apply balance adjustments if needed
        adjustments = self._calculate_adjustments(metrics)
        if adjustments:
            self._apply_stat_adjustments(enemy, adjustments)
            self._apply_behavior_adjustments(enemy, adjustments)
            self._apply_scaling_adjustments(enemy, adjustments)
        
        return enemy

    def spawn_enemy(self, location: str, player_level: int, context: Dict[str, Any] = None) -> Enemy:
        """Spawn an appropriate enemy for the given location"""
        if context is None:
            context = {}
        
        # Get spawn rules for location
        spawn_rules = self.spawn_rules.get(location)
        if not spawn_rules:
            raise ValueError(f"No spawn rules for location: {location}")
        
        # Check level range
        min_level, max_level = spawn_rules['level_range']
        if not min_level <= player_level <= max_level:
            player_level = max(min_level, min(max_level, player_level))
        
        # Apply time modifiers
        time_of_day = context.get('time_of_day')
        spawn_weights = spawn_rules['spawn_weights'].copy()
        if time_of_day and 'time_modifiers' in spawn_rules:
            time_mods = spawn_rules['time_modifiers'].get(time_of_day, {})
            for template_id, modifier in time_mods.items():
                if template_id in spawn_weights:
                    spawn_weights[template_id] *= modifier
        
        # Apply environment modifiers
        environment = context.get('environment', {})
        if environment and 'environment_modifiers' in spawn_rules:
            for env_condition, mods in spawn_rules['environment_modifiers'].items():
                if environment.get(env_condition):
                    for template_id, modifier in mods.items():
                        if template_id in spawn_weights:
                            spawn_weights[template_id] *= modifier
        
        # Select template based on weights
        total_weight = sum(spawn_weights.values())
        roll = random.uniform(0, total_weight)
        current_weight = 0
        selected_template = None
        
        for template_id, weight in spawn_weights.items():
            current_weight += weight
            if roll <= current_weight:
                selected_template = template_id
                break
        
        # Create enemy
        return self.create_enemy(selected_template, player_level, context)

    def update_enemy(self, enemy: Enemy, context: Dict[str, Any]):
        """Update enemy state based on context"""
        # Process system interactions
        self._process_faction_interactions(enemy, context)
        self._process_world_interactions(enemy, context)
        self._process_event_interactions(enemy, context)
        
        # Update phase if needed
        if enemy.phases:
            current_health_ratio = enemy.stats.health / enemy.stats.max_health
            for phase, conditions in enemy.phases.phase_conditions.items():
                if (conditions['health'] >= current_health_ratio and 
                    phase != enemy.phases.current_phase):
                    self._transition_to_phase(enemy, phase)
        
        # Update behavior patterns
        active_pattern = None
        max_priority = -1
        
        for pattern in enemy.behavior.patterns:
            if self._check_pattern_conditions(pattern['conditions'], enemy, context):
                if pattern['priority'] > max_priority:
                    max_priority = pattern['priority']
                    active_pattern = pattern
        
        if active_pattern:
            enemy.behavior.current_pattern = active_pattern
        
        # Check and process triggers
        for trigger_name, trigger_data in enemy.behavior.triggers.items():
            if self._check_trigger_conditions(trigger_data['condition'], enemy, context):
                self._process_trigger_response(enemy, trigger_name, trigger_data['response'])
        
        # Update stats based on current state
        self._update_stats_for_state(enemy)

    def get_enemy_info(self, enemy: Enemy) -> Dict[str, Any]:
        """Get detailed information about an enemy"""
        return {
            'id': enemy.core.id,
            'name': enemy.core.name,
            'type': enemy.core.type.value,
            'level': enemy.core.level,
            'rank': enemy.core.rank,
            'faction': enemy.core.faction,
            'lore': enemy.core.lore,
            'stats': {
                'health': enemy.stats.health,
                'max_health': enemy.stats.max_health,
                'damage': enemy.stats.damage,
                'defense': enemy.stats.defense,
                'speed': enemy.stats.speed
            },
            'abilities': {
                'basic_attacks': enemy.abilities.basic_attacks,
                'special_moves': enemy.abilities.special_moves,
                'ultimate_ability': enemy.abilities.ultimate_ability
            },
            'behavior': {
                'aggression': enemy.behavior.aggression,
                'intelligence': enemy.behavior.intelligence,
                'current_pattern': enemy.behavior.current_pattern['name'] if enemy.behavior.current_pattern else None
            },
            'phase': {
                'current': enemy.phases.current_phase if enemy.phases else None,
                'available_phases': enemy.phases.phases if enemy.phases else []
            },
            'metrics': {
                'power_rating': self._calculate_power_rating(enemy),
                'challenge_rating': self._calculate_challenge_rating(enemy, {}),
                'engagement_score': self._calculate_engagement_score(enemy, {}),
                'fairness_rating': self._calculate_fairness_rating(enemy, {})
            }
        }

@dataclass
class CombatCalculator:
    """Advanced combat calculations system"""
    base_damage_variance: float = 0.1
    critical_multiplier: float = 2.0
    defense_scaling: float = 100.0
    resistance_cap: float = 0.75
    vulnerability_multiplier: float = 1.5
    
    def calculate_damage(self, attacker: Enemy, target: Enemy, base_damage: float, damage_type: str) -> float:
        """Calculate final damage with all modifiers"""
        # Base damage variation (±10%)
        damage = base_damage * random.uniform(1 - self.base_damage_variance, 1 + self.base_damage_variance)
        
        # Critical hit check
        if random.random() < attacker.stats.critical_rate:
            damage *= self.critical_multiplier
            if hasattr(attacker.stats, 'critical_damage'):
                damage *= attacker.stats.critical_damage
        
        # Apply attacker's offensive modifiers
        damage *= (1 + attacker.stats.damage_modifier if hasattr(attacker.stats, 'damage_modifier') else 1.0)
        
        # Check target's resistances/vulnerabilities
        resistance = target.stats.resistance.get(damage_type, 0)
        resistance = min(resistance, self.resistance_cap)  # Cap resistance at 75%
        
        if damage_type in target.stats.weakness:
            damage *= self.vulnerability_multiplier
        
        # Apply defense formula: damage = damage * (100 / (100 + defense))
        damage *= (self.defense_scaling / (self.defense_scaling + target.stats.defense))
        
        # Apply resistance reduction
        damage *= (1 - resistance)
        
        return max(1, damage)  # Minimum 1 damage

    def calculate_healing(self, healer: Enemy, target: Enemy, base_healing: float) -> float:
        """Calculate healing amount with modifiers"""
        healing = base_healing
        
        # Apply healer's healing power modifier
        if hasattr(healer.stats, 'healing_power'):
            healing *= healer.stats.healing_power
        
        # Apply target's healing received modifier
        if hasattr(target.stats, 'healing_received'):
            healing *= target.stats.healing_received
        
        # Add variance
        healing *= random.uniform(0.9, 1.1)
        
        return max(1, healing)

@dataclass
class MovementPattern:
    """Sophisticated movement pattern system"""
    pattern_type: str
    params: Dict[str, Any]
    duration: Optional[float] = None
    priority: float = 1.0
    
    @staticmethod
    def create_pattern(pattern_type: str, **kwargs) -> 'MovementPattern':
        """Factory method for creating movement patterns"""
        pattern_params = {
            'circle': {
                'radius': kwargs.get('radius', 3),
                'speed': kwargs.get('speed', 1),
                'clockwise': kwargs.get('clockwise', True)
            },
            'flank': {
                'target_distance': kwargs.get('target_distance', 2),
                'angle': kwargs.get('angle', 45),
                'speed': kwargs.get('speed', 1.5)
            },
            'kite': {
                'min_distance': kwargs.get('min_distance', 4),
                'max_distance': kwargs.get('max_distance', 6),
                'speed': kwargs.get('speed', 1.2)
            },
            'ambush': {
                'stealth_threshold': kwargs.get('stealth_threshold', 0.3),
                'burst_speed': kwargs.get('burst_speed', 2),
                'approach_angle': kwargs.get('approach_angle', 30)
            },
            'formation': {
                'formation_type': kwargs.get('formation_type', 'triangle'),
                'spacing': kwargs.get('spacing', 2),
                'position_index': kwargs.get('position_index', 0)
            }
        }.get(pattern_type, {})
        
        return MovementPattern(pattern_type, pattern_params)

def update_movement(self, context: Dict[str, Any]):
    """Update enemy movement based on current pattern"""
    if not hasattr(self, 'current_movement_pattern'):
        return
    
    pattern = self.current_movement_pattern
    if pattern.pattern_type == 'circle':
        self._execute_circle_movement(pattern.params, context)
    elif pattern.pattern_type == 'flank':
        self._execute_flank_movement(pattern.params, context)
    elif pattern.pattern_type == 'kite':
        self._execute_kite_movement(pattern.params, context)
    elif pattern.pattern_type == 'ambush':
        self._execute_ambush_movement(pattern.params, context)
    elif pattern.pattern_type == 'formation':
        self._execute_formation_movement(pattern.params, context)

def _execute_circle_movement(self, params: Dict[str, Any], context: Dict[str, Any]):
    """Execute circular movement pattern"""
    target = context.get('target')
    if not target:
        return
    
    # Calculate new position on circle around target
    current_angle = math.atan2(self.position[1] - target.position[1],
                             self.position[0] - target.position[0])
    
    # Update angle based on direction and speed
    angle_change = params['speed'] * (1 if params['clockwise'] else -1)
    new_angle = current_angle + angle_change
    
    # Calculate new position
    new_x = target.position[0] + params['radius'] * math.cos(new_angle)
    new_y = target.position[1] + params['radius'] * math.sin(new_angle)
    
    # Update position if valid
    if self._is_valid_position((new_x, new_y)):
        self.position = (new_x, new_y)

def _execute_flank_movement(self, params: Dict[str, Any], context: Dict[str, Any]):
    """Execute flanking movement pattern"""
    target = context.get('target')
    if not target:
        return
    
    # Calculate flank position
    angle_rad = math.radians(params['angle'])
    dx = params['target_distance'] * math.cos(angle_rad)
    dy = params['target_distance'] * math.sin(angle_rad)
    
    flank_pos = (target.position[0] + dx, target.position[1] + dy)
    
    # Move towards flank position
    if self._is_valid_position(flank_pos):
        current_x, current_y = self.position
        direction_x = flank_pos[0] - current_x
        direction_y = flank_pos[1] - current_y
        
        # Normalize and apply speed
        length = math.sqrt(direction_x**2 + direction_y**2)
        if length > 0:
            move_x = current_x + (direction_x / length) * params['speed']
            move_y = current_y + (direction_y / length) * params['speed']
            
            if self._is_valid_position((move_x, move_y)):
                self.position = (move_x, move_y)

def _execute_kite_movement(self, params: Dict[str, Any], context: Dict[str, Any]):
    """Execute kiting movement pattern"""
    target = context.get('target')
    if not target:
        return
    
    # Calculate distance to target
    distance = self._calculate_distance(self.position, target.position)
    
    # Determine movement direction
    if distance < params['min_distance']:
        # Move away from target
        direction_x = self.position[0] - target.position[0]
        direction_y = self.position[1] - target.position[1]
    elif distance > params['max_distance']:
        # Move towards target
        direction_x = target.position[0] - self.position[0]
        direction_y = target.position[1] - self.position[1]
    else:
        # Maintain distance while moving sideways
        perpendicular_x = -(target.position[1] - self.position[1])
        perpendicular_y = target.position[0] - self.position[0]
        direction_x, direction_y = perpendicular_x, perpendicular_y
    
    # Normalize and apply speed
    length = math.sqrt(direction_x**2 + direction_y**2)
    if length > 0:
        move_x = self.position[0] + (direction_x / length) * params['speed']
        move_y = self.position[1] + (direction_y / length) * params['speed']
        
        if self._is_valid_position((move_x, move_y)):
            self.position = (move_x, move_y)

def _execute_ambush_movement(self, params: Dict[str, Any], context: Dict[str, Any]):
    """Execute ambush movement pattern"""
    target = context.get('target')
    if not target:
        return
    
    distance = self._calculate_distance(self.position, target.position)
    
    # Check if we're in stealth
    if distance > params['stealth_threshold']:
        # Calculate approach position
        angle_rad = math.radians(params['approach_angle'])
        dx = distance * math.cos(angle_rad)
        dy = distance * math.sin(angle_rad)
        
        approach_pos = (target.position[0] + dx, target.position[1] + dy)
        
        # Move towards approach position stealthily
        if self._is_valid_position(approach_pos):
            current_x, current_y = self.position
            direction_x = approach_pos[0] - current_x
            direction_y = approach_pos[1] - current_y
            
            # Use normal speed for stealth
            length = math.sqrt(direction_x**2 + direction_y**2)
            if length > 0:
                move_x = current_x + (direction_x / length) * params['speed']
                move_y = current_y + (direction_y / length) * params['speed']
                
                if self._is_valid_position((move_x, move_y)):
                    self.position = (move_x, move_y)
    else:
        # Burst towards target
        direction_x = target.position[0] - self.position[0]
        direction_y = target.position[1] - self.position[1]
        
        length = math.sqrt(direction_x**2 + direction_y**2)
        if length > 0:
            move_x = self.position[0] + (direction_x / length) * params['burst_speed']
            move_y = self.position[1] + (direction_y / length) * params['burst_speed']
            
            if self._is_valid_position((move_x, move_y)):
                self.position = (move_x, move_y)

def _execute_formation_movement(self, params: Dict[str, Any], context: Dict[str, Any]):
    """Execute formation movement pattern"""
    leader = context.get('formation_leader')
    if not leader:
        return
    
    # Calculate formation position based on type and position index
    formation_positions = self._calculate_formation_positions(
        leader.position,
        params['formation_type'],
        params['spacing']
    )
    
    # Get our designated position
    if params['position_index'] < len(formation_positions):
        target_pos = formation_positions[params['position_index']]
        
        # Move towards formation position
        current_x, current_y = self.position
        direction_x = target_pos[0] - current_x
        direction_y = target_pos[1] - current_y
        
        length = math.sqrt(direction_x**2 + direction_y**2)
        if length > 0:
            move_x = current_x + (direction_x / length) * params['speed']
            move_y = current_y + (direction_y / length) * params['speed']
            
            if self._is_valid_position((move_x, move_y)):
                self.position = (move_x, move_y)

def _calculate_formation_positions(self, leader_pos: tuple, formation_type: str, spacing: float) -> List[tuple]:
    """Calculate positions for formation movement"""
    positions = []
    x, y = leader_pos
    
    if formation_type == 'triangle':
        positions = [
            (x - spacing, y - spacing),
            (x + spacing, y - spacing),
            (x, y - spacing * 2)
        ]
    elif formation_type == 'line':
        positions = [
            (x - spacing * 2, y),
            (x - spacing, y),
            (x + spacing, y),
            (x + spacing * 2, y)
        ]
    elif formation_type == 'circle':
        for i in range(6):
            angle = i * (2 * math.pi / 6)
            pos_x = x + spacing * math.cos(angle)
            pos_y = y + spacing * math.sin(angle)
            positions.append((pos_x, pos_y))
    
    return positions

@dataclass
class StatusEffect:
    """Status effect template system"""
    effect_type: str
    potency: float
    duration: float
    tick_rate: Optional[float] = None
    stacks: int = 1
    max_stacks: int = 1
    
    @staticmethod
    def create_effect(effect_type: str, **kwargs) -> 'StatusEffect':
        """Factory method for creating status effects"""
        effect_templates = {
            'burn': {
                'potency': kwargs.get('potency', 0.1),
                'duration': kwargs.get('duration', 5),
                'tick_rate': 1.0,
                'max_stacks': 3
            },
            'freeze': {
                'potency': kwargs.get('potency', 0.5),
                'duration': kwargs.get('duration', 3),
                'tick_rate': None,
                'max_stacks': 1
            },
            'poison': {
                'potency': kwargs.get('potency', 0.08),
                'duration': kwargs.get('duration', 8),
                'tick_rate': 1.0,
                'max_stacks': 5
            },
            'stun': {
                'potency': 1.0,
                'duration': kwargs.get('duration', 1.5),
                'tick_rate': None,
                'max_stacks': 1
            },
            'bleed': {
                'potency': kwargs.get('potency', 0.15),
                'duration': kwargs.get('duration', 4),
                'tick_rate': 1.0,
                'max_stacks': 3
            },
            'weaken': {
                'potency': kwargs.get('potency', 0.25),
                'duration': kwargs.get('duration', 6),
                'tick_rate': None,
                'max_stacks': 2
            }
        }
        
        template = effect_templates.get(effect_type, {
            'potency': kwargs.get('potency', 1.0),
            'duration': kwargs.get('duration', 5),
            'tick_rate': kwargs.get('tick_rate'),
            'max_stacks': kwargs.get('max_stacks', 1)
        })
        
        return StatusEffect(
            effect_type=effect_type,
            **template
        )

    def apply_effect(self, target: Enemy):
        """Apply the status effect to a target"""
        if self.effect_type == 'burn':
            self._apply_burn(target)
        elif self.effect_type == 'freeze':
            self._apply_freeze(target)
        elif self.effect_type == 'poison':
            self._apply_poison(target)
        elif self.effect_type == 'stun':
            self._apply_stun(target)
        elif self.effect_type == 'bleed':
            self._apply_bleed(target)
        elif self.effect_type == 'weaken':
            self._apply_weaken(target)

    def _apply_burn(self, target: Enemy):
        """Apply burn effect"""
        # Damage over time
        damage_per_tick = target.stats.max_health * self.potency
        target.stats.active_effects['burn'] = {
            'damage': damage_per_tick,
            'duration': self.duration,
            'tick_rate': self.tick_rate,
            'stacks': min(self.stacks + 1, self.max_stacks)
        }

    def _apply_freeze(self, target: Enemy):
        """Apply freeze effect"""
        # Movement and attack speed reduction
        target.stats.speed *= (1 - self.potency)
        target.stats.active_effects['freeze'] = {
            'speed_mod': self.potency,
            'duration': self.duration
        }

    def _apply_poison(self, target: Enemy):
        """Apply poison effect"""
        # Damage over time and healing reduction
        damage_per_tick = target.stats.max_health * self.potency
        target.stats.active_effects['poison'] = {
            'damage': damage_per_tick,
            'healing_reduction': 0.3,
            'duration': self.duration,
            'tick_rate': self.tick_rate,
            'stacks': min(self.stacks + 1, self.max_stacks)
        }

    def _apply_stun(self, target: Enemy):
        """Apply stun effect"""
        # Complete immobilization
        target.stats.active_effects['stun'] = {
            'duration': self.duration
        }
        target.behavior.current_state = CombatState.STUNNED

    def _apply_bleed(self, target: Enemy):
        """Apply bleed effect"""
        # Physical damage over time
        damage_per_tick = target.stats.max_health * self.potency
        target.stats.active_effects['bleed'] = {
            'damage': damage_per_tick,
            'duration': self.duration,
            'tick_rate': self.tick_rate,
            'stacks': min(self.stacks + 1, self.max_stacks)
        }

    def _apply_weaken(self, target: Enemy):
        """Apply weaken effect"""
        # Reduce damage output
        target.stats.damage *= (1 - self.potency)
        target.stats.active_effects['weaken'] = {
            'damage_reduction': self.potency,
            'duration': self.duration,
            'stacks': min(self.stacks + 1, self.max_stacks)
        }

# Add to system_managers initialization
if __name__ == "__main__":
    system_managers.update({
        'enemy_system': EnemySystem(
            combat_system=system_managers.combat_system,
            world_system=system_managers.world_system,
            event_system=system_managers.event_system,
            faction_system=system_managers.faction_system
        ),
        'combat_calculator': CombatCalculator(),
        'status_effect_system': StatusEffect
    })