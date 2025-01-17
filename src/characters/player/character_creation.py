from enum import Enum
from typing import Dict, Any, Optional, List

class CharacterClass(Enum):
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ROGUE = "Rogue"
    MYSTIC = "Mystic"
    VOID_WALKER = "Void Walker"
    CELESTIAL = "Celestial"

class CharacterBackground(Enum):
    NOBLE = "Noble"
    WANDERER = "Wanderer"
    SCHOLAR = "Scholar"
    OUTCAST = "Outcast"
    MYSTIC = "Mystic"
    SOLDIER = "Soldier"

class CharacterOrigin(Enum):
    ASTRAL_PLAINS = "Astral Plains"
    VOID_REALM = "Void Realm"
    CELESTIAL_CITY = "Celestial City"
    SHADOW_ISLES = "Shadow Isles"
    CRYSTAL_PEAKS = "Crystal Peaks"
    ETHEREAL_FOREST = "Ethereal Forest"

class CharacterCreator:
    def __init__(self):
        self.class_descriptions = {
            CharacterClass.WARRIOR.value: "A master of martial combat, skilled with weapons and armor. Warriors excel at protecting allies and devastating foes.",
            CharacterClass.MAGE.value: "A wielder of arcane magic, capable of manipulating the elements and bending reality. Mages are powerful but vulnerable.",
            CharacterClass.ROGUE.value: "A cunning adventurer who uses stealth and skill to overcome challenges. Rogues excel at precision strikes and subterfuge.",
            CharacterClass.MYSTIC.value: "A spiritual warrior who channels divine energy. Mystics can heal allies and smite enemies with sacred power.",
            CharacterClass.VOID_WALKER.value: "A mysterious being who has touched the void between realms. Void Walkers manipulate space and time itself.",
            CharacterClass.CELESTIAL.value: "A blessed champion of the heavens. Celestials command divine light and can both protect and purify."
        }
        
        self.background_descriptions = {
            CharacterBackground.NOBLE.value: "Born to privilege and trained in the arts of leadership and diplomacy.",
            CharacterBackground.WANDERER.value: "A traveler who has seen many lands and learned many secrets.",
            CharacterBackground.SCHOLAR.value: "Educated in ancient lore and magical theories.",
            CharacterBackground.OUTCAST.value: "One who has lived on the fringes of society, learning to survive alone.",
            CharacterBackground.MYSTIC.value: "Raised in the ways of spiritual and magical traditions.",
            CharacterBackground.SOLDIER.value: "Trained in the art of war and disciplined in the ways of combat."
        }
        
        self.origin_descriptions = {
            CharacterOrigin.ASTRAL_PLAINS.value: "A realm of cosmic energy and celestial wonders.",
            CharacterOrigin.VOID_REALM.value: "The dark space between realities, home to ancient mysteries.",
            CharacterOrigin.CELESTIAL_CITY.value: "A floating citadel of divine light and heavenly knowledge.",
            CharacterOrigin.SHADOW_ISLES.value: "Mysterious islands shrouded in eternal twilight.",
            CharacterOrigin.CRYSTAL_PEAKS.value: "Mountains of living crystal that pulse with magical energy.",
            CharacterOrigin.ETHEREAL_FOREST.value: "An enchanted woodland where reality and dreams intertwine."
        }
        
        self.class_abilities = {
            CharacterClass.WARRIOR.value: {
                "Battle Stance": "Enter a defensive stance, increasing armor and block chance.",
                "Power Strike": "A mighty attack that deals bonus damage and can stun enemies.",
                "Rally": "Boost the morale of nearby allies, increasing their combat effectiveness.",
                "Shield Wall": "Create a protective barrier that reduces incoming damage.",
                "Weapon Mastery": "Passive ability that increases damage with all weapons."
            },
            CharacterClass.MAGE.value: {
                "Arcane Blast": "A powerful burst of arcane energy that damages enemies.",
                "Elemental Shield": "Create a barrier of elemental energy for protection.",
                "Teleport": "Instantly teleport to a nearby location.",
                "Time Dilation": "Slow down time in a small area.",
                "Spell Weaving": "Passive ability that increases spell damage and reduces casting time."
            },
            CharacterClass.ROGUE.value: {
                "Shadow Step": "Quickly dash through the shadows to a new position.",
                "Backstab": "A precise strike that deals bonus damage from behind.",
                "Smoke Bomb": "Create a cloud of smoke that blinds enemies.",
                "Poison Blade": "Coat your weapons in deadly poison.",
                "Stealth Mastery": "Passive ability that improves stealth and critical strike chance."
            },
            CharacterClass.MYSTIC.value: {
                "Divine Light": "Channel holy energy to heal allies and damage undead.",
                "Spirit Ward": "Create a protective ward that blocks negative effects.",
                "Soul Link": "Connect with an ally to share health and power.",
                "Purification": "Remove harmful effects from allies.",
                "Sacred Knowledge": "Passive ability that increases healing power and resistance to dark magic."
            },
            CharacterClass.VOID_WALKER.value: {
                "Void Step": "Phase through reality to avoid damage and move quickly.",
                "Dark Pulse": "Release a wave of void energy that damages and disorients.",
                "Reality Tear": "Create a temporary portal to the void.",
                "Entropy Touch": "Drain energy from enemies to restore your own.",
                "Void Affinity": "Passive ability that grants resistance to void damage and improves void abilities."
            },
            CharacterClass.CELESTIAL.value: {
                "Starfall": "Call down a shower of celestial energy.",
                "Divine Shield": "Create an impenetrable barrier of divine light.",
                "Blessing of the Stars": "Grant powerful buffs to allies.",
                "Celestial Form": "Transform into a being of pure celestial energy.",
                "Astral Connection": "Passive ability that increases all celestial powers and grants minor health regeneration."
            }
        }
        
    def get_class_description(self, class_name: str) -> str:
        """Get the description for a character class"""
        return self.class_descriptions.get(class_name, "No description available.")
        
    def get_background_description(self, background_name: str) -> str:
        """Get the description for a character background"""
        return self.background_descriptions.get(background_name, "No description available.")
        
    def get_origin_description(self, origin_name: str) -> str:
        """Get the description for a character origin"""
        return self.origin_descriptions.get(origin_name, "No description available.")
        
    def get_available_abilities(self, class_name: str) -> List[str]:
        """Get the list of available abilities for a class"""
        return list(self.class_abilities.get(class_name, {}).keys())
        
    def get_ability_description(self, class_name: str, ability_name: str) -> str:
        """Get the description of a specific ability"""
        return self.class_abilities.get(class_name, {}).get(ability_name, "No description available.")
        
    def create_character(self, name: str, char_class: str, background: str, origin: str, 
                        base_attributes: Optional[Dict[str, int]] = None,
                        abilities: Optional[List[str]] = None) -> Optional['Character']:
        """Create a new character with the given attributes and abilities"""
        try:
            # Convert string values to enum members
            class_enum = next(c for c in CharacterClass if c.value == char_class)
            background_enum = next(b for b in CharacterBackground if b.value == background)
            origin_enum = next(o for o in CharacterOrigin if o.value == origin)
            
            return Character(name, class_enum, background_enum, origin_enum, base_attributes, abilities)
        except Exception as e:
            print(f"Error creating character: {e}")
            return None

