from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Dict, Optional, Set
from .combat_types import Position
import math

class DimensionalLayer(Enum):
    """Different dimensional layers in combat"""
    PHYSICAL = auto()
    ETHEREAL = auto()
    VOID = auto()
    CELESTIAL = auto()
    PRIMORDIAL = auto()

class DimensionalEffect(Enum):
    """Effects that can occur between dimensions"""
    RESONANCE = auto()  # Amplifies effects between harmonious dimensions
    DISSONANCE = auto()  # Creates interference between conflicting dimensions
    PHASING = auto()    # Allows movement between dimensions
    ANCHORING = auto()  # Prevents dimensional movement
    WARPING = auto()    # Distorts space within a dimension

@dataclass
class DimensionalState:
    """Represents the state of a dimension in combat"""
    layer: DimensionalLayer
    stability: float  # 0.0 to 1.0, affects ability effectiveness
    distortion_level: float  # Amount of spatial distortion
    active_effects: Set[DimensionalEffect]
    connected_layers: Set[DimensionalLayer]

class DimensionalCombat:
    """Manages dimensional aspects of combat"""
    
    def __init__(self):
        self.dimensional_states: Dict[DimensionalLayer, DimensionalState] = {}
        self.initialize_dimensions()

    def initialize_dimensions(self):
        """Set up initial dimensional states"""
        for layer in DimensionalLayer:
            self.dimensional_states[layer] = DimensionalState(
                layer=layer,
                stability=1.0,
                distortion_level=0.0,
                active_effects=set(),
                connected_layers=set()
            )
        
        # Set up initial dimensional connections
        self._connect_dimensions(DimensionalLayer.PHYSICAL, DimensionalLayer.ETHEREAL)
        self._connect_dimensions(DimensionalLayer.ETHEREAL, DimensionalLayer.VOID)
        self._connect_dimensions(DimensionalLayer.VOID, DimensionalLayer.CELESTIAL)
        self._connect_dimensions(DimensionalLayer.CELESTIAL, DimensionalLayer.PRIMORDIAL)

    def _connect_dimensions(self, layer1: DimensionalLayer, layer2: DimensionalLayer):
        """Create a connection between two dimensional layers"""
        self.dimensional_states[layer1].connected_layers.add(layer2)
        self.dimensional_states[layer2].connected_layers.add(layer1)

    def calculate_dimensional_effect(self, 
                                  source_layer: DimensionalLayer,
                                  target_layer: DimensionalLayer,
                                  base_power: float) -> float:
        """Calculate how power changes when crossing dimensions"""
        source_state = self.dimensional_states[source_layer]
        target_state = self.dimensional_states[target_layer]
        
        # Base multiplier affected by stability
        multiplier = source_state.stability * target_state.stability
        
        # Apply resonance/dissonance effects
        if DimensionalEffect.RESONANCE in source_state.active_effects:
            multiplier *= 1.5
        if DimensionalEffect.DISSONANCE in target_state.active_effects:
            multiplier *= 0.7
            
        # Distance penalty for non-connected dimensions
        if target_layer not in source_state.connected_layers:
            multiplier *= 0.5
            
        return base_power * multiplier

    def apply_dimensional_distortion(self, 
                                  position: Position,
                                  layer: DimensionalLayer) -> Position:
        """Apply dimensional distortion to a position"""
        state = self.dimensional_states[layer]
        if state.distortion_level == 0:
            return position
            
        # Apply non-linear spatial distortion
        distortion = state.distortion_level
        theta = math.atan2(position.y, position.x)
        r = math.sqrt(position.x**2 + position.y**2)
        
        # Spiral distortion
        new_theta = theta + distortion * r / 10
        new_r = r * (1 + math.sin(theta) * distortion / 5)
        
        return Position(
            x=new_r * math.cos(new_theta),
            y=new_r * math.sin(new_theta),
            z=position.z * (1 + distortion/10),
            dimensional_layer=position.dimensional_layer
        )

    def can_traverse_dimensions(self,
                             source_layer: DimensionalLayer,
                             target_layer: DimensionalLayer) -> bool:
        """Check if dimensional traversal is possible"""
        source_state = self.dimensional_states[source_layer]
        
        # Check if dimensions are connected
        if target_layer not in source_state.connected_layers:
            return False
            
        # Check for blocking effects
        if DimensionalEffect.ANCHORING in source_state.active_effects:
            return False
            
        # Check stability requirements
        if source_state.stability < 0.3:
            return False
            
        return True

    def update_dimensional_stability(self, layer: DimensionalLayer, delta: float):
        """Update the stability of a dimensional layer"""
        state = self.dimensional_states[layer]
        state.stability = max(0.0, min(1.0, state.stability + delta))
        
        # Propagate instability to connected dimensions
        for connected_layer in state.connected_layers:
            connected_state = self.dimensional_states[connected_layer]
            connected_state.stability = max(0.0, min(1.0, 
                connected_state.stability + delta * 0.3))

    def add_dimensional_effect(self,
                            layer: DimensionalLayer,
                            effect: DimensionalEffect,
                            propagate: bool = True):
        """Add an effect to a dimensional layer"""
        state = self.dimensional_states[layer]
        state.active_effects.add(effect)
        
        if propagate:
            # Propagate effects to connected dimensions with reduced intensity
            for connected_layer in state.connected_layers:
                if effect not in self.dimensional_states[connected_layer].active_effects:
                    self.add_dimensional_effect(connected_layer, effect, False)

    def remove_dimensional_effect(self,
                               layer: DimensionalLayer,
                               effect: DimensionalEffect,
                               propagate: bool = True):
        """Remove an effect from a dimensional layer"""
        state = self.dimensional_states[layer]
        if effect in state.active_effects:
            state.active_effects.remove(effect)
            
        if propagate:
            for connected_layer in state.connected_layers:
                self.remove_dimensional_effect(connected_layer, effect, False) 