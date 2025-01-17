from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import time

from .save_manager import SaveManager, SaveMetadata
from ..game_state.game_state_manager import GameStateManager
from ..game_state.enums import GameState, Location

class SaveSystem:
    def __init__(self, game_state_manager: GameStateManager):
        self.game_state_manager = game_state_manager
        self.save_manager = SaveManager()
        self.auto_save_slot = 0  # Reserved slot for auto-saves
        
    def save_game(self, slot: int, is_auto_save: bool = False) -> bool:
        """Save the current game state to a slot."""
        try:
            # Get current game state
            game_data = {
                "difficulty": self.game_state_manager.difficulty.name,
                "location": self.game_state_manager.current_location.name if self.game_state_manager.current_location else None,
                "game_state": self.game_state_manager.current_state.name,
                "game_mode": self.game_state_manager.current_mode.name,
                "quest_status": {k: v.name for k, v in self.game_state_manager.quest_status.items()},
                "player_data": self.game_state_manager.player_data,
                "world_state": self.game_state_manager.world_state,
                "environmental_conditions": {
                    "weather_type": self.game_state_manager.environmental_conditions.weather_type,
                    "time_of_day": self.game_state_manager.environmental_conditions.time_of_day,
                    "visibility": self.game_state_manager.environmental_conditions.visibility,
                    "temperature": self.game_state_manager.environmental_conditions.temperature,
                    "wind_speed": self.game_state_manager.environmental_conditions.wind_speed,
                    "is_hazardous": self.game_state_manager.environmental_conditions.is_hazardous,
                    "active_effects": list(self.game_state_manager.environmental_conditions.active_effects),
                    "terrain_type": self.game_state_manager.environmental_conditions.terrain_type,
                    "light_level": self.game_state_manager.environmental_conditions.light_level
                },
                "faction_standings": self.game_state_manager.faction_standings,
                "active_faction_effects": list(self.game_state_manager.active_faction_effects),
                "difficulty_modifiers": self.game_state_manager.difficulty_modifiers.__dict__
            }
            
            # Get player info for metadata
            player_name = self.game_state_manager.player_data.get("name", "Unknown")
            player_level = self.game_state_manager.player_data.get("level", 1)
            location = self.game_state_manager.current_location.value if self.game_state_manager.current_location else "Unknown"
            playtime = self.game_state_manager.player_data.get("playtime", 0.0)
            
            # Save the game
            success = self.save_manager.save_game(
                slot=slot,
                data=game_data,
                player_name=player_name,
                player_level=player_level,
                location=location,
                playtime=playtime
            )
            
            if success and not is_auto_save:
                # Update last save location for manual saves
                self.game_state_manager.last_save_location = self.game_state_manager.current_location
            
            return success
            
        except Exception as e:
            print(f"Error in save_game: {e}")
            return False
    
    def load_game(self, slot: int) -> bool:
        """Load a game state from a slot."""
        try:
            # Load the game data
            game_data, metadata = self.save_manager.load_game(slot)
            
            if not game_data or not metadata:
                return False
            
            # Update game state
            self.game_state_manager.difficulty = GameState[game_data["difficulty"]]
            self.game_state_manager.current_location = Location[game_data["location"]] if game_data["location"] else None
            self.game_state_manager.current_state = GameState[game_data["game_state"]]
            self.game_state_manager.current_mode = GameState[game_data["game_mode"]]
            self.game_state_manager.quest_status = {k: GameState[v] for k, v in game_data["quest_status"].items()}
            self.game_state_manager.player_data = game_data["player_data"]
            self.game_state_manager.world_state = game_data["world_state"]
            
            # Update environmental conditions
            env_data = game_data["environmental_conditions"]
            self.game_state_manager.environmental_conditions.weather_type = env_data["weather_type"]
            self.game_state_manager.environmental_conditions.time_of_day = env_data["time_of_day"]
            self.game_state_manager.environmental_conditions.visibility = env_data["visibility"]
            self.game_state_manager.environmental_conditions.temperature = env_data["temperature"]
            self.game_state_manager.environmental_conditions.wind_speed = env_data["wind_speed"]
            self.game_state_manager.environmental_conditions.is_hazardous = env_data["is_hazardous"]
            self.game_state_manager.environmental_conditions.active_effects = set(env_data["active_effects"])
            self.game_state_manager.environmental_conditions.terrain_type = env_data["terrain_type"]
            self.game_state_manager.environmental_conditions.light_level = env_data["light_level"]
            
            # Update faction data
            self.game_state_manager.faction_standings = game_data["faction_standings"]
            self.game_state_manager.active_faction_effects = set(game_data["active_faction_effects"])
            
            # Update difficulty modifiers
            for key, value in game_data["difficulty_modifiers"].items():
                setattr(self.game_state_manager.difficulty_modifiers, key, value)
            
            # Update last save location
            self.game_state_manager.last_save_location = self.game_state_manager.current_location
            
            return True
            
        except Exception as e:
            print(f"Error in load_game: {e}")
            return False
    
    def get_save_slots(self) -> List[Tuple[int, SaveMetadata]]:
        """Get a list of all save slots and their metadata."""
        return self.save_manager.get_save_slots()
    
    def delete_save(self, slot: int) -> bool:
        """Delete a save slot."""
        return self.save_manager.delete_save(slot)
    
    def check_auto_save(self) -> bool:
        """Check if auto-save should be triggered."""
        if not self.save_manager.check_auto_save():
            return False
            
        # Don't auto-save during combat or dangerous situations
        if (self.game_state_manager.current_state == GameState.BATTLE or
            self.game_state_manager.world_state.get("in_danger", False) or
            self.game_state_manager.world_state.get("in_combat", False)):
            return False
            
        return True
    
    def perform_auto_save(self) -> bool:
        """Perform an auto-save if conditions are met."""
        if self.check_auto_save():
            success = self.save_game(self.auto_save_slot, is_auto_save=True)
            if success:
                self.save_manager.update_auto_save_time()
            return success
        return False 