class Character:
    def __init__(self, name: str, char_class: CharacterClass, background: CharacterBackground, 
                 origin: CharacterOrigin, base_attributes: Optional[Dict[str, int]] = None,
                 abilities: Optional[List[str]] = None):
        self.name = name
        self.char_class = char_class
        self.background = background
        self.origin = origin
        self.level = 1
        self.experience = 0
        self.attributes = base_attributes if base_attributes else self._get_base_attributes()
        self.abilities = abilities if abilities else []
        self._apply_background_bonus()
        
    def _get_base_attributes(self) -> Dict[str, int]:
        """Get base attributes based on character class"""
        base_attributes = {
            CharacterClass.WARRIOR: {
                "Strength": 15,
                "Constitution": 12,
                "Dexterity": 10,
                "Intelligence": 8,
                "Wisdom": 8,
                "Charisma": 8
            },
            CharacterClass.MAGE: {
                "Strength": 6,
                "Constitution": 8,
                "Dexterity": 8,
                "Intelligence": 15,
                "Wisdom": 12,
                "Charisma": 10
            },
            CharacterClass.ROGUE: {
                "Strength": 8,
                "Constitution": 8,
                "Dexterity": 15,
                "Intelligence": 10,
                "Wisdom": 10,
                "Charisma": 12
            },
            CharacterClass.MYSTIC: {
                "Strength": 8,
                "Constitution": 10,
                "Dexterity": 8,
                "Intelligence": 10,
                "Wisdom": 15,
                "Charisma": 12
            },
            CharacterClass.VOID_WALKER: {
                "Strength": 8,
                "Constitution": 10,
                "Dexterity": 12,
                "Intelligence": 12,
                "Wisdom": 12,
                "Charisma": 8
            },
            CharacterClass.CELESTIAL: {
                "Strength": 10,
                "Constitution": 10,
                "Dexterity": 8,
                "Intelligence": 10,
                "Wisdom": 12,
                "Charisma": 15
            }
        }
        return base_attributes[self.char_class].copy()
        
    def _apply_background_bonus(self):
        """Apply attribute bonuses based on background"""
        background_bonuses = {
            CharacterBackground.NOBLE: {
                "Charisma": 2,
                "Intelligence": 1
            },
            CharacterBackground.WANDERER: {
                "Dexterity": 2,
                "Constitution": 1
            },
            CharacterBackground.SCHOLAR: {
                "Intelligence": 2,
                "Wisdom": 1
            },
            CharacterBackground.OUTCAST: {
                "Dexterity": 2,
                "Wisdom": 1
            },
            CharacterBackground.MYSTIC: {
                "Wisdom": 2,
                "Charisma": 1
            },
            CharacterBackground.SOLDIER: {
                "Strength": 2,
                "Constitution": 1
            }
        }
        
        # Apply bonuses
        bonuses = background_bonuses[self.background]
        for attr, bonus in bonuses.items():
            self.attributes[attr] += bonus 