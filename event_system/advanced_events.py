from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from .event_manager import Event, EventType, EventTrigger, EventRequirements, EventEffects
from .specialized_events import SpecializedEventType

class AdvancedEventType(Enum):
    # Combat Integration Events
    LEGENDARY_BATTLE = "legendary_battle"
    SIEGE_WARFARE = "siege_warfare"
    GUERRILLA_WARFARE = "guerrilla_warfare"
    NAVAL_COMBAT = "naval_combat"
    
    # Economic Events
    MARKET_CRASH = "market_crash"
    RESOURCE_BOOM = "resource_boom"
    TRADE_REVOLUTION = "trade_revolution"
    BLACK_MARKET_SURGE = "black_market_surge"
    
    # Magical Research Events
    ARCANE_BREAKTHROUGH = "arcane_breakthrough"
    MAGICAL_CATASTROPHE = "magical_catastrophe"
    SPELL_EVOLUTION = "spell_evolution"
    ARTIFACT_AWAKENING = "artifact_awakening"
    
    # Dynamic World Events
    CITY_EVOLUTION = "city_evolution"
    TERRITORY_TRANSFORMATION = "territory_transformation"
    FACTION_METAMORPHOSIS = "faction_metamorphosis"
    DIVINE_INTERVENTION = "divine_intervention"

@dataclass
class CombatEventData:
    battle_type: str
    participating_armies: Dict[str, float]  # faction -> army strength
    terrain_modifiers: Dict[str, float]
    weather_conditions: List[str]
    strategic_objectives: Dict[str, str]  # faction -> objective
    duration_hours: int
    reinforcement_chances: Dict[str, float]

@dataclass
class EconomicEventData:
    affected_markets: List[str]
    price_modifiers: Dict[str, float]  # resource -> price change
    trade_route_impacts: Dict[str, bool]  # route -> active status
    merchant_faction_responses: Dict[str, str]
    duration_days: int
    recovery_rate: float

@dataclass
class MagicalResearchData:
    research_type: str
    participating_mages: List[str]
    power_level: float
    risk_factor: float
    potential_discoveries: List[str]
    affected_schools: List[str]
    duration_hours: int

@dataclass
class WorldTransformationData:
    transformation_type: str
    affected_regions: List[str]
    intensity: float
    permanent_changes: Dict[str, str]  # region -> change
    faction_reactions: Dict[str, str]
    duration_days: int

