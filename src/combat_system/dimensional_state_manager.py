from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Set
import json
import os
from datetime import datetime
from .dimensional_combat import DimensionalLayer, DimensionalEffect, DimensionalState, DimensionalCombat

@dataclass
class DimensionalStateSnapshot:
    """Represents a saveable snapshot of dimensional states"""
    timestamp: str
    version: str = "1.0.0"
    states: Dict[str, Dict] = None
    active_effects: Dict[str, List[str]] = None
    stability_history: Dict[str, List[float]] = None

class DimensionalStateManager:
    """Manages saving and loading of dimensional states"""
    
    def __init__(self, combat_system: DimensionalCombat, save_dir: str = "saves/dimensional"):
        self.combat_system = combat_system
        self.save_dir = save_dir
        self.current_version = "1.0.0"
        self._ensure_save_directory()
        self.stability_history: Dict[DimensionalLayer, List[float]] = {
            layer: [] for layer in DimensionalLayer
        }

    def _ensure_save_directory(self):
        """Create save directory if it doesn't exist"""
        os.makedirs(self.save_dir, exist_ok=True)

    def save_state(self, save_name: str = None) -> str:
        """Save current dimensional state to file"""
        if save_name is None:
            save_name = f"dimensional_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create state snapshot
        snapshot = DimensionalStateSnapshot(
            timestamp=datetime.now().isoformat(),
            version=self.current_version,
            states={
                layer.name: {
                    'stability': state.stability,
                    'distortion_level': state.distortion_level,
                    'connected_layers': [l.name for l in state.connected_layers]
                }
                for layer, state in self.combat_system.dimensional_states.items()
            },
            active_effects={
                layer.name: [effect.name for effect in state.active_effects]
                for layer, state in self.combat_system.dimensional_states.items()
            },
            stability_history={
                layer.name: self.stability_history[layer]
                for layer in DimensionalLayer
            }
        )

        # Save to file
        save_path = os.path.join(self.save_dir, f"{save_name}.json")
        with open(save_path, 'w') as f:
            json.dump(asdict(snapshot), f, indent=2)

        return save_path

    def load_state(self, save_name: str) -> bool:
        """Load dimensional state from file"""
        save_path = os.path.join(self.save_dir, f"{save_name}.json")
        if not os.path.exists(save_path):
            return False

        try:
            with open(save_path, 'r') as f:
                data = json.load(f)
                snapshot = DimensionalStateSnapshot(**data)

            # Version compatibility check
            if snapshot.version != self.current_version:
                self._migrate_version(snapshot)

            # Restore states
            for layer_name, state_data in snapshot.states.items():
                layer = DimensionalLayer[layer_name]
                state = self.combat_system.dimensional_states[layer]
                state.stability = state_data['stability']
                state.distortion_level = state_data['distortion_level']
                state.connected_layers = {
                    DimensionalLayer[name] for name in state_data['connected_layers']
                }

            # Restore effects
            for layer_name, effect_names in snapshot.active_effects.items():
                layer = DimensionalLayer[layer_name]
                state = self.combat_system.dimensional_states[layer]
                state.active_effects = {
                    DimensionalEffect[name] for name in effect_names
                }

            # Restore history
            self.stability_history = {
                DimensionalLayer[layer]: history
                for layer, history in snapshot.stability_history.items()
            }

            return True
        except Exception as e:
            print(f"Error loading dimensional state: {e}")
            return False

    def _migrate_version(self, snapshot: DimensionalStateSnapshot):
        """Migrate save data from older versions"""
        if snapshot.version == "1.0.0":
            return  # Current version, no migration needed
            
        # Add version migrations here as needed
        raise ValueError(f"Unsupported save version: {snapshot.version}")

    def get_save_list(self) -> List[Dict[str, str]]:
        """Get list of available save files"""
        saves = []
        for filename in os.listdir(self.save_dir):
            if filename.endswith('.json'):
                path = os.path.join(self.save_dir, filename)
                try:
                    with open(path, 'r') as f:
                        data = json.load(f)
                        saves.append({
                            'name': filename[:-5],  # Remove .json
                            'timestamp': data['timestamp'],
                            'version': data.get('version', 'unknown')
                        })
                except Exception:
                    continue
        return sorted(saves, key=lambda x: x['timestamp'], reverse=True)

    def record_stability(self, layer: DimensionalLayer, stability: float):
        """Record stability value for historical tracking"""
        self.stability_history[layer].append(stability)
        # Keep only last 100 values
        if len(self.stability_history[layer]) > 100:
            self.stability_history[layer].pop(0)

    def get_stability_trend(self, layer: DimensionalLayer) -> Dict[str, float]:
        """Get stability trend analysis for a dimension"""
        history = self.stability_history[layer]
        if not history:
            return {'trend': 0.0, 'volatility': 0.0}

        # Calculate trend
        trend = history[-1] - history[0] if len(history) > 1 else 0
        
        # Calculate volatility
        differences = [abs(b - a) for a, b in zip(history[:-1], history[1:])]
        volatility = sum(differences) / len(differences) if differences else 0

        return {
            'trend': trend,
            'volatility': volatility,
            'current': history[-1] if history else 0,
            'average': sum(history) / len(history)
        }

    def auto_save(self) -> Optional[str]:
        """Automatically save state with timestamp"""
        try:
            return self.save_state(f"autosave_dimensional")
        except Exception as e:
            print(f"Auto-save failed: {e}")
            return None

    def create_backup(self) -> Optional[str]:
        """Create a backup of current state"""
        try:
            return self.save_state(f"backup_dimensional_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        except Exception as e:
            print(f"Backup creation failed: {e}")
            return None

    def cleanup_old_saves(self, max_saves: int = 10):
        """Remove old save files keeping only the most recent ones"""
        saves = self.get_save_list()
        if len(saves) > max_saves:
            saves_to_remove = saves[max_saves:]
            for save in saves_to_remove:
                try:
                    os.remove(os.path.join(self.save_dir, f"{save['name']}.json"))
                except Exception:
                    continue 