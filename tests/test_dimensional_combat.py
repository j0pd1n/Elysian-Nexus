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

class TestDimensionalCombat(unittest.TestCase):
    """Test cases for dimensional combat system"""
    
    def setUp(self):
        """Set up test environment"""
        self.combat_system = DimensionalCombat()
        self.physical_layer = DimensionalLayer("Physical", stability=1.0)
        self.ethereal_layer = DimensionalLayer("Ethereal", stability=0.8)
        self.void_layer = DimensionalLayer("Void", stability=0.5)
        
    @TestDecorators.test_type(TestType.UNIT)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_dimension_initialization(self):
        """Test initialization of dimensional layers"""
        self.combat_system.add_dimension(self.physical_layer)
        self.combat_system.add_dimension(self.ethereal_layer)
        
        dimensions = self.combat_system.get_dimensions()
        self.assertEqual(len(dimensions), 2)
        self.assertIn("Physical", dimensions)
        self.assertIn("Ethereal", dimensions)
        
    @TestDecorators.test_type(TestType.INTEGRATION)
    @TestDecorators.test_priority(TestPriority.CRITICAL)
    @TestDecorators.requires_dimension("Physical")
    @TestDecorators.requires_dimension("Ethereal")
    def test_cross_dimension_combat(self):
        """Test combat calculations across dimensions"""
        # Setup combat scenario
        attacker_pos = Position(x=0, y=0, z=0)
        defender_pos = Position(x=1, y=1, z=0)
        
        # Test attack from Physical to Ethereal
        damage = self.combat_system.calculate_cross_dimension_damage(
            source_dimension="Physical",
            target_dimension="Ethereal",
            base_damage=100,
            attacker_pos=attacker_pos,
            defender_pos=defender_pos
        )
        
        # Damage should be reduced due to dimensional barrier
        self.assertLess(damage, 100)
        self.assertGreater(damage, 0)
        
    @TestDecorators.test_type(TestType.PERFORMANCE)
    @TestDecorators.test_priority(TestPriority.HIGH)
    @TestDecorators.performance_threshold(MetricType.ABILITY_CALCULATIONS, 50.0)
    def test_dimensional_ability_performance(self):
        """Test performance of dimensional ability calculations"""
        start_time = time.time()
        
        # Perform multiple ability calculations
        for _ in range(1000):
            self.combat_system.calculate_ability_effect(
                ability_name="Dimensional Slash",
                source_dimension="Physical",
                target_dimension="Ethereal",
                power=100,
                stability_cost=0.1
            )
            
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Convert to ms
        
        # Assert performance requirements
        self.assertLess(duration, 50.0)  # Should complete within 50ms
        
    @TestDecorators.test_type(TestType.STRESS)
    @TestDecorators.test_priority(TestPriority.MEDIUM)
    def test_dimension_stability_under_load(self):
        """Test dimensional stability under heavy combat load"""
        # Add multiple dimensions
        dimensions = [
            self.physical_layer,
            self.ethereal_layer,
            self.void_layer
        ]
        for dim in dimensions:
            self.combat_system.add_dimension(dim)
            
        # Simulate heavy combat load
        for _ in range(100):
            for source in dimensions:
                for target in dimensions:
                    if source != target:
                        self.combat_system.apply_dimensional_effect(
                            source_dimension=source.name,
                            target_dimension=target.name,
                            effect=DimensionalEffect(
                                name="Distortion",
                                power=10,
                                duration=5.0
                            )
                        )
                        
        # Check stability of all dimensions
        for dim in dimensions:
            stability = self.combat_system.get_dimension_stability(dim.name)
            self.assertGreater(stability, 0.2)  # Minimum stability threshold
            
    @TestDecorators.test_type(TestType.DIMENSION)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_dimensional_resonance(self):
        """Test dimensional resonance effects"""
        # Setup resonating dimensions
        self.combat_system.add_dimension(self.ethereal_layer)
        self.combat_system.add_dimension(self.void_layer)
        
        # Create resonance effect
        resonance = self.combat_system.create_dimensional_resonance(
            dimensions={"Ethereal", "Void"},
            power=50
        )
        
        # Test resonance properties
        self.assertEqual(len(resonance.affected_dimensions), 2)
        self.assertGreater(resonance.power, 0)
        
        # Test resonance effects on stability
        initial_stability = {
            dim: self.combat_system.get_dimension_stability(dim)
            for dim in resonance.affected_dimensions
        }
        
        self.combat_system.apply_resonance_effect(resonance)
        
        final_stability = {
            dim: self.combat_system.get_dimension_stability(dim)
            for dim in resonance.affected_dimensions
        }
        
        # Verify stability changes
        for dim in resonance.affected_dimensions:
            self.assertNotEqual(
                initial_stability[dim],
                final_stability[dim]
            )
            
    @TestDecorators.test_type(TestType.INTEGRATION)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_dimensional_combat_chain(self):
        """Test chain of dimensional combat effects"""
        # Setup combat chain
        chain = [
            ("Physical", "Ethereal", 100),
            ("Ethereal", "Void", 80),
            ("Void", "Physical", 60)
        ]
        
        # Add all dimensions
        for dim in [self.physical_layer, self.ethereal_layer, self.void_layer]:
            self.combat_system.add_dimension(dim)
            
        # Execute combat chain
        results = []
        for source, target, power in chain:
            damage = self.combat_system.calculate_cross_dimension_damage(
                source_dimension=source,
                target_dimension=target,
                base_damage=power,
                attacker_pos=Position(0, 0, 0),
                defender_pos=Position(1, 1, 0)
            )
            results.append(damage)
            
        # Verify chain effects
        self.assertEqual(len(results), 3)
        self.assertGreater(results[0], results[1])  # Damage should decrease
        self.assertGreater(results[1], results[2])  # along the chain

if __name__ == '__main__':
    unittest.main() 