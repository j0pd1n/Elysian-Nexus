import unittest
import time
from typing import Dict, Any
from dataclasses import dataclass

from testing_framework import GameSystemTest
from profiling_tools import SystemProfiler, FunctionProfiler
from weather_system import WeatherSystem, WeatherType, Season
from economic_system import EconomicSystem, ResourceType, MarketItem
from dynamic_events_system import (
    DynamicEventsSystem,
    EventCategory,
    WorldStateMetric,
    DynamicEvent
)

@dataclass
class SystemPerformanceMetrics:
    avg_update_time: float
    peak_update_time: float
    avg_memory_usage: float
    peak_memory_usage: float
    total_events_processed: int
    total_time: float

class SystemIntegrationTest(GameSystemTest):
    """Integration tests between game systems"""
    
    def setUp(self):
        super().setUp()
        self.profiler = SystemProfiler()
        self.weather = WeatherSystem()
        self.economy = EconomicSystem()
        self.events = DynamicEventsSystem(self.weather, self.economy)
        
    def test_weather_economic_integration(self):
        """Test weather effects on economic system"""
        # Start profiling
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Set up severe weather
        self.weather.current_weather.weather_type = WeatherType.STORM
        self.weather.current_weather.intensity = 0.9
        
        # Create test market
        market = self.economy.create_market("test_port")
        initial_prices = {
            item.resource_type: item.current_price
            for item in market.items
        }
        
        # Update systems
        self.weather.update(1.0)
        self.economy.update(1.0)
        
        # Verify economic impact
        current_prices = {
            item.resource_type: item.current_price
            for item in market.items
        }
        
        # Check that severe weather affected prices
        price_changes = any(
            abs(current_prices[rt] - initial_prices[rt]) > 0.1
            for rt in initial_prices
        )
        self.assertTrue(price_changes)
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="weather_economic_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_weather_events_integration(self):
        """Test weather influence on event generation"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Set up extreme weather
        self.weather.current_weather.weather_type = WeatherType.BLIZZARD
        self.weather.current_weather.intensity = 1.0
        
        # Track initial events
        initial_event_count = len(self.events.active_events)
        
        # Update systems
        self.weather.update(1.0)
        self.events.update(1.0)
        
        # Verify weather triggered events
        new_events = [
            event for event in self.events.active_events.values()
            if event.category == EventCategory.NATURAL
            and "blizzard" in event.description.lower()
        ]
        
        self.assertTrue(len(new_events) > 0)
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics(self.events)
        
        self.record_result(TestResult(
            test_name="weather_events_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_economic_events_integration(self):
        """Test economic system influence on event generation"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create market crisis conditions
        market = self.economy.create_market("test_market")
        for item in market.items:
            item.current_price *= 2  # Double all prices
            
        # Update systems
        self.economy.update(1.0)
        self.events.update(1.0)
        
        # Verify economic events were generated
        economic_events = [
            event for event in self.events.active_events.values()
            if event.category == EventCategory.ECONOMIC
        ]
        
        self.assertTrue(len(economic_events) > 0)
        
        # Check world state impact
        self.assertLess(
            self.events.world_state.metrics[WorldStateMetric.PROSPERITY],
            0.8  # Prosperity should decrease
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics(self.events)
        
        self.record_result(TestResult(
            test_name="economic_events_integration",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_full_system_integration(self):
        """Test full system integration with performance benchmarks"""
        self.profiler.start_profiling()
        start_time = time.time()
        update_times = []
        
        # Run system for multiple updates
        for _ in range(100):  # 100 update cycles
            cycle_start = time.time()
            
            # Update all systems
            self.weather.update(0.1)
            self.economy.update(0.1)
            self.events.update(0.1)
            
            update_times.append(time.time() - cycle_start)
            time.sleep(0.01)  # Small delay between updates
            
        end_time = time.time()
        self.profiler.stop_profiling()
        
        # Calculate performance metrics
        performance = SystemPerformanceMetrics(
            avg_update_time=sum(update_times) / len(update_times),
            peak_update_time=max(update_times),
            avg_memory_usage=sum(m["memory_usage"] for m in self.profiler.metrics_history) / len(self.profiler.metrics_history),
            peak_memory_usage=max(m["memory_usage"] for m in self.profiler.metrics_history),
            total_events_processed=len(self.events.active_events),
            total_time=end_time - start_time
        )
        
        # Performance assertions
        self.assertLess(performance.avg_update_time, 0.05)  # Average update under 50ms
        self.assertLess(performance.peak_update_time, 0.1)  # Peak update under 100ms
        self.assertLess(performance.peak_memory_usage, 90.0)  # Peak memory under 90%
        
        # Verify system stability
        self.assertTrue(all(
            0 <= metric <= 1
            for metric in self.events.world_state.metrics.values()
        ))
        
        # Record results with detailed metrics
        self.record_result(TestResult(
            test_name="full_system_integration",
            status="PASS",
            execution_time=end_time - start_time,
            system_metrics={
                "performance": vars(performance),
                "bottlenecks": self.profiler.analyze_bottlenecks(),
                "final_metrics": self.profiler.get_performance_report()
            }
        ))
        
    def test_seasonal_economic_cycle(self):
        """Test seasonal changes impact on economy over time"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        market = self.economy.create_market("test_town")
        seasonal_prices = {}
        
        # Track prices across seasons
        for season in Season:
            self.weather.current_season = season
            self.weather.update(1.0)
            self.economy.update(1.0)
            
            seasonal_prices[season] = {
                item.resource_type: item.current_price
                for item in market.items
            }
            
        # Verify seasonal price variations
        food_prices = {
            season: prices[ResourceType.FOOD]
            for season, prices in seasonal_prices.items()
        }
        
        # Winter food prices should be higher than summer
        self.assertGreater(
            food_prices[Season.WINTER],
            food_prices[Season.SUMMER]
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics()
        
        self.record_result(TestResult(
            test_name="seasonal_economic_cycle",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))
        
    def test_event_chain_reactions(self):
        """Test chain reactions between events"""
        self.profiler.start_profiling()
        start_time = time.time()
        
        # Create initial event
        bandit_event = self.events._generate_bandit_raid()
        self.events.active_events[bandit_event.event_id] = bandit_event
        
        # Track initial state
        initial_events = len(self.events.active_events)
        initial_quests = len(self.events.active_quests)
        
        # Update systems multiple times
        for _ in range(10):
            self.events.update(1.0)
            self.economy.update(1.0)
            
        # Verify chain reactions
        self.assertGreater(
            len(self.events.active_events),
            initial_events
        )
        self.assertGreater(
            len(self.events.active_quests),
            initial_quests
        )
        
        # Stop profiling and record metrics
        self.profiler.stop_profiling()
        metrics = self.profiler.collect_metrics(self.events)
        
        self.record_result(TestResult(
            test_name="event_chain_reactions",
            status="PASS",
            execution_time=time.time() - start_time,
            system_metrics=self.profiler._metrics_to_dict(metrics)
        ))

def run_integration_tests():
    """Run all integration tests with performance monitoring"""
    suite = unittest.TestLoader().loadTestsFromTestCase(SystemIntegrationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Export results
    test_instance = SystemIntegrationTest()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_instance.export_results(f"integration_test_results_{timestamp}.json")
    
    return result

if __name__ == "__main__":
    run_integration_tests() 