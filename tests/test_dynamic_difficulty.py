import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import numpy as np

from ..combat_system.dynamic_difficulty import (
    DynamicDifficulty,
    DifficultyTier,
    ChallengeType,
    PlayerMetrics,
    DifficultyModifiers,
    CelestialAlignment
)

class TestDynamicDifficulty(unittest.TestCase):
    def setUp(self):
        self.difficulty_system = DynamicDifficulty()
        
    def test_initialization(self):
        """Test system initialization"""
        self.assertIsNotNone(self.difficulty_system.base_difficulty)
        self.assertIsNotNone(self.difficulty_system.player_metrics)
        self.assertEqual(len(self.difficulty_system.recent_adjustments), 0)
        self.assertEqual(len(self.difficulty_system.performance_history), 0)
        
    def test_player_metrics_update(self):
        """Test updating player performance metrics"""
        # Test combat result update
        self.difficulty_system.update_player_metrics("combat_result", 1.0)
        self.assertGreater(self.difficulty_system.player_metrics.combat_win_rate, 0.5)
        
        # Test damage metrics
        self.difficulty_system.update_player_metrics("damage_dealt", 100.0)
        self.assertGreater(self.difficulty_system.player_metrics.average_damage_dealt, 0)
        
        # Test ritual success
        self.difficulty_system.update_player_metrics("ritual_result", 1.0)
        self.assertGreater(self.difficulty_system.player_metrics.ritual_success_rate, 0.5)
        
        # Test challenge completion time
        self.difficulty_system.update_player_metrics(
            "combat_result",
            1.0,
            challenge_id="test_challenge"
        )
        self.assertIn(
            "test_challenge",
            self.difficulty_system.player_metrics.challenge_completion_times
        )
        
    def test_difficulty_adjustment_calculation(self):
        """Test difficulty adjustment calculations"""
        # Set up test metrics
        self.difficulty_system.player_metrics.combat_win_rate = 0.8  # High performance
        self.difficulty_system.player_metrics.consecutive_victories = 6
        self.difficulty_system.player_metrics.celestial_mastery_level = 2
        
        adjustment = self.difficulty_system.calculate_difficulty_adjustment()
        self.assertGreater(adjustment, 0)  # Should increase difficulty
        
        # Test cooldown
        self.difficulty_system.recent_adjustments.append(
            (datetime.now(), adjustment)
        )
        second_adjustment = self.difficulty_system.calculate_difficulty_adjustment()
        self.assertEqual(second_adjustment, 0.0)  # Should be on cooldown
        
    def test_challenge_difficulty_generation(self):
        """Test challenge-specific difficulty generation"""
        # Test regular combat
        combat_difficulty = self.difficulty_system.get_challenge_difficulty(
            ChallengeType.COMBAT,
            player_level=5
        )
        self.assertIsInstance(combat_difficulty, DifficultyModifiers)
        
        # Test ritual difficulty
        ritual_difficulty = self.difficulty_system.get_challenge_difficulty(
            ChallengeType.RITUAL,
            player_level=5
        )
        self.assertGreater(
            ritual_difficulty.ritual_complexity_multiplier,
            combat_difficulty.ritual_complexity_multiplier
        )
        
        # Test celestial event
        celestial_difficulty = self.difficulty_system.get_challenge_difficulty(
            ChallengeType.CELESTIAL_EVENT,
            player_level=5,
            celestial_alignment=CelestialAlignment.SOLAR
        )
        self.assertGreater(
            celestial_difficulty.environmental_intensity_multiplier,
            combat_difficulty.environmental_intensity_multiplier
        )
        
    def test_party_size_recommendations(self):
        """Test party size recommendations"""
        # Test ritual party size
        min_size, max_size = self.difficulty_system.get_recommended_party_size(
            ChallengeType.RITUAL,
            base_difficulty=2.0
        )
        self.assertGreater(min_size, 2)
        self.assertEqual(max_size, min_size + 2)
        
        # Test celestial event party size
        min_size, max_size = self.difficulty_system.get_recommended_party_size(
            ChallengeType.CELESTIAL_EVENT,
            base_difficulty=2.0
        )
        self.assertGreater(min_size, 3)
        self.assertEqual(max_size, min_size + 3)
        
    def test_performance_trend_analysis(self):
        """Test performance trend analysis"""
        # Add some test performance data
        for _ in range(20):
            self.difficulty_system.performance_history.append(0.5)
        for _ in range(10):
            self.difficulty_system.performance_history.append(0.7)
            
        trend_data = self.difficulty_system.get_performance_trend()
        self.assertGreater(trend_data["trend"], 0)  # Should show improving trend
        self.assertGreater(trend_data["volatility"], 0)
        
    def test_difficulty_tier_progression(self):
        """Test difficulty tier determination"""
        # Test initial tier
        self.assertEqual(
            self.difficulty_system.get_difficulty_tier(),
            DifficultyTier.NOVICE
        )
        
        # Add high performance history
        for _ in range(10):
            self.difficulty_system.performance_history.append(0.9)
            
        # Should progress to higher tier
        self.assertIn(
            self.difficulty_system.get_difficulty_tier(),
            [DifficultyTier.CELESTIAL, DifficultyTier.MASTER]
        )
        
    def test_modifier_scaling(self):
        """Test difficulty modifier scaling"""
        base_modifiers = self.difficulty_system._get_base_modifiers()
        
        # Test positive adjustment
        adjusted = self.difficulty_system._apply_adjustment(base_modifiers, 0.2)
        self.assertGreater(adjusted.enemy_health_multiplier, base_modifiers.enemy_health_multiplier)
        
        # Test negative adjustment
        adjusted = self.difficulty_system._apply_adjustment(base_modifiers, -0.2)
        self.assertLess(adjusted.enemy_health_multiplier, base_modifiers.enemy_health_multiplier)
        
        # Test level scaling
        scaled = self.difficulty_system._scale_modifiers(base_modifiers, 1.5)
        self.assertEqual(
            scaled.enemy_health_multiplier,
            base_modifiers.enemy_health_multiplier * 1.5
        )
        
    def test_performance_history_management(self):
        """Test performance history management"""
        # Fill performance history
        for _ in range(150):
            self.difficulty_system._update_performance_history()
            
        # Check if history is capped
        self.assertLessEqual(len(self.difficulty_system.performance_history), 100)
        
    def test_difficulty_tiers_initialization(self):
        """Test difficulty tiers configuration"""
        tiers = self.difficulty_system.difficulty_tiers
        
        # Check all tiers are present
        for tier in DifficultyTier:
            self.assertIn(tier, tiers)
            
        # Check tier progression
        self.assertLess(
            tiers[DifficultyTier.NOVICE].enemy_health_multiplier,
            tiers[DifficultyTier.ADEPT].enemy_health_multiplier
        )
        self.assertLess(
            tiers[DifficultyTier.ADEPT].enemy_health_multiplier,
            tiers[DifficultyTier.EXPERT].enemy_health_multiplier
        )
        
    def test_challenge_completion_tracking(self):
        """Test challenge completion time tracking"""
        challenge_id = "test_ritual"
        completion_time = 300.0  # seconds
        
        self.difficulty_system.update_player_metrics(
            "ritual_result",
            1.0,
            challenge_id=challenge_id
        )
        
        self.assertIn(
            challenge_id,
            self.difficulty_system.player_metrics.challenge_completion_times
        )
        
if __name__ == '__main__':
    unittest.main() 