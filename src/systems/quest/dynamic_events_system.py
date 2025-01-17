from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple, Set, Callable
import random
import math
import time
import json
import logging
from collections import defaultdict

from weather_system import WeatherSystem, WeatherType, Season, EnvironmentalEffect
from economic_system import EconomicSystem, ResourceType, MarketEvent

class EventCategory(Enum):
    NATURAL = "natural"
    ECONOMIC = "economic"
    SOCIAL = "social"
    POLITICAL = "political"
    MILITARY = "military"
    SUPERNATURAL = "supernatural"

class EventSeverity(Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"
    CATASTROPHIC = "catastrophic"

class WorldStateMetric(Enum):
    STABILITY = "stability"
    PROSPERITY = "prosperity"
    DANGER_LEVEL = "danger_level"
    MORALE = "morale"
    CORRUPTION = "corruption"
    MAGIC_SATURATION = "magic_saturation"

@dataclass
class WorldState:
    metrics: Dict[WorldStateMetric, float]  # 0.0 to 1.0
    active_effects: Set[str]
    faction_relations: Dict[str, Dict[str, float]]  # -1.0 to 1.0
    location_states: Dict[str, Dict[str, Any]]
    last_update: float

@dataclass
class DynamicEvent:
    event_id: str
    category: EventCategory
    severity: EventSeverity
    location: str
    description: str
    triggers: Dict[str, Any]
    consequences: Dict[str, Any]
    duration: float
    start_time: float
    active: bool = True
    resolved: bool = False

class QuestState(Enum):
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"

@dataclass
class QuestEvent:
    quest_id: str
    title: str
    description: str
    requirements: Dict[str, Any]
    rewards: Dict[str, Any]
    state: QuestState
    linked_events: List[str]
    expiry_time: Optional[float]
    completion_conditions: Dict[str, Any]

class DynamicEventsSystem:
    def __init__(self, weather_system: WeatherSystem, economic_system: EconomicSystem):
        self.weather_system = weather_system
        self.economic_system = economic_system
        self.world_state = self._initialize_world_state()
        self.active_events: Dict[str, DynamicEvent] = {}
        self.event_history: List[DynamicEvent] = []
        self.active_quests: Dict[str, QuestEvent] = {}
        self.completed_quests: List[QuestEvent] = []
        self.event_handlers = self._initialize_event_handlers()
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("DynamicEventsSystem")
        logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler("logs/events.log")
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        logger.addHandler(handler)
        return logger
        
    def _initialize_world_state(self) -> WorldState:
        """Initialize default world state"""
        return WorldState(
            metrics={
                WorldStateMetric.STABILITY: 0.7,
                WorldStateMetric.PROSPERITY: 0.6,
                WorldStateMetric.DANGER_LEVEL: 0.3,
                WorldStateMetric.MORALE: 0.6,
                WorldStateMetric.CORRUPTION: 0.2,
                WorldStateMetric.MAGIC_SATURATION: 0.5
            },
            active_effects=set(),
            faction_relations={},
            location_states={},
            last_update=time.time()
        )
        
    def _initialize_event_handlers(self) -> Dict[EventCategory, List[Callable]]:
        """Initialize event generation handlers for each category"""
        return {
            EventCategory.NATURAL: [
                self._generate_weather_disaster,
                self._generate_natural_blessing
            ],
            EventCategory.ECONOMIC: [
                self._generate_market_crisis,
                self._generate_trade_opportunity
            ],
            EventCategory.SOCIAL: [
                self._generate_festival,
                self._generate_unrest
            ],
            EventCategory.POLITICAL: [
                self._generate_faction_conflict,
                self._generate_diplomatic_event
            ],
            EventCategory.MILITARY: [
                self._generate_bandit_raid,
                self._generate_monster_attack
            ],
            EventCategory.SUPERNATURAL: [
                self._generate_magical_phenomenon,
                self._generate_divine_intervention
            ]
        }
        
    def update(self, delta_time: float):
        """Update world state and generate events"""
        current_time = time.time()
        
        # Update world state
        self._update_world_state(delta_time)
        
        # Process active events
        self._process_active_events(current_time)
        
        # Generate new events
        self._generate_events()
        
        # Update quests
        self._update_quests(current_time)
        
    def _update_world_state(self, delta_time: float):
        """Update world state based on active events and conditions"""
        # Update metrics based on active effects
        for effect in self.world_state.active_effects:
            self._apply_world_effect(effect, delta_time)
            
        # Update location states
        for location in self.world_state.location_states:
            self._update_location_state(location, delta_time)
            
        # Normalize metrics
        for metric in self.world_state.metrics:
            self.world_state.metrics[metric] = max(0.0, min(1.0, self.world_state.metrics[metric]))
            
        self.world_state.last_update = time.time()
        
    def _process_active_events(self, current_time: float):
        """Process and update active events"""
        expired_events = []
        
        for event_id, event in self.active_events.items():
            if not event.active:
                continue
                
            # Check if event has expired
            if current_time - event.start_time >= event.duration:
                self._resolve_event(event)
                expired_events.append(event_id)
                continue
                
            # Apply ongoing effects
            self._apply_event_effects(event)
            
        # Remove expired events
        for event_id in expired_events:
            event = self.active_events.pop(event_id)
            event.active = False
            self.event_history.append(event)
            
    def _generate_events(self):
        """Generate new events based on current conditions"""
        for category in EventCategory:
            if self._should_generate_event(category):
                handlers = self.event_handlers[category]
                for handler in handlers:
                    if random.random() < 0.3:  # 30% chance per handler
                        event = handler()
                        if event:
                            self._add_event(event)
                            
    def _should_generate_event(self, category: EventCategory) -> bool:
        """Determine if a new event should be generated for a category"""
        base_chance = 0.1  # 10% base chance
        
        # Modify chance based on world state
        if category == EventCategory.NATURAL:
            base_chance += (1.0 - self.world_state.metrics[WorldStateMetric.STABILITY]) * 0.2
        elif category == EventCategory.ECONOMIC:
            base_chance += (1.0 - self.world_state.metrics[WorldStateMetric.PROSPERITY]) * 0.2
        elif category == EventCategory.SOCIAL:
            base_chance += (1.0 - self.world_state.metrics[WorldStateMetric.MORALE]) * 0.2
        elif category == EventCategory.SUPERNATURAL:
            base_chance += self.world_state.metrics[WorldStateMetric.MAGIC_SATURATION] * 0.2
            
        return random.random() < base_chance
        
    def _add_event(self, event: DynamicEvent):
        """Add a new event to the system"""
        self.active_events[event.event_id] = event
        self._trigger_event_consequences(event)
        
        # Generate related quests
        self._generate_related_quests(event)
        
        self.logger.info(
            f"New event: {event.category.value} - {event.severity.value} "
            f"at {event.location}"
        )
        
    def _resolve_event(self, event: DynamicEvent):
        """Resolve an event and apply final consequences"""
        event.resolved = True
        
        # Apply resolution effects
        if "resolution_effects" in event.consequences:
            for effect in event.consequences["resolution_effects"]:
                self._apply_resolution_effect(effect)
                
        self.logger.info(f"Resolved event: {event.event_id}")
        
    def _generate_weather_disaster(self) -> Optional[DynamicEvent]:
        """Generate a weather-related disaster event"""
        if not self.weather_system.current_weather:
            return None
            
        current_weather = self.weather_system.current_weather
        
        if current_weather.weather_type in [WeatherType.STORM, WeatherType.BLIZZARD]:
            return DynamicEvent(
                event_id=f"weather_disaster_{int(time.time())}",
                category=EventCategory.NATURAL,
                severity=EventSeverity.MAJOR,
                location="global",
                description=f"Severe {current_weather.weather_type.value} causing widespread disruption",
                triggers={
                    "weather_type": current_weather.weather_type.value,
                    "intensity": current_weather.intensity
                },
                consequences={
                    "trade_route_disruption": 0.8,
                    "resource_damage": {
                        ResourceType.FOOD.value: 0.3,
                        ResourceType.WOOD.value: 0.2
                    },
                    "stability_impact": -0.2
                },
                duration=current_weather.duration * 0.5,
                start_time=time.time()
            )
        return None
        
    def _generate_natural_blessing(self) -> Optional[DynamicEvent]:
        """Generate a positive natural event"""
        if random.random() > 0.3:  # 30% chance
            return None
            
        return DynamicEvent(
            event_id=f"natural_blessing_{int(time.time())}",
            category=EventCategory.NATURAL,
            severity=EventSeverity.MODERATE,
            location="global",
            description="Favorable conditions leading to increased prosperity",
            triggers={
                "season": self.weather_system.current_season.value
            },
            consequences={
                "resource_boost": {
                    ResourceType.FOOD.value: 0.2,
                    ResourceType.WOOD.value: 0.2
                },
                "morale_boost": 0.1
            },
            duration=86400,  # 24 hours
            start_time=time.time()
        )
        
    def _generate_market_crisis(self) -> Optional[DynamicEvent]:
        """Generate an economic crisis event"""
        if self.world_state.metrics[WorldStateMetric.PROSPERITY] > 0.7:
            return None
            
        affected_resources = random.sample(
            [r.value for r in ResourceType],
            k=random.randint(2, 4)
        )
        
        return DynamicEvent(
            event_id=f"market_crisis_{int(time.time())}",
            category=EventCategory.ECONOMIC,
            severity=EventSeverity.MAJOR,
            location="global",
            description="Economic crisis affecting multiple markets",
            triggers={
                "prosperity": self.world_state.metrics[WorldStateMetric.PROSPERITY],
                "affected_resources": affected_resources
            },
            consequences={
                "price_multiplier": 1.5,
                "supply_reduction": 0.5,
                "stability_impact": -0.1
            },
            duration=43200,  # 12 hours
            start_time=time.time()
        )
        
    def _generate_trade_opportunity(self) -> Optional[DynamicEvent]:
        """Generate a positive trade event"""
        if random.random() > 0.4:  # 40% chance
            return None
            
        return DynamicEvent(
            event_id=f"trade_opportunity_{int(time.time())}",
            category=EventCategory.ECONOMIC,
            severity=EventSeverity.MODERATE,
            location="global",
            description="Favorable trade conditions emerge",
            triggers={
                "prosperity": self.world_state.metrics[WorldStateMetric.PROSPERITY]
            },
            consequences={
                "trade_cost_multiplier": 0.8,
                "demand_boost": 1.2,
                "prosperity_boost": 0.1
            },
            duration=21600,  # 6 hours
            start_time=time.time()
        )
        
    def _apply_event_effects(self, event: DynamicEvent):
        """Apply ongoing effects of an active event"""
        if "trade_route_disruption" in event.consequences:
            self._apply_trade_disruption(event.consequences["trade_route_disruption"])
            
        if "resource_damage" in event.consequences:
            self._apply_resource_damage(event.consequences["resource_damage"])
            
        if "stability_impact" in event.consequences:
            self.world_state.metrics[WorldStateMetric.STABILITY] += \
                event.consequences["stability_impact"] * 0.1
                
        if "morale_boost" in event.consequences:
            self.world_state.metrics[WorldStateMetric.MORALE] += \
                event.consequences["morale_boost"] * 0.1
                
    def _apply_trade_disruption(self, severity: float):
        """Apply trade route disruption effects"""
        for route in self.economic_system.trade_routes:
            if random.random() < severity:
                route.active = False
                
    def _apply_resource_damage(self, damage_map: Dict[str, float]):
        """Apply damage to resources across markets"""
        for location, market in self.economic_system.markets.items():
            for resource_type, damage in damage_map.items():
                if resource_type in market:
                    market[ResourceType(resource_type)].quantity *= (1 - damage)
                    
    def _update_quests(self, current_time: float):
        """Update quest states and check completion conditions"""
        expired_quests = []
        
        for quest_id, quest in self.active_quests.items():
            if quest.state != QuestState.ACTIVE:
                continue
                
            # Check for expiry
            if quest.expiry_time and current_time > quest.expiry_time:
                quest.state = QuestState.EXPIRED
                expired_quests.append(quest_id)
                continue
                
            # Check completion conditions
            if self._check_quest_completion(quest):
                self._complete_quest(quest)
                expired_quests.append(quest_id)
                
        # Remove completed/expired quests
        for quest_id in expired_quests:
            quest = self.active_quests.pop(quest_id)
            self.completed_quests.append(quest)
            
    def _generate_related_quests(self, event: DynamicEvent):
        """Generate quests related to an event"""
        if event.severity in [EventSeverity.MAJOR, EventSeverity.CRITICAL]:
            quest = self._create_event_quest(event)
            if quest:
                self.active_quests[quest.quest_id] = quest
                
    def _create_event_quest(self, event: DynamicEvent) -> Optional[QuestEvent]:
        """Create a quest based on an event"""
        if event.category == EventCategory.NATURAL:
            return self._create_disaster_relief_quest(event)
        elif event.category == EventCategory.ECONOMIC:
            return self._create_economic_quest(event)
        elif event.category == EventCategory.MILITARY:
            return self._create_combat_quest(event)
        return None
        
    def _create_disaster_relief_quest(self, event: DynamicEvent) -> QuestEvent:
        """Create a disaster relief quest"""
        return QuestEvent(
            quest_id=f"relief_{event.event_id}",
            title=f"Disaster Relief: {event.location}",
            description=f"Help the people affected by the {event.description}",
            requirements={
                "min_level": 5,
                "required_items": {
                    ResourceType.FOOD.value: 100,
                    ResourceType.POTION.value: 50
                }
            },
            rewards={
                "experience": 1000,
                "gold": 500,
                "reputation": 100
            },
            state=QuestState.AVAILABLE,
            linked_events=[event.event_id],
            expiry_time=event.start_time + event.duration,
            completion_conditions={
                "items_delivered": False,
                "people_helped": 0,
                "target_helped": 10
            }
        )
        
    def _create_economic_quest(self, event: DynamicEvent) -> QuestEvent:
        """Create an economic recovery quest"""
        return QuestEvent(
            quest_id=f"economic_{event.event_id}",
            title="Market Stabilization",
            description="Help stabilize the market by trading specific goods",
            requirements={
                "min_level": 8,
                "trading_skill": 3
            },
            rewards={
                "experience": 1500,
                "gold": 1000,
                "trading_skill_exp": 200
            },
            state=QuestState.AVAILABLE,
            linked_events=[event.event_id],
            expiry_time=event.start_time + event.duration * 0.75,
            completion_conditions={
                "trades_completed": 0,
                "target_trades": 5,
                "profit_made": 0,
                "target_profit": 1000
            }
        )
        
    def _check_quest_completion(self, quest: QuestEvent) -> bool:
        """Check if a quest's completion conditions are met"""
        conditions = quest.completion_conditions
        
        if "items_delivered" in conditions:
            if not conditions["items_delivered"]:
                return False
                
        if "people_helped" in conditions:
            if conditions["people_helped"] < conditions["target_helped"]:
                return False
                
        if "trades_completed" in conditions:
            if conditions["trades_completed"] < conditions["target_trades"]:
                return False
                
        if "profit_made" in conditions:
            if conditions["profit_made"] < conditions["target_profit"]:
                return False
                
        return True
        
    def _complete_quest(self, quest: QuestEvent):
        """Complete a quest and grant rewards"""
        quest.state = QuestState.COMPLETED
        
        # Apply rewards (would be handled by player system)
        self.logger.info(f"Completed quest: {quest.quest_id}")
        
    def get_active_events(self, location: Optional[str] = None) -> List[DynamicEvent]:
        """Get list of active events, optionally filtered by location"""
        if location:
            return [
                event for event in self.active_events.values()
                if event.active and event.location == location
            ]
        return [event for event in self.active_events.values() if event.active]
        
    def get_available_quests(self, player_level: int) -> List[QuestEvent]:
        """Get list of available quests for player level"""
        return [
            quest for quest in self.active_quests.values()
            if quest.state == QuestState.AVAILABLE and
            quest.requirements.get("min_level", 0) <= player_level
        ]
        
    def get_world_state_report(self) -> Dict[str, Any]:
        """Get current world state report"""
        return {
            "metrics": {
                metric.value: value
                for metric, value in self.world_state.metrics.items()
            },
            "active_effects": list(self.world_state.active_effects),
            "active_events_count": len([e for e in self.active_events.values() if e.active]),
            "available_quests_count": len([q for q in self.active_quests.values() if q.state == QuestState.AVAILABLE])
        }
        
    def export_world_state(self, file_path: str):
        """Export world state and events data"""
        data = {
            "world_state": {
                "metrics": {
                    metric.value: value
                    for metric, value in self.world_state.metrics.items()
                },
                "active_effects": list(self.world_state.active_effects),
                "faction_relations": self.world_state.faction_relations,
                "location_states": self.world_state.location_states,
                "last_update": self.world_state.last_update
            },
            "active_events": [
                {
                    "event_id": event.event_id,
                    "category": event.category.value,
                    "severity": event.severity.value,
                    "location": event.location,
                    "description": event.description,
                    "triggers": event.triggers,
                    "consequences": event.consequences,
                    "duration": event.duration,
                    "start_time": event.start_time,
                    "active": event.active,
                    "resolved": event.resolved
                }
                for event in self.active_events.values()
            ],
            "active_quests": [
                {
                    "quest_id": quest.quest_id,
                    "title": quest.title,
                    "description": quest.description,
                    "requirements": quest.requirements,
                    "rewards": quest.rewards,
                    "state": quest.state.value,
                    "linked_events": quest.linked_events,
                    "expiry_time": quest.expiry_time,
                    "completion_conditions": quest.completion_conditions
                }
                for quest in self.active_quests.values()
            ]
        }
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
            
    def import_world_state(self, file_path: str):
        """Import world state and events data"""
        with open(file_path, "r") as f:
            data = json.load(f)
            
        # Import world state
        self.world_state = WorldState(
            metrics={
                WorldStateMetric(k): v
                for k, v in data["world_state"]["metrics"].items()
            },
            active_effects=set(data["world_state"]["active_effects"]),
            faction_relations=data["world_state"]["faction_relations"],
            location_states=data["world_state"]["location_states"],
            last_update=data["world_state"]["last_update"]
        )
        
        # Import active events
        self.active_events = {
            event_data["event_id"]: DynamicEvent(
                event_id=event_data["event_id"],
                category=EventCategory(event_data["category"]),
                severity=EventSeverity(event_data["severity"]),
                location=event_data["location"],
                description=event_data["description"],
                triggers=event_data["triggers"],
                consequences=event_data["consequences"],
                duration=event_data["duration"],
                start_time=event_data["start_time"],
                active=event_data["active"],
                resolved=event_data["resolved"]
            )
            for event_data in data["active_events"]
        }
        
        # Import active quests
        self.active_quests = {
            quest_data["quest_id"]: QuestEvent(
                quest_id=quest_data["quest_id"],
                title=quest_data["title"],
                description=quest_data["description"],
                requirements=quest_data["requirements"],
                rewards=quest_data["rewards"],
                state=QuestState(quest_data["state"]),
                linked_events=quest_data["linked_events"],
                expiry_time=quest_data["expiry_time"],
                completion_conditions=quest_data["completion_conditions"]
            )
            for quest_data in data["active_quests"]
        } 
        
    def _generate_festival(self) -> Optional[DynamicEvent]:
        """Generate a festival event"""
        if self.world_state.metrics[WorldStateMetric.MORALE] > 0.8:
            return None  # Already high morale
            
        festival_types = [
            "Harvest Festival",
            "Spring Fair",
            "Midsummer Celebration",
            "Winter Solstice",
            "Founding Day"
        ]
        
        return DynamicEvent(
            event_id=f"festival_{int(time.time())}",
            category=EventCategory.SOCIAL,
            severity=EventSeverity.MODERATE,
            location="global",
            description=f"{random.choice(festival_types)} brings joy to the people",
            triggers={
                "morale": self.world_state.metrics[WorldStateMetric.MORALE],
                "season": self.weather_system.current_season.value
            },
            consequences={
                "morale_boost": 0.2,
                "trade_boost": 0.1,
                "prosperity_boost": 0.05,
                "resource_consumption": {
                    ResourceType.FOOD.value: 0.1,
                    ResourceType.GOLD.value: 0.1
                }
            },
            duration=86400,  # 24 hours
            start_time=time.time()
        )
        
    def _generate_unrest(self) -> Optional[DynamicEvent]:
        """Generate social unrest event"""
        if (self.world_state.metrics[WorldStateMetric.STABILITY] > 0.6 or
            self.world_state.metrics[WorldStateMetric.MORALE] > 0.7):
            return None
            
        causes = [
            "high taxes",
            "food shortages",
            "corruption",
            "harsh laws",
            "military conscription"
        ]
        
        return DynamicEvent(
            event_id=f"unrest_{int(time.time())}",
            category=EventCategory.SOCIAL,
            severity=EventSeverity.MAJOR,
            location="global",
            description=f"Civil unrest due to {random.choice(causes)}",
            triggers={
                "stability": self.world_state.metrics[WorldStateMetric.STABILITY],
                "morale": self.world_state.metrics[WorldStateMetric.MORALE]
            },
            consequences={
                "stability_impact": -0.2,
                "trade_disruption": 0.3,
                "prosperity_impact": -0.1,
                "corruption_boost": 0.1
            },
            duration=43200,  # 12 hours
            start_time=time.time()
        )
        
    def _generate_faction_conflict(self) -> Optional[DynamicEvent]:
        """Generate political conflict between factions"""
        if self.world_state.metrics[WorldStateMetric.STABILITY] > 0.8:
            return None
            
        factions = list(self.world_state.faction_relations.keys())
        if len(factions) < 2:
            return None
            
        faction1, faction2 = random.sample(factions, 2)
        
        conflict_types = [
            "trade dispute",
            "border conflict",
            "diplomatic incident",
            "resource rights",
            "political influence"
        ]
        
        return DynamicEvent(
            event_id=f"faction_conflict_{int(time.time())}",
            category=EventCategory.POLITICAL,
            severity=EventSeverity.MAJOR,
            location="global",
            description=f"{faction1} and {faction2} in conflict over {random.choice(conflict_types)}",
            triggers={
                "stability": self.world_state.metrics[WorldStateMetric.STABILITY],
                "factions": [faction1, faction2]
            },
            consequences={
                "faction_relations": {
                    f"{faction1}_{faction2}": -0.2
                },
                "stability_impact": -0.1,
                "trade_impact": -0.1
            },
            duration=172800,  # 48 hours
            start_time=time.time()
        )
        
    def _generate_diplomatic_event(self) -> Optional[DynamicEvent]:
        """Generate positive diplomatic event"""
        factions = list(self.world_state.faction_relations.keys())
        if len(factions) < 2:
            return None
            
        faction1, faction2 = random.sample(factions, 2)
        
        event_types = [
            "trade agreement",
            "peace treaty",
            "cultural exchange",
            "royal marriage",
            "mutual defense pact"
        ]
        
        return DynamicEvent(
            event_id=f"diplomatic_{int(time.time())}",
            category=EventCategory.POLITICAL,
            severity=EventSeverity.MODERATE,
            location="global",
            description=f"{faction1} and {faction2} establish {random.choice(event_types)}",
            triggers={
                "factions": [faction1, faction2]
            },
            consequences={
                "faction_relations": {
                    f"{faction1}_{faction2}": 0.2
                },
                "stability_boost": 0.1,
                "prosperity_boost": 0.1,
                "trade_boost": 0.2
            },
            duration=259200,  # 72 hours
            start_time=time.time()
        )
        
    def _generate_bandit_raid(self) -> Optional[DynamicEvent]:
        """Generate bandit raid event"""
        if self.world_state.metrics[WorldStateMetric.DANGER_LEVEL] < 0.3:
            return None
            
        targets = [
            "trade caravan",
            "village",
            "mining camp",
            "farmland",
            "outpost"
        ]
        
        return DynamicEvent(
            event_id=f"bandit_raid_{int(time.time())}",
            category=EventCategory.MILITARY,
            severity=EventSeverity.MODERATE,
            location="global",
            description=f"Bandits attacking {random.choice(targets)}",
            triggers={
                "danger_level": self.world_state.metrics[WorldStateMetric.DANGER_LEVEL]
            },
            consequences={
                "resource_damage": {
                    ResourceType.GOLD.value: 0.1,
                    ResourceType.FOOD.value: 0.1
                },
                "trade_disruption": 0.2,
                "stability_impact": -0.1
            },
            duration=14400,  # 4 hours
            start_time=time.time()
        )
        
    def _generate_monster_attack(self) -> Optional[DynamicEvent]:
        """Generate monster attack event"""
        if self.world_state.metrics[WorldStateMetric.DANGER_LEVEL] < 0.5:
            return None
            
        monsters = [
            "Dragon",
            "Giant",
            "Demon",
            "Undead Horde",
            "Elemental Beast"
        ]
        
        return DynamicEvent(
            event_id=f"monster_attack_{int(time.time())}",
            category=EventCategory.MILITARY,
            severity=EventSeverity.CRITICAL,
            location="global",
            description=f"{random.choice(monsters)} attacking the region",
            triggers={
                "danger_level": self.world_state.metrics[WorldStateMetric.DANGER_LEVEL],
                "magic_saturation": self.world_state.metrics[WorldStateMetric.MAGIC_SATURATION]
            },
            consequences={
                "resource_damage": {
                    ResourceType.FOOD.value: 0.3,
                    ResourceType.WOOD.value: 0.3,
                    ResourceType.GOLD.value: 0.2
                },
                "stability_impact": -0.3,
                "morale_impact": -0.2,
                "danger_level_boost": 0.2
            },
            duration=28800,  # 8 hours
            start_time=time.time()
        )
        
    def _generate_magical_phenomenon(self) -> Optional[DynamicEvent]:
        """Generate magical phenomenon event"""
        if self.world_state.metrics[WorldStateMetric.MAGIC_SATURATION] < 0.6:
            return None
            
        phenomena = [
            "arcane storm",
            "magical surge",
            "planar convergence",
            "mana crystallization",
            "ethereal aurora"
        ]
        
        effects = [
            "enhancing magical abilities",
            "causing strange mutations",
            "creating magical anomalies",
            "altering the local reality",
            "summoning magical creatures"
        ]
        
        return DynamicEvent(
            event_id=f"magical_{int(time.time())}",
            category=EventCategory.SUPERNATURAL,
            severity=EventSeverity.MAJOR,
            location="global",
            description=f"{random.choice(phenomena)} {random.choice(effects)}",
            triggers={
                "magic_saturation": self.world_state.metrics[WorldStateMetric.MAGIC_SATURATION]
            },
            consequences={
                "magic_saturation_boost": 0.2,
                "resource_boost": {
                    ResourceType.MITHRIL.value: 0.3,
                    ResourceType.STARDUST.value: 0.2
                },
                "danger_level_boost": 0.1
            },
            duration=21600,  # 6 hours
            start_time=time.time()
        )
        
    def _generate_divine_intervention(self) -> Optional[DynamicEvent]:
        """Generate divine intervention event"""
        if random.random() > 0.1:  # Rare event, 10% base chance
            return None
            
        interventions = [
            "divine blessing",
            "holy miracle",
            "celestial sign",
            "prophetic vision",
            "divine judgment"
        ]
        
        is_positive = random.random() < 0.7  # 70% chance of positive intervention
        
        consequences = {
            "morale_boost": 0.3 if is_positive else -0.3,
            "stability_impact": 0.2 if is_positive else -0.2,
            "magic_saturation_boost": 0.2,
            "resource_boost": {
                ResourceType.FOOD.value: 0.2 if is_positive else -0.2,
                ResourceType.POTION.value: 0.3 if is_positive else -0.3
            }
        }
        
        return DynamicEvent(
            event_id=f"divine_{int(time.time())}",
            category=EventCategory.SUPERNATURAL,
            severity=EventSeverity.CRITICAL,
            location="global",
            description=f"A {random.choice(interventions)} affects the realm",
            triggers={
                "magic_saturation": self.world_state.metrics[WorldStateMetric.MAGIC_SATURATION],
                "stability": self.world_state.metrics[WorldStateMetric.STABILITY]
            },
            consequences=consequences,
            duration=43200,  # 12 hours
            start_time=time.time()
        )
        
    def _create_combat_quest(self, event: DynamicEvent) -> QuestEvent:
        """Create a combat-related quest"""
        if event.category != EventCategory.MILITARY:
            return None
            
        is_monster = "monster" in event.description.lower()
        
        return QuestEvent(
            quest_id=f"combat_{event.event_id}",
            title=f"{'Monster Slaying' if is_monster else 'Bandit Hunt'}: {event.location}",
            description=f"Defeat the threat described in: {event.description}",
            requirements={
                "min_level": 15 if is_monster else 10,
                "combat_skill": 5 if is_monster else 3
            },
            rewards={
                "experience": 2000 if is_monster else 1000,
                "gold": 1500 if is_monster else 800,
                "reputation": 200 if is_monster else 100,
                "special_item": True if is_monster else False
            },
            state=QuestState.AVAILABLE,
            linked_events=[event.event_id],
            expiry_time=event.start_time + event.duration * 0.75,
            completion_conditions={
                "enemies_defeated": 0,
                "target_defeats": 1 if is_monster else 5,
                "area_cleared": False
            }
        ) 