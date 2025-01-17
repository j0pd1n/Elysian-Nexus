from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Any
from enum import Enum, auto
import json
from datetime import datetime

from ..combat_system.dimensional_combat import DimensionalLayer, DimensionalEffect
from .ability_system import AbilityType
from .progression_system import StatType, ProgressionPath

class CustomizationLayer(Enum):
    """Layers for character customization"""
    BASE = auto()          # Base character model
    SKIN = auto()          # Skin textures and colors
    MARKINGS = auto()      # Tattoos, scars, etc.
    EQUIPMENT = auto()     # Worn equipment
    AURA = auto()          # Energy auras
    EFFECTS = auto()       # Visual effects
    DIMENSIONAL = auto()   # Dimensional modifications

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
    
    def blend_with(self, other: 'ColorScheme', factor: float) -> 'ColorScheme':
        """Blend two color schemes"""
        def blend_color(c1: Tuple[int, int, int], c2: Tuple[int, int, int], f: float) -> Tuple[int, int, int]:
            return tuple(int(c1[i] * (1 - f) + c2[i] * f) for i in range(3))
        
        return ColorScheme(
            primary=blend_color(self.primary, other.primary, factor),
            secondary=blend_color(self.secondary, other.secondary, factor),
            accent=blend_color(self.accent, other.accent, factor),
            glow=blend_color(self.glow, other.glow, factor) if self.glow and other.glow else self.glow or other.glow,
            particle_colors=[
                blend_color(c1, c2, factor)
                for c1, c2 in zip(self.particle_colors, other.particle_colors)
            ] if self.particle_colors and other.particle_colors else self.particle_colors or other.particle_colors
        )

@dataclass
class DimensionalAppearance:
    """Represents appearance modifications from dimensional influence"""
    dimension: DimensionalLayer
    distortion_level: float = 0.0
    corruption_level: float = 0.0
    effect_intensity: float = 1.0
    active_effects: Set[VisualEffect] = field(default_factory=set)
    color_scheme: Optional[ColorScheme] = None
    
    def blend_with(self, other: 'DimensionalAppearance', factor: float) -> 'DimensionalAppearance':
        """Blend two dimensional appearances"""
        return DimensionalAppearance(
            dimension=self.dimension,
            distortion_level=self.distortion_level * (1 - factor) + other.distortion_level * factor,
            corruption_level=self.corruption_level * (1 - factor) + other.corruption_level * factor,
            effect_intensity=self.effect_intensity * (1 - factor) + other.effect_intensity * factor,
            active_effects=self.active_effects.union(other.active_effects),
            color_scheme=self.color_scheme.blend_with(other.color_scheme, factor) if self.color_scheme and other.color_scheme else self.color_scheme or other.color_scheme
        )

@dataclass
class CustomizationOption:
    """Represents a single customization option"""
    id: str
    name: str
    description: str
    slot: CustomizationSlot
    layer: CustomizationLayer
    rarity: CustomizationRarity
    model_path: str
    texture_path: str
    effects: Set[VisualEffect]
    color_schemes: List[ColorScheme]
    dimension_requirements: Set[DimensionalLayer]
    stat_modifiers: Dict[StatType, float]
    ability_modifiers: Dict[AbilityType, float]
    dimensional_influence: Optional[DimensionalAppearance] = None
    unlock_condition: Optional[str] = None
    is_unlocked: bool = False
    
    def can_layer_with(self, other: 'CustomizationOption') -> bool:
        """Check if this option can be layered with another"""
        if self.slot != other.slot:
            return True
        if self.layer == other.layer:
            return False
        if self.layer == CustomizationLayer.BASE and other.layer != CustomizationLayer.BASE:
            return True
        if self.layer == CustomizationLayer.EFFECTS and other.layer != CustomizationLayer.EFFECTS:
            return True
        return False

