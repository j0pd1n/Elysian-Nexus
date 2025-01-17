import unittest
import time
from typing import Dict, Set, List
from src.infrastructure.test_framework import TestDecorators, TestType, TestPriority
from src.infrastructure.performance_monitor import MetricType
from src.combat_system.dimensional_combat import Position, DimensionalLayer
from src.combat_system.abilities import AbilitySystem, Ability, AbilityType, AbilityEffect
from src.combat_system.status_effects import StatusEffect, StatusEffectManager

class TestAbilityMechanics(unittest.TestCase):
    """Test cases for ability mechanics and interactions"""
    
    def setUp(self):
        """Set up test environment"""
        self.ability_system = AbilitySystem()
        self.effect_manager = StatusEffectManager()
        self.test_abilities = {
            "void_resonance": Ability(
                name="Void Resonance",
                type=AbilityType.VOID,
                base_power=100,
                stability_cost=0.15,
                effects=[StatusEffect.DIMENSIONAL_WEAKNESS]
            ),
            "ethereal_chain": Ability(
                name="Ethereal Chain",
                type=AbilityType.ETHEREAL,
                base_power=75,
                stability_cost=0.1,
                effects=[StatusEffect.DIMENSIONAL_ANCHOR]
            ),
            "primordial_surge": Ability(
                name="Primordial Surge",
                type=AbilityType.PRIMORDIAL,
                base_power=150,
                stability_cost=0.2,
                effects=[StatusEffect.DIMENSIONAL_SURGE]
            )
        }
        
    @TestDecorators.test_type(TestType.UNIT)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_ability_effect_stacking(self):
        """Test stacking of ability effects"""
        target_pos = Position(0, 0, 0)
        
        # Apply multiple effects
        self.ability_system.apply_ability(
            self.test_abilities["void_resonance"],
            target_pos,
            "Void"
        )
        self.ability_system.apply_ability(
            self.test_abilities["ethereal_chain"],
            target_pos,
            "Ethereal"
        )
        
        effects = self.effect_manager.get_active_effects(target_pos)
        self.assertEqual(len(effects), 2)
        self.assertTrue(any(e.type == StatusEffect.DIMENSIONAL_WEAKNESS for e in effects))
        
    @TestDecorators.test_type(TestType.INTEGRATION)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_ability_chain_resonance(self):
        """Test ability chain resonance effects"""
        target_pos = Position(0, 0, 0)
        
        # Create ability chain
        chain_result = self.ability_system.execute_ability_chain(
            [
                (self.test_abilities["void_resonance"], "Void"),
                (self.test_abilities["ethereal_chain"], "Ethereal"),
                (self.test_abilities["primordial_surge"], "Primordial")
            ],
            target_pos
        )
        
        self.assertTrue(chain_result.resonance_triggered)
        self.assertGreater(chain_result.total_damage, 
                          sum(a.base_power for a in self.test_abilities.values()))
        
    @TestDecorators.test_type(TestType.PERFORMANCE)
    @TestDecorators.test_priority(TestPriority.HIGH)
    @TestDecorators.performance_threshold(MetricType.ABILITY_PROCESSING, 2.0)
    def test_ability_processing_performance(self):
        """Test performance of ability processing"""
        target_pos = Position(0, 0, 0)
        iterations = 1000
        
        start_time = time.time()
        
        for _ in range(iterations):
            self.ability_system.apply_ability(
                self.test_abilities["void_resonance"],
                target_pos,
                "Void"
            )
            
        duration = (time.time() - start_time) * 1000 / iterations
        self.assertLess(duration, 2.0)  # Should process within 2ms per ability
        
    @TestDecorators.test_type(TestType.STRESS)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_concurrent_ability_processing(self):
        """Test processing of multiple concurrent abilities"""
        positions = [Position(x, x, 0) for x in range(10)]
        abilities = list(self.test_abilities.values()) * 10
        
        start_time = time.time()
        results = self.ability_system.process_concurrent_abilities(
            [(ability, pos, "Physical") for ability, pos in zip(abilities, positions)]
        )
        
        duration = (time.time() - start_time) * 1000
        self.assertLess(duration, 50.0)  # Should process within 50ms
        self.assertEqual(len(results), len(abilities))
        
    @TestDecorators.test_type(TestType.UNIT)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_dimensional_ability_interactions(self):
        """Test interactions between dimensional abilities"""
        target_pos = Position(0, 0, 0)
        
        # Apply abilities from different dimensions
        void_result = self.ability_system.apply_ability(
            self.test_abilities["void_resonance"],
            target_pos,
            "Void"
        )
        
        ethereal_result = self.ability_system.apply_ability(
            self.test_abilities["ethereal_chain"],
            target_pos,
            "Ethereal"
        )
        
        # Check for interaction effects
        self.assertTrue(void_result.created_dimensional_rift or 
                       ethereal_result.created_dimensional_rift)
        self.assertGreater(
            self.ability_system.get_dimensional_instability(target_pos),
            0.0
        )
        
    @TestDecorators.test_type(TestType.INTEGRATION)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_ability_effect_propagation(self):
        """Test propagation of ability effects through dimensions"""
        center_pos = Position(0, 0, 0)
        affected_positions = [
            Position(x, y, 0)
            for x in range(-2, 3)
            for y in range(-2, 3)
        ]
        
        # Apply area effect ability
        result = self.ability_system.apply_ability(
            self.test_abilities["primordial_surge"],
            center_pos,
            "Primordial",
            affected_positions=affected_positions
        )
        
        # Check effect propagation
        for pos in affected_positions:
            effects = self.effect_manager.get_active_effects(pos)
            self.assertTrue(any(e.type == StatusEffect.DIMENSIONAL_SURGE for e in effects))
            
        self.assertEqual(result.affected_positions, len(affected_positions))

if __name__ == '__main__':
    unittest.main() 