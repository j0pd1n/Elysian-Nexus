import unittest
import time
from typing import Dict, Set
from src.infrastructure.test_framework import TestDecorators, TestType, TestPriority
from src.infrastructure.performance_monitor import MetricType
from src.combat_system.dimensional_combat import (
    DimensionalLayer,
    DimensionalEffect,
    DimensionalCombat,
    Position
)

class TestDimensionalEffects(unittest.TestCase):
    """Test cases for dimensional effects system"""
    
    def setUp(self):
        """Set up test environment"""
        self.combat_system = DimensionalCombat()
        self.dimensions = {
            "Physical": DimensionalLayer("Physical", stability=1.0),
            "Ethereal": DimensionalLayer("Ethereal", stability=0.8),
            "Void": DimensionalLayer("Void", stability=0.5),
            "Celestial": DimensionalLayer("Celestial", stability=0.9),
            "Primordial": DimensionalLayer("Primordial", stability=0.3)
        }
        for dim in self.dimensions.values():
            self.combat_system.add_dimension(dim)
            
    @TestDecorators.test_type(TestType.UNIT)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_effect_stacking(self):
        """Test stacking of dimensional effects"""
        # Apply multiple distortion effects
        effects = [
            DimensionalEffect("Distortion", power=10, duration=5.0),
            DimensionalEffect("Distortion", power=15, duration=5.0),
            DimensionalEffect("Distortion", power=20, duration=5.0)
        ]
        
        for effect in effects:
            self.combat_system.apply_dimensional_effect(
                source_dimension="Void",
                target_dimension="Physical",
                effect=effect
            )
            
        # Get total distortion
        total_distortion = self.combat_system.get_total_effect_power(
            dimension="Physical",
            effect_name="Distortion"
        )
        
        # Should use diminishing returns formula
        self.assertLess(total_distortion, sum(e.power for e in effects))
        self.assertGreater(total_distortion, max(e.power for e in effects))
        
    @TestDecorators.test_type(TestType.INTEGRATION)
    @TestDecorators.test_priority(TestPriority.CRITICAL)
    def test_effect_interactions(self):
        """Test interactions between different effect types"""
        # Apply opposing effects
        self.combat_system.apply_dimensional_effect(
            source_dimension="Celestial",
            target_dimension="Void",
            effect=DimensionalEffect("Stabilize", power=30, duration=5.0)
        )
        
        self.combat_system.apply_dimensional_effect(
            source_dimension="Void",
            target_dimension="Void",
            effect=DimensionalEffect("Destabilize", power=20, duration=5.0)
        )
        
        # Check net stability change
        stability = self.combat_system.get_dimension_stability("Void")
        original_stability = self.dimensions["Void"].stability
        
        # Net effect should favor the stronger effect
        self.assertGreater(stability, original_stability)
        
    @TestDecorators.test_type(TestType.PERFORMANCE)
    @TestDecorators.test_priority(TestPriority.HIGH)
    @TestDecorators.performance_threshold(MetricType.ABILITY_CALCULATIONS, 20.0)
    def test_effect_propagation_performance(self):
        """Test performance of effect propagation through dimensions"""
        start_time = time.time()
        
        # Create chain reaction of effects
        effect = DimensionalEffect("Resonance", power=100, duration=10.0)
        self.combat_system.trigger_effect_cascade(
            source_dimension="Primordial",
            initial_effect=effect,
            propagation_depth=3
        )
        
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Convert to ms
        
        # Verify performance
        self.assertLess(duration, 20.0)  # Should process within 20ms
        
    @TestDecorators.test_type(TestType.STRESS)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_effect_system_under_load(self):
        """Test effect system under heavy load"""
        effect_types = [
            ("Distortion", 10),
            ("Resonance", 20),
            ("Stabilize", 15),
            ("Destabilize", 25),
            ("Anchor", 30)
        ]
        
        # Apply many effects rapidly
        for _ in range(100):
            for source in self.dimensions.values():
                for target in self.dimensions.values():
                    if source != target:
                        for effect_name, power in effect_types:
                            self.combat_system.apply_dimensional_effect(
                                source_dimension=source.name,
                                target_dimension=target.name,
                                effect=DimensionalEffect(
                                    effect_name,
                                    power=power,
                                    duration=5.0
                                )
                            )
                            
        # Verify system stability
        for dim_name, dim in self.dimensions.items():
            # Check effect count
            active_effects = self.combat_system.get_active_effects(dim_name)
            self.assertLess(len(active_effects), 1000)  # Effect cleanup should work
            
            # Check stability bounds
            stability = self.combat_system.get_dimension_stability(dim_name)
            self.assertGreaterEqual(stability, 0.0)
            self.assertLessEqual(stability, 1.0)
            
    @TestDecorators.test_type(TestType.DIMENSION)
    @TestDecorators.test_priority(TestPriority.CRITICAL)
    def test_dimensional_collapse_prevention(self):
        """Test system prevents dimensional collapse"""
        # Try to destabilize a dimension completely
        for _ in range(10):
            self.combat_system.apply_dimensional_effect(
                source_dimension="Void",
                target_dimension="Physical",
                effect=DimensionalEffect(
                    "Destabilize",
                    power=100,
                    duration=10.0
                )
            )
            
        # Dimension should maintain minimum stability
        stability = self.combat_system.get_dimension_stability("Physical")
        self.assertGreater(stability, 0.1)  # Minimum stability threshold
        
    @TestDecorators.test_type(TestType.INTEGRATION)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_effect_duration_and_cleanup(self):
        """Test effect duration tracking and cleanup"""
        # Apply effects with different durations
        effects = [
            ("Short", DimensionalEffect("Distortion", power=10, duration=1.0)),
            ("Medium", DimensionalEffect("Resonance", power=20, duration=3.0)),
            ("Long", DimensionalEffect("Anchor", power=30, duration=5.0))
        ]
        
        for label, effect in effects:
            self.combat_system.apply_dimensional_effect(
                source_dimension="Ethereal",
                target_dimension="Physical",
                effect=effect
            )
            
        # Wait for short effect to expire
        time.sleep(2.0)
        active_effects = self.combat_system.get_active_effects("Physical")
        self.assertNotIn("Distortion", [e.name for e in active_effects])
        
        # Wait for medium effect to expire
        time.sleep(2.0)
        active_effects = self.combat_system.get_active_effects("Physical")
        self.assertNotIn("Resonance", [e.name for e in active_effects])
        
        # Verify long effect still active
        self.assertIn("Anchor", [e.name for e in active_effects])

if __name__ == '__main__':
    unittest.main() 