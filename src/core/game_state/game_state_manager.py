import json
import time
from pathlib import Path
from typing import Dict, Optional, Any, Set
from dataclasses import dataclass, asdict

from .enums import GameState, GameMode, DifficultyLevel, Location, QuestStatus

@dataclass
class CheckpointData:
    timestamp: float
    location: Location
    game_state: GameState
    game_mode: GameMode
    quest_status: Dict[str, QuestStatus]
    player_data: Dict[str, Any]
    world_state: Dict[str, Any]

@dataclass
class DifficultyModifiers:
    # Combat Modifiers
    enemy_damage_multiplier: float
    enemy_health_multiplier: float
    enemy_aggression_multiplier: float
    boss_damage_multiplier: float
    boss_health_multiplier: float
    
    # Progression Modifiers
    xp_gain_multiplier: float
    skill_xp_multiplier: float
    reputation_gain_multiplier: float
    loot_quality_multiplier: float
    rare_drop_chance_multiplier: float
    
    # Resource Management
    resource_scarcity: float
    durability_loss_rate: float
    crafting_cost_multiplier: float
    repair_cost_multiplier: float
    
    # Player Mechanics
    stamina_drain_rate: float
    dodge_window_multiplier: float
    critical_hit_chance: float
    critical_damage_multiplier: float
    healing_effectiveness: float
    mana_regeneration_rate: float
    
    # Stealth Mechanics
    stealth_detection_range: float
    noise_generation_multiplier: float
    sneak_attack_multiplier: float
    
    # Environmental
    trap_damage_multiplier: float
    environmental_damage_multiplier: float
    weather_effect_intensity: float
    elemental_resistance_multiplier: float
    status_effect_duration: float
    
    # Economy
    merchant_price_multiplier: float
    sell_price_multiplier: float
    quest_reward_multiplier: float
    
    # Faction
    faction_reputation_gain: float
    faction_reputation_loss: float
    faction_quest_reward_multiplier: float
    faction_vendor_price_multiplier: float
    hostile_faction_damage_multiplier: float
    allied_faction_assistance_chance: float

@dataclass
class EnvironmentalConditions:
    weather_type: str  # clear, rain, storm, blizzard, etc.
    time_of_day: int  # 0-23 hours
    visibility: float  # 0.0 to 1.0
    temperature: float  # Celsius
    wind_speed: float  # m/s
    is_hazardous: bool
    active_effects: set[str]  # poison_mist, lightning, etc.
    terrain_type: str  # normal, difficult, treacherous
    light_level: float  # 0.0 to 1.0

