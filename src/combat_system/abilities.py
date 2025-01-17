from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass

class AbilityType(Enum):
    ATTACK = "Attack"
    DEFENSE = "Defense"
    UTILITY = "Utility"
    HEALING = "Healing"
    BUFF = "Buff"
    DEBUFF = "Debuff"

@dataclass
class Ability:
    name: str
    description: str
    ability_type: AbilityType
    mana_cost: int
    cooldown: int
    base_value: int
    scaling_stat: str
    scaling_factor: float
    level_requirement: int = 1
    unlocked: bool = False

class AbilityManager:
    def __init__(self):
        self.abilities: Dict[str, Ability] = {}
        self.initialize_abilities()

    def initialize_abilities(self):
        """Initialize all available abilities"""
        # Warrior abilities
        self.abilities["power_strike"] = Ability(
            name="Power Strike",
            description="A powerful melee attack that deals extra damage",
            ability_type=AbilityType.ATTACK,
            mana_cost=10,
            cooldown=3,
            base_value=20,
            scaling_stat="strength",
            scaling_factor=1.5
        )

        self.abilities["shield_wall"] = Ability(
            name="Shield Wall",
            description="Increase defense for a short duration",
            ability_type=AbilityType.DEFENSE,
            mana_cost=15,
            cooldown=10,
            base_value=30,
            scaling_stat="constitution",
            scaling_factor=1.2
        )

        # Mage abilities
        self.abilities["fireball"] = Ability(
            name="Fireball",
            description="Launch a ball of fire at enemies",
            ability_type=AbilityType.ATTACK,
            mana_cost=20,
            cooldown=4,
            base_value=30,
            scaling_stat="intelligence",
            scaling_factor=2.0
        )

        self.abilities["frost_armor"] = Ability(
            name="Frost Armor",
            description="Create protective armor of ice",
            ability_type=AbilityType.DEFENSE,
            mana_cost=25,
            cooldown=15,
            base_value=25,
            scaling_stat="intelligence",
            scaling_factor=1.3
        )

        # Rogue abilities
        self.abilities["backstab"] = Ability(
            name="Backstab",
            description="A sneaky attack that deals high damage",
            ability_type=AbilityType.ATTACK,
            mana_cost=15,
            cooldown=5,
            base_value=35,
            scaling_stat="dexterity",
            scaling_factor=1.8
        )

        self.abilities["smoke_bomb"] = Ability(
            name="Smoke Bomb",
            description="Create a cloud of smoke for evasion",
            ability_type=AbilityType.UTILITY,
            mana_cost=20,
            cooldown=12,
            base_value=0,
            scaling_stat="dexterity",
            scaling_factor=1.0
        )

    def get_ability(self, ability_name: str) -> Optional[Ability]:
        """Get an ability by name"""
        return self.abilities.get(ability_name)

    def unlock_ability(self, ability_name: str, character_level: int) -> bool:
        """Attempt to unlock an ability"""
        ability = self.get_ability(ability_name)
        if ability and character_level >= ability.level_requirement:
            ability.unlocked = True
            return True
        return False

    def get_available_abilities(self, character_class: str) -> List[Ability]:
        """Get list of abilities available for a character class"""
        if character_class == "Warrior":
            return [
                self.abilities["power_strike"],
                self.abilities["shield_wall"]
            ]
        elif character_class == "Mage":
            return [
                self.abilities["fireball"],
                self.abilities["frost_armor"]
            ]
        elif character_class == "Rogue":
            return [
                self.abilities["backstab"],
                self.abilities["smoke_bomb"]
            ]
        return []

    def calculate_ability_value(self, ability: Ability, stat_value: int) -> int:
        """Calculate the final value of an ability based on stats"""
        return int(ability.base_value * (1 + ability.scaling_factor * (stat_value / 10))) 