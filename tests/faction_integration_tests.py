import unittest
import time
import random
from typing import Dict, List, Any
from dataclasses import dataclass

from testing_framework import GameSystemTest
from profiling_tools import SystemProfiler
from faction_system import FactionSystem, Faction, FactionRelation, ReputationLevel
from combat_system import CombatSystem, CombatEntity
from economic_system import EconomicSystem, ResourceType, TradeRoute
from dynamic_events_system import (
    DynamicEventsSystem,
    EventCategory,
    EventSeverity,
    WorldStateMetric
)

class FactionIntegrationTest(GameSystemTest):
    """Integration tests for faction system interactions"""
    
    def setUp(self):
        super().setUp()
        self.profiler = SystemProfiler()
        self.faction_system = FactionSystem()
        self.combat_system = CombatSystem()
        self.economy = EconomicSystem()
        self.events = DynamicEventsSystem(None, self.economy)  # Weather not needed for these tests
        
        # Set up test factions
        self.kingdom = self.faction_system.create_faction(
            "Kingdom",
            power_level=0.7,
            resource_focus=[ResourceType.FOOD, ResourceType.IRON]
        )
        self.empire = self.faction_system.create_faction(
            "Empire",
            power_level=0.8,
            resource_focus=[ResourceType.GOLD, ResourceType.STEEL]
        )
        self.merchant_guild = self.faction_system.create_faction(
            "Merchant Guild",
            power_level=0.5,
            resource_focus=[ResourceType.GOLD, ResourceType.GEMS]
        )
        
    def test_faction_economic_integration(self):
        """Test faction influence on economic system"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create markets for each faction
        kingdom_market = self.economy.create_market("kingdom_capital")
        empire_market = self.economy.create_market("empire_capital")
        
        # Set up trade route between factions
        trade_route = self.economy.create_trade_route(
            "kingdom_capital",
            "empire_capital",
            [ResourceType.FOOD, ResourceType.IRON],
            distance=100
        )
        
        # Track initial prices
        initial_prices = {
            "kingdom": {
                item.resource_type: item.current_price
                for item in kingdom_market.items
            },
            "empire": {
                item.resource_type: item.current_price
                for item in empire_market.items
            }
        }
        
        # Simulate faction relation change
        self.faction_system.modify_relation(
            self.kingdom,
            self.empire,
            -0.3  # Significant decrease
        )
        
        # Update systems
        self.economy.update(1.0)
        
        # Check price changes
        current_prices = {
            "kingdom": {
                item.resource_type: item.current_price
                for item in kingdom_market.items
            },
            "empire": {
                item.resource_type: item.current_price
                for item in empire_market.items
            }
        }
        
        # Verify trade disruption affected prices
        self.assertGreater(
            current_prices["kingdom"][ResourceType.IRON],
            initial_prices["kingdom"][ResourceType.IRON]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_economic_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_faction_combat_integration(self):
        """Test faction influence on combat system"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create combat entities from different factions
        kingdom_soldier = CombatEntity(
            entity_id="kingdom_soldier",
            name="Kingdom Soldier",
            level=20,
            faction=self.kingdom.name
        )
        empire_soldier = CombatEntity(
            entity_id="empire_soldier",
            name="Empire Soldier",
            level=20,
            faction=self.empire.name
        )
        
        # Track initial relations
        initial_relation = self.faction_system.get_relation(
            self.kingdom,
            self.empire
        )
        
        # Simulate combat between factions
        self.combat_system.process_entity_defeat(
            empire_soldier,
            kingdom_soldier,
            location="border_region"
        )
        
        # Update faction relations
        self.faction_system.process_combat_outcome(
            victor_faction=self.kingdom.name,
            defeated_faction=self.empire.name,
            location="border_region"
        )
        
        # Verify relation changes
        current_relation = self.faction_system.get_relation(
            self.kingdom,
            self.empire
        )
        
        self.assertLess(
            current_relation.value,
            initial_relation.value
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_combat_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_faction_event_integration(self):
        """Test faction influence on event generation"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Set up faction conflict
        self.faction_system.modify_relation(
            self.kingdom,
            self.empire,
            -0.5  # Major decrease
        )
        
        # Track initial events
        initial_events = len(self.events.active_events)
        
        # Update systems
        self.events.update(1.0)
        
        # Verify new events were generated
        faction_events = [
            event for event in self.events.active_events.values()
            if event.category == EventCategory.POLITICAL
            and any(faction in event.description 
                   for faction in [self.kingdom.name, self.empire.name])
        ]
        
        self.assertTrue(len(faction_events) > 0)
        
        # Check world state impact
        self.assertLess(
            self.events.world_state.metrics[WorldStateMetric.STABILITY],
            0.8  # Stability should decrease
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics(self.events)
        
        self.record_result(TestResult(
            test_name="faction_event_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_reputation_system_integration(self):
        """Test player reputation effects across systems"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Set up player reputation
        player_reputation = {
            self.kingdom.name: ReputationLevel.FRIENDLY,
            self.empire.name: ReputationLevel.NEUTRAL,
            self.merchant_guild.name: ReputationLevel.HONORED
        }
        
        # Create markets
        kingdom_market = self.economy.create_market("kingdom_market")
        guild_market = self.economy.create_market("guild_market")
        
        # Apply reputation modifiers
        kingdom_prices = self.economy.get_prices_with_reputation(
            kingdom_market,
            player_reputation[self.kingdom.name]
        )
        guild_prices = self.economy.get_prices_with_reputation(
            guild_market,
            player_reputation[self.merchant_guild.name]
        )
        
        # Verify reputation affects prices
        self.assertLess(
            guild_prices[ResourceType.GEMS],
            kingdom_prices[ResourceType.GEMS]
        )
        
        # Test reputation impact on quest rewards
        quest = self.events._create_combat_quest(
            self.events._generate_monster_attack()
        )
        
        modified_rewards = self.faction_system.modify_quest_rewards(
            quest.rewards,
            player_reputation[self.kingdom.name],
            self.kingdom.name
        )
        
        self.assertGreater(
            modified_rewards["gold"],
            quest.rewards["gold"]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="reputation_system_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_faction_resource_control(self):
        """Test faction control over resources and markets"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Set up resource control
        self.faction_system.set_resource_control(
            self.kingdom,
            {
                ResourceType.IRON: 0.8,  # Strong control
                ResourceType.FOOD: 0.6
            }
        )
        
        self.faction_system.set_resource_control(
            self.merchant_guild,
            {
                ResourceType.GEMS: 0.9,
                ResourceType.GOLD: 0.7
            }
        )
        
        # Create markets
        kingdom_market = self.economy.create_market("kingdom_resource_market")
        guild_market = self.economy.create_market("guild_resource_market")
        
        # Track initial prices
        initial_prices = {
            "kingdom": {
                item.resource_type: item.current_price
                for item in kingdom_market.items
            },
            "guild": {
                item.resource_type: item.current_price
                for item in guild_market.items
            }
        }
        
        # Simulate resource control change
        self.faction_system.modify_resource_control(
            self.kingdom,
            ResourceType.IRON,
            -0.3  # Significant decrease
        )
        
        # Update economy
        self.economy.update(1.0)
        
        # Check price changes
        current_prices = {
            "kingdom": {
                item.resource_type: item.current_price
                for item in kingdom_market.items
            },
            "guild": {
                item.resource_type: item.current_price
                for item in guild_market.items
            }
        }
        
        # Verify resource control affects prices
        self.assertGreater(
            current_prices["kingdom"][ResourceType.IRON],
            initial_prices["kingdom"][ResourceType.IRON]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="faction_resource_control",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))

def run_faction_integration_tests():
    """Run all faction integration tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(FactionIntegrationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Export results
    test_instance = FactionIntegrationTest()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_instance.export_results(f"faction_integration_results_{timestamp}.json")
    
    return result

if __name__ == "__main__":
    run_faction_integration_tests() 