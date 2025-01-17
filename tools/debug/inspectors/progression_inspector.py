"""
Character Progression Inspector Tool

This tool provides real-time inspection and debugging of character progression systems.
"""

import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

@dataclass
class ProgressionSnapshot:
    timestamp: float
    level: int
    experience: float
    stats: Dict[str, float]
    masteries: Dict[str, Dict[str, Any]]
    specializations: Dict[str, List[str]]
    achievements: List[str]

class ProgressionInspector:
    def __init__(self, config_path: str = "config/features/progression_system.json"):
        self.config_path = Path(config_path)
        self.snapshots: List[ProgressionSnapshot] = []
        self.load_config()
        
    def load_config(self) -> None:
        """Load progression system configuration."""
        with open(self.config_path) as f:
            self.config = json.load(f)
            
    def take_snapshot(self, character_state: Any) -> None:
        """Take a snapshot of current character progression state."""
        snapshot = ProgressionSnapshot(
            timestamp=time.time(),
            level=character_state.level,
            experience=character_state.experience,
            stats=self._get_current_stats(character_state),
            masteries=self._get_mastery_progress(character_state),
            specializations=self._get_specialization_state(character_state),
            achievements=self._get_achievements(character_state)
        )
        self.snapshots.append(snapshot)
        
    def _get_current_stats(self, character_state: Any) -> Dict[str, float]:
        """Get current character stats."""
        return {
            stat: getattr(character_state, f"get_{stat.lower()}")()
            for stat in ["Strength", "Agility", "Intelligence", "Vitality", "Willpower"]
        }
        
    def _get_mastery_progress(self, character_state: Any) -> Dict[str, Dict[str, Any]]:
        """Get current mastery progress."""
        return {
            mastery: {
                "level": getattr(character_state, f"get_{mastery.lower()}_level")(),
                "experience": getattr(character_state, f"get_{mastery.lower()}_exp")(),
                "milestones": getattr(character_state, f"get_{mastery.lower()}_milestones")()
            }
            for mastery in ["Combat", "Dimensional", "Crafting", "Exploration"]
        }
        
    def _get_specialization_state(self, character_state: Any) -> Dict[str, List[str]]:
        """Get current specialization unlocks."""
        return {
            spec: character_state.get_unlocked_nodes(spec)
            for spec in ["blade_master", "void_walker", "reality_shaper"]
        }
        
    def _get_achievements(self, character_state: Any) -> List[str]:
        """Get current achievements."""
        return character_state.get_completed_achievements()
        
    def analyze_progression_rate(self, time_window: float = 3600) -> Dict[str, Any]:
        """Analyze progression rate over the specified time window (in seconds)."""
        current_time = time.time()
        relevant_snapshots = [
            s for s in self.snapshots
            if current_time - s.timestamp <= time_window
        ]
        
        if len(relevant_snapshots) < 2:
            return {"error": "Insufficient data for analysis"}
            
        first, last = relevant_snapshots[0], relevant_snapshots[-1]
        time_diff = last.timestamp - first.timestamp
        
        return {
            "time_period": time_diff,
            "level_progression": {
                "levels_gained": last.level - first.level,
                "exp_per_hour": (last.experience - first.experience) * (3600 / time_diff)
            },
            "stat_progression": {
                stat: (last.stats[stat] - first.stats[stat]) * (3600 / time_diff)
                for stat in first.stats
            },
            "mastery_progression": {
                mastery: {
                    "levels_gained": (
                        last.masteries[mastery]["level"] -
                        first.masteries[mastery]["level"]
                    ),
                    "exp_per_hour": (
                        last.masteries[mastery]["experience"] -
                        first.masteries[mastery]["experience"]
                    ) * (3600 / time_diff)
                }
                for mastery in first.masteries
            }
        }
        
    def get_progression_recommendations(self) -> Dict[str, Any]:
        """Generate progression recommendations based on current state."""
        if not self.snapshots:
            return {"error": "No progression data available"}
            
        current = self.snapshots[-1]
        
        recommendations = {
            "stat_focus": self._recommend_stat_focus(current.stats),
            "mastery_focus": self._recommend_mastery_focus(current.masteries),
            "specialization_path": self._recommend_specialization(
                current.stats,
                current.specializations
            )
        }
        
        return recommendations
        
    def _recommend_stat_focus(self, stats: Dict[str, float]) -> str:
        """Recommend which stat to focus on."""
        min_stat = min(stats.items(), key=lambda x: x[1])
        return f"Focus on increasing {min_stat[0]} to maintain balance"
        
    def _recommend_mastery_focus(
        self,
        masteries: Dict[str, Dict[str, Any]]
    ) -> str:
        """Recommend which mastery to focus on."""
        min_mastery = min(
            masteries.items(),
            key=lambda x: x[1]["level"]
        )
        return f"Focus on {min_mastery[0]} mastery to unlock new abilities"
        
    def _recommend_specialization(
        self,
        stats: Dict[str, float],
        specializations: Dict[str, List[str]]
    ) -> str:
        """Recommend specialization path based on stats."""
        # Implementation would depend on specific game balance
        return "Recommendation logic based on game design"
        
    def log_state(self, log_path: Optional[str] = None) -> None:
        """Log current progression state to file."""
        if not log_path:
            log_path = f"logs/debug/progression_state_{int(time.time())}.json"
            
        if not self.snapshots:
            return
            
        current = self.snapshots[-1]
        analysis = self.analyze_progression_rate()
        recommendations = self.get_progression_recommendations()
        
        state_data = {
            "timestamp": datetime.fromtimestamp(current.timestamp).isoformat(),
            "current_state": {
                "level": current.level,
                "experience": current.experience,
                "stats": current.stats,
                "masteries": current.masteries,
                "specializations": current.specializations
            },
            "progression_analysis": analysis,
            "recommendations": recommendations
        }
        
        with open(log_path, 'w') as f:
            json.dump(state_data, f, indent=2)
            
def main():
    """Main function for running the inspector independently."""
    inspector = ProgressionInspector()
    
    # Example usage with mock character state
    class MockCharacterState:
        def __init__(self):
            self.level = 10
            self.experience = 1500.0
            
        def get_strength(self): return 15.0
        def get_agility(self): return 12.0
        def get_intelligence(self): return 18.0
        def get_vitality(self): return 14.0
        def get_willpower(self): return 16.0
        
        def get_combat_level(self): return 5
        def get_dimensional_level(self): return 4
        def get_crafting_level(self): return 3
        def get_exploration_level(self): return 2
        
        def get_combat_exp(self): return 750.0
        def get_dimensional_exp(self): return 600.0
        def get_crafting_exp(self): return 450.0
        def get_exploration_exp(self): return 300.0
        
        def get_combat_milestones(self): return ["basic_combat", "advanced_stance"]
        def get_dimensional_milestones(self): return ["dimensional_sight"]
        def get_crafting_milestones(self): return ["basic_crafting"]
        def get_exploration_milestones(self): return []
        
        def get_unlocked_nodes(self, spec): return []
        def get_completed_achievements(self): return ["first_level", "dimensional_traveler"]
    
    # Take some snapshots
    mock_state = MockCharacterState()
    inspector.take_snapshot(mock_state)
    time.sleep(1)
    
    # Simulate some progression
    mock_state.level = 11
    mock_state.experience = 1800.0
    inspector.take_snapshot(mock_state)
    
    # Generate and save reports
    inspector.log_state()
    
if __name__ == "__main__":
    main() 