class AdvancedEventFactory:
    def __init__(self):
        self.event_counter = 0

    def create_combat_event(self, event_type: AdvancedEventType, data: CombatEventData) -> Event:
        """Create an advanced combat event"""
        self.event_counter += 1
        event_id = f"advanced_combat_{event_type.value}_{self.event_counter}"
        
        # Calculate total army strength for each faction
        total_strength = sum(data.participating_armies.values())
        
        requirements = EventRequirements(
            faction_reputation={
                faction: int(20 * (strength / total_strength))
                for faction, strength in data.participating_armies.items()
            },
            environmental_conditions=data.weather_conditions
        )
        
        effects = EventEffects(
            faction_reputation_changes={
                faction: 30 if "victory" in data.strategic_objectives[faction].lower() else -10
                for faction in data.participating_armies.keys()
            },
            territory_effects={
                objective: f"contested_{faction}"
                for faction, objective in data.strategic_objectives.items()
            }
        )
        
        return Event(
            event_id=event_id,
            name=f"Advanced Combat: {event_type.value.title()}",
            event_type=EventType.COMBAT,
            trigger=EventTrigger.FACTION_ACTION,
            requirements=requirements,
            effects=effects,
            duration=data.duration_hours * 3600,
            cooldown=data.duration_hours * 7200
        )

    def create_economic_event(self, event_type: AdvancedEventType, data: EconomicEventData) -> Event:
        """Create an advanced economic event"""
        self.event_counter += 1
        event_id = f"advanced_economic_{event_type.value}_{self.event_counter}"
        
        requirements = EventRequirements(
            faction_reputation={
                faction: 15 for faction in data.merchant_faction_responses.keys()
            }
        )
        
        effects = EventEffects(
            resource_changes={
                resource: change for resource, change in data.price_modifiers.items()
            },
            faction_reputation_changes={
                faction: 20 if "positive" in response.lower() else -15
                for faction, response in data.merchant_faction_responses.items()
            }
        )
        
        return Event(
            event_id=event_id,
            name=f"Economic Event: {event_type.value.title()}",
            event_type=EventType.FACTION,
            trigger=EventTrigger.DYNAMIC,
            requirements=requirements,
            effects=effects,
            duration=data.duration_days * 86400,
            cooldown=data.duration_days * 172800
        )

    def create_magical_research_event(self, event_type: AdvancedEventType, data: MagicalResearchData) -> Event:
        """Create an advanced magical research event"""
        self.event_counter += 1
        event_id = f"advanced_magical_{event_type.value}_{self.event_counter}"
        
        requirements = EventRequirements(
            celestial_alignment="research_favorable",
            environmental_conditions=[f"high_magic_{school}" for school in data.affected_schools]
        )
        
        effects = EventEffects(
            celestial_effects=[f"magical_surge_{school}" for school in data.affected_schools],
            environmental_changes=[
                f"arcane_disturbance_{data.power_level}",
                f"research_progress_{data.research_type}"
            ]
        )
        
        return Event(
            event_id=event_id,
            name=f"Magical Research: {event_type.value.title()}",
            event_type=EventType.RITUAL,
            trigger=EventTrigger.RITUAL_COMPLETION,
            requirements=requirements,
            effects=effects,
            duration=data.duration_hours * 3600,
            cooldown=data.duration_hours * 7200
        )

    def create_world_transformation_event(self, event_type: AdvancedEventType, data: WorldTransformationData) -> Event:
        """Create an advanced world transformation event"""
        self.event_counter += 1
        event_id = f"advanced_world_{event_type.value}_{self.event_counter}"
        
        requirements = EventRequirements(
            environmental_conditions=[f"transformation_catalyst_{data.transformation_type}"],
            faction_reputation={
                faction: 25 for faction in data.faction_reactions.keys()
            }
        )
        
        effects = EventEffects(
            environmental_changes=[f"world_shift_{data.intensity}"],
            territory_effects={
                region: change for region, change in data.permanent_changes.items()
            },
            faction_reputation_changes={
                faction: 30 if "embrace" in reaction.lower() else -20
                for faction, reaction in data.faction_reactions.items()
            }
        )
        
        return Event(
            event_id=event_id,
            name=f"World Transformation: {event_type.value.title()}",
            event_type=EventType.ENVIRONMENTAL,
            trigger=EventTrigger.ENVIRONMENTAL_CONDITION,
            requirements=requirements,
            effects=effects,
            duration=data.duration_days * 86400,
            cooldown=data.duration_days * 172800
        )

