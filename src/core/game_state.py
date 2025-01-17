from enum import Enum
from typing import Dict, Any, Optional
import json
import os
from datetime import datetime

class GameState(Enum):
    TITLE = "title"
    NEW_GAME = "new_game"
    PLAYING = "playing"
    PAUSED = "paused"
    SETTINGS = "settings"
    TUTORIAL = "tutorial"

class GameStateManager:
    def __init__(self):
        self.current_state = GameState.TITLE
        self.settings: Dict[str, Any] = {
            "display": {
                "resolution": "800x600",
                "fullscreen": False,
                "vsync": True
            },
            "audio": {
                "music_volume": 0.7,
                "effects_volume": 1.0,
                "ambient_volume": 0.5,
                "voice_volume": 0.8
            },
            "controls": {
                "movement": "WASD",
                "interact": "E",
                "menu": "ESC",
                "combat": "SPACE"
            },
            "gameplay": {
                "difficulty": "Normal",
                "tutorial_tips": True,
                "auto_save": 300  # seconds
            }
        }
        self.last_save = None
        self.last_auto_save = datetime.now()
        
    def change_state(self, new_state: GameState):
        """Change the current game state"""
        self.current_state = new_state
        
    def get_setting(self, category: str, setting: str) -> Any:
        """Get a specific setting value"""
        return self.settings.get(category, {}).get(setting)
        
    def update_setting(self, category: str, setting: str, value: Any):
        """Update a specific setting"""
        if category in self.settings and setting in self.settings[category]:
            self.settings[category][setting] = value
            return True
        return False
        
    def save_settings(self) -> bool:
        """Save current settings to file"""
        try:
            os.makedirs("config", exist_ok=True)
            with open("config/settings.json", "w") as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception:
            return False
            
    def load_settings(self) -> bool:
        """Load settings from file"""
        try:
            if os.path.exists("config/settings.json"):
                with open("config/settings.json", "r") as f:
                    self.settings = json.load(f)
                return True
        except Exception:
            pass
        return False 