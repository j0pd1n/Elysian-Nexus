import unittest
from unittest.mock import Mock, patch
import random
import time
import math
import threading
import gc
import psutil
import os
from ..event_system.celestial_event_handler import (
    CelestialEventHandler,
    CelestialAlignment,
    CelestialPattern
)
from ..event_system.event_manager import Event, EventType, EventTrigger

class TestCelestialEventHandler(unittest.TestCase):
    def setUp(self):
        self.handler = CelestialEventHandler()
        self.mock_game_state = {
            "player_level": 10,
            "faction_reputation": {
                "celestial_faction": 100,
                "void_faction": 75,
                "primal_faction": 50
            },
            "territories": {
                "mystic_valley": {
                    "stability": 0.8,
                    "resource_nodes": ["mana_crystal", "void_essence", "primal_stone"]
                },
                "shadow_peaks": {
                    "stability": 0.6,
                    "resource_nodes": ["shadow_crystal", "void_shard"]
                }
            }
        }

    def test_alignment_initialization(self):
        """Test initialization of celestial alignments"""
        self.assertEqual(len(self.handler.alignments), 3)
        
        celestial = self.handler.alignments["celestial"]
        self.assertIsInstance(celestial, CelestialAlignment)
        self.assertEqual(celestial.name, "Celestial")
        self.assertEqual(celestial.power_multiplier, 1.5)
        self.assertEqual(len(celestial.resonance_types), 3)
        self.assertEqual(len(celestial.opposing_types), 3)

    def test_celestial_event_generation(self):
        """Test generation of celestial events"""
        event = self.handler.generate_celestial_event(
            self.mock_game_state,
            "mystic_valley"
        )
        
        self.assertIsInstance(event, Event)
        self.assertEqual(event.event_type, EventType.CELESTIAL)
        self.assertEqual(event.trigger, EventTrigger.TIME)
        
        # Verify event properties
        self.assertTrue(event.event_id.startswith("celestial_"))
        self.assertTrue(event.name.endswith("Convergence"))
        self.assertGreater(event.duration, 0)
        self.assertGreater(event.cooldown, event.duration)
        
        # Verify effects
        self.assertIsNotNone(event.effects.faction_reputation_changes)
        self.assertIsNotNone(event.effects.resource_changes)
        self.assertIsNotNone(event.effects.environmental_changes)
        self.assertIsNotNone(event.effects.celestial_effects)
        self.assertIn("mystic_valley", event.effects.territory_effects)

    def test_celestial_pattern_update(self):
        """Test updating of celestial patterns"""
        # Force pattern update
        with patch('random.random', return_value=0.05):
            self.handler.update_celestial_pattern(self.mock_game_state)
            
        self.assertIsNotNone(self.handler.current_pattern)
        pattern = self.handler.current_pattern
        
        self.assertIn(pattern.primary_alignment, self.handler.alignments)
        self.assertTrue(0.8 <= pattern.intensity <= 1.5)
        self.assertTrue(300 <= pattern.duration <= 900)
        self.assertGreater(len(pattern.effects), 0)
        
        if pattern.secondary_alignment:
            self.assertIn(pattern.secondary_alignment, self.handler.alignments)
            self.assertNotEqual(pattern.primary_alignment, pattern.secondary_alignment)

    def test_power_modifier_calculation(self):
        """Test calculation of power modifiers"""
        # Test basic modifier
        base_power = 1.0
        modifier = self.handler.calculate_power_modifier(base_power, "celestial")
        self.assertEqual(modifier, 1.5)  # Base celestial multiplier
        
        # Test with position
        position = (1.0, 1.0, 1.0)
        modifier_with_pos = self.handler.calculate_power_modifier(
            base_power,
            "celestial",
            position
        )
        self.assertGreater(modifier_with_pos, modifier)
        
        # Test with pattern
        self.handler.current_pattern = CelestialPattern(
            primary_alignment="celestial",
            secondary_alignment="void",
            intensity=1.2,
            duration=600,
            effects=[]
        )
        
        modifier_with_pattern = self.handler.calculate_power_modifier(
            base_power,
            "celestial"
        )
        self.assertEqual(modifier_with_pattern, 1.5 * 1.2)
        
        # Test secondary alignment
        secondary_modifier = self.handler.calculate_power_modifier(
            base_power,
            "void"
        )
        self.assertEqual(secondary_modifier, 1.4 * 1.2 * 0.7)

    def test_base_power_calculation(self):
        """Test calculation of base power"""
        power = self.handler._calculate_base_power(self.mock_game_state)
        
        # Verify player level scaling
        expected_player_scale = 1 + (10 * 0.1)  # 1 + (player_level * 0.1)
        
        # Verify territory stability impact
        avg_stability = (0.8 + 0.6) / 2  # Average of territory stabilities
        expected_stability_scale = 2 - avg_stability
        
        expected_base = 1.0 * expected_player_scale * expected_stability_scale
        self.assertAlmostEqual(power, expected_base, places=2)

    def test_base_duration_calculation(self):
        """Test calculation of base duration"""
        duration = self.handler._calculate_base_duration(self.mock_game_state)
        
        # Base duration is 600, scaled by player level
        expected_duration = int(600 * (1 + 10 * 0.05))  # 600 * (1 + player_level * 0.05)
        self.assertEqual(duration, expected_duration)
        
        # Test with pattern
        self.handler.current_pattern = CelestialPattern(
            primary_alignment="celestial",
            secondary_alignment=None,
            intensity=1.2,
            duration=600,
            effects=[]
        )
        
        duration_with_pattern = self.handler._calculate_base_duration(self.mock_game_state)
        expected_duration = int(600 * 1.2 * (1 + 10 * 0.05))
        self.assertEqual(duration_with_pattern, expected_duration)

    def test_alignment_effect_generation(self):
        """Test generation of alignment-specific effects"""
        effects = self.handler._generate_alignment_effects("celestial", 1.0)
        
        # Verify faction reputation changes
        self.assertIn("celestial_faction", effects.faction_reputation_changes)
        
        # Verify resource changes
        for res_type in self.handler.alignments["celestial"].resonance_types:
            self.assertIn(f"{res_type}_essence", effects.resource_changes)
            
        # Verify environmental changes
        self.assertIn("celestial_resonance", effects.environmental_changes)
        
        # Verify celestial effects
        self.assertIn("celestial_power_surge", effects.celestial_effects)
        
        # Verify spawned entities
        self.assertTrue(all(
            entity.startswith("celestial_entity_")
            for entity in effects.spawned_entities
        ))

    def test_territory_effect_addition(self):
        """Test addition of territory-specific effects"""
        base_effects = self.handler._generate_alignment_effects("celestial", 1.0)
        modified_effects = self.handler._add_territory_effects(
            base_effects,
            "mystic_valley",
            self.mock_game_state
        )
        
        # Verify territory effect added
        self.assertIn("mystic_valley", modified_effects.territory_effects)
        self.assertEqual(
            modified_effects.territory_effects["mystic_valley"],
            "celestial_resonance"
        )
        
        # Verify resource node effects
        for node in self.mock_game_state["territories"]["mystic_valley"]["resource_nodes"]:
            self.assertIn(node, modified_effects.resource_changes)
            self.assertTrue(1.2 <= modified_effects.resource_changes[node] <= 1.5)

    def test_pattern_effect_generation(self):
        """Test generation of pattern effects"""
        # Test primary only
        effects = self.handler._generate_pattern_effects("celestial", None)
        self.assertIn("celestial_dominance", effects)
        self.assertIn("celestial_resonance", effects)
        
        for res_type in self.handler.alignments["celestial"].resonance_types:
            self.assertIn(f"{res_type}_enhancement", effects)
            
        # Test with secondary
        effects = self.handler._generate_pattern_effects("celestial", "void")
        self.assertIn("void_influence", effects)
        self.assertIn("void_resonance", effects)
        
        for res_type in self.handler.alignments["void"].resonance_types:
            self.assertIn(f"{res_type}_minor_enhancement", effects)

    def test_requirement_generation(self):
        """Test generation of event requirements"""
        requirements = self.handler._generate_requirements(
            self.mock_game_state,
            "celestial"
        )
        
        # Verify player level requirement
        self.assertEqual(requirements.player_level, 8)  # 10 * 0.8
        
        # Verify faction reputation requirement
        self.assertIn("celestial_faction", requirements.faction_reputation)
        self.assertEqual(
            requirements.faction_reputation["celestial_faction"],
            70  # 100 * 0.7
        )
        
        # Verify celestial alignment requirement
        self.assertEqual(requirements.celestial_alignment, "celestial")

    def test_empty_game_state_handling(self):
        """Test handling of empty game state"""
        empty_state = {}
        
        # Should not raise exceptions
        event = self.handler.generate_celestial_event(empty_state)
        
        self.assertIsInstance(event, Event)
        self.assertEqual(event.event_type, EventType.CELESTIAL)
        
        # Verify default values used
        self.assertEqual(
            event.requirements.player_level,
            1  # Minimum level
        )
        self.assertIsNotNone(event.effects)

    def test_invalid_territory_handling(self):
        """Test handling of invalid territory"""
        event = self.handler.generate_celestial_event(
            self.mock_game_state,
            "nonexistent_territory"
        )
        
        self.assertIsInstance(event, Event)
        self.assertEqual(len(event.effects.territory_effects), 0)

    def test_invalid_alignment_handling(self):
        """Test handling of invalid alignment"""
        with self.assertRaises(KeyError):
            self.handler.calculate_power_modifier(1.0, "invalid_alignment")

    def test_pattern_update_frequency(self):
        """Test celestial pattern update frequency"""
        update_count = 0
        total_iterations = 1000
        
        for _ in range(total_iterations):
            self.handler.update_celestial_pattern(self.mock_game_state)
            if self.handler.current_pattern:
                update_count += 1
                
        # Should be roughly 10% of iterations (0.1 chance to update)
        expected_updates = total_iterations * 0.1
        self.assertTrue(
            abs(update_count - expected_updates) < total_iterations * 0.05
        )

    def test_concurrent_event_generation(self):
        """Test generation of multiple events concurrently"""
        num_events = 100
        start_time = time.time()
        
        events = []
        for _ in range(num_events):
            event = self.handler.generate_celestial_event(
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

    def test_pattern_effect_scaling(self):
        """Test scaling of pattern effects with intensity"""
        # Create pattern with high intensity
        self.handler.current_pattern = CelestialPattern(
            primary_alignment="celestial",
            secondary_alignment="void",
            intensity=1.5,  # Maximum intensity
            duration=600,
            effects=[]
        )
        
        base_power = 1.0
        high_intensity_modifier = self.handler.calculate_power_modifier(
            base_power,
            "celestial"
        )
        
        # Create pattern with low intensity
        self.handler.current_pattern = CelestialPattern(
            primary_alignment="celestial",
            secondary_alignment="void",
            intensity=0.8,  # Minimum intensity
            duration=600,
            effects=[]
        )
        
        low_intensity_modifier = self.handler.calculate_power_modifier(
            base_power,
            "celestial"
        )
        
        # High intensity should produce stronger effects
        self.assertGreater(high_intensity_modifier, low_intensity_modifier)

    def test_position_effect_boundaries(self):
        """Test boundary cases for position-based effects"""
        base_power = 1.0
        alignment = "celestial"
        
        # Test extreme distances
        far_position = (1000.0, 1000.0, 1000.0)
        far_modifier = self.handler.calculate_power_modifier(
            base_power,
            alignment,
            far_position
        )
        
        near_position = (0.1, 0.1, 0.1)
        near_modifier = self.handler.calculate_power_modifier(
            base_power,
            alignment,
            near_position
        )
        
        # Near positions should have stronger effects
        self.assertGreater(near_modifier, far_modifier)
        
        # Test zero distance
        zero_position = (0.0, 0.0, 0.0)
        zero_modifier = self.handler.calculate_power_modifier(
            base_power,
            alignment,
            zero_position
        )
        
        # Should not produce infinite values
        self.assertFalse(math.isinf(zero_modifier))
        self.assertGreater(zero_modifier, near_modifier)

    def test_effect_stacking(self):
        """Test stacking of multiple celestial effects"""
        # Generate multiple events with overlapping effects
        events = []
        for _ in range(5):
            event = self.handler.generate_celestial_event(
                self.mock_game_state,
                "mystic_valley"
            )
            events.append(event)
            
        # Track cumulative effects
        resource_multipliers = {}
        faction_changes = {}
        
        for event in events:
            # Track resource changes
            for resource, multiplier in event.effects.resource_changes.items():
                if resource in resource_multipliers:
                    resource_multipliers[resource] *= multiplier
                else:
                    resource_multipliers[resource] = multiplier
                    
            # Track faction reputation changes
            for faction, change in event.effects.faction_reputation_changes.items():
                faction_changes[faction] = faction_changes.get(faction, 0) + change
                
        # Verify reasonable bounds for stacked effects
        for multiplier in resource_multipliers.values():
            self.assertLess(multiplier, 10.0)  # Should not stack to extreme values
            
        for change in faction_changes.values():
            self.assertLess(change, 1000)  # Should not stack to extreme values

    def test_memory_usage(self):
        """Test memory usage during intensive operations"""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Generate large number of events and patterns
        for _ in range(1000):
            self.handler.generate_celestial_event(self.mock_game_state)
            self.handler.update_celestial_pattern(self.mock_game_state)
            
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 10MB)
        self.assertLess(memory_increase, 10 * 1024 * 1024)

    def test_effect_cleanup(self):
        """Test cleanup of effects and patterns"""
        # Generate events and update patterns
        events = []
        for _ in range(100):
            event = self.handler.generate_celestial_event(self.mock_game_state)
            events.append(event)
            self.handler.update_celestial_pattern(self.mock_game_state)
            
        # Force garbage collection
        gc.collect()
        
        # Verify no memory leaks in active effects
        self.assertLessEqual(
            len(self.handler.active_effects),
            len(events)
        )

    def test_thread_safety(self):
        """Test thread safety of event generation"""
        def generate_events():
            for _ in range(100):
                self.handler.generate_celestial_event(self.mock_game_state)
                self.handler.update_celestial_pattern(self.mock_game_state)
                
        # Create multiple threads
        threads = []
        for _ in range(4):
            thread = threading.Thread(target=generate_events)
            threads.append(thread)
            
        # Start all threads
        for thread in threads:
            thread.start()
            
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            
        # Verify handler state is consistent
        self.assertIsNotNone(self.handler.current_pattern)
        self.assertIsInstance(self.handler.active_effects, dict) 