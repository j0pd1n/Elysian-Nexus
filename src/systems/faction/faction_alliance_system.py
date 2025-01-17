from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Tuple
import random
import math
import time
import logging
from collections import defaultdict

from weather_system import WeatherType, CelestialPattern
from economic_system import ResourceType, MarketEvent

class AllianceType(Enum):
    MILITARY = "military"
    ECONOMIC = "economic"
    MAGICAL = "magical"
    CELESTIAL = "celestial"
    RITUAL = "ritual"
    TERRITORIAL = "territorial"

class AllianceStatus(Enum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    STRAINED = "strained"
    BROKEN = "broken"
    DISSOLVED = "dissolved"

@dataclass
class Alliance:
    """Represents an alliance between factions"""
    alliance_type: AllianceType
    member_factions: Set[str]
    formation_time: float
    status: AllianceStatus
    strength: float  # 0.0 to 1.0
    benefits: Dict[str, float]
    conditions: Dict[str, any]
    celestial_resonance: float  # Affects alliance power during celestial events
    last_interaction: float = time.time()

@dataclass
class RitualCooperation:
    """Represents cooperative ritual between allied factions"""
    participating_factions: Set[str]
    ritual_type: str
    power_contribution: Dict[str, float]
    success_chance: float
    celestial_bonus: float
    territory_bonus: float
    start_time: float = time.time()

class FactionAllianceSystem:
    def __init__(self):
        self.alliances: Dict[str, Alliance] = {}
        self.faction_relations: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.ritual_cooperations: List[RitualCooperation] = []
        self.logger = self._setup_logger()
        
        # Celestial impact tracking
        self.celestial_influences: Dict[str, List[Tuple[CelestialPattern, float]]] = defaultdict(list)
        self.alliance_power_modifiers: Dict[str, float] = defaultdict(lambda: 1.0)

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("FactionAllianceSystem")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def propose_alliance(
        self,
        alliance_type: AllianceType,
        proposing_faction: str,
        target_faction: str,
        conditions: Dict[str, any]
    ) -> Optional[Alliance]:
        """Propose a new alliance between factions"""
        # Check existing relations
        current_relation = self.faction_relations[proposing_faction][target_faction]
        if current_relation < 0.3:  # Minimum relation threshold
            return None
            
        # Create alliance
        alliance_id = f"{proposing_faction}_{target_faction}_{int(time.time())}"
        alliance = Alliance(
            alliance_type=alliance_type,
            member_factions={proposing_faction, target_faction},
            formation_time=time.time(),
            status=AllianceStatus.PROPOSED,
            strength=current_relation,
            benefits=self._calculate_alliance_benefits(alliance_type, current_relation),
            conditions=conditions,
            celestial_resonance=random.uniform(0.7, 1.3)
        )
        
        self.alliances[alliance_id] = alliance
        return alliance

    def _calculate_alliance_benefits(
        self,
        alliance_type: AllianceType,
        relation_strength: float
    ) -> Dict[str, float]:
        """Calculate benefits based on alliance type and relation strength"""
        benefits = {}
        
        if alliance_type == AllianceType.MILITARY:
            benefits.update({
                "combat_strength": 0.2 * relation_strength,
                "defense_bonus": 0.15 * relation_strength,
                "shared_resources": 0.1 * relation_strength
            })
        elif alliance_type == AllianceType.ECONOMIC:
            benefits.update({
                "trade_bonus": 0.25 * relation_strength,
                "resource_sharing": 0.2 * relation_strength,
                "market_access": 0.15 * relation_strength
            })
        elif alliance_type == AllianceType.MAGICAL:
            benefits.update({
                "spell_power": 0.2 * relation_strength,
                "ritual_efficiency": 0.25 * relation_strength,
                "magical_defense": 0.15 * relation_strength
            })
        elif alliance_type == AllianceType.CELESTIAL:
            benefits.update({
                "celestial_power": 0.3 * relation_strength,
                "planar_influence": 0.25 * relation_strength,
                "reality_manipulation": 0.2 * relation_strength
            })
        elif alliance_type == AllianceType.RITUAL:
            benefits.update({
                "ritual_power": 0.3 * relation_strength,
                "cooperation_bonus": 0.25 * relation_strength,
                "magical_resonance": 0.2 * relation_strength
            })
        elif alliance_type == AllianceType.TERRITORIAL:
            benefits.update({
                "territory_control": 0.25 * relation_strength,
                "resource_yield": 0.2 * relation_strength,
                "influence_spread": 0.15 * relation_strength
            })
            
        return benefits

    def accept_alliance(self, alliance_id: str) -> bool:
        """Accept a proposed alliance"""
        if alliance_id not in self.alliances:
            return False
            
        alliance = self.alliances[alliance_id]
        if alliance.status != AllianceStatus.PROPOSED:
            return False
            
        alliance.status = AllianceStatus.ACTIVE
        
        # Update faction relations
        for faction1 in alliance.member_factions:
            for faction2 in alliance.member_factions:
                if faction1 != faction2:
                    self.faction_relations[faction1][faction2] += 0.2
                    
        self.logger.info(
            f"Alliance {alliance_id} activated between "
            f"{', '.join(alliance.member_factions)}"
        )
        return True

    def process_celestial_impact(
        self,
        alliance_id: str,
        pattern: CelestialPattern
    ):
        """Process celestial pattern effects on alliance"""
        if alliance_id not in self.alliances:
            return
            
        alliance = self.alliances[alliance_id]
        
        # Calculate celestial impact
        impact_strength = pattern.intensity * alliance.celestial_resonance
        
        # Modify alliance strength
        if pattern.alignment == alliance.alliance_type:
            alliance.strength = min(1.0, alliance.strength * (1 + 0.1 * impact_strength))
            self.alliance_power_modifiers[alliance_id] = 1 + 0.2 * impact_strength
        else:
            alliance.strength = max(0.1, alliance.strength * (1 - 0.05 * impact_strength))
            self.alliance_power_modifiers[alliance_id] = max(0.5, 1 - 0.1 * impact_strength)
            
        # Record celestial influence
        self.celestial_influences[alliance_id].append((pattern, time.time()))
        
        # Update benefits
        alliance.benefits = self._calculate_alliance_benefits(
            alliance.alliance_type,
            alliance.strength
        )

    def create_ritual_cooperation(
        self,
        ritual_type: str,
        participating_alliances: List[str],
        territory_name: Optional[str] = None
    ) -> Optional[RitualCooperation]:
        """Create a cooperative ritual between allied factions"""
        # Gather participating factions
        participating_factions = set()
        total_power = 0.0
        power_contributions = {}
        
        for alliance_id in participating_alliances:
            if alliance_id not in self.alliances:
                continue
                
            alliance = self.alliances[alliance_id]
            if alliance.status != AllianceStatus.ACTIVE:
                continue
                
            # Calculate power contribution
            base_power = alliance.strength * self.alliance_power_modifiers[alliance_id]
            if alliance.alliance_type == AllianceType.RITUAL:
                base_power *= 1.5
                
            for faction in alliance.member_factions:
                participating_factions.add(faction)
                faction_power = base_power * (1 + random.uniform(-0.1, 0.1))
                power_contributions[faction] = faction_power
                total_power += faction_power
                
        if not participating_factions:
            return None
            
        # Calculate success chance
        base_chance = 0.5 + (total_power / (len(participating_factions) * 2))
        celestial_bonus = sum(
            pattern.intensity * 0.1
            for alliance_id in participating_alliances
            for pattern, _ in self.celestial_influences[alliance_id]
        )
        
        # Territory bonus if specified
        territory_bonus = 0.0
        if territory_name:
            # Territory bonus would be calculated based on territory system
            territory_bonus = 0.1
            
        cooperation = RitualCooperation(
            participating_factions=participating_factions,
            ritual_type=ritual_type,
            power_contribution=power_contributions,
            success_chance=min(0.95, base_chance + celestial_bonus + territory_bonus),
            celestial_bonus=celestial_bonus,
            territory_bonus=territory_bonus
        )
        
        self.ritual_cooperations.append(cooperation)
        return cooperation

    def update_alliance_status(self, alliance_id: str):
        """Update alliance status based on recent interactions"""
        if alliance_id not in self.alliances:
            return
            
        alliance = self.alliances[alliance_id]
        current_time = time.time()
        
        # Check for inactivity
        if current_time - alliance.last_interaction > 86400:  # 24 hours
            alliance.strength *= 0.95
            
        # Update status based on strength
        if alliance.strength < 0.2:
            alliance.status = AllianceStatus.BROKEN
        elif alliance.strength < 0.4:
            alliance.status = AllianceStatus.STRAINED
            
        # Process active celestial effects
        active_effects = [
            (pattern, effect_time)
            for pattern, effect_time in self.celestial_influences[alliance_id]
            if current_time - effect_time < pattern.duration
        ]
        self.celestial_influences[alliance_id] = active_effects

    def get_alliance_status(self, alliance_id: str) -> Dict[str, any]:
        """Get current status of alliance"""
        if alliance_id not in self.alliances:
            return {"error": "Alliance not found"}
            
        alliance = self.alliances[alliance_id]
        current_time = time.time()
        
        return {
            "type": alliance.alliance_type.value,
            "status": alliance.status.value,
            "strength": alliance.strength,
            "member_factions": list(alliance.member_factions),
            "formation_time": alliance.formation_time,
            "active_duration": current_time - alliance.formation_time,
            "benefits": alliance.benefits,
            "conditions": alliance.conditions,
            "celestial_resonance": alliance.celestial_resonance,
            "power_modifier": self.alliance_power_modifiers[alliance_id],
            "active_effects": [
                {
                    "type": pattern.pattern_type,
                    "intensity": pattern.intensity,
                    "duration": current_time - effect_time
                }
                for pattern, effect_time in self.celestial_influences[alliance_id]
                if current_time - effect_time < pattern.duration
            ]
        } 