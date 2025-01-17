import unittest
import time
from typing import Dict, Set, List
from src.infrastructure.test_framework import TestDecorators, TestType, TestPriority
from src.infrastructure.performance_monitor import MetricType
from src.combat_system.dimensional_combat import (
    DimensionalLayer,
    DimensionalEffect,
    DimensionalCombat,
    Position,
    CombatAbility,
    DamageType,
    StatusEffect
)

class TestDimensionalMechanics(unittest.TestCase):
    """Test cases for dimensional combat mechanics"""
    
    def setUp(self):
        """Set up test environment"""
        self.combat_system = DimensionalCombat()
        self.test_abilities = {
            "void_strike": CombatAbility(
                name="Void Strike",
                damage_type=DamageType.VOID,
                base_power=100,
                dimensional_scaling=1.5,
                stability_cost=0.1
            ),
            "ethereal_blast": CombatAbility(
                name="Ethereal Blast",
                damage_type=DamageType.ETHEREAL,
                base_power=80,
                dimensional_scaling=1.2,
                stability_cost=0.05,
                area_effect=True
            ),
            "dimensional_anchor": CombatAbility(
                name="Dimensional Anchor",
                damage_type=DamageType.PHYSICAL,
                base_power=50,
                stability_cost=0.2,
                status_effects=[StatusEffect.ANCHORED]
            )
        }
        
    @TestDecorators.test_type(TestType.UNIT)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_ability_scaling(self):
        """Test dimensional ability scaling"""
        # Test scaling in different dimensions
        dimensions = ["Physical", "Ethereal", "Void"]
        base_power = 100
        
        for dim in dimensions:
            power = self.combat_system.calculate_ability_power(
                ability_name="Void Strike",
                base_power=base_power,
                source_dimension=dim,
                target_dimension="Physical"
            )
            
            if dim == "Void":
                self.assertGreater(power, base_power)  # Should get bonus
            elif dim == "Physical":
                self.assertEqual(power, base_power)  # No scaling
                
    @TestDecorators.test_type(TestType.INTEGRATION)
    @TestDecorators.test_priority(TestPriority.CRITICAL)
    def test_status_effect_interactions(self):
        """Test status effects in dimensional combat"""
        # Apply anchoring effect
        self.combat_system.apply_ability_effect(
            ability=self.test_abilities["dimensional_anchor"],
            target_position=Position(0, 0, 0),
            source_dimension="Physical",
            target_dimension="Ethereal"
        )
        
        # Verify dimension lock
        can_shift = self.combat_system.can_shift_dimensions(
            position=Position(0, 0, 0),
            from_dimension="Ethereal",
            to_dimension="Void"
        )
        self.assertFalse(can_shift)
        
        # Test effect duration
        self.combat_system.update_effects(time_delta=5.0)
        can_shift = self.combat_system.can_shift_dimensions(
            position=Position(0, 0, 0),
            from_dimension="Ethereal",
            to_dimension="Void"
        )
        self.assertTrue(can_shift)  # Effect should have expired
        
    @TestDecorators.test_type(TestType.PERFORMANCE)
    @TestDecorators.test_priority(TestPriority.HIGH)
    @TestDecorators.performance_threshold(MetricType.ABILITY_CALCULATIONS, 10.0)
    def test_area_effect_performance(self):
        """Test performance of area effect abilities"""
        start_time = time.time()
        
        # Create multiple targets
        targets = [
            Position(x, y, 0)
            for x in range(-5, 6, 2)
            for y in range(-5, 6, 2)
        ]
        
        # Apply area effect ability
        self.combat_system.apply_ability_effect(
            ability=self.test_abilities["ethereal_blast"],
            target_position=Position(0, 0, 0),
            source_dimension="Ethereal",
            target_dimension="Physical",
            affected_positions=targets
        )
        
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Convert to ms
        
        # Verify performance
        self.assertLess(duration, 10.0)  # Should process within 10ms
        
    @TestDecorators.test_type(TestType.STRESS)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_combat_system_under_load(self):
        """Test combat system under heavy ability usage"""
        abilities = list(self.test_abilities.values()) * 10  # Multiple copies
        positions = [
            Position(x, y, 0)
            for x in range(-10, 11, 2)
            for y in range(-10, 11, 2)
        ]
        
        start_time = time.time()
        
        # Rapid ability usage
        for ability in abilities:
            for pos in positions:
                self.combat_system.apply_ability_effect(
                    ability=ability,
                    target_position=pos,
                    source_dimension="Physical",
                    target_dimension="Ethereal"
                )
                
        # Update effects
        self.combat_system.update_effects(time_delta=0.016)  # One frame
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        # Verify system stability
        self.assertLess(total_duration, 1.0)  # Should complete within 1 second
        
    @TestDecorators.test_type(TestType.DIMENSION)
    @TestDecorators.test_priority(TestPriority.CRITICAL)
    def test_dimensional_resonance_combat(self):
        """Test combat with dimensional resonance"""
        # Setup resonance
        self.combat_system.create_dimensional_resonance(
            center=Position(0, 0, 0),
            affected_dimensions={"Physical", "Ethereal"},
            power=50
        )
        
        # Test ability power in resonance
        base_damage = self.combat_system.calculate_ability_power(
            ability_name="Ethereal Blast",
            base_power=80,
            source_dimension="Physical",
            target_dimension="Ethereal"
        )
        
        resonance_damage = self.combat_system.calculate_ability_power(
            ability_name="Ethereal Blast",
            base_power=80,
            source_dimension="Physical",
            target_dimension="Ethereal",
            position=Position(0, 0, 0)  # In resonance
        )
        
        self.assertGreater(resonance_damage, base_damage)
        
    @TestDecorators.test_type(TestType.INTEGRATION)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_ability_chain_effects(self):
        """Test chaining multiple abilities"""
        # Setup chain of abilities
        chain = [
            (self.test_abilities["void_strike"], "Void", "Physical"),
            (self.test_abilities["ethereal_blast"], "Physical", "Ethereal"),
            (self.test_abilities["dimensional_anchor"], "Ethereal", "Void")
        ]
        
        total_stability_cost = 0
        cumulative_damage = 0
        
        # Execute ability chain
        for ability, source, target in chain:
            result = self.combat_system.apply_ability_effect(
                ability=ability,
                target_position=Position(0, 0, 0),
                source_dimension=source,
                target_dimension=target
            )
            
            total_stability_cost += result.stability_cost
            cumulative_damage += result.damage
            
        # Verify chain effects
        self.assertGreater(cumulative_damage, 0)
        self.assertLess(total_stability_cost, 1.0)  # Should not destabilize completely
        
    @TestDecorators.test_type(TestType.PERFORMANCE)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_combat_metrics(self):
        """Test combat performance metrics"""
        metrics = {
            "ability_calculations": [],
            "effect_processing": [],
            "stability_updates": []
        }
        
        # Perform combat actions and measure
        for _ in range(100):
            start_time = time.time()
            
            # Ability calculation
            self.combat_system.calculate_ability_power(
                ability_name="Void Strike",
                base_power=100,
                source_dimension="Void",
                target_dimension="Physical"
            )
            
            metrics["ability_calculations"].append(time.time() - start_time)
            
            # Effect processing
            start_time = time.time()
            self.combat_system.update_effects(time_delta=0.016)
            metrics["effect_processing"].append(time.time() - start_time)
            
            # Stability updates
            start_time = time.time()
            self.combat_system.update_dimensional_stability(time_delta=0.016)
            metrics["stability_updates"].append(time.time() - start_time)
            
        # Verify metrics
        for category, timings in metrics.items():
            avg_time = sum(timings) / len(timings) * 1000  # Convert to ms
            self.assertLess(avg_time, 1.0)  # Each operation should take < 1ms

if __name__ == '__main__':
    unittest.main() 