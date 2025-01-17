import unittest
import time
import random
from typing import Dict, Any
from dataclasses import dataclass

from testing_framework import GameSystemTest
from profiling_tools import SystemProfiler
from combat_system import CombatSystem, CombatEntity, Ability, StatusEffect
from combat_ai import CombatAI, AIBehaviorType, CombatRole
from weather_system import WeatherSystem, WeatherType
from economic_system import EconomicSystem, ResourceType
from dynamic_events_system import (
    DynamicEventsSystem,
    EventCategory,
    EventSeverity,
    WorldStateMetric
)

class CombatIntegrationTest(GameSystemTest):
    """Integration tests between combat and other systems"""
    
    def setUp(self):
        super().setUp()
        self.profiler = SystemProfiler()
        self.combat_system = CombatSystem()
        self.combat_ai = CombatAI()
        self.weather = WeatherSystem()
        self.economy = EconomicSystem()
        self.events = DynamicEventsSystem(self.weather, self.economy)
        
    def _create_test_entity(self, is_player: bool = False) -> CombatEntity:
        """Create a test combat entity"""
        return CombatEntity(
            entity_id=f"player" if is_player else f"enemy_{random.randint(1,1000)}",
            name="Test Player" if is_player else "Test Enemy",
            level=random.randint(1, 50),
            health=100,
            energy=100,
            combat_role=random.choice(list(CombatRole)),
            behavior_type=AIBehaviorType.TACTICAL if is_player else random.choice(list(AIBehaviorType)),
            abilities=[
                Ability(f"ability_{i}", f"Test Ability {i}", 10, 20)
                for i in range(4)
            ]
        )
        
    def test_weather_combat_integration(self):
        """Test weather effects on combat performance"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create combat entities
        player = self._create_test_entity(is_player=True)
        enemy = self._create_test_entity()
        
        # Test combat in different weather conditions
        weather_impacts = {}
        
        for weather_type in [WeatherType.CLEAR, WeatherType.STORM, WeatherType.BLIZZARD]:
            # Set weather
            self.weather.current_weather.weather_type = weather_type
            self.weather.current_weather.intensity = 0.8
            self.weather.update(1.0)
            
            # Get weather modifiers
            modifiers = self.weather.get_combat_modifiers()
            
            # Test combat with weather effects
            ability = player.abilities[0]
            base_damage = ability.base_damage
            
            # Apply weather modifiers
            actual_damage = self.combat_system.calculate_damage(
                player, enemy, ability, modifiers
            )
            
            weather_impacts[weather_type] = {
                "base_damage": base_damage,
                "actual_damage": actual_damage,
                "modifiers": modifiers
            }
            
        # Verify weather affects combat
        self.assertNotEqual(
            weather_impacts[WeatherType.CLEAR]["actual_damage"],
            weather_impacts[WeatherType.BLIZZARD]["actual_damage"]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="weather_combat_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics={
                "weather_impacts": weather_impacts,
                "profiler_data": self.profiler.get_performance_report()
            }
        ))
        
    def test_combat_economic_integration(self):
        """Test combat outcomes affecting economy"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create market and track initial prices
        market = self.economy.create_market("combat_zone")
        initial_prices = {
            item.resource_type: item.current_price
            for item in market.items
        }
        
        # Simulate large battle affecting local economy
        battle_entities = [self._create_test_entity() for _ in range(20)]
        
        # Process combat with resource damage
        for entity in battle_entities:
            self.combat_system.apply_area_damage(
                entity,
                damage=30,
                resource_damage={
                    ResourceType.FOOD: 0.1,
                    ResourceType.WOOD: 0.1
                }
            )
            
        # Update economy
        self.economy.update(1.0)
        
        # Check price changes
        current_prices = {
            item.resource_type: item.current_price
            for item in market.items
        }
        
        # Verify resource damage affected prices
        self.assertGreater(
            current_prices[ResourceType.FOOD],
            initial_prices[ResourceType.FOOD]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="combat_economic_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_combat_event_integration(self):
        """Test combat triggering dynamic events"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create combat scenario
        player = self._create_test_entity(is_player=True)
        boss = self._create_test_entity()
        boss.level = 50  # High-level boss
        
        # Track initial events
        initial_events = len(self.events.active_events)
        
        # Simulate boss defeat
        self.combat_system.process_entity_defeat(
            boss,
            player,
            was_boss=True,
            location="dragon_lair"
        )
        
        # Update events system
        self.events.update(1.0)
        
        # Verify new events were generated
        new_events = [
            event for event in self.events.active_events.values()
            if event.category in [EventCategory.MILITARY, EventCategory.SUPERNATURAL]
            and event.start_time > start_time
        ]
        
        self.assertTrue(len(new_events) > 0)
        
        # Check world state changes
        self.assertGreater(
            self.events.world_state.metrics[WorldStateMetric.STABILITY],
            0.6  # Stability should increase after boss defeat
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics(self.events)
        
        self.record_result(TestResult(
            test_name="combat_event_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_full_combat_integration(self):
        """Test full integration of combat with all systems"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Set up initial conditions
        self.weather.current_weather.weather_type = WeatherType.STORM
        self.weather.current_weather.intensity = 0.7
        
        market = self.economy.create_market("battlefield")
        player = self._create_test_entity(is_player=True)
        enemies = [self._create_test_entity() for _ in range(5)]
        
        # Track initial state
        initial_state = {
            "events": len(self.events.active_events),
            "quests": len(self.events.active_quests),
            "prices": {
                item.resource_type: item.current_price
                for item in market.items
            },
            "world_metrics": self.events.world_state.metrics.copy()
        }
        
        # Run multiple combat rounds with system updates
        for _ in range(10):
            # Update weather and get modifiers
            self.weather.update(0.1)
            weather_mods = self.weather.get_combat_modifiers()
            
            # Process combat
            for enemy in enemies:
                if enemy.health > 0:
                    ability = random.choice(player.abilities)
                    damage = self.combat_system.calculate_damage(
                        player, enemy, ability, weather_mods
                    )
                    self.combat_system.apply_damage(enemy, damage)
                    
                    # Check for defeats
                    if enemy.health <= 0:
                        self.combat_system.process_entity_defeat(
                            enemy, player, location="battlefield"
                        )
                        
            # Update other systems
            self.economy.update(0.1)
            self.events.update(0.1)
            
        # Get final state
        final_state = {
            "events": len(self.events.active_events),
            "quests": len(self.events.active_quests),
            "prices": {
                item.resource_type: item.current_price
                for item in market.items
            },
            "world_metrics": self.events.world_state.metrics.copy()
        }
        
        # Verify system interactions
        self.assertNotEqual(
            initial_state["events"],
            final_state["events"]
        )
        self.assertNotEqual(
            initial_state["prices"],
            final_state["prices"]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics(self.events)
        
        self.record_result(TestResult(
            test_name="full_combat_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics={
                "initial_state": initial_state,
                "final_state": final_state,
                "profiler_data": self.profiler.get_performance_report()
            }
        ))
        
    def test_combat_quest_integration(self):
        """Test combat completion affecting quests"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create combat-related event
        monster_event = self.events._generate_monster_attack()
        self.events.active_events[monster_event.event_id] = monster_event
        
        # Generate associated quest
        quest = self.events._create_combat_quest(monster_event)
        self.events.active_quests[quest.quest_id] = quest
        
        # Create combat entities
        player = self._create_test_entity(is_player=True)
        monster = self._create_test_entity()
        monster.level = 30  # High-level monster
        
        # Track initial quest state
        initial_quest_state = quest.state
        
        # Simulate monster defeat
        self.combat_system.process_entity_defeat(
            monster,
            player,
            quest_id=quest.quest_id,
            location=monster_event.location
        )
        
        # Update events system
        self.events.update(1.0)
        
        # Verify quest progress
        self.assertNotEqual(
            quest.state,
            initial_quest_state
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics(self.events)
        
        self.record_result(TestResult(
            test_name="combat_quest_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))

def run_combat_integration_tests():
    """Run all combat integration tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(CombatIntegrationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Export results
    test_instance = CombatIntegrationTest()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_instance.export_results(f"combat_integration_results_{timestamp}.json")
    
    return result

if __name__ == "__main__":
    run_combat_integration_tests() 