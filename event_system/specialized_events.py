from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from .event_manager import Event, EventType, EventTrigger, EventRequirements, EventEffects

class SpecializedEventType(Enum):
    # Celestial Events
    ECLIPSE = "eclipse"
    METEOR_SHOWER = "meteor_shower"
    CONSTELLATION_ALIGNMENT = "constellation_alignment"
    
    # Environmental Events
    MAGICAL_STORM = "magical_storm"
    PLANAR_CONVERGENCE = "planar_convergence"
    ELEMENTAL_SURGE = "elemental_surge"
    
    # Political Events
    SUCCESSION_CRISIS = "succession_crisis"
    TRADE_AGREEMENT = "trade_agreement"
    DIPLOMATIC_INCIDENT = "diplomatic_incident"
    
    # Cultural Events
    FESTIVAL = "festival"
    RITUAL_CEREMONY = "ritual_ceremony"
    KNOWLEDGE_EXCHANGE = "knowledge_exchange"

@dataclass
class CelestialEventData:
    celestial_bodies: List[str]
    alignment_type: str
    energy_level: float
    duration_hours: int
    affected_regions: List[str]

@dataclass
class EnvironmentalEventData:
    element_type: str
    intensity: float
    spread_rate: float
    affected_territories: List[str]
    duration_minutes: int

@dataclass
class PoliticalEventData:
    involved_factions: List[str]
    influence_changes: Dict[str, float]
    resource_impacts: Dict[str, float]
    duration_days: int

@dataclass
class CulturalEventData:
    host_faction: str
    participating_factions: List[str]
    cultural_bonuses: Dict[str, float]
    knowledge_gained: List[str]
    duration_hours: int

class SpecializedEventFactory:
    def __init__(self):
        self.event_counter = 0

    def create_celestial_event(self, event_type: SpecializedEventType, data: CelestialEventData) -> Event:
        """Create a celestial event"""
        self.event_counter += 1
        event_id = f"celestial_{event_type.value}_{self.event_counter}"
        
        requirements = EventRequirements(
            celestial_alignment=data.alignment_type,
            environmental_conditions=["clear_sky", "night"]
        )
        
        effects = EventEffects(
            celestial_effects=[f"{body}_influence" for body in data.celestial_bodies],
            environmental_changes=[f"celestial_energy_{data.energy_level}"],
            territory_effects={region: "celestial_affected" for region in data.affected_regions}
        )
        
        return Event(
            event_id=event_id,
            name=f"Celestial Event: {event_type.value.title()}",
            event_type=EventType.CELESTIAL,
            trigger=EventTrigger.CELESTIAL_ALIGNMENT,
            requirements=requirements,
            effects=effects,
            duration=data.duration_hours * 3600,
            cooldown=data.duration_hours * 7200
        )

    def create_environmental_event(self, event_type: SpecializedEventType, data: EnvironmentalEventData) -> Event:
        """Create an environmental event"""
        self.event_counter += 1
        event_id = f"environmental_{event_type.value}_{self.event_counter}"
        
        requirements = EventRequirements(
            environmental_conditions=[f"{data.element_type}_presence"]
        )
        
        effects = EventEffects(
            environmental_changes=[
                f"{data.element_type}_surge",
                f"intensity_{data.intensity}"
            ],
            territory_effects={
                territory: f"{data.element_type}_affected"
                for territory in data.affected_territories
            }
        )
        
        return Event(
            event_id=event_id,
            name=f"Environmental Event: {event_type.value.title()}",
            event_type=EventType.ENVIRONMENTAL,
            trigger=EventTrigger.ENVIRONMENTAL_CONDITION,
            requirements=requirements,
            effects=effects,
            duration=data.duration_minutes * 60,
            cooldown=data.duration_minutes * 120
        )

    def create_political_event(self, event_type: SpecializedEventType, data: PoliticalEventData) -> Event:
        """Create a political event"""
        self.event_counter += 1
        event_id = f"political_{event_type.value}_{self.event_counter}"
        
        requirements = EventRequirements(
            faction_reputation={faction: 10 for faction in data.involved_factions}
        )
        
        effects = EventEffects(
            faction_reputation_changes=data.influence_changes,
            resource_changes=data.resource_impacts
        )
        
        return Event(
            event_id=event_id,
            name=f"Political Event: {event_type.value.title()}",
            event_type=EventType.FACTION,
            trigger=EventTrigger.FACTION_ACTION,
            requirements=requirements,
            effects=effects,
            duration=data.duration_days * 86400,
            cooldown=data.duration_days * 172800
        )

    def create_cultural_event(self, event_type: SpecializedEventType, data: CulturalEventData) -> Event:
        """Create a cultural event"""
        self.event_counter += 1
        event_id = f"cultural_{event_type.value}_{self.event_counter}"
        
        requirements = EventRequirements(
            faction_reputation={
                data.host_faction: 20,
                **{faction: 10 for faction in data.participating_factions}
            }
        )
        
        effects = EventEffects(
            faction_reputation_changes={
                faction: bonus for faction, bonus in data.cultural_bonuses.items()
            }
        )
        
        return Event(
            event_id=event_id,
            name=f"Cultural Event: {event_type.value.title()}",
            event_type=EventType.RITUAL,
            trigger=EventTrigger.FACTION_ACTION,
            requirements=requirements,
            effects=effects,
            duration=data.duration_hours * 3600,
            cooldown=data.duration_hours * 7200
        )

