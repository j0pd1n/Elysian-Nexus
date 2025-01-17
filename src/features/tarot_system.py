from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass
import random
from visual_system import VisualSystem
from sound_system import SoundManager, SoundType, SoundTheme, SoundProfile
from lore_system import LoreSystem, LoreJournal, LoreEntry, LoreCategory
import logging  # Added for logging errors

class TarotCardType(Enum):
    FOOL = "The Fool"                # 🎭
    MAGICIAN = "The Magician"        # 🪄
    HIGH_PRIESTESS = "The High Priestess" # 👸
    EMPRESS = "The Empress"          # 👑
    EMPEROR = "The Emperor"          # 🛡️
    LOVERS = "The Lovers"            # ❤️
    CHARIOT = "The Chariot"          # 🚗
    STRENGTH = "Strength"            # 💪
    HERMIT = "The Hermit"            # 🧙
    WHEEL_OF_FORTUNE = "Wheel of Fortune" # 🎡
    JUSTICE = "Justice"              # ⚖️
    HANGED_MAN = "The Hanged Man"    # 🪢
    DEATH = "Death"                  # 💀
    TEMPERANCE = "Temperance"        # ⚗️
    DEVIL = "The Devil"              # 😈
    TOWER = "The Tower"              # 🏰
    STAR = "The Star"                # 🌟
    MOON = "The Moon"                # 🌙
    SUN = "The Sun"                  # ☀️
    JUDGEMENT = "Judgement"          # 🔔
    WORLD = "The World"              # 🌍

@dataclass
class TarotCard:
    id: str
    name: TarotCardType
    description: str
    effect: str
    icon: str
    value: int

def initialize_tarot_cards():
    """Initialize tarot cards."""
    tarot_cards = [
        TarotCard(
            id="fool",
            name=TarotCardType.FOOL,
            description="Represents new beginnings and adventures.",
            effect="Grants a temporary boost to agility and luck.",
            icon="🎭",
            value=100
        ),
        TarotCard(
            id="magician",
            name=TarotCardType.MAGICIAN,
            description="Symbolizes skill and resourcefulness.",
            effect="Increases spell power and reduces mana cost for a short duration.",
            icon="🪄",
            value=150
        ),
        TarotCard(
            id="high_priestess",
            name=TarotCardType.HIGH_PRIESTESS,
            description="Represents intuition and wisdom.",
            effect="Provides insight into enemy weaknesses, increasing critical hit chance.",
            icon="👸",
            value=200
        ),
        TarotCard(
            id="empress",
            name=TarotCardType.EMPRESS,
            description="Symbolizes fertility and abundance.",
            effect="Restores health over time and increases resource gathering.",
            icon="👑",
            value=250
        ),
        TarotCard(
            id="emperor",
            name=TarotCardType.EMPEROR,
            description="Represents authority and control.",
            effect="Increases defense and grants temporary immunity to crowd control effects.",
            icon="🛡️",
            value=300
        ),
        TarotCard(
            id="lovers",
            name=TarotCardType.LOVERS,
            description="Symbolizes relationships and choices.",
            effect="Grants a temporary buff to allies, increasing their damage output.",
            icon="❤️",
            value=200
        ),
        TarotCard(
            id="chariot",
            name=TarotCardType.CHARIOT,
            description="Represents determination and willpower.",
            effect="Increases movement speed and reduces cooldowns for a short time.",
            icon="🚗",
            value=250
        ),
        TarotCard(
            id="strength",
            name=TarotCardType.STRENGTH,
            description="Symbolizes courage and inner strength.",
            effect="Temporarily increases strength and damage resistance.",
            icon="💪",
            value=300
        ),
        TarotCard(
            id="hermit",
            name=TarotCardType.HERMIT,
            description="Represents introspection and solitude.",
            effect="Grants temporary invisibility and increased stealth.",
            icon="🧙",
            value=350
        ),
        TarotCard(
            id="wheel_of_fortune",
            name=TarotCardType.WHEEL_OF_FORTUNE,
            description="Symbolizes fate and cycles.",
            effect="Randomly grants a buff or debuff to the player or enemies.",
            icon="🎡",
            value=400
        ),
        TarotCard(
            id="justice",
            name=TarotCardType.JUSTICE,
            description="Represents fairness and truth.",
            effect="Increases critical hit damage and accuracy for a short duration.",
            icon="⚖️",
            value=300
        ),
        TarotCard(
            id="hanged_man",
            name=TarotCardType.HANGED_MAN,
            description="Symbolizes sacrifice and letting go.",
            effect="Temporarily increases experience gain but reduces damage output.",
            icon="🪢",
            value=250
        ),
        TarotCard(
            id="death",
            name=TarotCardType.DEATH,
            description="Represents transformation and endings.",
            effect="Revives the player upon death with a portion of health.",
            icon="💀",
            value=500
        ),
        TarotCard(
            id="temperance",
            name=TarotCardType.TEMPERANCE,
            description="Symbolizes balance and moderation.",
            effect="Restores health and mana over time.",
            icon="⚗️",
            value=300
        ),
        TarotCard(
            id="devil",
            name=TarotCardType.DEVIL,
            description="Represents temptation and materialism.",
            effect="Grants a temporary power boost at the cost of health.",
            icon="😈",
            value=400
        ),
        TarotCard(
            id="tower",
            name=TarotCardType.TOWER,
            description="Symbolizes chaos and upheaval.",
            effect="Causes a random debuff to all enemies in the vicinity.",
            icon="🏰",
            value=450
        ),
        TarotCard(
            id="star",
            name=TarotCardType.STAR,
            description="Represents hope and inspiration.",
            effect="Grants a temporary boost to morale and luck.",
            icon="🌟",
            value=350
        ),
        TarotCard(
            id="moon",
            name=TarotCardType.MOON,
            description="Symbolizes intuition and the subconscious.",
            effect="Grants insight into hidden truths and increases stealth.",
            icon="🌙",
            value=400
        ),
        TarotCard(
            id="sun",
            name=TarotCardType.SUN,
            description="Represents joy and success.",
            effect="Restores health and grants a temporary buff to all stats.",
            icon="☀️",
            value=500
        ),
        TarotCard(
            id="judgement",
            name=TarotCardType.JUDGEMENT,
            description="Symbolizes rebirth and inner calling.",
            effect="Revives fallen allies with a portion of health.",
            icon="🔔",
            value=600
        ),
        TarotCard(
            id="world",
            name=TarotCardType.WORLD,
            description="Represents completion and fulfillment.",
            effect="Grants a significant boost to experience gain and resource gathering.",
            icon="🌍",
            value=700
        ),
    ]
    return tarot_cards 

@dataclass
class TarotNPC:
    card_type: TarotCardType
    name: str
    dialogue: str
    quest: Optional[str] = None
    
    def interact(self):
        """Handle interaction with the NPC."""
        print(f"{self.name}: {self.dialogue}")
        if self.quest:
            print(f"{self.name} offers you a quest: {self.quest}")
            # Trigger quest assignment logic here
            
    def play_sound_effect(self, sound_manager: SoundManager):
        """Play sound effects related to NPC interactions."""
        if self.card_type == TarotCardType.FOOL:
            sound_manager.play_sound(SoundType.EFFECT, "fool_npc_retro")
        elif self.card_type == TarotCardType.MAGICIAN:
            sound_manager.play_sound(SoundType.EFFECT, "magician_npc_retro")
        # Add more conditions for other tarot cards 