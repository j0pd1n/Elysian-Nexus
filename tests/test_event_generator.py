import unittest
from unittest.mock import Mock, patch
import random
from ..event_system.event_generator import EventGenerator
from ..event_system.event_manager import Event, EventType, EventTrigger, EventRequirements, EventEffects

class TestEventGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = EventGenerator()
        self.mock_game_state = {
            "player_level": 10,
            "faction_reputation": {
                "celestial_order": 100,
                "void_seekers": 75,
                "primal_circle": 50
            },
            "possible_alignments": ["celestial", "void", "primal"],
            "possible_conditions": ["storm", "clear", "mist", "rain"],
            "territories": {
                "mystic_valley": {
                    "resource_nodes": ["mana_crystal", "void_essence", "primal_stone"],
                    "control_level": 0.8,
                    "stability": 0.9
                }
            }
        }

    def test_event_chain_generation(self):
        """Test generation of event chains"""
        chain_id = "test_chain"
        length = 3
        event_types = [EventType.CELESTIAL, EventType.ENVIRONMENTAL]
        base_requirements = EventRequirements(
            player_level=5,
            faction_reputation={"celestial_order": 50},
            completed_events=None,
            celestial_alignment=None,
            environmental_conditions=None,
            required_items=None
        )

        events = self.generator.generate_event_chain(
            chain_id,
            length,
            event_types,
            base_requirements
        )

        self.assertEqual(len(events), length)
        
        # Verify chain properties
        for i, event in enumerate(events):
            self.assertTrue(event.event_id.startswith(chain_id))
            self.assertEqual(event.chain_id, chain_id)
            
            if i < length - 1:
                self.assertEqual(event.next_events, [f"{chain_id}_{i+1}"])
            else:
                self.assertIsNone(event.next_events)

            if i == 0:
                self.assertEqual(event.trigger, EventTrigger.TIME)
            else:
                self.assertEqual(event.trigger, EventTrigger.RITUAL_COMPLETION)

    def test_dynamic_event_generation(self):
        """Test generation of single dynamic events"""
        event = self.generator.generate_dynamic_event(
            EventType.CELESTIAL,
            self.mock_game_state,
            "mystic_valley"
        )

        self.assertIsInstance(event, Event)
        self.assertTrue(event.event_id.startswith("dynamic_celestial"))
        self.assertEqual(event.trigger, EventTrigger.TIME)
        self.assertIsNotNone(event.requirements)
        self.assertIsNotNone(event.effects)

        # Verify territory effects
        self.assertIn("mystic_valley", event.effects.territory_effects)
        for node in self.mock_game_state["territories"]["mystic_valley"]["resource_nodes"]:
            self.assertIn(node, event.effects.resource_changes)

    def test_requirement_scaling(self):
        """Test scaling of requirements based on chain position"""
        base_requirements = EventRequirements(
            player_level=10,
            faction_reputation={"celestial_order": 100},
            completed_events=None,
            celestial_alignment=None,
            environmental_conditions=None,
            required_items=None
        )

        scaled = self.generator._scale_requirements(base_requirements, 2, 4)
        
        # Position 2 in length 4 chain should scale by 1.5
        self.assertEqual(scaled.player_level, 15)  # 10 * 1.5
        self.assertEqual(scaled.faction_reputation["celestial_order"], 150)  # 100 * 1.5

    def test_effect_generation(self):
        """Test generation of effects with scaling"""
        template_effects = {
            "magical_amplification": (1.0, 2.0),
            "reality_instability": (0.1, 0.3),
            "dimensional_rifts": True
        }

        effects = self.generator._generate_effects(template_effects, 1, 3)
        
        # Verify effect structure
        self.assertIsInstance(effects, EventEffects)
        self.assertIsInstance(effects.faction_reputation_changes, dict)
        self.assertIsInstance(effects.resource_changes, dict)
        self.assertIsInstance(effects.environmental_changes, list)
        self.assertIsInstance(effects.spawned_entities, list)
        self.assertIsInstance(effects.celestial_effects, list)
        self.assertIsInstance(effects.territory_effects, dict)

    def test_territory_effect_addition(self):
        """Test addition of territory-specific effects"""
        base_effects = EventEffects(
            faction_reputation_changes={},
            resource_changes={},
            environmental_changes=[],
            spawned_entities=[],
            celestial_effects=[],
            territory_effects={}
        )

        modified_effects = self.generator._add_territory_effects(
            base_effects,
            "mystic_valley",
            self.mock_game_state
        )

        # Verify territory effects were added
        self.assertIn("mystic_valley", modified_effects.territory_effects)
        
        # Verify resource node effects
        for node in self.mock_game_state["territories"]["mystic_valley"]["resource_nodes"]:
            self.assertIn(node, modified_effects.resource_changes)
            self.assertTrue(1.2 <= modified_effects.resource_changes[node] <= 1.5)

    def test_requirement_generation(self):
        """Test generation of requirements based on game state"""
        requirements = self.generator._generate_requirements(
            self.mock_game_state,
            EventType.CELESTIAL
        )

        # Verify player level requirement
        self.assertEqual(requirements.player_level, 8)  # 10 * 0.8
        
        # Verify faction reputation requirements
        for faction, rep in requirements.faction_reputation.items():
            original_rep = self.mock_game_state["faction_reputation"][faction]
            self.assertEqual(rep, int(original_rep * 0.7))

        # Verify celestial alignment for celestial event
        self.assertIn(requirements.celestial_alignment, self.mock_game_state["possible_alignments"])

    def test_template_category_conversion(self):
        """Test conversion of EventType to template category"""
        self.assertEqual(
            self.generator._get_template_category(EventType.CELESTIAL),
            "celestial"
        )
        self.assertEqual(
            self.generator._get_template_category(EventType.ENVIRONMENTAL),
            "environmental"
        )
        self.assertEqual(
            self.generator._get_template_category(EventType.FACTION),
            "faction"
        ) 