class EventScenarioGenerator:
    def __init__(self, factory: SpecializedEventFactory):
        self.factory = factory

    def generate_celestial_convergence_scenario(self) -> List[Event]:
        """Generate a celestial convergence event chain"""
        events = []
        
        # Initial meteor shower
        meteor_data = CelestialEventData(
            celestial_bodies=["meteor_cluster"],
            alignment_type="meteor_shower",
            energy_level=0.7,
            duration_hours=2,
            affected_regions=["northern_realm", "central_plains"]
        )
        events.append(self.factory.create_celestial_event(
            SpecializedEventType.METEOR_SHOWER,
            meteor_data
        ))
        
        # Constellation alignment
        alignment_data = CelestialEventData(
            celestial_bodies=["dragon_constellation", "mage_constellation"],
            alignment_type="major_conjunction",
            energy_level=0.9,
            duration_hours=4,
            affected_regions=["all_regions"]
        )
        events.append(self.factory.create_celestial_event(
            SpecializedEventType.CONSTELLATION_ALIGNMENT,
            alignment_data
        ))
        
        # Magical storm aftermath
        storm_data = EnvironmentalEventData(
            element_type="arcane",
            intensity=0.8,
            spread_rate=0.5,
            affected_territories=["magical_wastes", "mystic_forest"],
            duration_minutes=120
        )
        events.append(self.factory.create_environmental_event(
            SpecializedEventType.MAGICAL_STORM,
            storm_data
        ))
        
        return events

    def generate_faction_conflict_scenario(self) -> List[Event]:
        """Generate a faction conflict event chain"""
        events = []
        
        # Diplomatic incident
        incident_data = PoliticalEventData(
            involved_factions=["empire", "republic"],
            influence_changes={"empire": -20, "republic": -20},
            resource_impacts={"trade_goods": -0.3, "military_supplies": 0.2},
            duration_days=3
        )
        events.append(self.factory.create_political_event(
            SpecializedEventType.DIPLOMATIC_INCIDENT,
            incident_data
        ))
        
        # Trade agreement attempt
        trade_data = PoliticalEventData(
            involved_factions=["merchant_guild", "empire", "republic"],
            influence_changes={"merchant_guild": 15, "empire": 10, "republic": 10},
            resource_impacts={"trade_goods": 0.5, "luxury_items": 0.3},
            duration_days=7
        )
        events.append(self.factory.create_political_event(
            SpecializedEventType.TRADE_AGREEMENT,
            trade_data
        ))
        
        # Cultural festival for peace
        festival_data = CulturalEventData(
            host_faction="merchant_guild",
            participating_factions=["empire", "republic"],
            cultural_bonuses={"empire": 25, "republic": 25, "merchant_guild": 40},
            knowledge_gained=["diplomatic_relations", "cultural_understanding"],
            duration_hours=48
        )
        events.append(self.factory.create_cultural_event(
            SpecializedEventType.FESTIVAL,
            festival_data
        ))
        
        return events

    def generate_magical_crisis_scenario(self) -> List[Event]:
        """Generate a magical crisis event chain"""
        events = []
        
        # Planar convergence
        convergence_data = EnvironmentalEventData(
            element_type="planar",
            intensity=0.9,
            spread_rate=0.7,
            affected_territories=["mage_towers", "ancient_ruins", "mystic_forest"],
            duration_minutes=180
        )
        events.append(self.factory.create_environmental_event(
            SpecializedEventType.PLANAR_CONVERGENCE,
            convergence_data
        ))
        
        # Emergency ritual ceremony
        ceremony_data = CulturalEventData(
            host_faction="mage_council",
            participating_factions=["druids_circle", "temple_order"],
            cultural_bonuses={"mage_council": 30, "druids_circle": 20, "temple_order": 20},
            knowledge_gained=["planar_magic", "containment_rituals"],
            duration_hours=6
        )
        events.append(self.factory.create_cultural_event(
            SpecializedEventType.RITUAL_CEREMONY,
            ceremony_data
        ))
        
        # Knowledge exchange
        exchange_data = CulturalEventData(
            host_faction="mage_council",
            participating_factions=["all_magical_factions"],
            cultural_bonuses={"mage_council": 50},
            knowledge_gained=["crisis_management", "planar_sealing"],
            duration_hours=12
        )
        events.append(self.factory.create_cultural_event(
            SpecializedEventType.KNOWLEDGE_EXCHANGE,
            exchange_data
        ))
        
        return events 