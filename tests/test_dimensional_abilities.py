import unittest
from src.combat_system.dimensional_combat import DimensionalCombat, DimensionalLayer, Position
from src.combat_system.dimensional_abilities import (
    DimensionalAbilityManager,
    DimensionalAbilityType,
    DimensionalAbility
)

class TestDimensionalAbilities(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.combat_system = DimensionalCombat()
        self.ability_manager = DimensionalAbilityManager(self.combat_system)
        
    def test_ability_initialization(self):
        """Test that base abilities are properly initialized"""
        # Check Dimensional Shift
        ability = self.ability_manager.abilities.get("Dimensional Shift")
        self.assertIsNotNone(ability)
        self.assertEqual(ability.dimensional_type, DimensionalAbilityType.SHIFT)
        self.assertEqual(ability.source_dimension, DimensionalLayer.PHYSICAL)
        
        # Check Void Strike
        ability = self.ability_manager.abilities.get("Void Strike")
        self.assertIsNotNone(ability)
        self.assertEqual(ability.dimensional_type, DimensionalAbilityType.DISRUPTION)
        self.assertEqual(ability.source_dimension, DimensionalLayer.VOID)
        
    def test_ability_requirements(self):
        """Test ability requirement checks"""
        # Test correct dimension
        can_use, reason = self.ability_manager.can_use_ability(
            "Dimensional Shift",
            DimensionalLayer.PHYSICAL
        )
        self.assertTrue(can_use)
        
        # Test wrong dimension
        can_use, reason = self.ability_manager.can_use_ability(
            "Dimensional Shift",
            DimensionalLayer.VOID
        )
        self.assertFalse(can_use)
        
        # Test stability requirement
        self.combat_system.update_dimensional_stability(
            DimensionalLayer.PHYSICAL,
            -0.8  # Reduce stability below requirement
        )
        can_use, reason = self.ability_manager.can_use_ability(
            "Dimensional Shift",
            DimensionalLayer.PHYSICAL
        )
        self.assertFalse(can_use)
        
    def test_ability_cooldowns(self):
        """Test ability cooldown system"""
        # Use ability
        position = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        success, _, _ = self.ability_manager.use_ability("Dimensional Shift", position)
        self.assertTrue(success)
        
        # Check cooldown
        can_use, reason = self.ability_manager.can_use_ability(
            "Dimensional Shift",
            DimensionalLayer.PHYSICAL
        )
        self.assertFalse(can_use)
        
        # Update cooldowns
        self.ability_manager.update_cooldowns(10.0)  # Full cooldown duration
        can_use, reason = self.ability_manager.can_use_ability(
            "Dimensional Shift",
            DimensionalLayer.PHYSICAL
        )
        self.assertTrue(can_use)
        
    def test_ability_effects(self):
        """Test ability effect application"""
        position = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        
        # Use Dimensional Shift
        self.ability_manager.use_ability("Dimensional Shift", position)
        
        # Check effect application
        physical_state = self.combat_system.dimensional_states[DimensionalLayer.PHYSICAL]
        self.assertTrue(any(effect.name == "PHASING" for effect in physical_state.active_effects))
        
    def test_cross_dimensional_power(self):
        """Test cross-dimensional power calculations"""
        source_pos = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.VOID.value)
        target_pos = Position(x=1, y=1, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        
        # Use Void Strike
        _, _, power = self.ability_manager.use_ability(
            "Void Strike",
            source_pos,
            target_pos
        )
        
        # Base power should be modified by dimensional effects
        self.assertNotEqual(power, self.ability_manager.abilities["Void Strike"].base_value)
        
    def test_ability_availability(self):
        """Test ability availability in different dimensions"""
        # Check Physical dimension abilities
        abilities = self.ability_manager.get_available_abilities(DimensionalLayer.PHYSICAL)
        self.assertTrue(any(a.name == "Dimensional Shift" for a in abilities))
        self.assertFalse(any(a.name == "Void Strike" for a in abilities))
        
        # Check Void dimension abilities
        abilities = self.ability_manager.get_available_abilities(DimensionalLayer.VOID)
        self.assertTrue(any(a.name == "Void Strike" for a in abilities))
        self.assertFalse(any(a.name == "Dimensional Shift" for a in abilities))
        
    def test_ability_costs(self):
        """Test ability cost application"""
        position = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        
        # Record initial stability
        initial_stability = self.combat_system.dimensional_states[DimensionalLayer.ETHEREAL].stability
        
        # Use ability
        self.ability_manager.use_ability("Dimensional Shift", position)
        
        # Check stability cost
        final_stability = self.combat_system.dimensional_states[DimensionalLayer.ETHEREAL].stability
        self.assertLess(final_stability, initial_stability)
        
    def test_dimension_compatibility(self):
        """Test dimension compatibility calculations"""
        # Test same dimension
        compatibility = self.ability_manager.get_dimension_compatibility(
            DimensionalLayer.PHYSICAL,
            DimensionalLayer.PHYSICAL
        )
        self.assertEqual(compatibility, 1.0)
        
        # Test connected dimensions
        compatibility = self.ability_manager.get_dimension_compatibility(
            DimensionalLayer.PHYSICAL,
            DimensionalLayer.ETHEREAL
        )
        self.assertGreater(compatibility, 0.0)
        
        # Test non-connected dimensions
        compatibility = self.ability_manager.get_dimension_compatibility(
            DimensionalLayer.PHYSICAL,
            DimensionalLayer.VOID
        )
        self.assertEqual(compatibility, 0.0)
        
    def test_ability_status(self):
        """Test ability status reporting"""
        status = self.ability_manager.get_ability_status("Dimensional Shift")
        
        self.assertIn('name', status)
        self.assertIn('type', status)
        self.assertIn('cooldowns', status)
        self.assertIn('stability_requirements', status)
        self.assertIn('effects', status)
        self.assertIn('target_dimensions', status)

if __name__ == '__main__':
    unittest.main() 