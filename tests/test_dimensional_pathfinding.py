import unittest
from src.combat_system.dimensional_combat import (
    DimensionalCombat,
    DimensionalLayer,
    DimensionalEffect,
    Position
)
from src.world.dimensional_pathfinding import DimensionalPathfinder

class TestDimensionalPathfinding(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.combat_system = DimensionalCombat()
        self.pathfinder = DimensionalPathfinder(self.combat_system)
        
    def test_same_dimension_path(self):
        """Test pathfinding within the same dimension"""
        start = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        goal = Position(x=3, y=4, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        
        path = self.pathfinder.find_path(start, goal)
        
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 8)  # Should take 7 steps to reach goal
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)
        
        # Verify all steps are in physical dimension
        for pos in path:
            self.assertEqual(
                pos.dimensional_layer,
                DimensionalLayer.PHYSICAL.value
            )
            
    def test_cross_dimension_path(self):
        """Test pathfinding across connected dimensions"""
        start = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        goal = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.ETHEREAL.value)
        
        path = self.pathfinder.find_path(start, goal)
        
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 2)  # Direct dimensional shift
        self.assertEqual(path[0].dimensional_layer, DimensionalLayer.PHYSICAL.value)
        self.assertEqual(path[1].dimensional_layer, DimensionalLayer.ETHEREAL.value)
        
    def test_dimensional_shift_limit(self):
        """Test maximum dimensional shift limit"""
        start = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        goal = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.VOID.value)
        
        # Test with default limit (3 shifts)
        path = self.pathfinder.find_path(start, goal)
        self.assertIsNotNone(path)
        
        # Count dimensional shifts
        shifts = sum(
            1 for i in range(len(path)-1)
            if path[i].dimensional_layer != path[i+1].dimensional_layer
        )
        self.assertLessEqual(shifts, 3)
        
        # Test with lower limit
        path = self.pathfinder.find_path(start, goal, max_dimensional_shifts=1)
        self.assertIsNone(path)  # Should not find path with only 1 shift
        
    def test_stability_effects(self):
        """Test pathfinding with stability effects"""
        start = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        goal = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.ETHEREAL.value)
        
        # Test with high stability
        path = self.pathfinder.find_path(start, goal)
        self.assertIsNotNone(path)
        
        # Reduce stability below threshold
        self.combat_system.update_dimensional_stability(
            DimensionalLayer.ETHEREAL,
            -0.9  # Reduces to 0.1, below 0.2 threshold
        )
        
        path = self.pathfinder.find_path(start, goal)
        self.assertIsNone(path)  # Should not find path with low stability
        
    def test_dimensional_effects(self):
        """Test pathfinding with dimensional effects"""
        start = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        goal = Position(x=3, y=4, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        
        # Get normal path first
        normal_path = self.pathfinder.find_path(start, goal)
        
        # Add warping effect
        self.combat_system.add_dimensional_effect(
            DimensionalLayer.PHYSICAL,
            DimensionalEffect.WARPING
        )
        
        warped_path = self.pathfinder.find_path(start, goal)
        
        # Warped path should be different (likely longer due to cost increase)
        self.assertNotEqual(len(normal_path), len(warped_path))
        
    def test_anchoring_effect(self):
        """Test pathfinding with anchoring effect"""
        start = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        goal = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.ETHEREAL.value)
        
        # Test normal path first
        path = self.pathfinder.find_path(start, goal)
        self.assertIsNotNone(path)
        
        # Add anchoring effect
        self.combat_system.add_dimensional_effect(
            DimensionalLayer.PHYSICAL,
            DimensionalEffect.ANCHORING
        )
        
        # Should not find path with anchoring
        path = self.pathfinder.find_path(start, goal)
        self.assertIsNone(path)
        
    def test_cost_calculations(self):
        """Test movement cost calculations"""
        start = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        physical_goal = Position(x=1, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        void_goal = Position(x=1, y=0, z=0, dimensional_layer=DimensionalLayer.VOID.value)
        
        # Calculate costs
        physical_cost = self.pathfinder._calculate_movement_cost(start, physical_goal)
        void_cost = self.pathfinder._calculate_movement_cost(start, void_goal)
        
        # Void movement should be more expensive
        self.assertGreater(void_cost, physical_cost)
        
    def test_unreachable_goal(self):
        """Test pathfinding to unreachable goal"""
        start = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        
        # Create unreachable goal by adding anchoring to all dimensions
        for layer in DimensionalLayer:
            self.combat_system.add_dimensional_effect(
                layer,
                DimensionalEffect.ANCHORING
            )
            
        goal = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.VOID.value)
        
        path = self.pathfinder.find_path(start, goal)
        self.assertIsNone(path)
        
    def test_optimal_path(self):
        """Test that pathfinder finds optimal path"""
        start = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        goal = Position(x=2, y=2, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        
        path = self.pathfinder.find_path(start, goal)
        
        # Optimal path should be 4 steps (diagonal movement)
        self.assertEqual(len(path), 5)
        
        # Verify path length matches expected distance
        total_distance = 0
        for i in range(len(path)-1):
            dx = path[i+1].x - path[i].x
            dy = path[i+1].y - path[i].y
            dz = path[i+1].z - path[i].z
            step_distance = (dx*dx + dy*dy + dz*dz) ** 0.5
            total_distance += step_distance
            
        expected_distance = 2 * 2**0.5  # Diagonal distance
        self.assertAlmostEqual(total_distance, expected_distance, places=2)

if __name__ == '__main__':
    unittest.main() 