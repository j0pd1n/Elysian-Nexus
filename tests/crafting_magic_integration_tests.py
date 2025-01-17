import unittest
import time
import random
from typing import Dict, List, Any
from dataclasses import dataclass

from testing_framework import GameSystemTest
from profiling_tools import SystemProfiler
from crafting_system import CraftingSystem, Recipe, CraftingStation, Quality
from magic_system import MagicSystem, SpellEffect, MagicSchool, ManaPool
from weather_system import WeatherSystem, WeatherType
from economic_system import EconomicSystem, ResourceType
from dynamic_events_system import (
    DynamicEventsSystem,
    EventCategory,
    WorldStateMetric
)

class CraftingMagicIntegrationTest(GameSystemTest):
    """Integration tests for crafting and magic systems"""
    
    def setUp(self):
        super().setUp()
        self.profiler = SystemProfiler()
        self.crafting = CraftingSystem()
        self.magic = MagicSystem()
        self.weather = WeatherSystem()
        self.economy = EconomicSystem()
        self.events = DynamicEventsSystem(self.weather, self.economy)
        
        # Set up test recipes
        self.potion_recipe = Recipe(
            "healing_potion",
            {
                ResourceType.HERBS: 2,
                ResourceType.WATER: 1,
                ResourceType.MANA_CRYSTAL: 1
            },
            required_skill=5,
            station_type="ALCHEMY"
        )
        
        self.enchanted_weapon_recipe = Recipe(
            "enchanted_sword",
            {
                ResourceType.IRON: 3,
                ResourceType.GEMS: 1,
                ResourceType.MANA_CRYSTAL: 2
            },
            required_skill=10,
            station_type="ENCHANTING"
        )
        
    def test_crafting_economy_integration(self):
        """Test crafting impact on economic system"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create market and track initial prices
        market = self.economy.create_market("crafting_district")
        initial_prices = {
            item.resource_type: item.current_price
            for item in market.items
        }
        
        # Simulate bulk crafting
        for _ in range(20):
            self.crafting.craft_item(
                self.potion_recipe,
                market,
                skill_level=10
            )
            
        # Update economy
        self.economy.update(1.0)
        
        # Check price changes
        current_prices = {
            item.resource_type: item.current_price
            for item in market.items
        }
        
        # Verify resource consumption affected prices
        self.assertGreater(
            current_prices[ResourceType.HERBS],
            initial_prices[ResourceType.HERBS]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="crafting_economy_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_magic_weather_integration(self):
        """Test magic system interaction with weather"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create mage and mana pool
        mage_mana = ManaPool(100, 100, regeneration_rate=5)
        
        # Track weather changes from spells
        weather_changes = {}
        
        for weather_type in [WeatherType.CLEAR, WeatherType.STORM]:
            # Set initial weather
            self.weather.current_weather.weather_type = weather_type
            self.weather.update(1.0)
            
            # Cast weather-affecting spell
            spell_power = self.magic.cast_weather_spell(
                "tempest",
                mage_mana,
                self.weather.current_weather
            )
            
            # Update weather
            self.weather.update(1.0)
            
            weather_changes[weather_type] = {
                "initial_intensity": self.weather.current_weather.intensity,
                "spell_power": spell_power,
                "final_intensity": self.weather.current_weather.intensity
            }
            
        # Verify magic affects weather
        self.assertNotEqual(
            weather_changes[WeatherType.CLEAR]["initial_intensity"],
            weather_changes[WeatherType.CLEAR]["final_intensity"]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="magic_weather_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_enchanting_crafting_integration(self):
        """Test enchanting effects on crafted items"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create enchanting station
        station = CraftingStation("master_enchanter", "ENCHANTING", quality=Quality.MASTERWORK)
        
        # Craft normal and enchanted items
        normal_sword = self.crafting.craft_item(
            Recipe("iron_sword", {ResourceType.IRON: 3}, required_skill=5, station_type="FORGE"),
            skill_level=10
        )
        
        enchanted_sword = self.crafting.craft_item(
            self.enchanted_weapon_recipe,
            skill_level=15,
            station=station
        )
        
        # Apply additional enchantment
        enchantment = self.magic.create_enchantment(
            "frost",
            power=50,
            school=MagicSchool.FROST
        )
        
        enhanced_sword = self.magic.enhance_item(
            enchanted_sword,
            enchantment,
            skill_level=20
        )
        
        # Verify enchantments stack properly
        self.assertGreater(
            enhanced_sword.magic_power,
            enchanted_sword.magic_power
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="enchanting_crafting_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_magic_event_integration(self):
        """Test magical phenomena triggering events"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create powerful spell effect
        ritual = self.magic.create_ritual(
            "summon_storm",
            power=100,
            school=MagicSchool.STORM,
            duration=3600
        )
        
        # Track initial events
        initial_events = len(self.events.active_events)
        
        # Cast ritual
        self.magic.perform_ritual(
            ritual,
            location="ritual_grounds",
            participants=3
        )
        
        # Update systems
        self.weather.update(1.0)
        self.events.update(1.0)
        
        # Verify magical events were generated
        magic_events = [
            event for event in self.events.active_events.values()
            if event.category == EventCategory.SUPERNATURAL
            and "magical" in event.description.lower()
        ]
        
        self.assertTrue(len(magic_events) > 0)
        
        # Check magic saturation
        self.assertGreater(
            self.events.world_state.metrics[WorldStateMetric.MAGIC_SATURATION],
            0.7  # High magic saturation
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics(self.events)
        
        self.record_result(TestResult(
            test_name="magic_event_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_crafting_magic_economy_integration(self):
        """Test combined crafting and magic effects on economy"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create market
        market = self.economy.create_market("magic_district")
        
        # Track magical resource prices
        initial_prices = {
            ResourceType.MANA_CRYSTAL: market.get_price(ResourceType.MANA_CRYSTAL),
            ResourceType.GEMS: market.get_price(ResourceType.GEMS)
        }
        
        # Simulate magical crafting surge
        for _ in range(10):
            # Craft enchanted items
            self.crafting.craft_item(
                self.enchanted_weapon_recipe,
                market,
                skill_level=15
            )
            
            # Cast enhancement spells
            self.magic.cast_enhancement_spell(
                "empower",
                cost=10,
                target_type="WEAPON"
            )
            
        # Update economy
        self.economy.update(1.0)
        
        # Check price changes
        current_prices = {
            ResourceType.MANA_CRYSTAL: market.get_price(ResourceType.MANA_CRYSTAL),
            ResourceType.GEMS: market.get_price(ResourceType.GEMS)
        }
        
        # Verify magical resource prices increased
        self.assertGreater(
            current_prices[ResourceType.MANA_CRYSTAL],
            initial_prices[ResourceType.MANA_CRYSTAL]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="crafting_magic_economy_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_weather_crafting_integration(self):
        """Test weather effects on crafting"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Test crafting in different weather
        crafting_results = {}
        
        for weather_type in [WeatherType.CLEAR, WeatherType.STORM, WeatherType.ARCANE_SURGE]:
            # Set weather
            self.weather.current_weather.weather_type = weather_type
            self.weather.current_weather.intensity = 0.8
            self.weather.update(1.0)
            
            # Get crafting modifiers
            modifiers = self.weather.get_crafting_modifiers()
            
            # Attempt crafting
            result = self.crafting.craft_item(
                self.potion_recipe,
                skill_level=10,
                weather_modifiers=modifiers
            )
            
            crafting_results[weather_type] = {
                "quality": result.quality,
                "modifiers": modifiers
            }
            
        # Verify weather affects crafting
        self.assertNotEqual(
            crafting_results[WeatherType.CLEAR]["quality"],
            crafting_results[WeatherType.ARCANE_SURGE]["quality"]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="weather_crafting_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))

def run_crafting_magic_integration_tests():
    """Run all crafting and magic integration tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(CraftingMagicIntegrationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Export results
    test_instance = CraftingMagicIntegrationTest()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_instance.export_results(f"crafting_magic_integration_results_{timestamp}.json")
    
    return result

if __name__ == "__main__":
    run_crafting_magic_integration_tests() 