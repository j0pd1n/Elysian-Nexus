"""
Dimensional Combat Inspector Tool

This tool provides real-time inspection and debugging of the dimensional combat system.
"""

import json
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DimensionState:
    name: str
    stability: float
    energy_cost: float
    current_effects: Dict[str, float]
    active_time: float
    transition_count: int

class DimensionalInspector:
    def __init__(self, config_path: str = "config/features/dimensional_combat.json"):
        self.config_path = Path(config_path)
        self.dimension_states: Dict[str, DimensionState] = {}
        self.active_dimension: Optional[str] = None
        self.load_config()
        
    def load_config(self) -> None:
        """Load dimensional combat configuration."""
        with open(self.config_path) as f:
            self.config = json.load(f)
            
    def start_monitoring(self, game_state: Any) -> None:
        """Begin monitoring dimensional combat state."""
        self.game_state = game_state
        self._initialize_states()
        
    def _initialize_states(self) -> None:
        """Initialize dimension states from current game state."""
        for dim_name, dim_config in self.config["dimensions"].items():
            self.dimension_states[dim_name] = DimensionState(
                name=dim_name,
                stability=dim_config["stability"],
                energy_cost=dim_config["energy_cost"],
                current_effects={},
                active_time=0.0,
                transition_count=0
            )
            
    def update(self, delta_time: float) -> None:
        """Update dimension states based on current game state."""
        if self.active_dimension:
            state = self.dimension_states[self.active_dimension]
            state.active_time += delta_time
            
            # Update effects
            current_effects = self._get_current_effects()
            state.current_effects.update(current_effects)
            
    def _get_current_effects(self) -> Dict[str, float]:
        """Get current dimensional effects from game state."""
        if not self.active_dimension:
            return {}
            
        dim_config = self.config["dimensions"][self.active_dimension]
        return {
            "damage_mult": dim_config["effects"]["damage_multiplier"],
            "defense_mult": dim_config["effects"]["defense_multiplier"],
            "healing_mult": dim_config["effects"]["healing_multiplier"]
        }
        
    def on_dimension_shift(self, from_dim: str, to_dim: str) -> None:
        """Handle dimension transition events."""
        if from_dim in self.dimension_states:
            self.dimension_states[from_dim].transition_count += 1
        self.active_dimension = to_dim
        
    def get_stability_report(self) -> Dict[str, Any]:
        """Generate stability report for all dimensions."""
        return {
            dim_name: {
                "stability": state.stability,
                "active_time": state.active_time,
                "transition_count": state.transition_count,
                "current_effects": state.current_effects
            }
            for dim_name, state in self.dimension_states.items()
        }
        
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for dimensional system."""
        return {
            "total_transitions": sum(
                state.transition_count for state in self.dimension_states.values()
            ),
            "dimension_usage": {
                dim_name: state.active_time
                for dim_name, state in self.dimension_states.items()
            },
            "current_stability": (
                self.dimension_states[self.active_dimension].stability
                if self.active_dimension else 1.0
            )
        }
        
    def log_state(self, log_path: Optional[str] = None) -> None:
        """Log current dimensional state to file."""
        if not log_path:
            log_path = f"logs/debug/dimension_state_{int(time.time())}.json"
            
        state_data = {
            "timestamp": time.time(),
            "active_dimension": self.active_dimension,
            "stability_report": self.get_stability_report(),
            "performance_metrics": self.get_performance_metrics()
        }
        
        with open(log_path, 'w') as f:
            json.dump(state_data, f, indent=2)
            
def main():
    """Main function for running the inspector independently."""
    inspector = DimensionalInspector()
    
    # Example usage
    inspector.start_monitoring(None)  # Replace with actual game state
    
    # Simulate some dimension shifts
    inspector.on_dimension_shift("physical", "ethereal")
    time.sleep(1)
    inspector.update(1.0)
    
    inspector.on_dimension_shift("ethereal", "void")
    time.sleep(1)
    inspector.update(1.0)
    
    # Generate and save reports
    inspector.log_state()
    
if __name__ == "__main__":
    main() 