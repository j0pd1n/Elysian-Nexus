from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Callable
from enum import Enum, auto
from .dimensional_combat import DimensionalLayer, DimensionalEffect, Position, DimensionalCombat
from .abilities import Ability, AbilityType

class DimensionalAbilityType(Enum):
    """Types of dimensional abilities"""
    SHIFT = auto()         # Move between dimensions
    MANIPULATION = auto()  # Manipulate dimensional properties
    RESONANCE = auto()     # Harness dimensional energies
    DISRUPTION = auto()    # Disrupt dimensional stability
    FUSION = auto()        # Combine dimensional effects

@dataclass
class DimensionalAbility(Ability):
    """Represents an ability that interacts with dimensions"""
    dimensional_type: DimensionalAbilityType
    source_dimension: DimensionalLayer
    target_dimensions: Set[DimensionalLayer]
    dimensional_effects: Set[DimensionalEffect]
    stability_cost: float
    dimension_requirements: Dict[DimensionalLayer, float]  # Required stability levels
    cooldown_per_dimension: Dict[DimensionalLayer, float]

class DimensionalAbilityManager:
    """Manages dimensional abilities and their effects"""
    
    def __init__(self, combat_system: DimensionalCombat):
        self.combat_system = combat_system
        self.abilities: Dict[str, DimensionalAbility] = {}
        self.cooldowns: Dict[str, Dict[DimensionalLayer, float]] = {}
        self.initialize_abilities()
        
    def initialize_abilities(self):
        """Initialize the base set of dimensional abilities"""
        # Dimensional Shift
        self.register_ability(DimensionalAbility(
            name="Dimensional Shift",
            description="Phase between connected dimensions",
            ability_type=AbilityType.UTILITY,
            dimensional_type=DimensionalAbilityType.SHIFT,
            mana_cost=25,
            cooldown=4,
            base_value=0,
            scaling_stat="intelligence",
            scaling_factor=1.0,
            source_dimension=DimensionalLayer.PHYSICAL,
            target_dimensions={DimensionalLayer.ETHEREAL},
            dimensional_effects={DimensionalEffect.PHASING},
            stability_cost=0.05,
            dimension_requirements={
                DimensionalLayer.PHYSICAL: 0.25,
                DimensionalLayer.ETHEREAL: 0.25
            },
            cooldown_per_dimension={
                DimensionalLayer.PHYSICAL: 4,
                DimensionalLayer.ETHEREAL: 4
            }
        ))
        
        # Void Strike
        self.register_ability(DimensionalAbility(
            name="Void Strike",
            description="Channel void energy for a powerful attack",
            ability_type=AbilityType.ATTACK,
            dimensional_type=DimensionalAbilityType.DISRUPTION,
            mana_cost=50,
            cooldown=8,
            base_value=90,
            scaling_stat="intelligence",
            scaling_factor=1.5,
            source_dimension=DimensionalLayer.VOID,
            target_dimensions={DimensionalLayer.PHYSICAL, DimensionalLayer.ETHEREAL},
            dimensional_effects={DimensionalEffect.DISSONANCE},
            stability_cost=0.25,
            dimension_requirements={
                DimensionalLayer.VOID: 0.4
            },
            cooldown_per_dimension={
                DimensionalLayer.VOID: 8
            }
        ))
        
        # Celestial Resonance
        self.register_ability(DimensionalAbility(
            name="Celestial Resonance",
            description="Harmonize with celestial energies",
            ability_type=AbilityType.BUFF,
            dimensional_type=DimensionalAbilityType.RESONANCE,
            mana_cost=55,
            cooldown=12,
            base_value=40,
            scaling_stat="wisdom",
            scaling_factor=1.2,
            source_dimension=DimensionalLayer.CELESTIAL,
            target_dimensions={DimensionalLayer.CELESTIAL, DimensionalLayer.ETHEREAL},
            dimensional_effects={DimensionalEffect.RESONANCE},
            stability_cost=0.12,
            dimension_requirements={
                DimensionalLayer.CELESTIAL: 0.35
            },
            cooldown_per_dimension={
                DimensionalLayer.CELESTIAL: 12
            }
        ))
        
        # Primordial Fusion
        self.register_ability(DimensionalAbility(
            name="Primordial Fusion",
            description="Combine dimensional energies for devastating effect",
            ability_type=AbilityType.ATTACK,
            dimensional_type=DimensionalAbilityType.FUSION,
            mana_cost=120,
            cooldown=20,
            base_value=150,
            scaling_stat="intelligence",
            scaling_factor=2.0,
            source_dimension=DimensionalLayer.PRIMORDIAL,
            target_dimensions={
                DimensionalLayer.VOID,
                DimensionalLayer.CELESTIAL
            },
            dimensional_effects={
                DimensionalEffect.RESONANCE,
                DimensionalEffect.WARPING
            },
            stability_cost=0.35,
            dimension_requirements={
                DimensionalLayer.PRIMORDIAL: 0.5,
                DimensionalLayer.VOID: 0.35,
                DimensionalLayer.CELESTIAL: 0.35
            },
            cooldown_per_dimension={
                DimensionalLayer.PRIMORDIAL: 20,
                DimensionalLayer.VOID: 10,
                DimensionalLayer.CELESTIAL: 10
            }
        ))
        
    def register_ability(self, ability: DimensionalAbility):
        """Register a new dimensional ability"""
        self.abilities[ability.name] = ability
        self.cooldowns[ability.name] = {
            dim: 0.0 for dim in ability.cooldown_per_dimension.keys()
        }
        
    def can_use_ability(self, 
                      ability_name: str,
                      current_dimension: DimensionalLayer) -> tuple[bool, str]:
        """Check if an ability can be used"""
        if ability_name not in self.abilities:
            return False, "Ability not found"
            
        ability = self.abilities[ability_name]
        
        # Check current dimension
        if current_dimension != ability.source_dimension:
            return False, f"Must be in {ability.source_dimension.name} dimension"
            
        # Check stability requirements
        for dim, required_stability in ability.dimension_requirements.items():
            current_stability = self.combat_system.dimensional_states[dim].stability
            if current_stability < required_stability:
                return False, f"Insufficient stability in {dim.name} dimension"
                
        # Check cooldowns
        for dim, cooldown in self.cooldowns[ability_name].items():
            if cooldown > 0:
                return False, f"Ability on cooldown in {dim.name} dimension"
                
        return True, "Ability ready"
        
    def use_ability(self,
                   ability_name: str,
                   user_position: Position,
                   target_position: Optional[Position] = None) -> tuple[bool, str, float]:
        """Use a dimensional ability"""
        can_use, reason = self.can_use_ability(
            ability_name,
            user_position.dimensional_layer
        )
        
        if not can_use:
            return False, reason, 0.0
            
        ability = self.abilities[ability_name]
        
        # Apply stability costs
        for dim in ability.target_dimensions:
            self.combat_system.update_dimensional_stability(
                dim,
                -ability.stability_cost
            )
            
        # Apply cooldowns
        for dim, cooldown in ability.cooldown_per_dimension.items():
            self.cooldowns[ability_name][dim] = cooldown
            
        # Calculate ability power
        base_power = ability.base_value
        
        # Apply dimensional effects
        for effect in ability.dimensional_effects:
            self.combat_system.add_dimensional_effect(
                user_position.dimensional_layer,
                effect
            )
            
        # Calculate cross-dimensional power modification
        if target_position and target_position.dimensional_layer in ability.target_dimensions:
            power = self.combat_system.calculate_dimensional_effect(
                user_position.dimensional_layer,
                target_position.dimensional_layer,
                base_power
            )
        else:
            power = base_power
            
        return True, "Ability used successfully", power
        
    def update_cooldowns(self, delta_time: float):
        """Update ability cooldowns"""
        for ability_name in self.abilities:
            for dimension in self.cooldowns[ability_name]:
                self.cooldowns[ability_name][dimension] = max(
                    0.0,
                    self.cooldowns[ability_name][dimension] - delta_time
                )
                
    def get_available_abilities(self, 
                             current_dimension: DimensionalLayer) -> List[DimensionalAbility]:
        """Get list of abilities available in current dimension"""
        return [
            ability for ability in self.abilities.values()
            if ability.source_dimension == current_dimension
        ]
        
    def get_ability_status(self, ability_name: str) -> Dict[str, any]:
        """Get detailed status of an ability"""
        if ability_name not in self.abilities:
            return {}
            
        ability = self.abilities[ability_name]
        return {
            'name': ability.name,
            'type': ability.dimensional_type.name,
            'cooldowns': self.cooldowns[ability_name],
            'stability_requirements': ability.dimension_requirements,
            'effects': [effect.name for effect in ability.dimensional_effects],
            'target_dimensions': [dim.name for dim in ability.target_dimensions]
        }
        
    def get_dimension_compatibility(self,
                                 source_dim: DimensionalLayer,
                                 target_dim: DimensionalLayer) -> float:
        """Calculate compatibility between dimensions for ability use"""
        if source_dim == target_dim:
            return 1.0
            
        # Check if dimensions are connected
        if not self.combat_system.can_traverse_dimensions(source_dim, target_dim):
            return 0.0
            
        # Calculate based on stability
        source_stability = self.combat_system.dimensional_states[source_dim].stability
        target_stability = self.combat_system.dimensional_states[target_dim].stability
        
        return min(source_stability, target_stability) 