class AdvancedScenarioGenerator:
    def __init__(self, factory: AdvancedEventFactory):
        self.factory = factory

    def generate_epic_warfare_scenario(self) -> List[Event]:
        """Generate an epic warfare scenario with multiple battle types"""
        events = []
        
        # Initial guerrilla warfare
        guerrilla_data = CombatEventData(
            battle_type="guerrilla",
            participating_armies={
                "rebels": 0.4,
                "empire": 0.8
            },
            terrain_modifiers={
                "forest": 1.5,
                "mountains": 1.3
            },
            weather_conditions=["rain", "fog"],
            strategic_objectives={
                "rebels": "weaken_supply_lines",
                "empire": "secure_territory"
            },
            duration_hours=48,
            reinforcement_chances={"rebels": 0.3, "empire": 0.6}
        )
        events.append(self.factory.create_combat_event(
            AdvancedEventType.GUERRILLA_WARFARE,
            guerrilla_data
        ))
        
        # Escalate to siege warfare
        siege_data = CombatEventData(
            battle_type="siege",
            participating_armies={
                "rebels": 0.7,
                "empire": 0.9,
                "mercenaries": 0.4
            },
            terrain_modifiers={
                "city_walls": 2.0,
                "gates": 1.5
            },
            weather_conditions=["clear", "windy"],
            strategic_objectives={
                "rebels": "capture_city",
                "empire": "defend_city",
                "mercenaries": "raid_supplies"
            },
            duration_hours=72,
            reinforcement_chances={"rebels": 0.5, "empire": 0.8, "mercenaries": 0.3}
        )
        events.append(self.factory.create_combat_event(
            AdvancedEventType.SIEGE_WARFARE,
            siege_data
        ))
        
        # Culminate in legendary battle
        legendary_data = CombatEventData(
            battle_type="legendary",
            participating_armies={
                "rebels": 1.0,
                "empire": 1.0,
                "mercenaries": 0.6,
                "neutral_factions": 0.4
            },
            terrain_modifiers={
                "plains": 1.0,
                "high_ground": 1.4,
                "river": 0.8
            },
            weather_conditions=["storm", "lightning"],
            strategic_objectives={
                "rebels": "decisive_victory",
                "empire": "crush_rebellion",
                "mercenaries": "maximize_profit",
                "neutral_factions": "maintain_balance"
            },
            duration_hours=24,
            reinforcement_chances={"rebels": 0.9, "empire": 0.9, "mercenaries": 0.5}
        )
        events.append(self.factory.create_combat_event(
            AdvancedEventType.LEGENDARY_BATTLE,
            legendary_data
        ))
        
        return events

    def generate_magical_catastrophe_scenario(self) -> List[Event]:
        """Generate a magical catastrophe scenario"""
        events = []
        
        # Initial magical breakthrough
        breakthrough_data = MagicalResearchData(
            research_type="forbidden_magic",
            participating_mages=["arch_mage", "dark_researcher", "rogue_wizard"],
            power_level=0.8,
            risk_factor=0.7,
            potential_discoveries=["void_magic", "time_manipulation"],
            affected_schools=["void", "temporal"],
            duration_hours=12
        )
        events.append(self.factory.create_magical_research_event(
            AdvancedEventType.ARCANE_BREAKTHROUGH,
            breakthrough_data
        ))
        
        # Escalating magical catastrophe
        catastrophe_data = MagicalResearchData(
            research_type="containment_breach",
            participating_mages=["all_available_mages"],
            power_level=0.95,
            risk_factor=0.9,
            potential_discoveries=["magical_containment", "power_suppression"],
            affected_schools=["all_schools"],
            duration_hours=24
        )
        events.append(self.factory.create_magical_research_event(
            AdvancedEventType.MAGICAL_CATASTROPHE,
            catastrophe_data
        ))
        
        # World transformation aftermath
        transformation_data = WorldTransformationData(
            transformation_type="magical_restructuring",
            affected_regions=["mage_quarter", "surrounding_territories", "ley_line_nexus"],
            intensity=0.85,
            permanent_changes={
                "mage_quarter": "permanently_altered",
                "ley_line_nexus": "restructured",
                "surrounding_territories": "magically_saturated"
            },
            faction_reactions={
                "mage_council": "emergency_protocols",
                "city_council": "evacuation_order",
                "merchants_guild": "profit_opportunity",
                "religious_order": "divine_intervention"
            },
            duration_days=7
        )
        events.append(self.factory.create_world_transformation_event(
            AdvancedEventType.TERRITORY_TRANSFORMATION,
            transformation_data
        ))
        
        return events

    def generate_economic_crisis_scenario(self) -> List[Event]:
        """Generate an economic crisis scenario"""
        events = []
        
        # Initial market crash
        crash_data = EconomicEventData(
            affected_markets=["luxury_goods", "magical_items", "raw_materials"],
            price_modifiers={
                "luxury_goods": -0.4,
                "magical_items": -0.3,
                "raw_materials": -0.2
            },
            trade_route_impacts={
                "northern_route": False,
                "silk_road": True,
                "sea_route": True
            },
            merchant_faction_responses={
                "merchant_guild": "emergency_measures",
                "trade_federation": "market_manipulation",
                "smugglers": "opportunity"
            },
            duration_days=14,
            recovery_rate=0.1
        )
        events.append(self.factory.create_economic_event(
            AdvancedEventType.MARKET_CRASH,
            crash_data
        ))
        
        # Black market surge
        black_market_data = EconomicEventData(
            affected_markets=["contraband", "information", "rare_items"],
            price_modifiers={
                "contraband": 0.5,
                "information": 0.3,
                "rare_items": 0.4
            },
            trade_route_impacts={
                "underground_network": True,
                "shadow_paths": True
            },
            merchant_faction_responses={
                "thieves_guild": "expand_operations",
                "city_guard": "crackdown",
                "corrupt_officials": "profit"
            },
            duration_days=10,
            recovery_rate=0.2
        )
        events.append(self.factory.create_economic_event(
            AdvancedEventType.BLACK_MARKET_SURGE,
            black_market_data
        ))
        
        # Trade revolution
        revolution_data = EconomicEventData(
            affected_markets=["all_markets"],
            price_modifiers={
                "technology": 0.3,
                "magic_items": 0.2,
                "luxury_goods": 0.1
            },
            trade_route_impacts={
                "all_routes": True,
                "new_routes": True
            },
            merchant_faction_responses={
                "merchant_guild": "embrace_change",
                "traditionalists": "resist",
                "innovators": "lead"
            },
            duration_days=30,
            recovery_rate=0.05
        )
        events.append(self.factory.create_economic_event(
            AdvancedEventType.TRADE_REVOLUTION,
            revolution_data
        ))
        
        return events 