from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional, Set, Tuple, Any
from .combat_types import Position, DamageType
import math
import random
from datetime import datetime

class DimensionalLayer(Enum):
    """Different dimensional layers in combat"""
    PHYSICAL = auto()    # Normal physical realm
    ETHEREAL = auto()    # Spirit/energy realm
    VOID = auto()        # Chaos/entropy realm
    CELESTIAL = auto()   # Cosmic/stellar realm
    PRIMORDIAL = auto()  # Reality-warping realm

class DimensionalEffect(Enum):
    """Effects that can occur between dimensions"""
    RESONANCE = auto()    # Amplifies effects between harmonious dimensions
    DISSONANCE = auto()   # Creates interference between conflicting dimensions
    PHASING = auto()      # Allows movement between dimensions
    ANCHORING = auto()    # Prevents dimensional movement
    WARPING = auto()      # Distorts space within a dimension
    CORRUPTION = auto()   # Corrupts and destabilizes dimensions
    PURIFICATION = auto() # Cleanses and stabilizes dimensions
    CONVERGENCE = auto()  # Merges dimensional effects
    DIVERGENCE = auto()   # Separates dimensional effects
    CRYSTALLIZATION = auto() # Freezes dimensional state

class DimensionalAffinity(Enum):
    """Relationships between dimensions"""
    HARMONIOUS = auto()  # Dimensions work well together
    NEUTRAL = auto()     # No special interaction
    CONFLICTING = auto() # Dimensions interfere with each other
    CATALYZING = auto()  # Dimensions amplify each other
    NULLIFYING = auto()  # Dimensions cancel each other

@dataclass
class DimensionalState:
    """Represents the state of a dimension in combat"""
    layer: DimensionalLayer
    stability: float = 1.0  # 0.0 to 1.0, affects ability effectiveness
    distortion_level: float = 0.0  # Amount of spatial distortion
    corruption_level: float = 0.0  # Amount of dimensional corruption
    energy_level: float = 1.0  # Available dimensional energy
    active_effects: Set[DimensionalEffect] = field(default_factory=set)
    connected_layers: Set[DimensionalLayer] = field(default_factory=set)
    affinity_modifiers: Dict[DimensionalLayer, DimensionalAffinity] = field(default_factory=dict)

@dataclass
class CombatModifier:
    """Represents a combat stat modifier"""
    value: float
    duration: float  # Duration in seconds
    is_multiplicative: bool = False
    source: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

