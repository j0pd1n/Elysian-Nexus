import unittest
from unittest.mock import Mock, patch
import time
from typing import Dict, Any

from dynamic_events_system import (
    DynamicEventsSystem,
    EventCategory,
    EventSeverity,
    WorldStateMetric,
    QuestState,
    DynamicEvent,
    QuestEvent
)
from weather_system import WeatherSystem, WeatherType
from economic_system import EconomicSystem, ResourceType

class TestDynamicEventsSystem(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.weather_system = Mock(spec=WeatherSystem)
        self.economic_system = Mock(spec=EconomicSystem)
        
        # Configure weather system mock
        self.weather_system.current_season.value = "summer"
        self.weather_system.current_weather = Mock(
            weather_type=WeatherType.CLEAR,
            intensity=0.5,
            duration=3600
        )
        
        # Configure economic system mock
        self.economic_system.markets = {}
        self.economic_system.trade_routes = []
        
        self.events_system = DynamicEventsSystem(
            self.weather_system,
            self.economic_system
        )
        
    def test_world_state_initialization(self):
        """Test that world state is properly initialized"""
        self.assertIsNotNone(self.events_system.world_state)
        self.assertEqual(len(self.events_system.world_state.metrics), 6)
        self.assertTrue(0 <= self.events_system.world_state.metrics[WorldStateMetric.STABILITY] <= 1)
        
    def test_event_generation_natural(self):
        """Test natural event generation"""
        # Set up conditions for weather disaster
        self.weather_system.current_weather.weather_type = WeatherType.STORM
        self.weather_system.current_weather.intensity = 0.8
        
        event = self.events_system._generate_weather_disaster()
        
        self.assertIsNotNone(event)
        self.assertEqual(event.category, EventCategory.NATURAL)
        self.assertEqual(event.severity, EventSeverity.MAJOR)
        self.assertIn("storm", event.description.lower())
        
    def test_event_generation_economic(self):
        """Test economic event generation"""
        # Set up conditions for market crisis
        self.events_system.world_state.metrics[WorldStateMetric.PROSPERITY] = 0.3
        
        event = self.events_system._generate_market_crisis()
        
        self.assertIsNotNone(event)
        self.assertEqual(event.category, EventCategory.ECONOMIC)
        self.assertIn("crisis", event.description.lower())
        self.assertGreater(len(event.consequences), 0)
        
    def test_event_generation_social(self):
        """Test social event generation"""
        # Test festival generation
        self.events_system.world_state.metrics[WorldStateMetric.MORALE] = 0.5
        
        event = self.events_system._generate_festival()
        
        self.assertIsNotNone(event)
        self.assertEqual(event.category, EventCategory.SOCIAL)
        self.assertIn("festival", event.description.lower())
        
        # Test unrest generation
        self.events_system.world_state.metrics[WorldStateMetric.STABILITY] = 0.3
        self.events_system.world_state.metrics[WorldStateMetric.MORALE] = 0.3
        
        event = self.events_system._generate_unrest()
        
        self.assertIsNotNone(event)
        self.assertEqual(event.category, EventCategory.SOCIAL)
        self.assertIn("unrest", event.description.lower())
        
    def test_event_generation_political(self):
        """Test political event generation"""
        # Set up test factions
        self.events_system.world_state.faction_relations = {
            "Kingdom": {"Empire": 0.5},
            "Empire": {"Kingdom": 0.5}
        }
        
        # Test faction conflict
        event = self.events_system._generate_faction_conflict()
        
        self.assertIsNotNone(event)
        self.assertEqual(event.category, EventCategory.POLITICAL)
        self.assertIn("conflict", event.description.lower())
        
        # Test diplomatic event
        event = self.events_system._generate_diplomatic_event()
        
        self.assertIsNotNone(event)
        self.assertEqual(event.category, EventCategory.POLITICAL)
        self.assertTrue(
            any(term in event.description.lower() 
                for term in ["treaty", "agreement", "exchange", "marriage", "pact"])
        )
        
    def test_event_generation_military(self):
        """Test military event generation"""
        # Test bandit raid
        self.events_system.world_state.metrics[WorldStateMetric.DANGER_LEVEL] = 0.6
        
        event = self.events_system._generate_bandit_raid()
        
        self.assertIsNotNone(event)
        self.assertEqual(event.category, EventCategory.MILITARY)
        self.assertIn("bandit", event.description.lower())
        
        # Test monster attack
        self.events_system.world_state.metrics[WorldStateMetric.DANGER_LEVEL] = 0.8
        
        event = self.events_system._generate_monster_attack()
        
        self.assertIsNotNone(event)
        self.assertEqual(event.category, EventCategory.MILITARY)
        self.assertTrue(
            any(monster.lower() in event.description.lower()
                for monster in ["dragon", "giant", "demon", "undead", "elemental"])
        )
        
    def test_event_generation_supernatural(self):
        """Test supernatural event generation"""
        # Test magical phenomenon
        self.events_system.world_state.metrics[WorldStateMetric.MAGIC_SATURATION] = 0.8
        
        event = self.events_system._generate_magical_phenomenon()
        
        self.assertIsNotNone(event)
        self.assertEqual(event.category, EventCategory.SUPERNATURAL)
        self.assertTrue(
            any(term in event.description.lower()
                for term in ["storm", "surge", "convergence", "crystallization", "aurora"])
        )
        
        # Test divine intervention
        with patch('random.random', return_value=0.05):  # Ensure event triggers
            event = self.events_system._generate_divine_intervention()
            
            self.assertIsNotNone(event)
            self.assertEqual(event.category, EventCategory.SUPERNATURAL)
            self.assertTrue(
                any(term in event.description.lower()
                    for term in ["blessing", "miracle", "sign", "vision", "judgment"])
            )
            
    def test_quest_generation(self):
        """Test quest generation from events"""
        # Test combat quest generation
        event = DynamicEvent(
            event_id="test_monster",
            category=EventCategory.MILITARY,
            severity=EventSeverity.CRITICAL,
            location="test_location",
            description="Dragon attacking the region",
            triggers={},
            consequences={},
            duration=3600,
            start_time=time.time()
        )
        
        quest = self.events_system._create_combat_quest(event)
        
        self.assertIsNotNone(quest)
        self.assertEqual(quest.state, QuestState.AVAILABLE)
        self.assertIn("Monster Slaying", quest.title)
        self.assertEqual(quest.requirements["min_level"], 15)
        
    def test_event_processing(self):
        """Test event processing and effects"""
        # Create test event
        event = DynamicEvent(
            event_id="test_event",
            category=EventCategory.ECONOMIC,
            severity=EventSeverity.MAJOR,
            location="global",
            description="Test economic event",
            triggers={},
            consequences={
                "stability_impact": -0.1,
                "trade_disruption": 0.5,
                "resource_damage": {
                    ResourceType.FOOD.value: 0.2
                }
            },
            duration=3600,
            start_time=time.time() - 1800  # Half duration passed
        )
        
        self.events_system.active_events[event.event_id] = event
        initial_stability = self.events_system.world_state.metrics[WorldStateMetric.STABILITY]
        
        # Process events
        self.events_system._process_active_events(time.time())
        
        # Check effects
        self.assertLess(
            self.events_system.world_state.metrics[WorldStateMetric.STABILITY],
            initial_stability
        )
        
    def test_world_state_update(self):
        """Test world state updates"""
        initial_time = time.time()
        
        # Add test effect
        self.events_system.world_state.active_effects.add("test_effect")
        
        # Update world state
        self.events_system._update_world_state(3600)  # 1 hour
        
        # Check that update occurred
        self.assertGreater(
            self.events_system.world_state.last_update,
            initial_time
        )
        
        # Check metric normalization
        for metric, value in self.events_system.world_state.metrics.items():
            self.assertTrue(0 <= value <= 1)
            
    def test_quest_completion(self):
        """Test quest completion checking"""
        quest = QuestEvent(
            quest_id="test_quest",
            title="Test Quest",
            description="Test quest description",
            requirements={"min_level": 5},
            rewards={"gold": 100},
            state=QuestState.ACTIVE,
            linked_events=[],
            expiry_time=time.time() + 3600,
            completion_conditions={
                "items_delivered": True,
                "people_helped": 10,
                "target_helped": 10
            }
        )
        
        # Check completion
        self.assertTrue(self.events_system._check_quest_completion(quest))
        
        # Modify conditions to be incomplete
        quest.completion_conditions["people_helped"] = 5
        self.assertFalse(self.events_system._check_quest_completion(quest))
        
if __name__ == '__main__':
    unittest.main() 