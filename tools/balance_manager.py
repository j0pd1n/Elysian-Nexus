from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
import math
import logging
import time
from collections import deque

class DifficultyLevel(Enum):
    VERY_EASY = "very_easy"
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    VERY_HARD = "very_hard"
    ADAPTIVE = "adaptive"

class BalanceMetric(Enum):
    PLAYER_DAMAGE = "player_damage"
    ENEMY_DAMAGE = "enemy_damage"
    SURVIVAL_TIME = "survival_time"
    VICTORY_RATE = "victory_rate"
    RESOURCE_USAGE = "resource_usage"
    ABILITY_USAGE = "ability_usage"

@dataclass
class CombatMetrics:
    player_damage_dealt: float
    player_damage_taken: float
    combat_duration: float
    resources_used: Dict[str, int]
    abilities_used: Dict[str, int]
    victory: bool
    difficulty_level: DifficultyLevel

class BalanceManager:
    def __init__(self):
        self.current_difficulty = DifficultyLevel.NORMAL
        self.metrics_history: List[CombatMetrics] = []
        self.performance_window = deque(maxlen=10)  # Last 10 combats
        self.target_victory_rate = 0.6  # 60% target victory rate
        self.adjustment_threshold = 0.1  # 10% deviation triggers adjustment
        self.logger = self._setup_logger()
        
        # Balance multipliers
        self.balance_multipliers = {
            DifficultyLevel.VERY_EASY: {
                "player_damage": 1.5,
                "enemy_damage": 0.5,
                "enemy_health": 0.7,
                "resource_cost": 0.5
            },
            DifficultyLevel.EASY: {
                "player_damage": 1.2,
                "enemy_damage": 0.8,
                "enemy_health": 0.9,
                "resource_cost": 0.8
            },
            DifficultyLevel.NORMAL: {
                "player_damage": 1.0,
                "enemy_damage": 1.0,
                "enemy_health": 1.0,
                "resource_cost": 1.0
            },
            DifficultyLevel.HARD: {
                "player_damage": 0.8,
                "enemy_damage": 1.2,
                "enemy_health": 1.3,
                "resource_cost": 1.2
            },
            DifficultyLevel.VERY_HARD: {
                "player_damage": 0.7,
                "enemy_damage": 1.5,
                "enemy_health": 1.5,
                "resource_cost": 1.5
            }
        }
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger("BalanceManager")
        logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler("logs/balance.log")
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        logger.addHandler(handler)
        return logger

    def record_combat_metrics(self, metrics: CombatMetrics):
        """Record metrics from a combat encounter"""
        self.metrics_history.append(metrics)
        self.performance_window.append(metrics)
        
        if len(self.performance_window) >= 5:  # Wait for enough data
            self._adjust_difficulty()
            
        self.logger.info(
            f"Combat recorded - Difficulty: {metrics.difficulty_level.value}, "
            f"Victory: {metrics.victory}, Duration: {metrics.combat_duration:.1f}s"
        )

    def _adjust_difficulty(self):
        """Adjust difficulty based on recent performance"""
        recent_victories = sum(1 for m in self.performance_window if m.victory)
        victory_rate = recent_victories / len(self.performance_window)
        
        if self.current_difficulty == DifficultyLevel.ADAPTIVE:
            self._apply_adaptive_adjustment(victory_rate)
        else:
            self._apply_fixed_adjustment(victory_rate)
            
        self.logger.info(
            f"Difficulty adjusted - Current: {self.current_difficulty.value}, "
            f"Victory Rate: {victory_rate:.2f}"
        )

    def _apply_adaptive_adjustment(self, victory_rate: float):
        """Apply fine-tuned adaptive difficulty adjustments"""
        deviation = victory_rate - self.target_victory_rate
        
        if abs(deviation) < self.adjustment_threshold:
            return  # Within acceptable range
            
        # Calculate adjustment factors
        adjustment_strength = min(abs(deviation) * 2, 0.2)  # Cap at 20% change
        
        # Update multipliers
        for metric in self.balance_multipliers[DifficultyLevel.NORMAL].keys():
            current = self._get_current_multiplier(metric)
            if deviation > 0:  # Too easy
                new_value = current * (1 - adjustment_strength)
            else:  # Too hard
                new_value = current * (1 + adjustment_strength)
                
            self._set_adaptive_multiplier(metric, new_value)

    def _apply_fixed_adjustment(self, victory_rate: float):
        """Apply fixed difficulty level adjustments"""
        if victory_rate > self.target_victory_rate + self.adjustment_threshold:
            self._increase_difficulty()
        elif victory_rate < self.target_victory_rate - self.adjustment_threshold:
            self._decrease_difficulty()

    def _increase_difficulty(self):
        """Increase to next difficulty level"""
        current_index = list(DifficultyLevel).index(self.current_difficulty)
        if current_index < len(DifficultyLevel) - 2:  # Don't include ADAPTIVE
            self.current_difficulty = list(DifficultyLevel)[current_index + 1]

    def _decrease_difficulty(self):
        """Decrease to previous difficulty level"""
        current_index = list(DifficultyLevel).index(self.current_difficulty)
        if current_index > 0:
            self.current_difficulty = list(DifficultyLevel)[current_index - 1]

    def get_current_multipliers(self) -> Dict[str, float]:
        """Get current balance multipliers"""
        if self.current_difficulty == DifficultyLevel.ADAPTIVE:
            return self._get_adaptive_multipliers()
        return self.balance_multipliers[self.current_difficulty]

    def _get_adaptive_multipliers(self) -> Dict[str, float]:
        """Get current adaptive multipliers"""
        return {
            metric: self._get_current_multiplier(metric)
            for metric in self.balance_multipliers[DifficultyLevel.NORMAL].keys()
        }

    def _get_current_multiplier(self, metric: str) -> float:
        """Get current multiplier for a specific metric"""
        return self.balance_multipliers[DifficultyLevel.NORMAL][metric]

    def _set_adaptive_multiplier(self, metric: str, value: float):
        """Set adaptive multiplier for a specific metric"""
        self.balance_multipliers[DifficultyLevel.ADAPTIVE] = \
            self.balance_multipliers.get(DifficultyLevel.ADAPTIVE, {})
        self.balance_multipliers[DifficultyLevel.ADAPTIVE][metric] = value

    def analyze_balance(self) -> Dict[str, Any]:
        """Analyze current game balance"""
        if not self.metrics_history:
            return {"status": "no_data"}
            
        analysis = {
            "total_combats": len(self.metrics_history),
            "victory_rate": 0,
            "average_duration": 0,
            "difficulty_distribution": {},
            "resource_usage": {},
            "ability_usage": {},
            "damage_stats": {
                "average_dealt": 0,
                "average_taken": 0,
                "damage_ratio": 0
            }
        }
        
        # Calculate statistics
        victories = 0
        total_duration = 0
        total_damage_dealt = 0
        total_damage_taken = 0
        
        for metrics in self.metrics_history:
            victories += 1 if metrics.victory else 0
            total_duration += metrics.combat_duration
            total_damage_dealt += metrics.player_damage_dealt
            total_damage_taken += metrics.player_damage_taken
            
            # Difficulty distribution
            diff_key = metrics.difficulty_level.value
            analysis["difficulty_distribution"][diff_key] = \
                analysis["difficulty_distribution"].get(diff_key, 0) + 1
                
            # Resource usage
            for resource, amount in metrics.resources_used.items():
                if resource not in analysis["resource_usage"]:
                    analysis["resource_usage"][resource] = 0
                analysis["resource_usage"][resource] += amount
                
            # Ability usage
            for ability, count in metrics.abilities_used.items():
                if ability not in analysis["ability_usage"]:
                    analysis["ability_usage"][ability] = 0
                analysis["ability_usage"][ability] += count
                
        # Calculate averages
        total = len(self.metrics_history)
        analysis["victory_rate"] = victories / total
        analysis["average_duration"] = total_duration / total
        analysis["damage_stats"]["average_dealt"] = total_damage_dealt / total
        analysis["damage_stats"]["average_taken"] = total_damage_taken / total
        
        if total_damage_taken > 0:
            analysis["damage_stats"]["damage_ratio"] = \
                total_damage_dealt / total_damage_taken
                
        # Convert counts to percentages
        for diff in analysis["difficulty_distribution"]:
            analysis["difficulty_distribution"][diff] = \
                analysis["difficulty_distribution"][diff] / total * 100
                
        return analysis

    def get_difficulty_recommendation(self) -> DifficultyLevel:
        """Get recommended difficulty based on player performance"""
        if not self.metrics_history:
            return DifficultyLevel.NORMAL
            
        recent_metrics = self.metrics_history[-10:]  # Last 10 combats
        
        # Calculate performance metrics
        victory_rate = sum(1 for m in recent_metrics if m.victory) / len(recent_metrics)
        avg_duration = sum(m.combat_duration for m in recent_metrics) / len(recent_metrics)
        
        # Decision logic
        if victory_rate > 0.8 and avg_duration < 60:  # Quick victories
            return DifficultyLevel.HARD
        elif victory_rate < 0.3:  # Frequent defeats
            return DifficultyLevel.EASY
        elif 0.4 <= victory_rate <= 0.7:  # Balanced
            return DifficultyLevel.NORMAL
        else:
            return DifficultyLevel.ADAPTIVE

    def export_balance_data(self, file_path: str):
        """Export balance data for analysis"""
        data = {
            "current_difficulty": self.current_difficulty.value,
            "balance_multipliers": self.balance_multipliers,
            "metrics_history": [
                {
                    "player_damage_dealt": m.player_damage_dealt,
                    "player_damage_taken": m.player_damage_taken,
                    "combat_duration": m.combat_duration,
                    "resources_used": m.resources_used,
                    "abilities_used": m.abilities_used,
                    "victory": m.victory,
                    "difficulty_level": m.difficulty_level.value
                }
                for m in self.metrics_history
            ]
        }
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def import_balance_data(self, file_path: str):
        """Import balance data"""
        with open(file_path, "r") as f:
            data = json.load(f)
            
        self.current_difficulty = DifficultyLevel(data["current_difficulty"])
        self.balance_multipliers = data["balance_multipliers"]
        
        self.metrics_history = [
            CombatMetrics(
                player_damage_dealt=m["player_damage_dealt"],
                player_damage_taken=m["player_damage_taken"],
                combat_duration=m["combat_duration"],
                resources_used=m["resources_used"],
                abilities_used=m["abilities_used"],
                victory=m["victory"],
                difficulty_level=DifficultyLevel(m["difficulty_level"])
            )
            for m in data["metrics_history"]
        ] 