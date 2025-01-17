from game_state import GameState, GameStateManager
from typing import Optional
import json
import os

class GameSystem:
    def __init__(self):
        self.state_manager = GameStateManager()
        self.player_name: Optional[str] = None
        
    def start_new_game(self) -> str:
        """Start a new game"""
        self.state_manager.change_state(GameState.NEW_GAME)
        return "🌟 Initializing new journey through the cosmos..."
        
    def continue_game(self) -> str:
        """Load the most recent save game"""
        save_files = self._get_save_files()
        if not save_files:
            return "❌ No saved journeys found."
            
        latest_save = max(save_files)
        try:
            with open(os.path.join("saves", latest_save), 'r') as f:
                data = json.load(f)
                self.player_name = data.get("name", "Unknown Traveler")
                self.state_manager.change_state(GameState.PLAYING)
                return f"✨ Welcome back, {self.player_name}!"
        except Exception as e:
            return f"❌ Error loading save: {str(e)}"
            
    def show_star_charts(self) -> str:
        """Display game statistics and achievements"""
        if not self.player_name:
            return "📊 Cosmic Statistics:\n- No active journeys found\n- Start a new journey to begin recording your legacy!"
            
        return f"""📊 Cosmic Statistics for {self.player_name}:
- Current Location: The Void
- Achievements: 0/100
- Discoveries: 0/50
- Quests Completed: 0/25
- Time in Space: 0 hours"""
        
    def show_settings(self) -> str:
        """Show game settings"""
        self.state_manager.change_state(GameState.SETTINGS)
        settings = self.state_manager.settings
        
        display_settings = settings["display"]
        audio_settings = settings["audio"]
        control_settings = settings["controls"]
        gameplay_settings = settings["gameplay"]
        
        return f"""⚙️ Nebula Settings:

1. Display
   - Resolution: {display_settings["resolution"]}
   - Fullscreen: {"Yes" if display_settings["fullscreen"] else "No"}
   - VSync: {"On" if display_settings["vsync"] else "Off"}
   
2. Audio
   - Music Volume: {int(audio_settings["music_volume"] * 100)}%
   - Effects Volume: {int(audio_settings["effects_volume"] * 100)}%
   - Ambient Volume: {int(audio_settings["ambient_volume"] * 100)}%
   - Voice Volume: {int(audio_settings["voice_volume"] * 100)}%
   
3. Controls
   - Movement: {control_settings["movement"]}
   - Interact: {control_settings["interact"]}
   - Menu: {control_settings["menu"]}
   - Combat: {control_settings["combat"]}
   
4. Gameplay
   - Difficulty: {gameplay_settings["difficulty"]}
   - Tutorial Tips: {"On" if gameplay_settings["tutorial_tips"] else "Off"}
   - Auto-Save: Every {gameplay_settings["auto_save"] // 60} minutes"""
        
    def exit_game(self) -> str:
        """Handle game exit"""
        if self.player_name:
            self._save_game()
            return f"👋 Journey saved, {self.player_name}. May the stars guide your return..."
        return "👋 Thank you for visiting Elysian Nexus. Until we meet again..."
        
    def _save_game(self) -> bool:
        """Save current game state"""
        if not self.player_name:
            return False
            
        try:
            save_data = {
                "name": self.player_name,
                "state": self.state_manager.current_state.value,
                "settings": self.state_manager.settings
            }
            
            os.makedirs("saves", exist_ok=True)
            filename = f"save_{self.player_name.lower()}.json"
            with open(os.path.join("saves", filename), 'w') as f:
                json.dump(save_data, f, indent=2)
            return True
        except Exception:
            return False
            
    def _get_save_files(self) -> list:
        """Get list of save files"""
        if not os.path.exists("saves"):
            return []
        return [f for f in os.listdir("saves") if f.endswith('.json')] 