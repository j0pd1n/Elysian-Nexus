from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import random

class FactionType(Enum):
    KINGDOM = "kingdom"
    GUILD = "guild"
    CULT = "cult"
    TRIBE = "tribe"
    MERCHANT = "merchant"
    CRIMINAL = "criminal"
    MILITARY = "military"
    RELIGIOUS = "religious"

class RelationType(Enum):
    ALLIED = "allied"
    FRIENDLY = "friendly"
    NEUTRAL = "neutral"
    UNFRIENDLY = "unfriendly"
    HOSTILE = "hostile"
    WAR = "war"

class DiplomaticAction(Enum):
    TRADE = "trade"
    ALLIANCE = "alliance"
    WAR = "war"
    PEACE = "peace"
    TRIBUTE = "tribute"
    EMBARGO = "embargo"

@dataclass
class FactionStats:
    military: int
    economy: int
    influence: int
    stability: int
    territory: int

@dataclass
class Faction:
    name: str
    type: FactionType
    stats: FactionStats
    leader: str
    description: str
    relations: Dict[str, RelationType] = None
    allies: List[str] = None
    enemies: List[str] = None
    controlled_regions: List[str] = None

    def __post_init__(self):
        self.relations = self.relations or {}
        self.allies = self.allies or []
        self.enemies = self.enemies or []
        self.controlled_regions = self.controlled_regions or []

class FactionSystem:
    def __init__(self):
        self.factions: Dict[str, Faction] = {}
        self.relation_modifiers = {
            DiplomaticAction.TRADE: 10,
            DiplomaticAction.ALLIANCE: 30,
            DiplomaticAction.WAR: -50,
            DiplomaticAction.PEACE: 20,
            DiplomaticAction.TRIBUTE: 15,
            DiplomaticAction.EMBARGO: -20
        }

    def create_faction(self, name: str, type: FactionType, stats: FactionStats,
                      leader: str, description: str) -> Faction:
        """Create a new faction"""
        faction = Faction(name, type, stats, leader, description)
        self.factions[name] = faction
        return faction

    def remove_faction(self, name: str):
        """Remove a faction"""
        if name in self.factions:
            del self.factions[name]

    def get_faction(self, name: str) -> Optional[Faction]:
        """Get a faction by name"""
        return self.factions.get(name)

    def set_relation(self, faction1: str, faction2: str, relation: RelationType):
        """Set the relation between two factions"""
        if faction1 in self.factions and faction2 in self.factions:
            self.factions[faction1].relations[faction2] = relation
            self.factions[faction2].relations[faction1] = relation

            if relation == RelationType.ALLIED:
                self._add_alliance(faction1, faction2)
            elif relation == RelationType.WAR:
                self._add_war(faction1, faction2)

    def get_relation(self, faction1: str, faction2: str) -> RelationType:
        """Get the relation between two factions"""
        if faction1 in self.factions and faction2 in self.factions:
            return self.factions[faction1].relations.get(faction2, RelationType.NEUTRAL)
        return RelationType.NEUTRAL

    def modify_relation(self, faction1: str, faction2: str, action: DiplomaticAction):
        """Modify relation between factions based on diplomatic action"""
        if faction1 in self.factions and faction2 in self.factions:
            current_relation = self.get_relation(faction1, faction2)
            modifier = self.relation_modifiers[action]
            
            # Determine new relation based on current relation and modifier
            relations = list(RelationType)
            current_index = relations.index(current_relation)
            new_index = max(0, min(len(relations) - 1, current_index + (1 if modifier > 0 else -1)))
            new_relation = relations[new_index]
            
            self.set_relation(faction1, faction2, new_relation)

    def get_allies(self, faction_name: str) -> List[str]:
        """Get all allies of a faction"""
        if faction_name in self.factions:
            return self.factions[faction_name].allies
        return []

    def get_enemies(self, faction_name: str) -> List[str]:
        """Get all enemies of a faction"""
        if faction_name in self.factions:
            return self.factions[faction_name].enemies
        return []

    def declare_war(self, aggressor: str, target: str):
        """Declare war between factions"""
        if aggressor in self.factions and target in self.factions:
            self.modify_relation(aggressor, target, DiplomaticAction.WAR)
            # Handle war declarations from allies
            for ally in self.get_allies(target):
                if random.random() < 0.7:  # 70% chance for allies to join
                    self.modify_relation(aggressor, ally, DiplomaticAction.WAR)

    def make_peace(self, faction1: str, faction2: str):
        """Make peace between factions"""
        if faction1 in self.factions and faction2 in self.factions:
            self.modify_relation(faction1, faction2, DiplomaticAction.PEACE)

    def form_alliance(self, faction1: str, faction2: str):
        """Form an alliance between factions"""
        if faction1 in self.factions and faction2 in self.factions:
            self.modify_relation(faction1, faction2, DiplomaticAction.ALLIANCE)

    def break_alliance(self, faction1: str, faction2: str):
        """Break an alliance between factions"""
        if faction1 in self.factions and faction2 in self.factions:
            self._remove_alliance(faction1, faction2)
            self.set_relation(faction1, faction2, RelationType.NEUTRAL)

    def get_faction_power(self, faction_name: str) -> int:
        """Calculate the total power of a faction"""
        if faction_name in self.factions:
            faction = self.factions[faction_name]
            return (faction.stats.military + faction.stats.economy +
                   faction.stats.influence + faction.stats.stability +
                   faction.stats.territory)
        return 0

    def get_strongest_factions(self, count: int = 3) -> List[Tuple[str, int]]:
        """Get the strongest factions by power"""
        faction_power = [(name, self.get_faction_power(name))
                        for name in self.factions]
        return sorted(faction_power, key=lambda x: x[1], reverse=True)[:count]

    def add_controlled_region(self, faction_name: str, region: str):
        """Add a controlled region to a faction"""
        if faction_name in self.factions:
            self.factions[faction_name].controlled_regions.append(region)
            self.factions[faction_name].stats.territory += 1

    def remove_controlled_region(self, faction_name: str, region: str):
        """Remove a controlled region from a faction"""
        if faction_name in self.factions:
            if region in self.factions[faction_name].controlled_regions:
                self.factions[faction_name].controlled_regions.remove(region)
                self.factions[faction_name].stats.territory -= 1

    def get_controlled_regions(self, faction_name: str) -> List[str]:
        """Get all regions controlled by a faction"""
        if faction_name in self.factions:
            return self.factions[faction_name].controlled_regions
        return []

    def _add_alliance(self, faction1: str, faction2: str):
        """Add alliance between factions"""
        self.factions[faction1].allies.append(faction2)
        self.factions[faction2].allies.append(faction1)
        
        # Remove from enemies if present
        if faction2 in self.factions[faction1].enemies:
            self.factions[faction1].enemies.remove(faction2)
        if faction1 in self.factions[faction2].enemies:
            self.factions[faction2].enemies.remove(faction1)

    def _remove_alliance(self, faction1: str, faction2: str):
        """Remove alliance between factions"""
        if faction2 in self.factions[faction1].allies:
            self.factions[faction1].allies.remove(faction2)
        if faction1 in self.factions[faction2].allies:
            self.factions[faction2].allies.remove(faction1)

    def _add_war(self, faction1: str, faction2: str):
        """Add war between factions"""
        self.factions[faction1].enemies.append(faction2)
        self.factions[faction2].enemies.append(faction1)
        
        # Remove from allies if present
        if faction2 in self.factions[faction1].allies:
            self.factions[faction1].allies.remove(faction2)
        if faction1 in self.factions[faction2].allies:
            self.factions[faction2].allies.remove(faction1)