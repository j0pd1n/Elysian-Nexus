import unittest
import time
from typing import Dict, Set, List
from src.infrastructure.test_framework import TestDecorators, TestType, TestPriority
from src.infrastructure.performance_monitor import MetricType
from src.combat_system.dimensional_combat import Position, DimensionalLayer
from src.ai.tactical_ai import TacticalAI, TacticalDecision, CombatRole
from src.ai.pathfinding import DimensionalPathfinder

class TestAIMechanics(unittest.TestCase):
    """Test cases for AI mechanics and pathfinding"""
    
    def setUp(self):
        """Set up test environment"""
        self.tactical_ai = TacticalAI()
        self.pathfinder = DimensionalPathfinder()
        self.test_positions = {
            "start": Position(0, 0, 0),
            "enemy": Position(10, 10, 0),
            "cover": Position(5, 5, 0),
            "dimension_rift": Position(7, 7, 0)
        }
        
    @TestDecorators.test_type(TestType.UNIT)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_tactical_decision_making(self):
        """Test AI tactical decision making"""
        decision = self.tactical_ai.evaluate_combat_situation(
            position=self.test_positions["start"],
            enemy_position=self.test_positions["enemy"],
            current_health=70,
            available_abilities=["void_strike", "dimensional_anchor"],
            combat_role=CombatRole.ASSAULT
        )
        
        self.assertIsInstance(decision, TacticalDecision)
        self.assertTrue(decision.should_engage or decision.should_reposition)
        
    @TestDecorators.test_type(TestType.INTEGRATION)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_dimensional_awareness(self):
        """Test AI awareness of dimensional opportunities"""
        opportunities = self.tactical_ai.analyze_dimensional_opportunities(
            current_position=self.test_positions["start"],
            current_dimension="Physical",
            available_dimensions=["Ethereal", "Void"],
            enemy_position=self.test_positions["enemy"]
        )
        
        self.assertGreater(len(opportunities), 0)
        self.assertTrue(any(opp.advantage_score > 0 for opp in opportunities))
        
    @TestDecorators.test_type(TestType.PERFORMANCE)
    @TestDecorators.test_priority(TestPriority.HIGH)
    @TestDecorators.performance_threshold(MetricType.PATHFINDING, 5.0)
    def test_pathfinding_performance(self):
        """Test pathfinding performance across dimensions"""
        start_time = time.time()
        
        path = self.pathfinder.find_path(
            start=self.test_positions["start"],
            end=self.test_positions["enemy"],
            allowed_dimensions=["Physical", "Ethereal"],
            max_dimensional_shifts=2
        )
        
        duration = (time.time() - start_time) * 1000
        self.assertLess(duration, 5.0)  # Should complete within 5ms
        self.assertIsNotNone(path)
        
    @TestDecorators.test_type(TestType.STRESS)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_multi_agent_pathfinding(self):
        """Test pathfinding with multiple agents"""
        agents = [(Position(x, y, 0), Position(x+10, y+10, 0)) 
                 for x, y in [(0,0), (5,5), (10,10), (15,15), (20,20)]]
        
        start_time = time.time()
        paths = []
        
        for start, end in agents:
            path = self.pathfinder.find_path(
                start=start,
                end=end,
                allowed_dimensions=["Physical", "Ethereal"],
                avoid_positions=[p for p, _ in agents]
            )
            paths.append(path)
            
        duration = (time.time() - start_time) * 1000
        self.assertLess(duration, 20.0)  # Should complete within 20ms
        self.assertTrue(all(path is not None for path in paths))
        
    @TestDecorators.test_type(TestType.UNIT)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_combat_role_behavior(self):
        """Test AI behavior for different combat roles"""
        roles = [CombatRole.ASSAULT, CombatRole.SUPPORT, CombatRole.CONTROL]
        
        for role in roles:
            decision = self.tactical_ai.evaluate_combat_situation(
                position=self.test_positions["start"],
                enemy_position=self.test_positions["enemy"],
                current_health=100,
                available_abilities=["void_strike", "ethereal_blast"],
                combat_role=role
            )
            
            if role == CombatRole.ASSAULT:
                self.assertTrue(decision.should_engage)
            elif role == CombatRole.SUPPORT:
                self.assertTrue(decision.should_maintain_distance)
            elif role == CombatRole.CONTROL:
                self.assertTrue(decision.should_control_space)
                
    @TestDecorators.test_type(TestType.INTEGRATION)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_obstacle_avoidance(self):
        """Test pathfinding with obstacles and dimensional shifts"""
        obstacles = [Position(x, x, 0) for x in range(1, 10)]
        
        path = self.pathfinder.find_path(
            start=self.test_positions["start"],
            end=self.test_positions["enemy"],
            allowed_dimensions=["Physical", "Ethereal"],
            obstacles=obstacles,
            prefer_dimensional_shifts=True
        )
        
        self.assertIsNotNone(path)
        self.assertTrue(any(p.dimension != "Physical" for p in path))
        self.assertTrue(all(p not in obstacles for p in path))

if __name__ == '__main__':
    unittest.main() 