from typing import Dict, List, Optional, Set
from .event_manager import Event, EventType, EventTrigger, EventRequirements, EventEffects

class FactionEventHandler:
    def __init__(self):
        self.faction_relationships: Dict[str, Dict[str, float]] = {}  # faction_a -> {faction_b -> relationship_value}
        self.territory_control: Dict[str, str] = {}  # territory_id -> controlling_faction
        self.active_conflicts: Set[str] = set()  # Set of territory_ids with active conflicts
        self.alliance_networks: Dict[str, Set[str]] = {}  # faction -> set of allied factions

    def initialize_faction(self, faction_id: str):
        """Initialize a new faction in the system"""
        if faction_id not in self.faction_relationships:
            self.faction_relationships[faction_id] = {}
            self.alliance_networks[faction_id] = set()

    def set_relationship(self, faction_a: str, faction_b: str, value: float):
        """Set relationship value between two factions"""
        if faction_a not in self.faction_relationships:
            self.initialize_faction(faction_a)
        if faction_b not in self.faction_relationships:
            self.initialize_faction(faction_b)
            
        self.faction_relationships[faction_a][faction_b] = value
        self.faction_relationships[faction_b][faction_a] = value
        
        # Update alliances if relationship is very positive
        if value >= 0.8:
            self.alliance_networks[faction_a].add(faction_b)
            self.alliance_networks[faction_b].add(faction_a)
        elif value < 0.5:  # Break alliance if relationship deteriorates
            self.alliance_networks[faction_a].discard(faction_b)
            self.alliance_networks[faction_b].discard(faction_a)

    def claim_territory(self, faction_id: str, territory_id: str) -> bool:
        """Attempt to claim territory for a faction"""
        if territory_id in self.territory_control:
            current_controller = self.territory_control[territory_id]
            if current_controller != faction_id:
                self.active_conflicts.add(territory_id)
                return False
        
        self.territory_control[territory_id] = faction_id
        return True

    def resolve_territory_dispute(self, territory_id: str, winner_faction: str):
        """Resolve a territory dispute"""
        if territory_id in self.active_conflicts:
            old_controller = self.territory_control.get(territory_id)
            if old_controller:
                # Deteriorate relationship between factions
                current_relation = self.faction_relationships[winner_faction].get(old_controller, 0)
                self.set_relationship(winner_faction, old_controller, max(-1.0, current_relation - 0.3))
            
            self.territory_control[territory_id] = winner_faction
            self.active_conflicts.remove(territory_id)

    def generate_faction_event(self, faction_id: str, territory_id: Optional[str] = None) -> Event:
        """Generate a faction-related event"""
        event_id = f"faction_event_{faction_id}_{territory_id or 'general'}"
        
        requirements = EventRequirements(
            faction_reputation={faction_id: 0}  # Minimum reputation to participate
        )
        
        effects = EventEffects(
            faction_reputation_changes={faction_id: 10},  # Base reputation gain
            territory_effects={territory_id: "contested"} if territory_id else None
        )
        
        return Event(
            event_id=event_id,
            name=f"Faction Activity: {faction_id}",
            event_type=EventType.FACTION,
            trigger=EventTrigger.FACTION_ACTION,
            requirements=requirements,
            effects=effects,
            duration=3600,  # 1 hour
            cooldown=7200,  # 2 hours
        )

    def get_faction_allies(self, faction_id: str) -> Set[str]:
        """Get all allies of a faction"""
        return self.alliance_networks.get(faction_id, set())

    def get_faction_enemies(self, faction_id: str) -> Set[str]:
        """Get factions with negative relationships"""
        enemies = set()
        for other_faction, relation in self.faction_relationships.get(faction_id, {}).items():
            if relation < -0.3:  # Threshold for considering a faction an enemy
                enemies.add(other_faction)
        return enemies

    def get_contested_territories(self) -> List[str]:
        """Get list of currently contested territories"""
        return list(self.active_conflicts)

    def get_faction_territory_count(self, faction_id: str) -> int:
        """Get number of territories controlled by a faction"""
        return sum(1 for controller in self.territory_control.values() if controller == faction_id) 