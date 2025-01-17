from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum, auto
import json
from src.combat_system.dimensional_combat import DimensionalLayer, DimensionalEffect
from src.character.ability_system import AbilityType
from src.character.progression_system import StatType, ProgressionPath

class CustomizationSlot(Enum):
    HEAD = auto()
    FACE = auto()
    HAIR = auto()
    BODY = auto()
    ARMS = auto()
    LEGS = auto()
    ACCESSORIES = auto()
    DIMENSIONAL_AURA = auto()

class VisualEffect(Enum):
    GLOW = auto()
    PARTICLES = auto()
    TRAIL = auto()
    DISTORTION = auto()
    ETHEREAL = auto()
    VOID_TENDRILS = auto()
    CELESTIAL_MARKS = auto()
    PRIMORDIAL_RUNES = auto()

class CustomizationRarity(Enum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    EPIC = auto()
    LEGENDARY = auto()
    DIMENSIONAL = auto()

@dataclass
class ColorScheme:
    """Represents a color scheme for customization"""
    primary: Tuple[int, int, int]
    secondary: Tuple[int, int, int]
    accent: Tuple[int, int, int]
    glow: Optional[Tuple[int, int, int]] = None
    particle_colors: List[Tuple[int, int, int]] = field(default_factory=list)

@dataclass
class CustomizationOption:
    """Represents a single customization option"""
    id: str
    name: str
    description: str
    slot: CustomizationSlot
    rarity: CustomizationRarity
    model_path: str
    texture_path: str
    effects: Set[VisualEffect]
    color_schemes: List[ColorScheme]
    dimension_requirements: Set[DimensionalLayer]
    stat_modifiers: Dict[StatType, float]
    ability_modifiers: Dict[AbilityType, float]
    unlock_condition: Optional[str] = None
    is_unlocked: bool = False

class CharacterCustomization:
    """Manages character customization options and appearances"""
    
    def __init__(self):
        self.available_options: Dict[CustomizationSlot, List[CustomizationOption]] = {
            slot: [] for slot in CustomizationSlot
        }
        self.equipped_options: Dict[CustomizationSlot, Optional[CustomizationOption]] = {
            slot: None for slot in CustomizationSlot
        }
        self.active_color_schemes: Dict[CustomizationSlot, ColorScheme] = {}
        self.unlocked_effects: Set[VisualEffect] = set()
        
        self._initialize_customization_options()
        
    def _initialize_customization_options(self) -> None:
        """Initialize available customization options"""
        # Basic options (always available)
        self._add_basic_options()
        
        # Dimensional options (unlocked through progression)
        self._add_dimensional_options()
        
    def _add_basic_options(self) -> None:
        """Add basic customization options"""
        # Head options
        self.available_options[CustomizationSlot.HEAD].extend([
            CustomizationOption(
                id="basic_helm",
                name="Basic Helm",
                description="A simple protective helm",
                slot=CustomizationSlot.HEAD,
                rarity=CustomizationRarity.COMMON,
                model_path="models/head/basic_helm.obj",
                texture_path="textures/head/basic_helm.png",
                effects=set(),
                color_schemes=[
                    ColorScheme(
                        primary=(128, 128, 128),
                        secondary=(96, 96, 96),
                        accent=(64, 64, 64)
                    )
                ],
                dimension_requirements={DimensionalLayer.PHYSICAL},
                stat_modifiers={StatType.DEFENSE: 0.1},
                ability_modifiers={},
                is_unlocked=True
            ),
            # Add more basic head options...
        ])
        
        # Add other basic options for each slot...
        
    def _add_dimensional_options(self) -> None:
        """Add dimension-specific customization options"""
        # Ethereal options
        self.available_options[CustomizationSlot.DIMENSIONAL_AURA].extend([
            CustomizationOption(
                id="ethereal_aura",
                name="Ethereal Aura",
                description="A mystical aura from the Ethereal Dimension",
                slot=CustomizationSlot.DIMENSIONAL_AURA,
                rarity=CustomizationRarity.DIMENSIONAL,
                model_path="models/aura/ethereal.obj",
                texture_path="textures/aura/ethereal.png",
                effects={VisualEffect.ETHEREAL, VisualEffect.GLOW},
                color_schemes=[
                    ColorScheme(
                        primary=(200, 220, 255),
                        secondary=(150, 180, 255),
                        accent=(100, 140, 255),
                        glow=(180, 200, 255),
                        particle_colors=[(220, 230, 255), (180, 200, 255)]
                    )
                ],
                dimension_requirements={DimensionalLayer.ETHEREAL},
                stat_modifiers={
                    StatType.DIMENSIONAL_ATTUNEMENT: 0.2,
                    StatType.STABILITY_CONTROL: 0.1
                },
                ability_modifiers={AbilityType.ETHEREAL: 0.15},
                unlock_condition="ethereal_mastery"
            )
        ])
        
        # Add other dimensional options...
        
    def unlock_option(
        self,
        option_id: str,
        available_dimensions: Set[DimensionalLayer]
    ) -> bool:
        """Attempt to unlock a customization option"""
        for options in self.available_options.values():
            for option in options:
                if option.id == option_id:
                    if not option.dimension_requirements.issubset(available_dimensions):
                        return False
                    option.is_unlocked = True
                    return True
        return False
        
    def equip_option(
        self,
        option_id: str,
        available_dimensions: Set[DimensionalLayer]
    ) -> bool:
        """Attempt to equip a customization option"""
        for options in self.available_options.values():
            for option in options:
                if option.id == option_id:
                    if not option.is_unlocked:
                        return False
                    if not option.dimension_requirements.issubset(available_dimensions):
                        return False
                    self.equipped_options[option.slot] = option
                    return True
        return False
        
    def unequip_option(self, slot: CustomizationSlot) -> bool:
        """Unequip option from slot"""
        if self.equipped_options[slot] is None:
            return False
        self.equipped_options[slot] = None
        return True
        
    def set_color_scheme(
        self,
        slot: CustomizationSlot,
        color_scheme: ColorScheme
    ) -> bool:
        """Set color scheme for a slot"""
        if slot not in self.equipped_options or self.equipped_options[slot] is None:
            return False
            
        option = self.equipped_options[slot]
        if color_scheme not in option.color_schemes:
            return False
            
        self.active_color_schemes[slot] = color_scheme
        return True
        
    def unlock_effect(self, effect: VisualEffect) -> None:
        """Unlock a visual effect"""
        self.unlocked_effects.add(effect)
        
    def get_active_effects(self) -> Set[VisualEffect]:
        """Get all currently active visual effects"""
        active_effects = set()
        for option in self.equipped_options.values():
            if option is not None:
                active_effects.update(
                    effect for effect in option.effects
                    if effect in self.unlocked_effects
                )
        return active_effects
        
    def get_stat_modifiers(self) -> Dict[StatType, float]:
        """Get combined stat modifiers from equipped options"""
        modifiers = {}
        for option in self.equipped_options.values():
            if option is not None:
                for stat, mod in option.stat_modifiers.items():
                    modifiers[stat] = modifiers.get(stat, 0.0) + mod
        return modifiers
        
    def get_ability_modifiers(self) -> Dict[AbilityType, float]:
        """Get combined ability modifiers from equipped options"""
        modifiers = {}
        for option in self.equipped_options.values():
            if option is not None:
                for ability_type, mod in option.ability_modifiers.items():
                    modifiers[ability_type] = modifiers.get(ability_type, 0.0) + mod
        return modifiers
        
    def save_customization(self, file_path: str) -> None:
        """Save current customization to file"""
        save_data = {
            "equipped_options": {
                slot.name: option.id if option else None
                for slot, option in self.equipped_options.items()
            },
            "active_color_schemes": {
                slot.name: {
                    "primary": scheme.primary,
                    "secondary": scheme.secondary,
                    "accent": scheme.accent,
                    "glow": scheme.glow,
                    "particle_colors": scheme.particle_colors
                }
                for slot, scheme in self.active_color_schemes.items()
            },
            "unlocked_effects": [effect.name for effect in self.unlocked_effects]
        }
        
        with open(file_path, 'w') as f:
            json.dump(save_data, f, indent=2)
            
    def load_customization(
        self,
        file_path: str,
        available_dimensions: Set[DimensionalLayer]
    ) -> bool:
        """Load customization from file"""
        try:
            with open(file_path, 'r') as f:
                save_data = json.load(f)
                
            # Load equipped options
            for slot_name, option_id in save_data["equipped_options"].items():
                if option_id:
                    self.equip_option(option_id, available_dimensions)
                    
            # Load color schemes
            for slot_name, scheme_data in save_data["active_color_schemes"].items():
                slot = CustomizationSlot[slot_name]
                scheme = ColorScheme(
                    primary=tuple(scheme_data["primary"]),
                    secondary=tuple(scheme_data["secondary"]),
                    accent=tuple(scheme_data["accent"]),
                    glow=tuple(scheme_data["glow"]) if scheme_data["glow"] else None,
                    particle_colors=[
                        tuple(color) for color in scheme_data["particle_colors"]
                    ]
                )
                self.set_color_scheme(slot, scheme)
                
            # Load unlocked effects
            self.unlocked_effects = {
                VisualEffect[effect_name]
                for effect_name in save_data["unlocked_effects"]
            }
            
            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return False 