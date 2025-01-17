import unittest
import time
import random
from typing import List, Dict, Any
from dataclasses import dataclass

from testing_framework import GameSystemTest
from profiling_tools import SystemProfiler, FunctionProfiler
from combat_ai import CombatAI, AIBehaviorType, CombatRole
from combat_system import CombatSystem, CombatEntity, Ability, StatusEffect

@dataclass
class CombatBenchmarkMetrics:
    ai_decision_time: float
    ability_processing_time: float
    status_update_time: float
    total_memory_used: float
    entities_processed: int
    abilities_used: int
    total_time: float

class CombatBenchmarkTest(GameSystemTest):
    """Performance benchmark tests for combat system"""
    
    def setUp(self):
        super().setUp()
        self.profiler = SystemProfiler()
        self.combat_system = CombatSystem()
        self.combat_ai = CombatAI()
        
    def _create_test_entities(self, count: int) -> List[CombatEntity]:
        """Create test combat entities"""
        entities = []
        roles = list(CombatRole)
        behaviors = list(AIBehaviorType)
        
        for i in range(count):
            entity = CombatEntity(
                entity_id=f"test_entity_{i}",
                name=f"Test Entity {i}",
                level=random.randint(1, 50),
                health=100,
                energy=100,
                combat_role=random.choice(roles),
                behavior_type=random.choice(behaviors),
                abilities=[
                    Ability(f"ability_{j}", "Test Ability", 10, 20)
                    for j in range(random.randint(3, 6))
                ]
            )
            entities.append(entity)
            
        return entities
        
    def test_ai_decision_making(self):
        """Benchmark AI decision making performance"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create test scenario
        allies = self._create_test_entities(5)
        enemies = self._create_test_entities(5)
        decision_times = []
        
        # Run multiple AI decisions
        for entity in allies:
            for _ in range(100):  # 100 decisions per entity
                decision_start = time.time()
                
                action = self.combat_ai.decide_action(
                    entity,
                    allies,
                    enemies,
                    random.random()  # Random threat level
                )
                
                decision_times.append(time.time() - decision_start)
                
        end_time = time.time()
        self.profiler.stop_profiling()
        
        # Calculate metrics
        metrics = CombatBenchmarkMetrics(
            ai_decision_time=sum(decision_times) / len(decision_times),
            ability_processing_time=0.0,  # Not measured in this test
            status_update_time=0.0,  # Not measured in this test
            total_memory_used=self.profiler.current_metrics.memory_usage,
            entities_processed=len(allies) + len(enemies),
            abilities_used=0,
            total_time=end_time - start_time
        )
        
        # Performance assertions
        self.assertLess(metrics.ai_decision_time, 0.001)  # Under 1ms per decision
        self.assertLess(metrics.total_memory_used, 85.0)  # Under 85% memory usage
        
        self.record_result(TestResult(
            test_name="ai_decision_making",
            status="PASS",
            execution_time=metrics.total_time,
            system_metrics={
                "performance": vars(metrics),
                "profiler_data": self.profiler.get_performance_report()
            }
        ))
        
    def test_combat_processing(self):
        """Benchmark combat action processing performance"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create large combat scenario
        team_a = self._create_test_entities(10)
        team_b = self._create_test_entities(10)
        processing_times = []
        ability_count = 0
        
        # Process multiple combat rounds
        for _ in range(50):  # 50 combat rounds
            round_start = time.time()
            
            # Process actions for all entities
            for entity in team_a + team_b:
                if entity.energy >= 20:  # Ensure enough energy
                    ability = random.choice(entity.abilities)
                    targets = random.sample(
                        team_b if entity in team_a else team_a,
                        min(3, len(team_b))
                    )
                    
                    self.combat_system.process_ability(
                        entity,
                        ability,
                        targets
                    )
                    ability_count += 1
                    
            processing_times.append(time.time() - round_start)
            
        end_time = time.time()
        self.profiler.stop_profiling()
        
        # Calculate metrics
        metrics = CombatBenchmarkMetrics(
            ai_decision_time=0.0,  # Not measured in this test
            ability_processing_time=sum(processing_times) / len(processing_times),
            status_update_time=0.0,  # Not measured in this test
            total_memory_used=self.profiler.current_metrics.memory_usage,
            entities_processed=len(team_a) + len(team_b),
            abilities_used=ability_count,
            total_time=end_time - start_time
        )
        
        # Performance assertions
        self.assertLess(metrics.ability_processing_time, 0.02)  # Under 20ms per round
        self.assertLess(metrics.total_memory_used, 85.0)
        
        self.record_result(TestResult(
            test_name="combat_processing",
            status="PASS",
            execution_time=metrics.total_time,
            system_metrics={
                "performance": vars(metrics),
                "profiler_data": self.profiler.get_performance_report()
            }
        ))
        
    def test_status_effect_processing(self):
        """Benchmark status effect processing performance"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create entities with status effects
        entities = self._create_test_entities(20)
        status_times = []
        
        # Add random status effects
        effects = [
            StatusEffect("burning", "DOT", 5, 3),
            StatusEffect("poisoned", "DOT", 3, 5),
            StatusEffect("blessed", "HOT", 5, 3),
            StatusEffect("cursed", "Debuff", -2, 4),
            StatusEffect("strengthened", "Buff", 2, 3)
        ]
        
        for entity in entities:
            entity.status_effects.extend(
                random.sample(effects, random.randint(1, 3))
            )
            
        # Process status effects over time
        for _ in range(100):  # 100 update cycles
            update_start = time.time()
            
            for entity in entities:
                self.combat_system.process_status_effects(entity)
                
            status_times.append(time.time() - update_start)
            
        end_time = time.time()
        self.profiler.stop_profiling()
        
        # Calculate metrics
        metrics = CombatBenchmarkMetrics(
            ai_decision_time=0.0,  # Not measured in this test
            ability_processing_time=0.0,  # Not measured in this test
            status_update_time=sum(status_times) / len(status_times),
            total_memory_used=self.profiler.current_metrics.memory_usage,
            entities_processed=len(entities),
            abilities_used=0,
            total_time=end_time - start_time
        )
        
        # Performance assertions
        self.assertLess(metrics.status_update_time, 0.005)  # Under 5ms per update
        self.assertLess(metrics.total_memory_used, 85.0)
        
        self.record_result(TestResult(
            test_name="status_effect_processing",
            status="PASS",
            execution_time=metrics.total_time,
            system_metrics={
                "performance": vars(metrics),
                "profiler_data": self.profiler.get_performance_report()
            }
        ))
        
    def test_large_scale_combat(self):
        """Benchmark large-scale combat performance"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create large battle scenario
        team_a = self._create_test_entities(50)
        team_b = self._create_test_entities(50)
        
        combat_metrics = {
            "ai_decisions": [],
            "ability_processing": [],
            "status_updates": []
        }
        
        ability_count = 0
        
        # Run large-scale combat simulation
        for _ in range(20):  # 20 combat rounds
            # AI decisions
            ai_start = time.time()
            for entity in team_a + team_b:
                self.combat_ai.decide_action(
                    entity,
                    team_a if entity in team_a else team_b,
                    team_b if entity in team_a else team_a,
                    random.random()
                )
            combat_metrics["ai_decisions"].append(time.time() - ai_start)
            
            # Ability processing
            ability_start = time.time()
            for entity in team_a + team_b:
                if entity.energy >= 20:
                    ability = random.choice(entity.abilities)
                    targets = random.sample(
                        team_b if entity in team_a else team_a,
                        min(3, len(team_b))
                    )
                    self.combat_system.process_ability(entity, ability, targets)
                    ability_count += 1
            combat_metrics["ability_processing"].append(time.time() - ability_start)
            
            # Status effect processing
            status_start = time.time()
            for entity in team_a + team_b:
                self.combat_system.process_status_effects(entity)
            combat_metrics["status_updates"].append(time.time() - status_start)
            
        end_time = time.time()
        self.profiler.stop_profiling()
        
        # Calculate metrics
        metrics = CombatBenchmarkMetrics(
            ai_decision_time=sum(combat_metrics["ai_decisions"]) / len(combat_metrics["ai_decisions"]),
            ability_processing_time=sum(combat_metrics["ability_processing"]) / len(combat_metrics["ability_processing"]),
            status_update_time=sum(combat_metrics["status_updates"]) / len(combat_metrics["status_updates"]),
            total_memory_used=self.profiler.current_metrics.memory_usage,
            entities_processed=len(team_a) + len(team_b),
            abilities_used=ability_count,
            total_time=end_time - start_time
        )
        
        # Performance assertions
        self.assertLess(metrics.ai_decision_time, 0.05)  # Under 50ms for AI
        self.assertLess(metrics.ability_processing_time, 0.1)  # Under 100ms for abilities
        self.assertLess(metrics.status_update_time, 0.02)  # Under 20ms for status
        self.assertLess(metrics.total_memory_used, 90.0)
        
        self.record_result(TestResult(
            test_name="large_scale_combat",
            status="PASS",
            execution_time=metrics.total_time,
            system_metrics={
                "performance": vars(metrics),
                "profiler_data": self.profiler.get_performance_report(),
                "combat_metrics": combat_metrics
            }
        ))

def run_combat_benchmarks():
    """Run all combat performance benchmarks"""
    suite = unittest.TestLoader().loadTestsFromTestCase(CombatBenchmarkTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Export results
    test_instance = CombatBenchmarkTest()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_instance.export_results(f"combat_benchmark_results_{timestamp}.json")
    
    return result

if __name__ == "__main__":
    run_combat_benchmarks() 