class GameStateManager:
    # Define valid state transitions with detailed conditions
    VALID_STATE_TRANSITIONS = {
        GameState.MAIN_MENU: {
            GameState.CHARACTER_CREATION: lambda self: True,
            GameState.LOADING: lambda self: len(self.get_save_slots()) > 0
        },
        GameState.CHARACTER_CREATION: {
            GameState.TOWN: lambda self: bool(self.player_data.get('character_created')) 
                          and bool(self.player_data.get('tutorial_completed'))
        },
        GameState.TOWN: {
            GameState.EXPLORATION: lambda self: not self.world_state.get('town_lockdown', False)
                                 and not self.world_state.get('active_event', False),
            GameState.SHOP: lambda self: self._is_during_shop_hours(),
            GameState.INVENTORY: lambda self: True,
            GameState.QUEST_LOG: lambda self: True,
            GameState.SAVE_GAME: lambda self: not self.world_state.get('in_danger', False),
            GameState.PAUSED: lambda self: True
        },
        GameState.EXPLORATION: {
            GameState.BATTLE: lambda self: (bool(self.world_state.get('enemies_nearby')) 
                            and not self.world_state.get('in_safe_zone', False)),
            GameState.TOWN: lambda self: (self.current_location in {Location.NEXUS_CITY, Location.CRYSTAL_PEAKS}
                           and not self.world_state.get('in_combat', False)
                           and not self.world_state.get('being_pursued', False)),
            GameState.INVENTORY: lambda self: not self.world_state.get('in_combat', False),
            GameState.QUEST_LOG: lambda self: not self.world_state.get('in_combat', False),
            GameState.SAVE_GAME: lambda self: (not self.world_state.get('in_combat', False)
                                and not self.world_state.get('in_danger', False)
                                and not self.world_state.get('being_pursued', False)),
            GameState.PAUSED: lambda self: True
        },
        GameState.BATTLE: {
            GameState.EXPLORATION: lambda self: (not self.world_state.get('in_combat', False)
                                  and not self.world_state.get('boss_battle', False)),
            GameState.INVENTORY: lambda self: (not self.world_state.get('boss_battle', False)
                               and self.player_data.get('combat_turns_since_inventory', 0) >= 3),
            GameState.PAUSED: lambda self: True
        },
        GameState.SHOP: {
            GameState.TOWN: lambda self: not self.world_state.get('transaction_in_progress', False),
            GameState.INVENTORY: lambda self: True,
            GameState.SAVE_GAME: lambda self: True,
            GameState.PAUSED: lambda self: True
        },
        GameState.INVENTORY: {
            GameState.TOWN: lambda self: self.current_state in {GameState.TOWN, GameState.SHOP},
            GameState.EXPLORATION: lambda self: self.current_state == GameState.EXPLORATION,
            GameState.BATTLE: lambda self: self.current_state == GameState.BATTLE,
            GameState.SHOP: lambda self: self.current_state == GameState.SHOP,
            GameState.PAUSED: lambda self: True
        },
        GameState.QUEST_LOG: {
            GameState.TOWN: lambda self: self.current_state == GameState.TOWN,
            GameState.EXPLORATION: lambda self: self.current_state == GameState.EXPLORATION,
            GameState.PAUSED: lambda self: True
        },
        GameState.SAVE_GAME: {
            GameState.TOWN: lambda self: self.current_state in {GameState.TOWN, GameState.SHOP},
            GameState.EXPLORATION: lambda self: self.current_state == GameState.EXPLORATION,
            GameState.SHOP: lambda self: self.current_state == GameState.SHOP
        },
        GameState.PAUSED: {
            GameState.MAIN_MENU: lambda self: True,
            GameState.TOWN: lambda self: self.current_state != GameState.BATTLE or not self.world_state.get('in_combat', False),
            GameState.EXPLORATION: lambda self: self.current_state != GameState.BATTLE or not self.world_state.get('in_combat', False),
            GameState.BATTLE: lambda self: self.current_state == GameState.BATTLE,
            GameState.SHOP: lambda self: self.current_state == GameState.SHOP,
            GameState.INVENTORY: lambda self: True,
            GameState.QUEST_LOG: lambda self: True
        },
        GameState.LOADING: {
            GameState.TOWN: lambda self: True,
            GameState.EXPLORATION: lambda self: True,
            GameState.BATTLE: lambda self: self.world_state.get('in_combat', False)
        }
    }

    # Define difficulty presets with expanded modifiers
    DIFFICULTY_PRESETS = {
        DifficultyLevel.EASY: DifficultyModifiers(
            enemy_damage_multiplier=0.75,
            enemy_health_multiplier=0.75,
            xp_gain_multiplier=1.25,
            loot_quality_multiplier=1.25,
            resource_scarcity=0.75,
            stamina_drain_rate=0.75,
            dodge_window_multiplier=1.5,
            critical_hit_chance=1.25,
            healing_effectiveness=1.25,
            trap_damage_multiplier=0.75,
            stealth_detection_range=0.75,
            merchant_price_multiplier=0.9
        ),
        DifficultyLevel.NORMAL: DifficultyModifiers(
            enemy_damage_multiplier=1.0,
            enemy_health_multiplier=1.0,
            xp_gain_multiplier=1.0,
            loot_quality_multiplier=1.0,
            resource_scarcity=1.0,
            stamina_drain_rate=1.0,
            dodge_window_multiplier=1.0,
            critical_hit_chance=1.0,
            healing_effectiveness=1.0,
            trap_damage_multiplier=1.0,
            stealth_detection_range=1.0,
            merchant_price_multiplier=1.0
        ),
        DifficultyLevel.HARD: DifficultyModifiers(
            enemy_damage_multiplier=1.25,
            enemy_health_multiplier=1.25,
            xp_gain_multiplier=0.75,
            loot_quality_multiplier=0.75,
            resource_scarcity=1.25,
            stamina_drain_rate=1.25,
            dodge_window_multiplier=0.75,
            critical_hit_chance=0.75,
            healing_effectiveness=0.75,
            trap_damage_multiplier=1.25,
            stealth_detection_range=1.25,
            merchant_price_multiplier=1.1
        ),
        DifficultyLevel.EXPERT: DifficultyModifiers(
            enemy_damage_multiplier=1.5,
            enemy_health_multiplier=1.5,
            xp_gain_multiplier=0.5,
            loot_quality_multiplier=0.5,
            resource_scarcity=1.5,
            stamina_drain_rate=1.5,
            dodge_window_multiplier=0.5,
            critical_hit_chance=0.5,
            healing_effectiveness=0.5,
            trap_damage_multiplier=1.5,
            stealth_detection_range=1.5,
            merchant_price_multiplier=1.25
        )
    }

    def __init__(self):
        self.current_state: GameState = GameState.MAIN_MENU
        self.current_mode: GameMode = GameMode.MENU
        self.difficulty: DifficultyLevel = DifficultyLevel.NORMAL
        self.difficulty_modifiers: DifficultyModifiers = self.DIFFICULTY_PRESETS[DifficultyLevel.NORMAL]
        self.current_location: Optional[Location] = None
        self.player_data: Dict[str, Any] = {}
        self.world_state: Dict[str, Any] = {}
        self.quest_status: Dict[str, QuestStatus] = {}
        self.last_checkpoint: Optional[CheckpointData] = None
        self.save_directory = Path("saves")
        self.checkpoint_directory = Path("checkpoints")
        self.last_checkpoint_time = time.time()
        self.checkpoint_interval = 300  # 5 minutes in seconds
        self.last_health_percentage = 100
        self.last_combat_turn = 0
        self.last_save_location = None
        self.active_effects = set()
        self.last_merchant_interaction = 0
        self.consecutive_deaths = 0
        
        # Create necessary directories
        self.save_directory.mkdir(exist_ok=True)
        self.checkpoint_directory.mkdir(exist_ok=True)

        self.environmental_conditions = EnvironmentalConditions(
            weather_type='clear',
            time_of_day=12,
            visibility=1.0,
            temperature=20.0,
            wind_speed=0.0,
            is_hazardous=False,
            active_effects=set(),
            terrain_type='normal',
            light_level=1.0
        )
        self.faction_standings = {}  # faction_id -> reputation value
        self.active_faction_effects = set()  # Current faction-based effects

    def is_valid_state_transition(self, current: GameState, new: GameState) -> bool:
        """Enhanced state transition validation including environmental and faction conditions."""
        if current == new:
            return True
        
        # Check basic state transition rules
        valid_transitions = self.VALID_STATE_TRANSITIONS.get(current, {})
        if new not in valid_transitions or not valid_transitions[new](self):
            return False
            
        # Check environmental restrictions
        for condition, restrictions in self.ENVIRONMENTAL_RESTRICTIONS.items():
            if condition in self.environmental_conditions.active_effects:
                if new in restrictions and not restrictions[new](self):
                    return False
        
        # Check faction-based restrictions
        if not self._check_faction_restrictions(new):
            return False
            
        # Check time-based restrictions
        if not self._check_time_restrictions(new):
            return False
            
        # Check weather-based movement restrictions
        if new == GameState.EXPLORATION and not self._is_safe_to_explore():
            return False
            
        return True

    def _check_faction_restrictions(self, new_state: GameState) -> bool:
        """Check if faction standings allow the state transition."""
        current_location = self.current_location
        if not current_location:
            return True
            
        controlling_faction = self.world_state.get(f'{current_location.name}_controlling_faction')
        if not controlling_faction:
            return True
            
        faction_standing = self.faction_standings.get(controlling_faction, 0)
        
        # State-specific faction requirements
        if new_state == GameState.TOWN:
            return faction_standing > -50  # Minimal standing to enter town
        elif new_state == GameState.SHOP:
            return faction_standing > 0  # Positive standing to trade
        elif new_state == GameState.QUEST_LOG:
            return faction_standing > -25  # Some tolerance for quest access
            
        return True

    def _check_time_restrictions(self, new_state: GameState) -> bool:
        """Check if the current time allows the state transition."""
        time_of_day = self.environmental_conditions.time_of_day
        
        if new_state == GameState.SHOP:
            return 6 <= time_of_day <= 20  # Shop hours
        elif new_state == GameState.EXPLORATION:
            # Night exploration requires light source or night vision
            if 22 <= time_of_day or time_of_day <= 4:
                return (self.player_data.get('light_source', False) or
                       self.player_data.get('night_vision', False))
                       
        return True

    def _is_safe_to_explore(self) -> bool:
        """Check if current environmental conditions allow safe exploration."""
        conditions = self.environmental_conditions
        
        # Check for extreme weather conditions
        if conditions.weather_type in {'blizzard', 'tornado', 'sandstorm'}:
            return False
            
        # Check for dangerous visibility conditions
        if conditions.visibility < 0.2:  # Very low visibility
            return self.player_data.get('enhanced_vision', False)
            
        # Check for extreme temperatures
        if conditions.temperature < -20 or conditions.temperature > 45:
            return False
            
        # Check for dangerous wind conditions
        if conditions.wind_speed > 30:  # Strong winds
            return False
            
        return True

    def _calculate_danger_level(self) -> float:
        """Enhanced danger level calculation including environmental and faction factors."""
        danger_score = super()._calculate_danger_level()
        
        # Environmental danger factors
        conditions = self.environmental_conditions
        if conditions.is_hazardous:
            danger_score += 0.2
        if conditions.terrain_type == 'treacherous':
            danger_score += 0.15
        if conditions.light_level < 0.3:
            danger_score += 0.1
        if conditions.visibility < 0.5:
            danger_score += 0.1
            
        # Faction-based danger
        location = self.current_location
        if location:
            controlling_faction = self.world_state.get(f'{location.name}_controlling_faction')
            if controlling_faction:
                faction_standing = self.faction_standings.get(controlling_faction, 0)
                if faction_standing < -75:  # Hostile territory
                    danger_score += 0.3
                elif faction_standing < -25:  # Unfriendly territory
                    danger_score += 0.1
                    
        return min(danger_score, 1.0)

    def _check_auto_checkpoint(self):
        """Enhanced checkpoint check with sophisticated conditions."""
        current_time = time.time()
        current_health = self.player_data.get('health', 100)
        max_health = self.player_data.get('max_health', 100)
        health_percentage = (current_health / max_health) * 100 if max_health > 0 else 100
        
        danger_level = self._calculate_danger_level()
        resource_status = self._calculate_resource_status()
        combat_intensity = self._calculate_combat_intensity()
        
        should_checkpoint = (
            # Time and interval based triggers
            self._check_time_based_triggers(current_time, danger_level)
            
            # Location and exploration triggers
            or self._check_location_triggers()
            
            # Combat and danger triggers
            or self._check_combat_triggers(combat_intensity)
            
            # Health and resource triggers
            or self._check_health_triggers(health_percentage, resource_status)
            
            # Achievement and progression triggers
            or self._check_progression_triggers()
            
            # Environmental triggers
            or self._check_environmental_checkpoint_triggers()
            
            # Faction-based triggers
            or self._check_faction_checkpoint_triggers()
            
            # Special event triggers
            or self._check_special_event_triggers()
        )
        
        if should_checkpoint:
            self.create_checkpoint()
            self._update_checkpoint_state()

    def _check_time_based_triggers(self, current_time: float, danger_level: float) -> bool:
        """Check time-based checkpoint triggers."""
        # Dynamic interval based on danger and player status
        base_interval = self.checkpoint_interval * (1 - danger_level)
        
        # Reduce interval if player has valuable unsaved progress
        if self.player_data.get('valuable_items_found', 0) > 0:
            base_interval *= 0.75
            
        # Reduce interval in dangerous areas
        if self.current_location and self.world_state.get(f'{self.current_location.name}_danger_level', 0) > 0.7:
            base_interval *= 0.5
            
        return current_time - self.last_checkpoint_time >= base_interval

    def _check_location_triggers(self) -> bool:
        """Check location-based checkpoint triggers."""
        return (
            # Basic location changes
            self.current_state in {GameState.TOWN, GameState.SAVE_GAME}
            or (self.current_location != self.last_save_location 
                and not self.world_state.get('in_danger', False))
            
            # Discovery triggers
            or self.world_state.get('area_discovered', False)
            or self.world_state.get('secret_found', False)
            or self.world_state.get('map_updated', False)
            
            # Strategic locations
            or self.world_state.get('strategic_position_reached', False)
            or self.world_state.get('vantage_point_found', False)
            
            # Resource locations
            or self.world_state.get('resource_node_found', False)
            or self.world_state.get('crafting_station_found', False)
        )

    def _check_combat_triggers(self, combat_intensity: float) -> bool:
        """Check combat-related checkpoint triggers."""
        return (
            # Basic combat state
            (self.current_mode in {GameMode.EXPLORATION, GameMode.COMBAT} 
             and not self.world_state.get('in_combat', False))
            
            # Combat milestones
            or self.world_state.get('boss_defeated', False)
            or self.world_state.get('elite_defeated', False)
            or combat_intensity > 0.8  # High-intensity combat
            
            # Combat achievements
            or self.world_state.get('perfect_combat', False)
            or self.world_state.get('combo_achieved', False)
            
            # Strategic combat events
            or self.world_state.get('ambush_survived', False)
            or self.world_state.get('reinforcements_arrived', False)
        )

    def _check_health_triggers(self, health_percentage: float, resource_status: float) -> bool:
        """Check health and resource-related checkpoint triggers."""
        return (
            # Health thresholds with dynamic danger adjustment
            (health_percentage < self.last_health_percentage - (25 * (1 + self._calculate_danger_level()))
             and health_percentage > 0)
            
            # Resource management
            or resource_status < 0.2  # Critical resource levels
            or self.player_data.get('resources_depleted', False)
            
            # Recovery events
            or (self.consecutive_deaths > 0 and health_percentage > 75)
            or self.world_state.get('full_recovery', False)
            
            # Buff and status effects
            or self.world_state.get('major_buff_acquired', False)
            or self.world_state.get('status_effect_cleared', False)
        )

    def _check_progression_triggers(self) -> bool:
        """Check progression-related checkpoint triggers."""
        return (
            # Quest progress
            any(status == QuestStatus.COMPLETED for status in self.quest_status.values())
            or self.world_state.get('quest_milestone_reached', False)
            or self.world_state.get('quest_chain_advanced', False)
            
            # Character progression
            or self.player_data.get('leveled_up', False)
            or self.player_data.get('skill_unlocked', False)
            or self.player_data.get('ability_mastered', False)
            
            # Item progression
            or self.player_data.get('rare_item_found', False)
            or self.player_data.get('equipment_upgraded', False)
            or self.player_data.get('set_bonus_completed', False)
            
            # Achievement progression
            or self.player_data.get('achievement_unlocked', False)
            or self.player_data.get('milestone_reached', False)
            or self.player_data.get('collection_completed', False)
        )

    def _check_special_event_triggers(self) -> bool:
        """Check special event-related checkpoint triggers."""
        return (
            # World events
            self.world_state.get('world_boss_appeared', False)
            or self.world_state.get('invasion_started', False)
            or self.world_state.get('special_event_started', False)
            
            # Time-limited events
            or self.world_state.get('limited_event_progress', False)
            or self.world_state.get('daily_objective_completed', False)
            
            # Random events
            or self.world_state.get('rare_spawn_encountered', False)
            or self.world_state.get('treasure_found', False)
            
            # Story events
            or self.world_state.get('cutscene_watched', False)
            or self.world_state.get('dialogue_choice_made', False)
            or self.world_state.get('story_branch_chosen', False)
        )

    def _calculate_resource_status(self) -> float:
        """Calculate current resource status (0.0 to 1.0)."""
        resources = [
            self.player_data.get('health_percentage', 1.0),
            self.player_data.get('mana_percentage', 1.0),
            self.player_data.get('stamina_percentage', 1.0),
            self.player_data.get('ammunition_percentage', 1.0),
            self.player_data.get('consumables_percentage', 1.0)
        ]
        return sum(resources) / len(resources)

    def _calculate_combat_intensity(self) -> float:
        """Calculate current combat intensity (0.0 to 1.0)."""
        intensity = 0.0
        
        if self.world_state.get('in_combat', False):
            # Base combat factors
            intensity += 0.3
            if self.world_state.get('boss_battle', False):
                intensity += 0.4
            if self.world_state.get('elite_enemies', False):
                intensity += 0.2
                
            # Situational factors
            if self.world_state.get('surrounded', False):
                intensity += 0.2
            if self.world_state.get('low_health', False):
                intensity += 0.2
            if self.world_state.get('out_of_resources', False):
                intensity += 0.1
                
            # Environmental factors
            if self.environmental_conditions.is_hazardous:
                intensity += 0.1
            if self.environmental_conditions.visibility < 0.5:
                intensity += 0.1
                
        return min(intensity, 1.0)

    def _check_environmental_checkpoint_triggers(self) -> bool:
        """Check environment-specific checkpoint triggers."""
        conditions = self.environmental_conditions
        
        return (
            # Weather changes
            self.world_state.get('weather_changed', False)
            # Day/night transitions
            or (self.world_state.get('previous_time_of_day', 12) < 18 <= conditions.time_of_day)  # Nightfall
            or (self.world_state.get('previous_time_of_day', 12) >= 18 > conditions.time_of_day)  # Dawn
            # Entering hazardous areas
            or (not self.world_state.get('previous_is_hazardous', False) and conditions.is_hazardous)
            # Significant terrain changes
            or self.world_state.get('terrain_type_changed', False)
            # Shelter found during extreme conditions
            or (conditions.weather_type in {'blizzard', 'storm'} and self.current_state == GameState.TOWN)
        )

    def _check_faction_checkpoint_triggers(self) -> bool:
        """Check faction-related checkpoint triggers."""
        return (
            # Significant reputation changes
            any(abs(self.faction_standings.get(faction, 0) - 
                   self.world_state.get(f'previous_faction_standing_{faction}', 0)) >= 25
                for faction in self.faction_standings)
            # Entering new faction territory
            or self.world_state.get('faction_territory_changed', False)
            # Faction quest completion
            or self.world_state.get('faction_quest_completed', False)
            # Alliance changes
            or self.world_state.get('faction_alliance_changed', False)
            # Becoming hostile/friendly with a faction
            or any(standing == -75 or standing == 75 
                  for standing in self.faction_standings.values())
        )

    def _update_checkpoint_state(self):
        """Update state tracking for checkpoint triggers."""
        super()._reset_checkpoint_triggers()
        
        # Update environmental state tracking
        self.world_state['previous_time_of_day'] = self.environmental_conditions.time_of_day
        self.world_state['previous_is_hazardous'] = self.environmental_conditions.is_hazardous
        self.world_state['weather_changed'] = False
        self.world_state['terrain_type_changed'] = False
        
        # Update faction state tracking
        for faction in self.faction_standings:
            self.world_state[f'previous_faction_standing_{faction}'] = self.faction_standings[faction]
        self.world_state['faction_territory_changed'] = False
        self.world_state['faction_quest_completed'] = False
        self.world_state['faction_alliance_changed'] = False

    def create_checkpoint(self) -> CheckpointData:
        """Create a checkpoint of the current game state."""
        checkpoint = CheckpointData(
            timestamp=time.time(),
            location=self.current_location,
            game_state=self.current_state,
            game_mode=self.current_mode,
            quest_status=self.quest_status.copy(),
            player_data=self.player_data.copy(),
            world_state=self.world_state.copy()
        )
        self.last_checkpoint = checkpoint
        
        # Save checkpoint to disk
        checkpoint_path = self.checkpoint_directory / f"checkpoint_{int(checkpoint.timestamp)}.json"
        with open(checkpoint_path, 'w') as f:
            json.dump(asdict(checkpoint), f, indent=2)
        
        return checkpoint

    def load_checkpoint(self, checkpoint: CheckpointData):
        """Restore game state from a checkpoint."""
        self.current_location = checkpoint.location
        self.current_state = checkpoint.game_state
        self.current_mode = checkpoint.game_mode
        self.quest_status = checkpoint.quest_status.copy()
        self.player_data = checkpoint.player_data.copy()
        self.world_state = checkpoint.world_state.copy()

    def save_game(self, slot: int):
        """Save the current game state to a specified slot."""
        save_data = {
            'timestamp': time.time(),
            'difficulty': self.difficulty.name,
            'location': self.current_location.name if self.current_location else None,
            'game_state': self.current_state.name,
            'game_mode': self.current_mode.name,
            'quest_status': {k: v.name for k, v in self.quest_status.items()},
            'player_data': self.player_data,
            'world_state': self.world_state
        }
        
        save_path = self.save_directory / f"save_{slot}.json"
        with open(save_path, 'w') as f:
            json.dump(save_data, f, indent=2)

    def load_game(self, slot: int) -> bool:
        """Load a game state from a specified slot. Returns True if successful."""
        save_path = self.save_directory / f"save_{slot}.json"
        
        try:
            with open(save_path, 'r') as f:
                save_data = json.load(f)
            
            self.difficulty = DifficultyLevel[save_data['difficulty']]
            self.current_location = Location[save_data['location']] if save_data['location'] else None
            self.current_state = GameState[save_data['game_state']]
            self.current_mode = GameMode[save_data['game_mode']]
            self.quest_status = {k: QuestStatus[v] for k, v in save_data['quest_status'].items()}
            self.player_data = save_data['player_data']
            self.world_state = save_data['world_state']
            return True
            
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return False

    def get_save_slots(self) -> Dict[int, float]:
        """Return a dictionary of save slots and their timestamps."""
        save_slots = {}
        for save_file in self.save_directory.glob("save_*.json"):
            try:
                slot = int(save_file.stem.split('_')[1])
                with open(save_file, 'r') as f:
                    save_data = json.load(f)
                save_slots[slot] = save_data['timestamp']
            except (ValueError, json.JSONDecodeError, KeyError):
                continue
        return save_slots 