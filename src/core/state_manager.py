from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import time
import json
import copy

class GameStateType(Enum):
    MAIN_MENU = "main_menu"
    EXPLORATION = "exploration"
    COMBAT = "combat"
    DIALOGUE = "dialogue"
    INVENTORY = "inventory"
    QUEST = "quest"
    SHOP = "shop"
    CHARACTER = "character"

@dataclass
class StateSnapshot:
    timestamp: float
    state_type: GameStateType
    state_data: Dict[str, Any]
    
class StateManager:
    def __init__(self):
        self.current_state: GameStateType = GameStateType.MAIN_MENU
        self.state_data: Dict[str, Any] = {}
        self.state_history: List[StateSnapshot] = []
        self.max_history = 50
        self.validation_rules = self._initialize_validation_rules()
        
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize validation rules for different state types"""
        return {
            GameStateType.EXPLORATION: {
                "required_fields": ["location", "player_position", "discovered_areas"],
                "field_types": {
                    "location": str,
                    "player_position": dict,
                    "discovered_areas": list
                }
            },
            GameStateType.COMBAT: {
                "required_fields": ["enemies", "player_stats", "combat_round"],
                "field_types": {
                    "enemies": list,
                    "player_stats": dict,
                    "combat_round": int
                }
            },
            GameStateType.DIALOGUE: {
                "required_fields": ["npc_id", "dialogue_tree", "conversation_history"],
                "field_types": {
                    "npc_id": str,
                    "dialogue_tree": dict,
                    "conversation_history": list
                }
            }
        }

    def transition_state(self, new_state: GameStateType, state_data: Dict[str, Any]) -> bool:
        """Transition to a new game state with validation"""
        try:
            if not self._validate_state_data(new_state, state_data):
                return False
                
            # Create snapshot of current state
            self._create_snapshot()
            
            # Update state
            self.current_state = new_state
            self.state_data = copy.deepcopy(state_data)
            
            # Manage history size
            if len(self.state_history) > self.max_history:
                self.state_history.pop(0)
                
            return True
            
        except Exception as e:
            print(f"Error transitioning state: {e}")
            return False

    def _validate_state_data(self, state_type: GameStateType, state_data: Dict[str, Any]) -> bool:
        """Validate state data against rules"""
        if state_type not in self.validation_rules:
            return True  # No validation rules for this state type
            
        rules = self.validation_rules[state_type]
        
        # Check required fields
        for field in rules["required_fields"]:
            if field not in state_data:
                print(f"Missing required field: {field}")
                return False
                
        # Check field types
        for field, expected_type in rules["field_types"].items():
            if field in state_data and not isinstance(state_data[field], expected_type):
                print(f"Invalid type for field {field}")
                return False
                
        return True

    def _create_snapshot(self):
        """Create a snapshot of the current state"""
        snapshot = StateSnapshot(
            timestamp=time.time(),
            state_type=self.current_state,
            state_data=copy.deepcopy(self.state_data)
        )
        self.state_history.append(snapshot)

    def rollback_state(self, steps: int = 1) -> bool:
        """Rollback to a previous state"""
        try:
            if not self.state_history or steps > len(self.state_history):
                return False
                
            # Get target snapshot
            target_snapshot = self.state_history[-steps]
            
            # Restore state
            self.current_state = target_snapshot.state_type
            self.state_data = copy.deepcopy(target_snapshot.state_data)
            
            # Remove rolled back snapshots
            self.state_history = self.state_history[:-steps]
            
            return True
            
        except Exception as e:
            print(f"Error rolling back state: {e}")
            return False

    def get_current_state(self) -> Dict[str, Any]:
        """Get current state data"""
        return {
            "type": self.current_state.value,
            "data": copy.deepcopy(self.state_data),
            "timestamp": time.time()
        }

    def update_state_data(self, updates: Dict[str, Any]) -> bool:
        """Update specific fields in the current state"""
        try:
            # Create snapshot before update
            self._create_snapshot()
            
            # Apply updates
            for key, value in updates.items():
                self.state_data[key] = copy.deepcopy(value)
                
            return True
            
        except Exception as e:
            print(f"Error updating state: {e}")
            return False

    def get_state_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get state transition history"""
        history = [
            {
                "timestamp": snapshot.timestamp,
                "state_type": snapshot.state_type.value,
                "data": snapshot.state_data
            }
            for snapshot in self.state_history
        ]
        
        if limit:
            history = history[-limit:]
            
        return history

    def clear_history(self):
        """Clear state history"""
        self.state_history.clear()

    def add_validation_rule(self, state_type: GameStateType, rules: Dict[str, Any]):
        """Add new validation rules for a state type"""
        if state_type not in self.validation_rules:
            self.validation_rules[state_type] = rules
        else:
            self.validation_rules[state_type].update(rules)

    def export_state(self, file_path: str) -> bool:
        """Export current state to file"""
        try:
            state_data = {
                "current_state": self.current_state.value,
                "state_data": self.state_data,
                "timestamp": time.time()
            }
            
            with open(file_path, "w") as f:
                json.dump(state_data, f, indent=4)
                
            return True
            
        except Exception as e:
            print(f"Error exporting state: {e}")
            return False

    def import_state(self, file_path: str) -> bool:
        """Import state from file"""
        try:
            with open(file_path, "r") as f:
                state_data = json.load(f)
                
            # Validate imported state
            if "current_state" not in state_data or "state_data" not in state_data:
                print("Invalid state file format")
                return False
                
            # Convert state type string to enum
            try:
                state_type = GameStateType(state_data["current_state"])
            except ValueError:
                print("Invalid state type in file")
                return False
                
            # Validate and apply state
            if self._validate_state_data(state_type, state_data["state_data"]):
                self.current_state = state_type
                self.state_data = state_data["state_data"]
                return True
                
            return False
            
        except Exception as e:
            print(f"Error importing state: {e}")
            return False 