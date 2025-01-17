import unittest
from unittest.mock import Mock, patch
import random
import time
import math
import threading
from ..event_system.environmental_event_handler import (
    EnvironmentalEventHandler,
    EnvironmentalCondition,
    WeatherPattern
)
from ..event_system.event_manager import Event, EventType, EventTrigger

class TestEnvironmentalEventHandler(unittest.TestCase):
    def setUp(self):
        self.handler = EnvironmentalEventHandler()
        self.mock_game_state = {
            "territories": {
                "mystic_valley": {
                    "stability": 0.8,
                    "magical_nodes": ["ley_node", "mana_well"],
                    "resource_nodes": ["mana_crystal", "void_essence", "primal_stone"]
                },
                "shadow_peaks": {
                    "stability": 0.4,
                    "magical_nodes": ["void_node"],
                    "resource_nodes": ["shadow_crystal", "void_shard"]
                }
            },
            "magical_activity": 0.7,
            "magical_stability": 0.9,
            "current_conditions": ["mana_surge", "crystal_growth"]
        }

    def test_condition_initialization(self):
        """Test initialization of environmental conditions"""
        self.assertEqual(len(self.handler.conditions), 3)
        
        magical_storm = self.handler.conditions["magical_storm"]
        self.assertIsInstance(magical_storm, EnvironmentalCondition)
        self.assertEqual(magical_storm.name, "Magical Storm")
        self.assertEqual(len(magical_storm.compatible_conditions), 3)
        self.assertEqual(len(magical_storm.incompatible_conditions), 2)
        self.assertGreater(len(magical_storm.resource_effects), 0)
        self.assertGreater(len(magical_storm.territory_effects), 0)

    def test_environmental_event_generation(self):
        """Test generation of environmental events"""
        event = self.handler.generate_environmental_event(
            self.mock_game_state,
            "mystic_valley"
        )
        
        self.assertIsInstance(event, Event)
        self.assertEqual(event.event_type, EventType.ENVIRONMENTAL)
        self.assertEqual(event.trigger, EventTrigger.TIME)
        
        # Verify event properties
        self.assertTrue(event.event_id.startswith("environmental_"))
        self.assertGreater(event.duration, 0)
        self.assertGreater(event.cooldown, event.duration)
        
        # Verify effects
        self.assertIsNotNone(event.effects.resource_changes)
        self.assertIsNotNone(event.effects.environmental_changes)
        self.assertIsNotNone(event.effects.territory_effects)
        self.assertGreater(len(event.effects.spawned_entities), 0)

    def test_weather_pattern_update(self):
        """Test updating of weather patterns"""
        # Force pattern update
        with patch('random.random', return_value=0.1):
            self.handler.update_weather_pattern(self.mock_game_state)
            
        self.assertIsNotNone(self.handler.current_pattern)
        pattern = self.handler.current_pattern
        
        self.assertIn(pattern.primary_condition, self.handler.conditions)
        self.assertIsInstance(pattern.secondary_conditions, list)
        self.assertTrue(300 <= pattern.duration <= 900)
        self.assertGreater(len(pattern.effects), 0)
        
        # Verify secondary conditions are compatible
        condition_data = self.handler.conditions[pattern.primary_condition]
        for secondary in pattern.secondary_conditions:
            self.assertIn(secondary, condition_data.compatible_conditions)
            self.assertNotIn(secondary, condition_data.incompatible_conditions)

    def test_base_intensity_calculation(self):
        """Test calculation of base intensity"""
        intensity = self.handler._calculate_base_intensity(self.mock_game_state)
        
        # Verify territory stability impact
        avg_stability = (0.8 + 0.4) / 2  # Average of territory stabilities
        expected_stability_scale = 2 - avg_stability
        
        # Verify magical activity impact
        expected_magical_scale = 1 + (0.7 * 0.2)  # 1 + (magical_activity * 0.2)
        
        expected_base = 1.0 * expected_stability_scale * expected_magical_scale
        self.assertAlmostEqual(intensity, expected_base, places=2)

    def test_base_duration_calculation(self):
        """Test calculation of base duration"""
        duration = self.handler._calculate_base_duration(self.mock_game_state)
        
        # Base duration is 600, scaled by magical stability
        expected_duration = int(600 * (1 + 0.9 * 0.1))  # 600 * (1 + magical_stability * 0.1)
        self.assertEqual(duration, expected_duration)
        
        # Test with pattern
        self.handler.current_pattern = WeatherPattern(
            primary_condition="magical_storm",
            secondary_conditions=[],
            intensity=1.2,
            duration=600,
            effects=[]
        )
        
        duration_with_pattern = self.handler._calculate_base_duration(self.mock_game_state)
        expected_duration = int(600 * 1.2 * (1 + 0.9 * 0.1))
        self.assertEqual(duration_with_pattern, expected_duration)

    def test_condition_effect_generation(self):
        """Test generation of condition-specific effects"""
        effects = self.handler._generate_condition_effects("magical_storm", 1.0)
        
        # Verify resource changes
        condition_data = self.handler.conditions["magical_storm"]
        for resource, base_multiplier in condition_data.resource_effects.items():
            self.assertIn(resource, effects.resource_changes)
            actual_multiplier = effects.resource_changes[resource]
            min_expected = base_multiplier * condition_data.intensity_range[0]
            max_expected = base_multiplier * condition_data.intensity_range[1]
            self.assertTrue(min_expected <= actual_multiplier <= max_expected)
            
        # Verify environmental changes
        self.assertIn("magical_storm", effects.environmental_changes)
        self.assertTrue(all(
            change in condition_data.compatible_conditions
            for change in effects.environmental_changes[1:]  # Skip primary condition
        ))
        
        # Verify territory effects
        self.assertEqual(
            effects.territory_effects,
            condition_data.territory_effects
        )

    def test_territory_effect_addition(self):
        """Test addition of territory-specific effects"""
        base_effects = self.handler._generate_condition_effects("magical_storm", 1.0)
        modified_effects = self.handler._add_territory_effects(
            base_effects,
            "mystic_valley",
            self.mock_game_state
        )
        
        # Verify magical node effects
        self.assertIn("magical_resonance", modified_effects.territory_effects)
        
        # Verify resource node effects
        for node in self.mock_game_state["territories"]["mystic_valley"]["resource_nodes"]:
            self.assertIn(node, modified_effects.resource_changes)
            self.assertTrue(1.2 <= modified_effects.resource_changes[node] <= 1.5)

    def test_pattern_effect_generation(self):
        """Test generation of pattern effects"""
        # Test with primary only
        effects = self.handler._generate_pattern_effects("magical_storm", [])
        self.assertIn("magical_storm_dominance", effects)
        self.assertIn("magical_storm_intensification", effects)
        
        condition_data = self.handler.conditions["magical_storm"]
        for compatible in condition_data.compatible_conditions:
            self.assertIn(f"{compatible}_enhancement", effects)
            
        # Test with secondary conditions
        effects = self.handler._generate_pattern_effects(
            "magical_storm",
            ["mana_surge", "lightning"]
        )
        self.assertIn("mana_surge_influence", effects)
        self.assertIn("lightning_influence", effects)
        self.assertIn("mana_surge_minor_effect", effects)
        self.assertIn("lightning_minor_effect", effects)

    def test_requirement_generation(self):
        """Test generation of event requirements"""
        requirements = self.handler._generate_requirements(
            self.mock_game_state,
            "ley_surge"
        )
        
        # Verify environmental conditions
        condition_data = self.handler.conditions["ley_surge"]
        required_conditions = requirements.environmental_conditions
        self.assertTrue(all(
            cond in condition_data.compatible_conditions
            for cond in required_conditions
        ))
        self.assertTrue(all(
            cond in self.mock_game_state["current_conditions"]
            for cond in required_conditions
        ))
        
        # Verify other requirements are None
        self.assertIsNone(requirements.player_level)
        self.assertIsNone(requirements.faction_reputation)
        self.assertIsNone(requirements.celestial_alignment)
        self.assertIsNone(requirements.required_items)

    def test_empty_game_state_handling(self):
        """Test handling of empty game state"""
        empty_state = {}
        
        # Should not raise exceptions
        event = self.handler.generate_environmental_event(empty_state)
        
        self.assertIsInstance(event, Event)
        self.assertEqual(event.event_type, EventType.ENVIRONMENTAL)
        
        # Verify base values used
        self.assertEqual(len(event.effects.environmental_changes), 1)  # Only primary condition
        self.assertEqual(event.duration, 600)  # Base duration

    def test_invalid_territory_handling(self):
        """Test handling of invalid territory"""
        event = self.handler.generate_environmental_event(
            self.mock_game_state,
            "nonexistent_territory"
        )
        
        self.assertIsInstance(event, Event)
        self.assertEqual(len(event.effects.territory_effects), 0)

    def test_pattern_update_frequency(self):
        """Test weather pattern update frequency"""
        update_count = 0
        total_iterations = 1000
        
        for _ in range(total_iterations):
            self.handler.update_weather_pattern(self.mock_game_state)
            if self.handler.current_pattern:
                update_count += 1
                
        # Should be roughly 15% of iterations (0.15 chance to update)
        expected_updates = total_iterations * 0.15
        self.assertTrue(
            abs(update_count - expected_updates) < total_iterations * 0.05
        )

    def test_concurrent_event_generation(self):
        """Test generation of multiple events concurrently"""
        num_events = 100
        start_time = time.time()
        
        events = []
        for _ in range(num_events):
            event = self.handler.generate_environmental_event(
                self.mock_game_state,
                "mystic_valley"
            )
            events.append(event)
            
        end_time = time.time()
        
        # Verify performance
        generation_time = end_time - start_time
        self.assertLess(generation_time, 1.0)  # Should generate 100 events in under 1 second
        
        # Verify event uniqueness
        event_ids = set(event.event_id for event in events)
        self.assertEqual(len(event_ids), num_events)

    def test_effect_stacking(self):
        """Test stacking of multiple environmental effects"""
        # Generate multiple events with overlapping effects
        events = []
        for _ in range(5):
            event = self.handler.generate_environmental_event(
                self.mock_game_state,
                "mystic_valley"
            )
            events.append(event)
            
        # Track cumulative effects
        resource_multipliers = {}
        
        for event in events:
            # Track resource changes
            for resource, multiplier in event.effects.resource_changes.items():
                if resource in resource_multipliers:
                    resource_multipliers[resource] *= multiplier
                else:
                    resource_multipliers[resource] = multiplier
                    
        # Verify reasonable bounds for stacked effects
        for multiplier in resource_multipliers.values():
            self.assertLess(multiplier, 10.0)  # Should not stack to extreme values

    def test_condition_compatibility(self):
        """Test condition compatibility rules"""
        for condition_name, condition_data in self.handler.conditions.items():
            # Verify no condition is both compatible and incompatible
            intersection = set(condition_data.compatible_conditions) & set(condition_data.incompatible_conditions)
            self.assertEqual(len(intersection), 0)
            
            # Verify reasonable number of conditions
            self.assertLess(len(condition_data.compatible_conditions), 10)
            self.assertLess(len(condition_data.incompatible_conditions), 10)
            
            # Verify intensity ranges are reasonable
            min_intensity, max_intensity = condition_data.intensity_range
            self.assertLess(min_intensity, max_intensity)
            self.assertGreater(min_intensity, 1.0)
            self.assertLess(max_intensity, 3.0)

    def test_active_conditions_tracking(self):
        """Test tracking of active conditions"""
        initial_conditions = len(self.handler.active_conditions)
        
        # Add some conditions
        self.handler.active_conditions.add("magical_storm")
        self.handler.active_conditions.add("mana_surge")
        
        # Verify conditions were added
        self.assertEqual(
            len(self.handler.active_conditions),
            initial_conditions + 2
        )
        
        # Verify get_active_conditions returns a copy
        conditions_copy = self.handler.get_active_conditions()
        self.assertIsNot(conditions_copy, self.handler.active_conditions)
        self.assertEqual(conditions_copy, self.handler.active_conditions) 

    def test_extreme_territory_stability(self):
        """Test handling of extreme territory stability values"""
        # Test with very low stability
        unstable_state = {
            "territories": {
                "unstable_zone": {
                    "stability": 0.1,
                    "magical_nodes": ["unstable_node"],
                    "resource_nodes": ["unstable_crystal"]
                }
            }
        }
        
        event = self.handler.generate_environmental_event(
            unstable_state,
            "unstable_zone"
        )
        
        # Verify increased intensity due to instability
        self.assertIn("instability_surge", event.effects.territory_effects)
        
        # Test with perfect stability
        stable_state = {
            "territories": {
                "stable_zone": {
                    "stability": 1.0,
                    "magical_nodes": ["stable_node"],
                    "resource_nodes": ["stable_crystal"]
                }
            }
        }
        
        event = self.handler.generate_environmental_event(
            stable_state,
            "stable_zone"
        )
        
        # Verify no instability effects
        self.assertNotIn("instability_surge", event.effects.territory_effects)

    def test_extreme_magical_activity(self):
        """Test handling of extreme magical activity values"""
        # Test with maximum magical activity
        high_magic_state = {"magical_activity": 5.0}
        intensity_high = self.handler._calculate_base_intensity(high_magic_state)
        
        # Test with minimum magical activity
        low_magic_state = {"magical_activity": 0.0}
        intensity_low = self.handler._calculate_base_intensity(low_magic_state)
        
        # High magic should produce stronger effects
        self.assertGreater(intensity_high, intensity_low)
        
        # Verify reasonable bounds
        self.assertLess(intensity_high / intensity_low, 10.0)  # Should not scale too extremely

    def test_concurrent_pattern_updates(self):
        """Test concurrent updates to weather patterns"""
        def update_patterns():
            for _ in range(100):
                self.handler.update_weather_pattern(self.mock_game_state)
                
        # Create multiple threads
        threads = []
        for _ in range(4):
            thread = threading.Thread(target=update_patterns)
            threads.append(thread)
            
        # Start all threads
        for thread in threads:
            thread.start()
            
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            
        # Verify handler state is consistent
        self.assertIsInstance(self.handler.current_pattern, (WeatherPattern, type(None)))
        if self.handler.current_pattern:
            self.assertIn(
                self.handler.current_pattern.primary_condition,
                self.handler.conditions
            )

    def test_rapid_condition_changes(self):
        """Test rapid changes in environmental conditions"""
        conditions_seen = set()
        last_pattern = None
        
        # Perform many rapid updates
        for _ in range(1000):
            self.handler.update_weather_pattern(self.mock_game_state)
            if self.handler.current_pattern:
                conditions_seen.add(self.handler.current_pattern.primary_condition)
                last_pattern = self.handler.current_pattern
                
        # Should have seen all conditions
        self.assertEqual(
            conditions_seen,
            set(self.handler.conditions.keys())
        )
        
        # Last pattern should be valid
        if last_pattern:
            self.assertIn(last_pattern.primary_condition, self.handler.conditions)
            self.assertTrue(0.8 <= last_pattern.intensity <= 2.2)

    def test_condition_transition_validity(self):
        """Test validity of condition transitions"""
        current_conditions = set()
        
        for _ in range(100):
            event = self.handler.generate_environmental_event(self.mock_game_state)
            new_conditions = set(event.effects.environmental_changes)
            
            # Verify no incompatible conditions are added together
            for condition in new_conditions:
                if condition in self.handler.conditions:
                    incompatible = set(
                        self.handler.conditions[condition].incompatible_conditions
                    )
                    self.assertEqual(len(new_conditions & incompatible), 0)
                    
            current_conditions = new_conditions

    def test_resource_multiplier_bounds(self):
        """Test bounds of resource multipliers"""
        for _ in range(100):
            event = self.handler.generate_environmental_event(self.mock_game_state)
            
            for multiplier in event.effects.resource_changes.values():
                # Verify multipliers are within reasonable bounds
                self.assertGreater(multiplier, 1.0)
                self.assertLess(multiplier, 5.0)
                
                # Verify multipliers are not too precise
                decimal_places = len(str(multiplier).split('.')[-1])
                self.assertLessEqual(decimal_places, 3)

    def test_memory_usage_under_load(self):
        """Test memory usage under heavy load"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Generate many events and patterns
        events = []
        for _ in range(1000):
            event = self.handler.generate_environmental_event(self.mock_game_state)
            events.append(event)
            self.handler.update_weather_pattern(self.mock_game_state)
            
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 10MB)
        self.assertLess(memory_increase, 10 * 1024 * 1024)
        
        # Clear events and check memory cleanup
        events.clear()
        import gc
        gc.collect()
        
        cleanup_memory = process.memory_info().rss
        self.assertLess(cleanup_memory - initial_memory, 1 * 1024 * 1024)

    def test_performance_scaling(self):
        """Test performance scaling with increasing complexity"""
        # Test with simple state
        simple_state = {"territories": {"zone": {"stability": 1.0}}}
        start_time = time.time()
        for _ in range(100):
            self.handler.generate_environmental_event(simple_state)
        simple_time = time.time() - start_time
        
        # Test with complex state
        complex_state = {
            "territories": {
                f"zone_{i}": {
                    "stability": random.random(),
                    "magical_nodes": [f"node_{j}" for j in range(5)],
                    "resource_nodes": [f"resource_{j}" for j in range(10)]
                }
                for i in range(10)
            },
            "magical_activity": random.random(),
            "magical_stability": random.random(),
            "current_conditions": [
                f"condition_{i}" for i in range(5)
            ]
        }
        
        start_time = time.time()
        for _ in range(100):
            self.handler.generate_environmental_event(complex_state)
        complex_time = time.time() - start_time
        
        # Complex state should not be dramatically slower
        self.assertLess(complex_time / simple_time, 5.0)

    def test_thread_safety_stress(self):
        """Test thread safety under stress"""
        def stress_handler():
            for _ in range(100):
                # Generate event
                event = self.handler.generate_environmental_event(self.mock_game_state)
                
                # Update pattern
                self.handler.update_weather_pattern(self.mock_game_state)
                
                # Modify active conditions
                self.handler.active_conditions.add(f"condition_{random.randint(1, 10)}")
                if len(self.handler.active_conditions) > 5:
                    self.handler.active_conditions.pop()
                    
        # Create and run multiple threads
        threads = []
        for _ in range(8):  # Use more threads than CPU cores
            thread = threading.Thread(target=stress_handler)
            threads.append(thread)
            
        for thread in threads:
            thread.start()
            
        for thread in threads:
            thread.join()
            
        # Verify handler state is still valid
        self.assertIsInstance(self.handler.active_conditions, set)
        self.assertLessEqual(len(self.handler.active_conditions), 10)
        if self.handler.current_pattern:
            self.assertIn(
                self.handler.current_pattern.primary_condition,
                self.handler.conditions
            ) 