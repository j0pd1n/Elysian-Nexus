from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
from .event_manager import Event, EventType
from .advanced_events import AdvancedEventType, AdvancedEventFactory
from .event_orchestrator import EventOrchestrator

class GameSystem(Enum):
    COMBAT = "combat"
    ECONOMY = "economy"
    MAGIC = "magic"
    FACTION = "faction"
    WORLD = "world"
    QUEST = "quest"
    INVENTORY = "inventory"
    CHARACTER = "character"

@dataclass
class SystemState:
    system_type: GameSystem
    active: bool
    data: Dict[str, Any]
    last_update: float
    dependencies: List[GameSystem]

class SystemEffect:
    def __init__(self, 
                 target_system: GameSystem,
                 effect_type: str,
                 magnitude: float,
                 duration: Optional[int] = None,
                 conditions: Optional[Dict[str, Any]] = None):
        self.target_system = target_system
        self.effect_type = effect_type
        self.magnitude = magnitude
        self.duration = duration
        self.conditions = conditions or {}

class SystemIntegrationManager:
    def __init__(self, event_orchestrator: EventOrchestrator):
        self.orchestrator = event_orchestrator
        self.system_states: Dict[GameSystem, SystemState] = {}
        self.effect_handlers: Dict[str, Callable] = {}
        self.active_effects: List[SystemEffect] = []
        self.system_listeners: Dict[GameSystem, List[Callable]] = {}
        
        self.initialize_systems()
        self.register_effect_handlers()

    def initialize_systems(self):
        """Initialize all game systems and their states"""
        self.system_states[GameSystem.COMBAT] = SystemState(
            system_type=GameSystem.COMBAT,
            active=True,
            data={
                "active_battles": {},
                "combat_modifiers": {},
                "terrain_effects": {}
            },
            last_update=0.0,
            dependencies=[GameSystem.CHARACTER, GameSystem.INVENTORY]
        )
        
        self.system_states[GameSystem.ECONOMY] = SystemState(
            system_type=GameSystem.ECONOMY,
            active=True,
            data={
                "market_prices": {},
                "trade_routes": {},
                "economic_modifiers": {}
            },
            last_update=0.0,
            dependencies=[GameSystem.FACTION, GameSystem.INVENTORY]
        )
        
        self.system_states[GameSystem.MAGIC] = SystemState(
            system_type=GameSystem.MAGIC,
            active=True,
            data={
                "magical_energy": 1.0,
                "active_spells": {},
                "magical_anomalies": {}
            },
            last_update=0.0,
            dependencies=[GameSystem.CHARACTER]
        )
        
        self.system_states[GameSystem.FACTION] = SystemState(
            system_type=GameSystem.FACTION,
            active=True,
            data={
                "faction_relations": {},
                "territory_control": {},
                "active_conflicts": {}
            },
            last_update=0.0,
            dependencies=[]
        )
        
        self.system_states[GameSystem.WORLD] = SystemState(
            system_type=GameSystem.WORLD,
            active=True,
            data={
                "weather": "normal",
                "time_of_day": "day",
                "world_states": {}
            },
            last_update=0.0,
            dependencies=[GameSystem.MAGIC]
        )

    def register_effect_handlers(self):
        """Register handlers for different types of system effects"""
        self.effect_handlers.update({
            # Combat effect handlers
            "modify_combat_strength": self._handle_combat_strength_modification,
            "apply_terrain_effect": self._handle_terrain_effect,
            "trigger_reinforcements": self._handle_reinforcements,
            
            # Economic effect handlers
            "modify_market_prices": self._handle_market_price_changes,
            "alter_trade_routes": self._handle_trade_route_changes,
            "economic_crisis": self._handle_economic_crisis,
            
            # Magical effect handlers
            "modify_magical_energy": self._handle_magical_energy_change,
            "spawn_magical_anomaly": self._handle_magical_anomaly,
            "alter_spell_effects": self._handle_spell_modification,
            
            # World effect handlers
            "change_weather": self._handle_weather_change,
            "transform_territory": self._handle_territory_transformation,
            "trigger_natural_disaster": self._handle_natural_disaster
        })

    def apply_event_effects(self, event: Event):
        """Apply an event's effects to relevant game systems"""
        effects = []
        
        # Handle combat effects
        if event.event_type == EventType.COMBAT:
            effects.extend(self._generate_combat_effects(event))
            
        # Handle economic effects
        if event.effects.resource_changes:
            effects.extend(self._generate_economic_effects(event))
            
        # Handle magical effects
        if event.effects.celestial_effects:
            effects.extend(self._generate_magical_effects(event))
            
        # Handle world effects
        if event.effects.environmental_changes:
            effects.extend(self._generate_world_effects(event))
            
        # Apply all generated effects
        for effect in effects:
            self._apply_system_effect(effect)

    def _generate_combat_effects(self, event: Event) -> List[SystemEffect]:
        """Generate combat-related system effects"""
        effects = []
        
        if "battle" in event.name.lower():
            effects.append(SystemEffect(
                target_system=GameSystem.COMBAT,
                effect_type="modify_combat_strength",
                magnitude=1.2,
                duration=event.duration,
                conditions={"in_battle": True}
            ))
            
        if event.effects.territory_effects:
            effects.append(SystemEffect(
                target_system=GameSystem.COMBAT,
                effect_type="apply_terrain_effect",
                magnitude=1.0,
                conditions={"territories": list(event.effects.territory_effects.keys())}
            ))
            
        return effects

    def _generate_economic_effects(self, event: Event) -> List[SystemEffect]:
        """Generate economy-related system effects"""
        effects = []
        
        for resource, change in event.effects.resource_changes.items():
            effects.append(SystemEffect(
                target_system=GameSystem.ECONOMY,
                effect_type="modify_market_prices",
                magnitude=change,
                duration=event.duration,
                conditions={"resource": resource}
            ))
            
        return effects

    def _generate_magical_effects(self, event: Event) -> List[SystemEffect]:
        """Generate magic-related system effects"""
        effects = []
        
        for effect in event.effects.celestial_effects:
            if "surge" in effect:
                effects.append(SystemEffect(
                    target_system=GameSystem.MAGIC,
                    effect_type="modify_magical_energy",
                    magnitude=1.5,
                    duration=event.duration
                ))
            elif "anomaly" in effect:
                effects.append(SystemEffect(
                    target_system=GameSystem.MAGIC,
                    effect_type="spawn_magical_anomaly",
                    magnitude=1.0,
                    conditions={"type": effect}
                ))
                
        return effects

    def _generate_world_effects(self, event: Event) -> List[SystemEffect]:
        """Generate world-related system effects"""
        effects = []
        
        for change in event.effects.environmental_changes:
            if "weather" in change:
                effects.append(SystemEffect(
                    target_system=GameSystem.WORLD,
                    effect_type="change_weather",
                    magnitude=1.0,
                    duration=event.duration,
                    conditions={"weather_type": change}
                ))
            elif "transform" in change:
                effects.append(SystemEffect(
                    target_system=GameSystem.WORLD,
                    effect_type="transform_territory",
                    magnitude=1.0,
                    conditions={"transformation": change}
                ))
                
        return effects

    def _apply_system_effect(self, effect: SystemEffect):
        """Apply a system effect using the appropriate handler"""
        if effect.effect_type in self.effect_handlers:
            handler = self.effect_handlers[effect.effect_type]
            handler(effect)
            self.active_effects.append(effect)
            self._notify_system_listeners(effect.target_system, effect)

    def register_system_listener(self, system: GameSystem, callback: Callable):
        """Register a callback for system state changes"""
        if system not in self.system_listeners:
            self.system_listeners[system] = []
        self.system_listeners[system].append(callback)

    def _notify_system_listeners(self, system: GameSystem, effect: SystemEffect):
        """Notify all listeners of a system state change"""
        if system in self.system_listeners:
            for listener in self.system_listeners[system]:
                listener(effect)

    # Effect Handlers
    def _handle_combat_strength_modification(self, effect: SystemEffect):
        """Handle combat strength modification effects"""
        system_state = self.system_states[GameSystem.COMBAT]
        if "combat_modifiers" not in system_state.data:
            system_state.data["combat_modifiers"] = {}
            
        modifier_id = f"strength_mod_{len(system_state.data['combat_modifiers'])}"
        system_state.data["combat_modifiers"][modifier_id] = {
            "magnitude": effect.magnitude,
            "duration": effect.duration,
            "conditions": effect.conditions
        }

    def _handle_terrain_effect(self, effect: SystemEffect):
        """Handle terrain effect application"""
        system_state = self.system_states[GameSystem.COMBAT]
        for territory in effect.conditions.get("territories", []):
            if "terrain_effects" not in system_state.data:
                system_state.data["terrain_effects"] = {}
            system_state.data["terrain_effects"][territory] = effect.magnitude

    def _handle_market_price_changes(self, effect: SystemEffect):
        """Handle market price modifications"""
        system_state = self.system_states[GameSystem.ECONOMY]
        resource = effect.conditions.get("resource")
        if resource:
            if "market_prices" not in system_state.data:
                system_state.data["market_prices"] = {}
            current_price = system_state.data["market_prices"].get(resource, 1.0)
            system_state.data["market_prices"][resource] = current_price * (1 + effect.magnitude)

    def _handle_magical_energy_change(self, effect: SystemEffect):
        """Handle magical energy level changes"""
        system_state = self.system_states[GameSystem.MAGIC]
        current_energy = system_state.data.get("magical_energy", 1.0)
        system_state.data["magical_energy"] = current_energy * effect.magnitude

    def update_systems(self, game_state: Dict[str, Any], delta_time: float):
        """Update all game systems"""
        current_time = game_state.get("current_time", 0.0)
        
        # Update system states
        for system in GameSystem:
            if system in self.system_states and self.system_states[system].active:
                self._update_system(system, current_time, delta_time)
                
        # Clean up expired effects
        self._cleanup_expired_effects(current_time)
        
        # Process event interactions
        self._process_system_interactions()

    def _update_system(self, system: GameSystem, current_time: float, delta_time: float):
        """Update a specific game system"""
        system_state = self.system_states[system]
        system_state.last_update = current_time
        
        # Update system-specific logic
        if system == GameSystem.COMBAT:
            self._update_combat_system(delta_time)
        elif system == GameSystem.ECONOMY:
            self._update_economy_system(delta_time)
        elif system == GameSystem.MAGIC:
            self._update_magic_system(delta_time)
        elif system == GameSystem.WORLD:
            self._update_world_system(delta_time)

    def _cleanup_expired_effects(self, current_time: float):
        """Remove expired effects"""
        active_effects = []
        for effect in self.active_effects:
            if effect.duration is None or effect.duration > 0:
                if effect.duration is not None:
                    effect.duration -= 1
                active_effects.append(effect)
        self.active_effects = active_effects

    def _process_system_interactions(self):
        """Process interactions between different systems"""
        # Combat-Magic interaction
        if self._check_system_active(GameSystem.COMBAT) and self._check_system_active(GameSystem.MAGIC):
            combat_state = self.system_states[GameSystem.COMBAT]
            magic_state = self.system_states[GameSystem.MAGIC]
            
            # Modify combat based on magical energy
            if magic_state.data.get("magical_energy", 1.0) > 1.5:
                combat_state.data["combat_modifiers"]["magical_enhancement"] = 1.2
                
        # Economy-Faction interaction
        if self._check_system_active(GameSystem.ECONOMY) and self._check_system_active(GameSystem.FACTION):
            economy_state = self.system_states[GameSystem.ECONOMY]
            faction_state = self.system_states[GameSystem.FACTION]
            
            # Adjust trade routes based on faction relations
            for faction, relations in faction_state.data.get("faction_relations", {}).items():
                if "trade_routes" in economy_state.data:
                    route_key = f"route_{faction}"
                    economy_state.data["trade_routes"][route_key] = relations > 0

    def _check_system_active(self, system: GameSystem) -> bool:
        """Check if a system is active and has all dependencies met"""
        if system not in self.system_states:
            return False
            
        system_state = self.system_states[system]
        if not system_state.active:
            return False
            
        # Check dependencies
        for dependency in system_state.dependencies:
            if not self._check_system_active(dependency):
                return False
                
        return True

    # System-specific update methods
    def _update_combat_system(self, delta_time: float):
        """Update combat system state"""
        combat_state = self.system_states[GameSystem.COMBAT]
        
        # Update active battles
        for battle_id, battle_data in combat_state.data.get("active_battles", {}).copy().items():
            battle_data["duration"] -= delta_time
            if battle_data["duration"] <= 0:
                del combat_state.data["active_battles"][battle_id]

    def _update_economy_system(self, delta_time: float):
        """Update economy system state"""
        economy_state = self.system_states[GameSystem.ECONOMY]
        
        # Update market prices
        for resource, price in economy_state.data.get("market_prices", {}).copy().items():
            # Apply gradual price normalization
            target_price = 1.0
            economy_state.data["market_prices"][resource] += (target_price - price) * 0.1 * delta_time

    def _update_magic_system(self, delta_time: float):
        """Update magic system state"""
        magic_state = self.system_states[GameSystem.MAGIC]
        
        # Update magical energy levels
        current_energy = magic_state.data.get("magical_energy", 1.0)
        target_energy = 1.0
        magic_state.data["magical_energy"] = current_energy + (target_energy - current_energy) * 0.05 * delta_time

    def _update_world_system(self, delta_time: float):
        """Update world system state"""
        world_state = self.system_states[GameSystem.WORLD]
        
        # Update time of day
        current_time = world_state.data.get("time_of_day", "day")
        if current_time == "day":
            world_state.data["time_of_day"] = "night" if delta_time > 12 else "day"
        else:
            world_state.data["time_of_day"] = "day" if delta_time > 12 else "night" 