class DimensionalCombat:
    """Manages dimensional aspects of combat"""
    
    def __init__(self):
        self.dimensional_states: Dict[DimensionalLayer, DimensionalState] = {}
        self.combat_modifiers: Dict[str, List[CombatModifier]] = {
            'damage': [],
            'defense': [],
            'speed': [],
            'critical': [],
            'dimensional_power': []
        }
        self.balance_metrics: Dict[str, float] = {
            'avg_damage_per_second': 0.0,
            'avg_survival_time': 0.0,
            'dimension_usage_distribution': 0.0,
            'effect_uptime': 0.0
        }
        self.initialize_dimensions()
        self._setup_affinity_matrix()

    def _setup_affinity_matrix(self):
        """Setup the affinity relationships between dimensions"""
        affinities = {
            DimensionalLayer.PHYSICAL: {
                DimensionalLayer.ETHEREAL: DimensionalAffinity.NEUTRAL,
                DimensionalLayer.VOID: DimensionalAffinity.CONFLICTING,
                DimensionalLayer.CELESTIAL: DimensionalAffinity.HARMONIOUS,
                DimensionalLayer.PRIMORDIAL: DimensionalAffinity.NULLIFYING
            },
            DimensionalLayer.ETHEREAL: {
                DimensionalLayer.VOID: DimensionalAffinity.CATALYZING,
                DimensionalLayer.CELESTIAL: DimensionalAffinity.HARMONIOUS,
                DimensionalLayer.PRIMORDIAL: DimensionalAffinity.CONFLICTING
            },
            DimensionalLayer.VOID: {
                DimensionalLayer.CELESTIAL: DimensionalAffinity.NULLIFYING,
                DimensionalLayer.PRIMORDIAL: DimensionalAffinity.CATALYZING
            },
            DimensionalLayer.CELESTIAL: {
                DimensionalLayer.PRIMORDIAL: DimensionalAffinity.HARMONIOUS
            }
        }
        
        # Apply affinities to dimensional states
        for source_layer, target_affinities in affinities.items():
            state = self.dimensional_states[source_layer]
            state.affinity_modifiers.update(target_affinities)

    def calculate_dimensional_effect(self, 
                                  source_layer: DimensionalLayer,
                                  target_layer: DimensionalLayer,
                                  base_power: float,
                                  effect_type: Optional[DimensionalEffect] = None) -> Tuple[float, List[DimensionalEffect]]:
        """Calculate how power changes when crossing dimensions"""
        source_state = self.dimensional_states[source_layer]
        target_state = self.dimensional_states[target_layer]
        
        # Base multiplier affected by stability and energy
        multiplier = (source_state.stability * target_state.stability * 
                     source_state.energy_level * (1 - target_state.corruption_level))
        
        # Apply affinity modifiers
        affinity = source_state.affinity_modifiers.get(target_layer, DimensionalAffinity.NEUTRAL)
        affinity_multipliers = {
            DimensionalAffinity.HARMONIOUS: 1.5,
            DimensionalAffinity.NEUTRAL: 1.0,
            DimensionalAffinity.CONFLICTING: 0.7,
            DimensionalAffinity.CATALYZING: 2.0,
            DimensionalAffinity.NULLIFYING: 0.3
        }
        multiplier *= affinity_multipliers[affinity]
        
        # Apply active effects
        triggered_effects = []
        if DimensionalEffect.RESONANCE in source_state.active_effects:
            multiplier *= 1.5
            triggered_effects.append(DimensionalEffect.RESONANCE)
        if DimensionalEffect.DISSONANCE in target_state.active_effects:
            multiplier *= 0.7
            triggered_effects.append(DimensionalEffect.DISSONANCE)
        
        # Special effect interactions
        if effect_type:
            if effect_type == DimensionalEffect.CONVERGENCE:
                multiplier *= 1.0 + len(source_state.active_effects) * 0.1
            elif effect_type == DimensionalEffect.DIVERGENCE:
                multiplier *= 1.0 + len(target_state.active_effects) * 0.1
            triggered_effects.append(effect_type)
        
        # Apply combat modifiers
        multiplier *= self._get_total_modifier('dimensional_power')
        
        return base_power * multiplier, triggered_effects

    def apply_dimensional_distortion(self, 
                                  position: Position,
                                  layer: DimensionalLayer,
                                  intensity: float = 1.0) -> Position:
        """Apply dimensional distortion to a position"""
        state = self.dimensional_states[layer]
        if state.distortion_level == 0:
            return position
            
        # Calculate distortion parameters
        base_distortion = state.distortion_level * intensity
        corruption_factor = 1.0 + state.corruption_level
        energy_factor = state.energy_level
        
        # Apply non-linear spatial distortion with corruption influence
        theta = math.atan2(position.y, position.x)
        r = math.sqrt(position.x**2 + position.y**2)
        
        # Complex distortion patterns
        new_theta = theta + base_distortion * r / (10 * energy_factor)
        new_r = r * (1 + math.sin(theta * corruption_factor) * base_distortion / 5)
        
        # Apply vertical distortion based on corruption
        z_distortion = position.z * (1 + base_distortion/10)
        if state.corruption_level > 0:
            z_distortion += math.sin(r * state.corruption_level) * base_distortion
        
        return Position(
            x=new_r * math.cos(new_theta),
            y=new_r * math.sin(new_theta),
            z=z_distortion,
            dimensional_layer=position.dimensional_layer
        )

    def update_dimensional_stability(self, 
                                  layer: DimensionalLayer, 
                                  delta: float,
                                  update_type: str = 'normal'):
        """Update the stability of a dimensional layer"""
        state = self.dimensional_states[layer]
        
        # Apply different update rules based on type
        if update_type == 'corruption':
            # Corruption accelerates instability
            delta *= (1 + state.corruption_level * 2)
        elif update_type == 'purification':
            # Purification helps stability
            delta = abs(delta) * (1 + state.energy_level)
        elif update_type == 'crystallization':
            # Crystallization resists change
            delta *= 0.5
            
        # Update stability with bounds
        state.stability = max(0.0, min(1.0, state.stability + delta))
        
        # Update connected dimensions based on affinity
        for connected_layer in state.connected_layers:
            affinity = state.affinity_modifiers.get(connected_layer, DimensionalAffinity.NEUTRAL)
            connected_state = self.dimensional_states[connected_layer]
            
            # Affinity affects stability propagation
            propagation_factors = {
                DimensionalAffinity.HARMONIOUS: 0.4,
                DimensionalAffinity.NEUTRAL: 0.3,
                DimensionalAffinity.CONFLICTING: 0.2,
                DimensionalAffinity.CATALYZING: 0.5,
                DimensionalAffinity.NULLIFYING: 0.1
            }
            
            connected_delta = delta * propagation_factors[affinity]
            connected_state.stability = max(0.0, min(1.0, 
                connected_state.stability + connected_delta))

    def add_combat_modifier(self,
                          modifier_type: str,
                          value: float,
                          duration: float,
                          is_multiplicative: bool = False,
                          source: str = "") -> None:
        """Add a combat modifier"""
        if modifier_type in self.combat_modifiers:
            self.combat_modifiers[modifier_type].append(
                CombatModifier(
                    value=value,
                    duration=duration,
                    is_multiplicative=is_multiplicative,
                    source=source
                )
            )

    def _get_total_modifier(self, modifier_type: str) -> float:
        """Calculate total value for a modifier type"""
        if modifier_type not in self.combat_modifiers:
            return 1.0
            
        current_time = datetime.now()
        active_modifiers = [
            mod for mod in self.combat_modifiers[modifier_type]
            if (current_time - mod.timestamp).total_seconds() < mod.duration
        ]
        
        # Clean up expired modifiers
        self.combat_modifiers[modifier_type] = active_modifiers
        
        # Calculate total
        additive_total = sum(mod.value for mod in active_modifiers if not mod.is_multiplicative)
        multiplicative_total = math.prod(1 + mod.value for mod in active_modifiers if mod.is_multiplicative)
        
        return (1 + additive_total) * multiplicative_total

    def update_balance_metrics(self, combat_data: Dict[str, Any]) -> None:
        """Update combat balance metrics"""
        # Update damage metrics
        if 'damage_dealt' in combat_data:
            alpha = 0.1  # Smoothing factor
            self.balance_metrics['avg_damage_per_second'] = (
                (1 - alpha) * self.balance_metrics['avg_damage_per_second'] +
                alpha * combat_data['damage_dealt']
            )
            
        # Update survival metrics
        if 'survival_time' in combat_data:
            self.balance_metrics['avg_survival_time'] = (
                (1 - alpha) * self.balance_metrics['avg_survival_time'] +
                alpha * combat_data['survival_time']
            )
            
        # Update dimension usage
        if 'dimension_usage' in combat_data:
            total_usage = sum(combat_data['dimension_usage'].values())
            if total_usage > 0:
                usage_distribution = [
                    count/total_usage for count in combat_data['dimension_usage'].values()
                ]
                entropy = -sum(p * math.log2(p) for p in usage_distribution if p > 0)
                max_entropy = math.log2(len(DimensionalLayer))
                self.balance_metrics['dimension_usage_distribution'] = entropy / max_entropy
                
        # Update effect metrics
        if 'effect_duration' in combat_data and 'total_duration' in combat_data:
            self.balance_metrics['effect_uptime'] = (
                combat_data['effect_duration'] / combat_data['total_duration']
            )

    def get_balance_recommendations(self) -> List[str]:
        """Get balance recommendations based on metrics"""
        recommendations = []
        
        # Check damage balance
        if self.balance_metrics['avg_damage_per_second'] > 100:
            recommendations.append("Consider reducing base damage values")
        elif self.balance_metrics['avg_damage_per_second'] < 20:
            recommendations.append("Consider increasing base damage values")
            
        # Check survival balance
        if self.balance_metrics['avg_survival_time'] < 30:
            recommendations.append("Consider reducing enemy damage or increasing defense options")
        elif self.balance_metrics['avg_survival_time'] > 180:
            recommendations.append("Consider increasing combat challenge")
            
        # Check dimension usage
        if self.balance_metrics['dimension_usage_distribution'] < 0.7:
            recommendations.append("Some dimensions are underutilized, consider rebalancing dimensional benefits")
            
        # Check effect balance
        if self.balance_metrics['effect_uptime'] > 0.8:
            recommendations.append("Effects might be too prevalent, consider increasing cooldowns")
        elif self.balance_metrics['effect_uptime'] < 0.3:
            recommendations.append("Effects might be too rare, consider reducing cooldowns")
            
        return recommendations 