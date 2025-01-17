import unittest
from unittest.mock import Mock, patch
import time
from typing import Dict, List, Set

from faction_territory_system import (
    FactionTerritorySystem,
    TerritoryType,
    ResourceNodeType,
    InfluencePointType,
    Territory,
    ResourceNode,
    InfluencePoint
)
from faction_alliance_system import (
    FactionAllianceSystem,
    AllianceType,
    AllianceStatus,
    Alliance,
    RitualCooperation
)
from weather_system import CelestialPattern

class TestFactionSystems(unittest.TestCase):
    def setUp(self):
        self.territory_system = FactionTerritorySystem()
        self.alliance_system = FactionAllianceSystem()
        
        # Test factions
        self.celestial_order = "Celestial Order"
        self.void_seekers = "Void Seekers"
        self.primal_circle = "Primal Circle"
        
        # Test territory
        self.test_territory = self.territory_system.create_territory(
            name="Crystal Valley",
            territory_type=TerritoryType.CELESTIAL,
            controlling_faction=self.celestial_order,
            strategic_value=75.0
        )

    def test_territory_creation(self):
        """Test territory creation and initialization"""
        self.assertIn("Crystal Valley", self.territory_system.territories)
        territory = self.territory_system.territories["Crystal Valley"]
        
        self.assertEqual(territory.name, "Crystal Valley")
        self.assertEqual(territory.territory_type, TerritoryType.CELESTIAL)
        self.assertEqual(territory.controlling_faction, self.celestial_order)
        self.assertEqual(territory.strategic_value, 75.0)
        self.assertTrue(0.7 <= territory.magical_stability <= 1.0)
        self.assertTrue(0.0 <= territory.celestial_alignment <= 1.0)

    def test_resource_node_management(self):
        """Test resource node creation and management"""
        # Add resource node
        node = self.territory_system.add_resource_node(
            territory_name="Crystal Valley",
            node_name="Celestial Anchor",
            node_type=ResourceNodeType.CELESTIAL_ANCHOR,
            base_yield=100.0,
            quality=0.9
        )
        
        self.assertIsNotNone(node)
        self.assertEqual(node.node_type, ResourceNodeType.CELESTIAL_ANCHOR)
        self.assertEqual(node.base_yield, 100.0)
        self.assertEqual(node.quality, 0.9)
        self.assertTrue(0.5 <= node.magical_resonance <= 1.5)

    def test_influence_point_creation(self):
        """Test influence point creation and abilities"""
        # Create influence point
        point = self.territory_system.create_influence_point(
            territory_name="Crystal Valley",
            point_name="Observatory",
            point_type=InfluencePointType.OBSERVATORY,
            controlling_faction=self.celestial_order
        )
        
        self.assertIsNotNone(point)
        self.assertEqual(point.point_type, InfluencePointType.OBSERVATORY)
        self.assertEqual(point.controlling_faction, self.celestial_order)
        self.assertIn("celestial_scrying", point.special_abilities)
        self.assertIn("weather_prediction", point.special_abilities)

    def test_territory_control_update(self):
        """Test territory control mechanics"""
        # Add competing influence
        self.territory_system.faction_influence["Crystal Valley"][self.void_seekers] = 80.0
        
        # Update control
        self.territory_system.update_territory_control("Crystal Valley")
        
        # Verify control change
        territory = self.territory_system.territories["Crystal Valley"]
        self.assertEqual(territory.controlling_faction, self.void_seekers)
        
        # Check resource node control transfer
        for node in territory.resource_nodes.values():
            self.assertEqual(node.controlling_faction, self.void_seekers)

    def test_celestial_effect_on_territory(self):
        """Test celestial pattern effects on territory"""
        # Add resource node
        self.territory_system.add_resource_node(
            territory_name="Crystal Valley",
            node_name="Mana Well",
            node_type=ResourceNodeType.MANA_WELL,
            base_yield=100.0
        )
        
        # Create celestial pattern
        pattern = Mock(
            pattern_type="CELESTIAL_CONVERGENCE",
            alignment=TerritoryType.CELESTIAL,
            intensity=0.8
        )
        
        # Process effect
        self.territory_system.process_celestial_effect("Crystal Valley", pattern)
        
        # Verify effects
        territory = self.territory_system.territories["Crystal Valley"]
        self.assertTrue(territory.magical_stability > 0.7)
        
        node = territory.resource_nodes["Mana Well"]
        self.assertTrue(node.current_yield > node.base_yield)

    def test_ritual_network_creation(self):
        """Test ritual network creation and power calculation"""
        # Create ritual points
        points = ["Circle1", "Circle2", "Circle3"]
        for point_name in points:
            self.territory_system.create_influence_point(
                territory_name="Crystal Valley",
                point_name=point_name,
                point_type=InfluencePointType.RITUAL_CIRCLE,
                controlling_faction=self.celestial_order
            )
            
        # Create network
        success = self.territory_system.create_ritual_network(
            "Crystal Valley",
            points
        )
        
        self.assertTrue(success)
        self.assertEqual(
            len(self.territory_system.ritual_networks["Crystal Valley"]),
            3
        )
        
        # Calculate power
        power = self.territory_system.calculate_ritual_power(
            "Crystal Valley",
            points
        )
        
        self.assertTrue(power > 0)

    def test_alliance_creation(self):
        """Test alliance creation and initialization"""
        # Propose alliance
        self.alliance_system.faction_relations[self.celestial_order][self.primal_circle] = 0.5
        
        alliance = self.alliance_system.propose_alliance(
            alliance_type=AllianceType.CELESTIAL,
            proposing_faction=self.celestial_order,
            target_faction=self.primal_circle,
            conditions={"mutual_defense": True}
        )
        
        self.assertIsNotNone(alliance)
        self.assertEqual(alliance.alliance_type, AllianceType.CELESTIAL)
        self.assertEqual(len(alliance.member_factions), 2)
        self.assertEqual(alliance.status, AllianceStatus.PROPOSED)
        self.assertTrue(0.7 <= alliance.celestial_resonance <= 1.3)

    def test_alliance_benefits(self):
        """Test alliance benefit calculations"""
        # Create alliance
        alliance = self.alliance_system.propose_alliance(
            alliance_type=AllianceType.RITUAL,
            proposing_faction=self.celestial_order,
            target_faction=self.primal_circle,
            conditions={}
        )
        
        # Verify benefits
        self.assertIn("ritual_power", alliance.benefits)
        self.assertIn("cooperation_bonus", alliance.benefits)
        self.assertIn("magical_resonance", alliance.benefits)

    def test_celestial_impact_on_alliance(self):
        """Test celestial pattern effects on alliance"""
        # Create alliance
        alliance = self.alliance_system.propose_alliance(
            alliance_type=AllianceType.CELESTIAL,
            proposing_faction=self.celestial_order,
            target_faction=self.primal_circle,
            conditions={}
        )
        
        alliance_id = next(iter(self.alliance_system.alliances.keys()))
        
        # Create celestial pattern
        pattern = Mock(
            pattern_type="CELESTIAL_CONVERGENCE",
            alignment=AllianceType.CELESTIAL,
            intensity=0.8,
            duration=3600
        )
        
        # Process impact
        self.alliance_system.process_celestial_impact(alliance_id, pattern)
        
        # Verify effects
        alliance = self.alliance_system.alliances[alliance_id]
        self.assertTrue(alliance.strength > 0.5)
        self.assertTrue(self.alliance_system.alliance_power_modifiers[alliance_id] > 1.0)

    def test_ritual_cooperation(self):
        """Test ritual cooperation between allied factions"""
        # Create alliances
        alliance1 = self.alliance_system.propose_alliance(
            alliance_type=AllianceType.RITUAL,
            proposing_faction=self.celestial_order,
            target_faction=self.primal_circle,
            conditions={}
        )
        
        alliance2 = self.alliance_system.propose_alliance(
            alliance_type=AllianceType.MAGICAL,
            proposing_faction=self.void_seekers,
            target_faction=self.primal_circle,
            conditions={}
        )
        
        alliance_ids = list(self.alliance_system.alliances.keys())
        
        # Accept alliances
        for alliance_id in alliance_ids:
            self.alliance_system.accept_alliance(alliance_id)
            
        # Create ritual cooperation
        cooperation = self.alliance_system.create_ritual_cooperation(
            ritual_type="celestial_convergence",
            participating_alliances=alliance_ids,
            territory_name="Crystal Valley"
        )
        
        self.assertIsNotNone(cooperation)
        self.assertTrue(len(cooperation.participating_factions) >= 2)
        self.assertTrue(0.0 <= cooperation.success_chance <= 1.0)
        self.assertTrue(cooperation.territory_bonus > 0)

    def test_integrated_systems(self):
        """Test integration between territory and alliance systems"""
        # Create territory setup
        self.territory_system.add_resource_node(
            territory_name="Crystal Valley",
            node_name="Celestial Anchor",
            node_type=ResourceNodeType.CELESTIAL_ANCHOR,
            base_yield=100.0
        )
        
        self.territory_system.create_influence_point(
            territory_name="Crystal Valley",
            point_name="Observatory",
            point_type=InfluencePointType.OBSERVATORY,
            controlling_faction=self.celestial_order
        )
        
        # Create alliance
        alliance = self.alliance_system.propose_alliance(
            alliance_type=AllianceType.CELESTIAL,
            proposing_faction=self.celestial_order,
            target_faction=self.primal_circle,
            conditions={}
        )
        
        alliance_id = next(iter(self.alliance_system.alliances.keys()))
        self.alliance_system.accept_alliance(alliance_id)
        
        # Create celestial pattern
        pattern = Mock(
            pattern_type="CELESTIAL_CONVERGENCE",
            alignment=TerritoryType.CELESTIAL,
            intensity=0.8,
            duration=3600
        )
        
        # Process effects
        self.territory_system.process_celestial_effect("Crystal Valley", pattern)
        self.alliance_system.process_celestial_impact(alliance_id, pattern)
        
        # Verify integrated effects
        territory = self.territory_system.territories["Crystal Valley"]
        alliance = self.alliance_system.alliances[alliance_id]
        
        self.assertTrue(territory.magical_stability > 0.7)
        self.assertTrue(alliance.strength > 0.5)
        
        # Create ritual cooperation in territory
        cooperation = self.alliance_system.create_ritual_cooperation(
            ritual_type="celestial_convergence",
            participating_alliances=[alliance_id],
            territory_name="Crystal Valley"
        )
        
        self.assertTrue(cooperation.success_chance > 0.5)
        self.assertTrue(cooperation.territory_bonus > 0) 