import unittest
from unittest.mock import Mock, patch
import time
from ..event_system.event_processor import EventProcessor, EventState
from ..event_system.event_manager import Event, EventType, EventTrigger, EventRequirements, EventEffects

class TestEventProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = EventProcessor()
        self.mock_game_state = {
            "player_level": 10,
            "faction_reputation": {
                "celestial_order": 100,
                "void_seekers": 75,
                "primal_circle": 50
            },
            "current_alignment": "celestial",
            "environmental_conditions": ["clear", "night"],
            "inventory": {
                "mana_crystal": 5,
                "void_essence": 3
            },
            "resources": {
                "gold": 1000,
                "mana": 500
            },
            "territories": {
                "mystic_valley": {
                    "active_effects": [],
                    "control_level": 0.8
                }
            }
        }

    def test_event_activation(self):
        """Test event activation"""
        event = Event(
            event_id="test_event",
            name="Test Event",
            event_type=EventType.CELESTIAL,
            trigger=EventTrigger.TIME,
            requirements=EventRequirements(
                player_level=5,
                faction_reputation=None,
                completed_events=None,
                celestial_alignment=None,
                environmental_conditions=None,
                required_items=None
            ),
            effects=EventEffects(
                faction_reputation_changes={},
                resource_changes={},
                environmental_changes=[],
                spawned_entities=[],
                celestial_effects=[],
                territory_effects={}
            ),
            duration=60,
            cooldown=300
        )

        self.processor.add_event(event)
        
        # Verify event was activated
        self.assertIn(event.event_id, self.processor.active_events)
        self.assertIn(event.event_id, self.processor.event_states)
        
        state = self.processor.event_states[event.event_id]
        self.assertTrue(state.is_active)
        self.assertFalse(state.effects_applied)
        self.assertFalse(state.cleanup_performed)

    def test_requirement_checking(self):
        """Test requirement checking"""
        requirements = EventRequirements(
            player_level=8,
            faction_reputation={"celestial_order": 80},
            completed_events=None,
            celestial_alignment="celestial",
            environmental_conditions=["clear"],
            required_items={"mana_crystal": 3}
        )

        # Should pass all requirements
        self.assertTrue(self.processor.check_requirements(requirements, self.mock_game_state))

        # Test failing requirements
        requirements.player_level = 15
        self.assertFalse(self.processor.check_requirements(requirements, self.mock_game_state))

        requirements.player_level = 8
        requirements.faction_reputation = {"celestial_order": 150}
        self.assertFalse(self.processor.check_requirements(requirements, self.mock_game_state))

    def test_effect_application(self):
        """Test application of event effects"""
        effects = EventEffects(
            faction_reputation_changes={"celestial_order": 20},
            resource_changes={"gold": 1.5},
            environmental_changes=["storm"],
            spawned_entities=["test_entity"],
            celestial_effects=["test_effect"],
            territory_effects={"mystic_valley": "test_territory_effect"}
        )

        self.processor.apply_effects(effects, self.mock_game_state)

        # Verify faction reputation changes
        self.assertEqual(
            self.mock_game_state["faction_reputation"]["celestial_order"],
            120  # 100 + 20
        )

        # Verify resource changes
        self.assertEqual(
            self.mock_game_state["resources"]["gold"],
            1500  # 1000 * 1.5
        )

        # Verify environmental changes
        self.assertIn("storm", self.mock_game_state["environmental_conditions"])

        # Verify entity spawning
        self.assertIn("test_entity", self.mock_game_state["active_entities"])

        # Verify celestial effects
        self.assertIn("test_effect", self.mock_game_state["celestial_effects"])

        # Verify territory effects
        self.assertIn(
            "test_territory_effect",
            self.mock_game_state["territories"]["mystic_valley"]["active_effects"]
        )

    def test_effect_removal(self):
        """Test removal of event effects"""
        # First apply effects
        effects = EventEffects(
            faction_reputation_changes={},
            resource_changes={},
            environmental_changes=["storm"],
            spawned_entities=["test_entity"],
            celestial_effects=["test_effect"],
            territory_effects={"mystic_valley": "test_territory_effect"}
        )

        self.processor.apply_effects(effects, self.mock_game_state)
        self.processor.remove_effects(effects, self.mock_game_state)

        # Verify environmental changes removed
        self.assertNotIn("storm", self.mock_game_state["environmental_conditions"])

        # Verify entity removed
        self.assertNotIn("test_entity", self.mock_game_state["active_entities"])

        # Verify celestial effects removed
        self.assertNotIn("test_effect", self.mock_game_state["celestial_effects"])

        # Verify territory effects removed
        self.assertNotIn(
            "test_territory_effect",
            self.mock_game_state["territories"]["mystic_valley"]["active_effects"]
        )

    @patch('time.time')
    def test_event_lifecycle(self, mock_time):
        """Test complete event lifecycle"""
        start_time = 1000.0
        mock_time.return_value = start_time

        event = Event(
            event_id="lifecycle_test",
            name="Lifecycle Test",
            event_type=EventType.CELESTIAL,
            trigger=EventTrigger.TIME,
            requirements=EventRequirements(
                player_level=5,
                faction_reputation=None,
                completed_events=None,
                celestial_alignment=None,
                environmental_conditions=None,
                required_items=None
            ),
            effects=EventEffects(
                faction_reputation_changes={"celestial_order": 10},
                resource_changes={},
                environmental_changes=["test_condition"],
                spawned_entities=[],
                celestial_effects=[],
                territory_effects={}
            ),
            duration=60,
            cooldown=300
        )

        # Add and process event
        self.processor.add_event(event)
        self.processor.update(self.mock_game_state)

        # Verify effects applied
        self.assertTrue(self.processor.event_states[event.event_id].effects_applied)
        self.assertEqual(
            self.mock_game_state["faction_reputation"]["celestial_order"],
            110  # 100 + 10
        )

        # Advance time past duration
        mock_time.return_value = start_time + 70
        self.processor.update(self.mock_game_state)

        # Verify event completed and cleaned up
        self.assertIn(event.event_id, self.processor.completed_events)
        self.assertNotIn(event.event_id, self.processor.active_events)
        self.assertNotIn(event.event_id, self.processor.event_states)

    def test_event_chain_processing(self):
        """Test processing of event chains"""
        # Create chain of events
        events = []
        for i in range(3):
            event = Event(
                event_id=f"chain_event_{i}",
                name=f"Chain Event {i}",
                event_type=EventType.CELESTIAL,
                trigger=EventTrigger.TIME if i == 0 else EventTrigger.RITUAL_COMPLETION,
                requirements=EventRequirements(
                    player_level=5,
                    faction_reputation=None,
                    completed_events=None,
                    celestial_alignment=None,
                    environmental_conditions=None,
                    required_items=None
                ),
                effects=EventEffects(
                    faction_reputation_changes={},
                    resource_changes={},
                    environmental_changes=[],
                    spawned_entities=[],
                    celestial_effects=[],
                    territory_effects={}
                ),
                duration=60,
                cooldown=300,
                chain_id="test_chain",
                next_events=[f"chain_event_{i+1}"] if i < 2 else None
            )
            events.append(event)
            self.processor.active_events[event.event_id] = event

        # Start with first event
        self.processor.add_event(events[0])
        
        # Verify first event activated
        self.assertIn("chain_event_0", self.processor.event_states)
        self.assertTrue(self.processor.event_states["chain_event_0"].is_active)

        # Process chain
        self.processor.update(self.mock_game_state)
        
        # Verify subsequent events are pending
        self.assertIn(events[1], self.processor.pending_events)
        self.assertIn(events[2], self.processor.pending_events)

    def test_concurrent_event_processing(self):
        """Test processing of multiple concurrent events"""
        events = []
        for i in range(10):
            event = Event(
                event_id=f"concurrent_event_{i}",
                name=f"Concurrent Event {i}",
                event_type=EventType.CELESTIAL,
                trigger=EventTrigger.TIME,
                requirements=EventRequirements(
                    player_level=5,
                    faction_reputation=None,
                    completed_events=None,
                    celestial_alignment=None,
                    environmental_conditions=None,
                    required_items=None
                ),
                effects=EventEffects(
                    faction_reputation_changes={"celestial_order": 10},
                    resource_changes={"gold": 1.1},
                    environmental_changes=[f"effect_{i}"],
                    spawned_entities=[],
                    celestial_effects=[],
                    territory_effects={}
                ),
                duration=60,
                cooldown=300
            )
            events.append(event)
            self.processor.add_event(event)

        # Process all events
        self.processor.update(self.mock_game_state)

        # Verify all events are active
        self.assertEqual(len(self.processor.active_events), 10)
        self.assertEqual(len(self.processor.event_states), 10)

        # Verify cumulative effects
        self.assertEqual(
            self.mock_game_state["faction_reputation"]["celestial_order"],
            200  # 100 + (10 * 10)
        )
        self.assertEqual(len(self.mock_game_state["environmental_conditions"]), 12)  # 2 initial + 10 new

    def test_event_cleanup_edge_cases(self):
        """Test cleanup of events in edge cases"""
        # Create event with missing territory
        event = Event(
            event_id="cleanup_test",
            name="Cleanup Test",
            event_type=EventType.CELESTIAL,
            trigger=EventTrigger.TIME,
            requirements=EventRequirements(
                player_level=5,
                faction_reputation=None,
                completed_events=None,
                celestial_alignment=None,
                environmental_conditions=None,
                required_items=None
            ),
            effects=EventEffects(
                faction_reputation_changes={},
                resource_changes={},
                environmental_changes=["test_condition"],
                spawned_entities=["test_entity"],
                celestial_effects=["test_effect"],
                territory_effects={"nonexistent_territory": "test_effect"}
            ),
            duration=60,
            cooldown=300
        )

        # Apply and remove effects (should not raise exceptions)
        self.processor.apply_effects(event.effects, self.mock_game_state)
        self.processor.remove_effects(event.effects, self.mock_game_state)

    @patch('time.time')
    def test_event_timing_edge_cases(self, mock_time):
        """Test event timing edge cases"""
        start_time = 1000.0
        mock_time.return_value = start_time

        # Create event with zero duration
        event = Event(
            event_id="timing_test",
            name="Timing Test",
            event_type=EventType.CELESTIAL,
            trigger=EventTrigger.TIME,
            requirements=EventRequirements(
                player_level=5,
                faction_reputation=None,
                completed_events=None,
                celestial_alignment=None,
                environmental_conditions=None,
                required_items=None
            ),
            effects=EventEffects(
                faction_reputation_changes={},
                resource_changes={},
                environmental_changes=[],
                spawned_entities=[],
                celestial_effects=[],
                territory_effects={}
            ),
            duration=0,
            cooldown=0
        )

        self.processor.add_event(event)
        self.processor.update(self.mock_game_state)

        # Event should be completed immediately
        self.assertIn(event.event_id, self.processor.completed_events)

    def test_requirement_edge_cases(self):
        """Test requirement checking edge cases"""
        # Test with empty game state
        empty_game_state = {}
        requirements = EventRequirements(
            player_level=None,
            faction_reputation=None,
            completed_events=None,
            celestial_alignment=None,
            environmental_conditions=None,
            required_items=None
        )

        # Should pass with no requirements
        self.assertTrue(self.processor.check_requirements(requirements, empty_game_state))

        # Test with invalid faction
        requirements.faction_reputation = {"nonexistent_faction": 100}
        self.assertFalse(self.processor.check_requirements(requirements, empty_game_state))

        # Test with invalid completed event
        requirements.completed_events = ["nonexistent_event"]
        self.assertFalse(self.processor.check_requirements(requirements, empty_game_state))

    @patch('time.time')
    def test_performance_stress(self, mock_time):
        """Test performance under stress"""
        start_time = 1000.0
        mock_time.return_value = start_time

        # Create large number of events
        num_events = 100
        events = []
        for i in range(num_events):
            event = Event(
                event_id=f"stress_test_{i}",
                name=f"Stress Test {i}",
                event_type=EventType.CELESTIAL,
                trigger=EventTrigger.TIME,
                requirements=EventRequirements(
                    player_level=5,
                    faction_reputation=None,
                    completed_events=None,
                    celestial_alignment=None,
                    environmental_conditions=None,
                    required_items=None
                ),
                effects=EventEffects(
                    faction_reputation_changes={"celestial_order": 1},
                    resource_changes={"gold": 1.01},
                    environmental_changes=[f"effect_{i}"],
                    spawned_entities=[f"entity_{i}"],
                    celestial_effects=[f"celestial_{i}"],
                    territory_effects={"mystic_valley": f"territory_{i}"}
                ),
                duration=60,
                cooldown=300
            )
            events.append(event)
            self.processor.add_event(event)

        # Process events and measure time
        start_process = time.time()
        self.processor.update(self.mock_game_state)
        end_process = time.time()

        process_time = end_process - start_process
        self.assertLess(process_time, 1.0)  # Should process 100 events in less than 1 second

        # Verify all events were processed
        self.assertEqual(len(self.processor.active_events), num_events)
        self.assertEqual(
            len(self.mock_game_state["territories"]["mystic_valley"]["active_effects"]),
            num_events
        ) 