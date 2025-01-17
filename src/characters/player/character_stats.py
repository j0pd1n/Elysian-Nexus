from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass

class AttributeType(Enum):
    STRENGTH = "Strength"
    DEXTERITY = "Dexterity"
    CONSTITUTION = "Constitution"
    INTELLIGENCE = "Intelligence"
    WISDOM = "Wisdom"
    CHARISMA = "Charisma"

class StatusEffect(Enum):
    BLESSED = "Blessed"
    CURSED = "Cursed"
    EMPOWERED = "Empowered"
    WEAKENED = "Weakened"
    PROTECTED = "Protected"
    VULNERABLE = "Vulnerable"
    INSPIRED = "Inspired"
    DISCOURAGED = "Discouraged"
    ENLIGHTENED = "Enlightened"
    CONFUSED = "Confused"

@dataclass
class Effect:
    type: StatusEffect
    duration: int
    magnitude: float
    icon: str
    description: str

class CharacterStats:
    def __init__(self, name: str, attributes: Dict[str, int]):
        self.name = name
        self.attributes = attributes
        self.level = 1
        self.experience = 0
        self.health = 100
        self.max_health = 100
        self.mana = 100
        self.max_mana = 100
        self.gold = 0
        self.active_effects: List[Effect] = []
        
        # Calculate derived stats
        self.update_derived_stats()
    
    def update_derived_stats(self):
        """Update stats derived from attributes"""
        # Health is influenced by Constitution
        constitution = self.attributes.get(AttributeType.CONSTITUTION.value, 10)
        self.max_health = 100 + (constitution - 10) * 10
        self.health = min(self.health, self.max_health)
        
        # Mana is influenced by Intelligence and Wisdom
        intelligence = self.attributes.get(AttributeType.INTELLIGENCE.value, 10)
        wisdom = self.attributes.get(AttributeType.WISDOM.value, 10)
        self.max_mana = 100 + ((intelligence + wisdom) / 2 - 10) * 10
        self.mana = min(self.mana, self.max_mana)
    
    def add_effect(self, effect_type: StatusEffect, duration: int, magnitude: float = 1.0):
        """Add a status effect to the character"""
        effect_data = {
            StatusEffect.BLESSED: {
                "icon": "✨",
                "description": "Increased luck and divine favor"
            },
            StatusEffect.CURSED: {
                "icon": "💀",
                "description": "Decreased luck and misfortune"
            },
            StatusEffect.EMPOWERED: {
                "icon": "💪",
                "description": "Increased strength and power"
            },
            StatusEffect.WEAKENED: {
                "icon": "🌧️",
                "description": "Decreased strength and power"
            },
            StatusEffect.PROTECTED: {
                "icon": "🛡️",
                "description": "Increased defense"
            },
            StatusEffect.VULNERABLE: {
                "icon": "🎯",
                "description": "Decreased defense"
            },
            StatusEffect.INSPIRED: {
                "icon": "⭐",
                "description": "Increased creativity and skill"
            },
            StatusEffect.DISCOURAGED: {
                "icon": "💔",
                "description": "Decreased morale"
            },
            StatusEffect.ENLIGHTENED: {
                "icon": "🌟",
                "description": "Increased wisdom and insight"
            },
            StatusEffect.CONFUSED: {
                "icon": "💫",
                "description": "Decreased accuracy and focus"
            }
        }
        
        effect_info = effect_data.get(effect_type)
        if effect_info:
            effect = Effect(
                type=effect_type,
                duration=duration,
                magnitude=magnitude,
                icon=effect_info["icon"],
                description=effect_info["description"]
            )
            self.active_effects.append(effect)
            print(f"{effect.icon} Gained effect: {effect_type.value} ({effect.description})")
    
    def remove_effect(self, effect_type: StatusEffect):
        """Remove a status effect from the character"""
        self.active_effects = [e for e in self.active_effects if e.type != effect_type]
    
    def update_effects(self):
        """Update duration of active effects and remove expired ones"""
        expired = []
        for effect in self.active_effects:
            effect.duration -= 1
            if effect.duration <= 0:
                expired.append(effect)
        
        for effect in expired:
            print(f"Effect {effect.type.value} has expired!")
            self.active_effects.remove(effect)
    
    def gain_experience(self, amount: int):
        """Add experience points and handle level ups"""
        self.experience += amount
        
        # Check for level up
        while self.experience >= 100:
            self.level_up()
            self.experience -= 100
    
    def level_up(self):
        """Handle level up logic"""
        self.level += 1
        print(f"\n✨ Level Up! Now level {self.level}")
        
        # Increase max health and mana
        old_max_health = self.max_health
        old_max_mana = self.max_mana
        
        self.max_health += 10
        self.max_mana += 5
        
        # Heal to full on level up
        self.health = self.max_health
        self.mana = self.max_mana
        
        print(f"Max Health increased by {self.max_health - old_max_health}")
        print(f"Max Mana increased by {self.max_mana - old_max_mana}")
        
        # Allow attribute increase
        print("\nChoose an attribute to increase:")
        for attr in AttributeType:
            print(f"{attr.value}: {self.attributes[attr.value]}")
        
        while True:
            choice = input("\nEnter attribute name: ").capitalize()
            if choice in [attr.value for attr in AttributeType]:
                self.attributes[choice] += 1
                print(f"✨ {choice} increased to {self.attributes[choice]}")
                break
            print("Invalid attribute choice!")
        
        # Update derived stats
        self.update_derived_stats()
    
    def modify_health(self, amount: int):
        """Modify character's health, keeping it within bounds"""
        self.health = max(0, min(self.health + amount, self.max_health))
        if amount > 0:
            print(f"💚 Healed for {amount} health")
        else:
            print(f"💔 Took {-amount} damage")
    
    def modify_mana(self, amount: int):
        """Modify character's mana, keeping it within bounds"""
        self.mana = max(0, min(self.mana + amount, self.max_mana))
        if amount > 0:
            print(f"✨ Gained {amount} mana")
        else:
            print(f"💫 Used {-amount} mana")
    
    def modify_gold(self, amount: int):
        """Modify character's gold"""
        self.gold = max(0, self.gold + amount)
        if amount > 0:
            print(f"💰 Gained {amount} gold")
        else:
            print(f"💸 Spent {-amount} gold")
    
    def get_status(self) -> str:
        """Get a formatted string of the character's current status"""
        status = [
            f"=== {self.name}'s Status ===",
            f"Level: {self.level} ({self.experience}/100 XP)",
            f"Health: {self.health}/{self.max_health}",
            f"Mana: {self.mana}/{self.max_mana}",
            f"Gold: {self.gold}",
            "\nAttributes:"
        ]
        
        for attr, value in self.attributes.items():
            status.append(f"  {attr}: {value}")
        
        if self.active_effects:
            status.append("\nActive Effects:")
            for effect in self.active_effects:
                status.append(f"  {effect.icon} {effect.type.value} ({effect.duration}s)")
        
        return "\n".join(status) 