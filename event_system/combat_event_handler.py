from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum
from .event_manager import Event, EventType, EventTrigger, EventRequirements, EventEffects

class CombatEventType(Enum):
    AMBUSH = "ambush"
    SIEGE = "siege"
    SKIRMISH = "skirmish"
    RAID = "raid"
    TERRITORY_DEFENSE = "territory_defense"
    FACTION_WAR = "faction_war"

@dataclass
class CombatParticipant:
    faction_id: str
    strength: float
    position: Tuple[float, float]  # x, y coordinates
    is_player_allied: bool

class CombatEventHandler:
    def __init__(self):
        self.active_combats: Dict[str, List[CombatParticipant]] = {}  # combat_id -> participants
        self.combat_outcomes: Dict[str, Dict[str, float]] = {}  # combat_id -> {faction_id -> success_rate}
        self.territory_conflicts: Dict[str, Set[str]] = {}  # territory_id -> set of involved factions

    def initialize_combat(self, combat_id: str, combat_type: CombatEventType) -> Event:
        """Initialize a new combat event"""
        if combat_id in self.active_combats:
            return None
            
        self.active_combats[combat_id] = []
        self.combat_outcomes[combat_id] = {}
        
        return Event(
            event_id=combat_id,
            name=f"Combat Event: {combat_type.value}",
            event_type=EventType.COMBAT,
            trigger=EventTrigger.FACTION_ACTION,
            requirements=EventRequirements(),
            effects=EventEffects(),
            duration=1800,  # 30 minutes
            cooldown=3600,  # 1 hour
        )

    def add_participant(self, combat_id: str, participant: CombatParticipant):
        """Add a participant to an active combat"""
        if combat_id in self.active_combats:
            self.active_combats[combat_id].append(participant)
            self.combat_outcomes[combat_id][participant.faction_id] = 0.0

    def update_combat_state(self, combat_id: str, game_state: Dict) -> Dict[str, float]:
        """Update the state of an active combat"""
        if combat_id not in self.active_combats:
            return {}
            
        participants = self.active_combats[combat_id]
        total_strength = sum(p.strength for p in participants)
        
        # Calculate success rates based on relative strength and position
        for participant in participants:
            relative_strength = participant.strength / total_strength
            position_bonus = self._calculate_position_bonus(participant.position, game_state)
            success_rate = relative_strength * (1 + position_bonus)
            self.combat_outcomes[combat_id][participant.faction_id] = min(1.0, success_rate)
            
        return self.combat_outcomes[combat_id]

    def _calculate_position_bonus(self, position: Tuple[float, float], game_state: Dict) -> float:
        """Calculate position-based combat bonus"""
        # This would integrate with the game's terrain and environmental systems
        # For now, return a simple random bonus between -0.1 and 0.1
        return (position[0] * position[1]) % 0.2 - 0.1

    def generate_ambush_event(self, territory_id: str, attacker_faction: str) -> Event:
        """Generate an ambush event"""
        event_id = f"ambush_{territory_id}_{attacker_faction}"
        
        requirements = EventRequirements(
            faction_reputation={attacker_faction: -20},  # Negative reputation required for ambush
            environmental_conditions=["night"] # Example condition
        )
        
        effects = EventEffects(
            faction_reputation_changes={attacker_faction: -10},  # Reputation penalty for ambushing
            territory_effects={territory_id: "ambushed"}
        )
        
        return Event(
            event_id=event_id,
            name=f"Ambush in {territory_id}",
            event_type=EventType.COMBAT,
            trigger=EventTrigger.FACTION_ACTION,
            requirements=requirements,
            effects=effects,
            duration=900,  # 15 minutes
            cooldown=7200,  # 2 hours
        )

    def generate_territory_defense_event(self, territory_id: str, defender_faction: str) -> Event:
        """Generate a territory defense event"""
        event_id = f"defense_{territory_id}_{defender_faction}"
        
        requirements = EventRequirements(
            faction_reputation={defender_faction: 10},
            environmental_conditions=["daylight"]
        )
        
        effects = EventEffects(
            faction_reputation_changes={defender_faction: 15},
            territory_effects={territory_id: "defended"}
        )
        
        return Event(
            event_id=event_id,
            name=f"Territory Defense: {territory_id}",
            event_type=EventType.COMBAT,
            trigger=EventTrigger.FACTION_ACTION,
            requirements=requirements,
            effects=effects,
            duration=1800,  # 30 minutes
            cooldown=3600,  # 1 hour
        )

    def resolve_combat(self, combat_id: str) -> Optional[str]:
        """Resolve a combat event and return the winning faction"""
        if combat_id not in self.combat_outcomes:
            return None
            
        outcomes = self.combat_outcomes[combat_id]
        if not outcomes:
            return None
            
        winner = max(outcomes.items(), key=lambda x: x[1])[0]
        
        # Cleanup
        del self.active_combats[combat_id]
        del self.combat_outcomes[combat_id]
        
        return winner

    def get_active_combats_in_territory(self, territory_id: str) -> List[str]:
        """Get all active combats in a territory"""
        return [
            combat_id for combat_id in self.active_combats.keys()
            if any(p.position[0] == territory_id for p in self.active_combats[combat_id])
        ]

    def get_combat_participants(self, combat_id: str) -> List[CombatParticipant]:
        """Get all participants in a combat"""
        return self.active_combats.get(combat_id, []) 