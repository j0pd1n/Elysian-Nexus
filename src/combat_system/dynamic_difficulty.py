from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math
import random

class DifficultyLevel(Enum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    EXPERT = "expert"

@dataclass
class CombatStats:
    health: float
    damage: float
    defense: float
    speed: float
    abilities: List[str]

class DynamicDifficulty:
    def __init__(self):
        self.base_difficulty = DifficultyLevel.NORMAL
        self.player_performance_history: List[float] = []
        self.encounter_history: List[Dict] = []
        
    def adjust_difficulty(
        self,
        player_stats: CombatStats,
        current_performance: float
    ) -> DifficultyLevel:
        """Adjust difficulty based on player performance"""
        self.player_performance_history.append(current_performance)
        
        # Calculate trend
        if len(self.player_performance_history) >= 3:
            recent_trend = sum(self.player_performance_history[-3:]) / 3
            if recent_trend > 0.8:
                return DifficultyLevel.HARD
            elif recent_trend < 0.4:
                return DifficultyLevel.EASY
                
        return self.base_difficulty 