class CharacterCustomization:
    """Manages character customization options and appearances"""
    
    def __init__(self):
        self.available_options: Dict[CustomizationSlot, Dict[CustomizationLayer, List[CustomizationOption]]] = {
            slot: {layer: [] for layer in CustomizationLayer}
            for slot in CustomizationSlot
        }
        self.equipped_options: Dict[CustomizationSlot, Dict[CustomizationLayer, Optional[CustomizationOption]]] = {
            slot: {layer: None for layer in CustomizationLayer}
            for slot in CustomizationSlot
        }
        self.active_color_schemes: Dict[CustomizationSlot, Dict[CustomizationLayer, ColorScheme]] = {
            slot: {} for slot in CustomizationSlot
        }
        self.dimensional_appearances: Dict[DimensionalLayer, DimensionalAppearance] = {}
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
        # Base layer options
        base_options = [
            CustomizationOption(
                id="basic_humanoid",
                name="Basic Humanoid Form",
                description="Standard humanoid form",
                slot=CustomizationSlot.BODY,
                layer=CustomizationLayer.BASE,
                rarity=CustomizationRarity.COMMON,
                model_path="models/base/humanoid.obj",
                texture_path="textures/base/humanoid.png",
                effects=set(),
                color_schemes=[
                    ColorScheme(
                        primary=(200, 180, 160),
                        secondary=(180, 160, 140),
                        accent=(160, 140, 120)
                    )
                ],
                dimension_requirements={DimensionalLayer.PHYSICAL},
                stat_modifiers={},
                ability_modifiers={},
                is_unlocked=True
            )
        ]
        
        for option in base_options:
            self.available_options[option.slot][option.layer].append(option)
            
        # Add other basic options for each slot and layer...
        
    def _add_dimensional_options(self) -> None:
        """Add dimension-specific customization options"""
        # Ethereal dimension options
        ethereal_options = [
            CustomizationOption(
                id="ethereal_form",
                name="Ethereal Form",
                description="A form influenced by the Ethereal Dimension",
                slot=CustomizationSlot.BODY,
                layer=CustomizationLayer.DIMENSIONAL,
                rarity=CustomizationRarity.DIMENSIONAL,
                model_path="models/dimensional/ethereal_body.obj",
                texture_path="textures/dimensional/ethereal_body.png",
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
                dimensional_influence=DimensionalAppearance(
                    dimension=DimensionalLayer.ETHEREAL,
                    effect_intensity=1.0,
                    active_effects={VisualEffect.ETHEREAL, VisualEffect.GLOW}
                ),
                unlock_condition="ethereal_mastery"
            )
        ]
        
        for option in ethereal_options:
            self.available_options[option.slot][option.layer].append(option)
            
        # Add other dimensional options...
        
    def unlock_option(
        self,
        option_id: str,
        available_dimensions: Set[DimensionalLayer]
    ) -> bool:
        """Attempt to unlock a customization option"""
        for slot_options in self.available_options.values():
            for layer_options in slot_options.values():
                for option in layer_options:
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
        # Find the option
        target_option = None
        for slot_options in self.available_options.values():
            for layer_options in slot_options.values():
                for option in layer_options:
                    if option.id == option_id:
                        target_option = option
                        break
                if target_option:
                    break
            if target_option:
                break
                
        if not target_option:
            return False
            
        if not target_option.is_unlocked:
            return False
            
        if not target_option.dimension_requirements.issubset(available_dimensions):
            return False
            
        # Check layer compatibility
        current_options = self.equipped_options[target_option.slot]
        for layer, equipped in current_options.items():
            if equipped and not target_option.can_layer_with(equipped):
                return False
                
        # Equip the option
        self.equipped_options[target_option.slot][target_option.layer] = target_option
        
        # Apply dimensional influence if present
        if target_option.dimensional_influence:
            self.apply_dimensional_influence(target_option.dimensional_influence)
            
        return True
        
    def apply_dimensional_influence(
        self,
        influence: DimensionalAppearance
    ) -> None:
        """Apply dimensional influence to character appearance"""
        if influence.dimension not in self.dimensional_appearances:
            self.dimensional_appearances[influence.dimension] = influence
        else:
            current = self.dimensional_appearances[influence.dimension]
            self.dimensional_appearances[influence.dimension] = current.blend_with(
                influence,
                influence.effect_intensity
            )
            
    def get_current_appearance(self) -> Dict[str, Any]:
        """Get current character appearance data"""
        appearance = {
            'equipped_options': {},
            'color_schemes': {},
            'effects': list(self.get_active_effects()),
            'dimensional_influences': {}
        }
        
        # Gather equipped options
        for slot in CustomizationSlot:
            appearance['equipped_options'][slot.name] = {
                layer.name: option.id if option else None
                for layer, option in self.equipped_options[slot].items()
            }
            
        # Gather color schemes
        for slot in CustomizationSlot:
            if slot in self.active_color_schemes:
                appearance['color_schemes'][slot.name] = {
                    layer.name: {
                        'primary': scheme.primary,
                        'secondary': scheme.secondary,
                        'accent': scheme.accent,
                        'glow': scheme.glow,
                        'particle_colors': scheme.particle_colors
                    }
                    for layer, scheme in self.active_color_schemes[slot].items()
                }
                
        # Gather dimensional influences
        for dimension, influence in self.dimensional_appearances.items():
            appearance['dimensional_influences'][dimension.name] = {
                'distortion_level': influence.distortion_level,
                'corruption_level': influence.corruption_level,
                'effect_intensity': influence.effect_intensity,
                'active_effects': [effect.name for effect in influence.active_effects]
            }
            
        return appearance
        
    def save_customization(self, file_path: str) -> None:
        """Save current customization to file"""
        save_data = self.get_current_appearance()
        with open(file_path, 'w') as f:
            json.dump(save_data, f, indent=4)
            
    def load_customization(
        self,
        file_path: str,
        available_dimensions: Set[DimensionalLayer]
    ) -> bool:
        """Load customization from file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            # Clear current customization
            self.__init__()
            
            # Load equipped options
            for slot_name, layers in data['equipped_options'].items():
                slot = CustomizationSlot[slot_name]
                for layer_name, option_id in layers.items():
                    if option_id:
                        self.equip_option(option_id, available_dimensions)
                        
            # Load color schemes
            for slot_name, layers in data['color_schemes'].items():
                slot = CustomizationSlot[slot_name]
                for layer_name, scheme_data in layers.items():
                    layer = CustomizationLayer[layer_name]
                    self.active_color_schemes[slot][layer] = ColorScheme(
                        primary=tuple(scheme_data['primary']),
                        secondary=tuple(scheme_data['secondary']),
                        accent=tuple(scheme_data['accent']),
                        glow=tuple(scheme_data['glow']) if scheme_data['glow'] else None,
                        particle_colors=[tuple(c) for c in scheme_data['particle_colors']]
                    )
                    
            return True
        except Exception as e:
            print(f"Error loading customization: {e}")
            return False
            
    def get_stat_modifiers(self) -> Dict[StatType, float]:
        """Get combined stat modifiers from equipped options"""
        modifiers = {}
        for slot_options in self.equipped_options.values():
            for option in slot_options.values():
                if option:
                    for stat, mod in option.stat_modifiers.items():
                        modifiers[stat] = modifiers.get(stat, 0.0) + mod
        return modifiers
        
    def get_ability_modifiers(self) -> Dict[AbilityType, float]:
        """Get combined ability modifiers from equipped options"""
        modifiers = {}
        for slot_options in self.equipped_options.values():
            for option in slot_options.values():
                if option:
                    for ability_type, mod in option.ability_modifiers.items():
                        modifiers[ability_type] = modifiers.get(ability_type, 0.0) + mod
        return modifiers
        
    def get_active_effects(self) -> Set[VisualEffect]:
        """Get all currently active visual effects"""
        active_effects = set()
        
        # Get effects from equipped options
        for slot_options in self.equipped_options.values():
            for option in slot_options.values():
                if option:
                    active_effects.update(
                        effect for effect in option.effects
                        if effect in self.unlocked_effects
                    )
                    
        # Get effects from dimensional influences
        for influence in self.dimensional_appearances.values():
            active_effects.update(influence.active_effects)
            
        return active_effects 