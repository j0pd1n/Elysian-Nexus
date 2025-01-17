import unittest
import logging
import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TestResult:
    test_name: str
    status: str
    execution_time: float
    error_message: Optional[str] = None
    system_metrics: Optional[Dict[str, Any]] = None

class GameSystemTest(unittest.TestCase):
    """Base class for testing game systems"""
    
    def setUp(self):
        self.logger = self._setup_logger()
        self.results: List[TestResult] = []
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("GameSystemTest")
        logger.setLevel(logging.DEBUG)
        
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        handler = logging.FileHandler("logs/test_results.log")
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        logger.addHandler(handler)
        return logger
        
    def record_result(self, result: TestResult):
        """Record test result and log it"""
        self.results.append(result)
        
        log_message = f"Test: {result.test_name} - Status: {result.status}"
        if result.error_message:
            log_message += f" - Error: {result.error_message}"
            
        if result.status == "PASS":
            self.logger.info(log_message)
        else:
            self.logger.error(log_message)
            
    def export_results(self, file_path: str):
        """Export test results to JSON file"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(self.results),
            "passed": len([r for r in self.results if r.status == "PASS"]),
            "failed": len([r for r in self.results if r.status == "FAIL"]),
            "results": [
                {
                    "test_name": r.test_name,
                    "status": r.status,
                    "execution_time": r.execution_time,
                    "error_message": r.error_message,
                    "system_metrics": r.system_metrics
                }
                for r in self.results
            ]
        }
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

class WeatherSystemTest(GameSystemTest):
    """Test cases for the weather system"""
    
    def test_weather_generation(self):
        from weather_system import WeatherSystem
        weather = WeatherSystem()
        
        # Test weather generation
        new_weather = weather._generate_new_weather()
        self.assertIsNotNone(new_weather)
        self.assertIn(new_weather.weather_type, weather.WeatherType)
        
    def test_seasonal_changes(self):
        from weather_system import WeatherSystem
        weather = WeatherSystem()
        
        # Test seasonal patterns
        for season in weather.Season:
            patterns = weather._get_seasonal_patterns(season)
            self.assertIsNotNone(patterns)
            self.assertTrue(len(patterns) > 0)
            
    def test_environmental_effects(self):
        from weather_system import WeatherSystem
        weather = WeatherSystem()
        
        # Test effect application
        effects = weather.get_current_effects()
        self.assertIsNotNone(effects)
        self.assertIsInstance(effects, dict)

class EconomicSystemTest(GameSystemTest):
    """Test cases for the economic system"""
    
    def test_market_creation(self):
        from economic_system import EconomicSystem
        economy = EconomicSystem()
        
        # Test market creation
        market = economy.create_market("test_location")
        self.assertIsNotNone(market)
        self.assertTrue(len(market.items) > 0)
        
    def test_price_updates(self):
        from economic_system import EconomicSystem
        economy = EconomicSystem()
        
        # Test price updating
        market = economy.create_market("test_location")
        initial_prices = {item.resource_type: item.current_price for item in market.items}
        
        economy.update(1.0)  # Update with 1 second delta
        
        # Check that prices have changed
        current_prices = {item.resource_type: item.current_price for item in market.items}
        self.assertNotEqual(initial_prices, current_prices)
        
    def test_trade_routes(self):
        from economic_system import EconomicSystem
        economy = EconomicSystem()
        
        # Test trade route creation
        route = economy.create_trade_route(
            "source", "destination",
            ["WOOD", "IRON"],
            distance=100,
            risk_level="MEDIUM"
        )
        
        self.assertIsNotNone(route)
        self.assertTrue(route.active)

class DynamicEventsTest(GameSystemTest):
    """Test cases for the dynamic events system"""
    
    def test_event_generation(self):
        from dynamic_events import DynamicEventsSystem
        events = DynamicEventsSystem()
        
        # Test event generation
        new_event = events._generate_events()
        self.assertIsNotNone(new_event)
        self.assertIn(new_event.category, events.EventCategory)
        
    def test_world_state_updates(self):
        from dynamic_events import DynamicEventsSystem
        events = DynamicEventsSystem()
        
        # Test world state updates
        initial_state = events.world_state
        events.update(1.0)  # Update with 1 second delta
        
        self.assertNotEqual(initial_state, events.world_state)
        
    def test_quest_generation(self):
        from dynamic_events import DynamicEventsSystem
        events = DynamicEventsSystem()
        
        # Test quest generation from event
        event = events._generate_events()
        quest = events._generate_quest_from_event(event)
        
        self.assertIsNotNone(quest)
        self.assertEqual(quest.linked_events[0], event.event_id)

def run_all_tests():
    """Run all system tests and generate report"""
    test_classes = [
        WeatherSystemTest,
        EconomicSystemTest,
        DynamicEventsTest
    ]
    
    suite = unittest.TestSuite()
    for test_class in test_classes:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_class))
        
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Export results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for test_class in test_classes:
        test_instance = test_class()
        test_instance.export_results(f"test_results_{test_class.__name__}_{timestamp}.json")
        
    return result

if __name__ == "__main__":
    run_all_tests() 