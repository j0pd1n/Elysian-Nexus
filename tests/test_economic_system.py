import unittest
from unittest.mock import Mock, patch, ANY
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from ..economic_system import (
    EconomicSystem, MarketItem, TradeGoodCategory,
    ResourceType, MarketEvent, CelestialAlignment,
    BlackMarket, SmugglingRoute
)

# Test configuration constants
TEST_TIMEOUT = 30  # seconds
DEFAULT_MARKET_UPDATE_INTERVAL = 3600  # 1 hour in seconds
MAX_ITEMS_PER_MARKET = 100

# Test data constants
TEST_LOCATIONS = [
    "central_market",
    "black_market_hub",
    "trading_outpost",
    "celestial_bazaar",
    "void_market"
]

TEST_RESOURCES = [
    ResourceType.MANA_CRYSTAL,
    ResourceType.VOID_ESSENCE,
    ResourceType.CHAOS_FRAGMENT,
    ResourceType.ASTRAL_DUST,
    ResourceType.CELESTIAL_SILVER
]

TEST_CATEGORIES = [
    TradeGoodCategory.CONTRABAND,
    TradeGoodCategory.FORBIDDEN_ARTIFACTS,
    TradeGoodCategory.RESTRICTED_MATERIALS,
    TradeGoodCategory.CRAFTING_SUPPLIES
]

class MarketEvent(Enum):
    CELESTIAL_SURGE = "CELESTIAL_SURGE"
    VOID_MARKET = "VOID_MARKET"
    ASTRAL_TRADING = "ASTRAL_TRADING"

class TestEconomicSystem(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.economic_system = EconomicSystem()
        
        # Set up test markets
        self.test_location = TEST_LOCATIONS[0]
        self.black_market_location = TEST_LOCATIONS[1]
        
        # Set up a regular market
        self.economic_system.create_market(self.test_location)
        
        # Set up a black market
        self.black_market = self.economic_system.create_black_market(self.black_market_location)
        
        # Initialize test items
        self.test_items = {}
        for resource in TEST_RESOURCES:
            self.test_items[resource] = MarketItem(
                resource_type=resource,
                base_price=100,
                current_price=100,
                quantity=10,
                demand=1.0,
                supply=1.0,
                category=TradeGoodCategory.CRAFTING_SUPPLIES,
                quality=1.0,
                last_update=time.time()
            )
            
        # Add test items to regular market
        for resource, item in self.test_items.items():
            self.economic_system.markets[self.test_location][resource] = item.copy()
            
    def tearDown(self):
        """Clean up test fixtures after each test method."""
        self.economic_system.cleanup()
        self.economic_system = None
        self.test_items = None
        self.black_market = None

    def test_black_market_creation(self):
        """Test black market initialization and properties"""
        # Test basic creation
        self.assertIn(self.black_market_location, self.economic_system.black_markets)
        black_market = self.economic_system.black_markets[self.black_market_location]
        
        # Check basic properties with specific ranges
        self.assertGreaterEqual(black_market.risk_level, 0.2, "Risk level too low")
        self.assertLessEqual(black_market.risk_level, 0.8, "Risk level too high")
        self.assertGreaterEqual(black_market.guard_activity, 0.1, "Guard activity too low")
        self.assertLessEqual(black_market.guard_activity, 0.9, "Guard activity too high")
        self.assertGreaterEqual(black_market.raid_chance, 0.05, "Raid chance too low")
        self.assertLessEqual(black_market.raid_chance, 0.3, "Raid chance too high")
        
        # Check initial goods
        self.assertTrue(len(black_market.available_goods) > 0, "No goods in black market")
        for item in black_market.available_goods.values():
            self.assertIn(item.category, TEST_CATEGORIES[:3], "Invalid item category")
            self.assertGreater(item.current_price, item.base_price, "Black market price not marked up")
            
        # Test invalid creation
        with self.assertRaises(ValueError):
            self.economic_system.create_black_market("")
        with self.assertRaises(ValueError):
            self.economic_system.create_black_market(None)
        with self.assertRaises(ValueError):
            self.economic_system.create_black_market(self.black_market_location)  # Duplicate

    def test_smuggling_route_creation(self):
        """Test creation and validation of smuggling routes"""
        # Test valid route creation
        test_goods = TEST_RESOURCES[:2]
        route = self.economic_system.create_smuggling_route(
            self.black_market_location,
            self.test_location,
            test_goods
        )
        
        # Verify route properties
        self.assertIsNotNone(route)
        self.assertEqual(route.source_location, self.black_market_location)
        self.assertEqual(route.destination_location, self.test_location)
        self.assertEqual(route.goods, test_goods)
        self.assertGreaterEqual(route.risk_level, 0.1)
        self.assertLessEqual(route.risk_level, 0.9)
        
        # Test route constraints
        with self.assertRaises(ValueError):
            # Same source and destination
            self.economic_system.create_smuggling_route(
                self.test_location,
                self.test_location,
                test_goods
            )
            
        with self.assertRaises(ValueError):
            # Empty goods list
            self.economic_system.create_smuggling_route(
                self.black_market_location,
                self.test_location,
                []
            )
            
        with self.assertRaises(ValueError):
            # Invalid locations
            self.economic_system.create_smuggling_route(
                "nonexistent_market",
                self.test_location,
                test_goods
            )

    @patch('time.time')
    def test_black_market_update(self, mock_time):
        """Test black market state updates and price fluctuations"""
        mock_time.return_value = 0
        
        # Record initial state
        initial_prices = {
            resource: item.current_price
            for resource, item in self.black_market.available_goods.items()
        }
        initial_risk = self.black_market.risk_level
        initial_guard = self.black_market.guard_activity
        
        # Simulate time passing
        mock_time.return_value = DEFAULT_MARKET_UPDATE_INTERVAL
        self.economic_system.update_black_markets(DEFAULT_MARKET_UPDATE_INTERVAL)
        
        # Check price changes
        price_changes = False
        for resource, item in self.black_market.available_goods.items():
            if item.current_price != initial_prices[resource]:
                price_changes = True
                # Verify price constraints
                self.assertGreater(item.current_price, 0, "Price dropped to zero or below")
                self.assertLess(
                    item.current_price, 
                    item.base_price * 5, 
                    "Price increased beyond reasonable limits"
                )
        self.assertTrue(price_changes, "No price changes occurred during update")
        
        # Verify state changes
        self.assertNotEqual(self.black_market.risk_level, initial_risk)
        self.assertNotEqual(self.black_market.guard_activity, initial_guard)

    @patch('time.time')
    def test_market_raid(self, mock_time):
        """Test market raid mechanics and effects"""
        mock_time.return_value = 0
        
        # Record initial state
        initial_guard = self.black_market.guard_activity
        initial_risk = self.black_market.risk_level
        initial_goods = len(self.black_market.available_goods)
        
        # Force a raid
        self.economic_system._trigger_market_raid(self.black_market_location)
        
        black_market = self.economic_system.black_markets[self.black_market_location]
        
        # Check raid effects
        self.assertIn(self.black_market_location, self.economic_system.raid_cooldowns)
        self.assertGreater(black_market.guard_activity, initial_guard)
        self.assertGreater(black_market.risk_level, initial_risk)
        
        # Verify goods were confiscated
        self.assertLess(len(black_market.available_goods), initial_goods)
        
        # Test raid cooldown
        with self.assertRaises(ValueError):
            self.economic_system._trigger_market_raid(self.black_market_location)
            
        # Test raid recovery
        mock_time.return_value = DEFAULT_MARKET_UPDATE_INTERVAL * 2
        self.economic_system.update_black_markets(DEFAULT_MARKET_UPDATE_INTERVAL)
        
        # Verify market recovery
        self.assertLess(black_market.guard_activity, initial_guard * 1.5)
        self.assertGreaterEqual(len(black_market.available_goods), initial_goods // 2)

    @patch('time.time')
    def test_celestial_market_effect_creation(self, mock_time):
        """Test creation and validation of celestial market effects"""
        mock_time.return_value = 0
        
        # Test effect creation with different alignments
        for alignment in CelestialAlignment:
            effect = self.economic_system.create_celestial_market_effect(
                MarketEvent.CELESTIAL_SURGE,
                alignment,
                duration=DEFAULT_MARKET_UPDATE_INTERVAL
            )
            
            # Verify effect properties
            self.assertIsNotNone(effect)
            self.assertEqual(effect.event_type, MarketEvent.CELESTIAL_SURGE)
            self.assertEqual(effect.alignment, alignment)
            self.assertEqual(effect.duration, DEFAULT_MARKET_UPDATE_INTERVAL)
            
            # Verify multipliers and modifiers
            self.assertTrue(len(effect.price_multipliers) > 0)
            self.assertTrue(len(effect.trade_modifiers) > 0)
            self.assertTrue(len(effect.affected_categories) > 0)
            
            # Verify multiplier ranges
            for multiplier in effect.price_multipliers.values():
                self.assertGreaterEqual(multiplier, 0.5)
                self.assertLessEqual(multiplier, 2.0)
                
        # Test invalid effect creation
        with self.assertRaises(ValueError):
            self.economic_system.create_celestial_market_effect(
                "INVALID_EVENT",
                CelestialAlignment.SOLAR
            )
            
        with self.assertRaises(ValueError):
            self.economic_system.create_celestial_market_effect(
                MarketEvent.CELESTIAL_SURGE,
                "INVALID_ALIGNMENT"
            )

    @patch('time.time')
    def test_celestial_effect_on_prices(self, mock_time):
        """Test impact of celestial effects on market prices and trading"""
        mock_time.return_value = 0
        
        # Create test items for each resource type
        test_items = {}
        for resource in TEST_RESOURCES:
            test_items[resource] = MarketItem(
                resource_type=resource,
                base_price=100,
                current_price=100,
                quantity=10,
                demand=1.0,
                supply=1.0,
                category=TradeGoodCategory.CRAFTING_SUPPLIES,
                quality=1.0,
                last_update=0
            )
            self.economic_system.markets[self.test_location][resource] = test_items[resource]
        
        # Create celestial effect
        effect = self.economic_system.create_celestial_market_effect(
            MarketEvent.CELESTIAL_SURGE,
            CelestialAlignment.CONVERGENCE,
            duration=DEFAULT_MARKET_UPDATE_INTERVAL
        )
        
        # Record initial prices
        initial_prices = {
            resource: item.current_price
            for resource, item in test_items.items()
        }
        
        # Update market
        mock_time.return_value = DEFAULT_MARKET_UPDATE_INTERVAL // 2
        self.economic_system.update_markets(DEFAULT_MARKET_UPDATE_INTERVAL)
        
        # Verify price changes
        price_changes = False
        for resource, item in test_items.items():
            if resource in effect.price_multipliers:
                expected_min = initial_prices[resource] * effect.price_multipliers[resource] * 0.8
                expected_max = initial_prices[resource] * effect.price_multipliers[resource] * 1.2
                
                self.assertGreaterEqual(
                    item.current_price, 
                    expected_min,
                    f"Price too low for {resource}"
                )
                self.assertLessEqual(
                    item.current_price, 
                    expected_max,
                    f"Price too high for {resource}"
                )
                if item.current_price != initial_prices[resource]:
                    price_changes = True
                    
        self.assertTrue(price_changes, "No price changes occurred from celestial effect")

    @patch('time.time')
    def test_void_market_effects(self, mock_time):
        """Test specific void market event effects and interactions"""
        mock_time.return_value = 0
        
        # Create void market effect
        effect = self.economic_system.create_celestial_market_effect(
            MarketEvent.VOID_MARKET,
            CelestialAlignment.VOID,
            duration=DEFAULT_MARKET_UPDATE_INTERVAL
        )
        
        # Check void essence price reduction
        self.assertIn(ResourceType.VOID_ESSENCE, effect.price_multipliers)
        self.assertTrue(
            effect.price_multipliers[ResourceType.VOID_ESSENCE] < 1.0,
            "Void essence prices should be reduced during void market"
        )
        
        # Check void goods supply increase
        self.assertIn("void_goods_supply", effect.trade_modifiers)
        self.assertTrue(
            effect.trade_modifiers["void_goods_supply"] > 1.0,
            "Void goods supply should increase during void market"
        )
        
        # Test effect on black market
        initial_void_items = len([
            item for item in self.black_market.available_goods.values()
            if item.resource_type == ResourceType.VOID_ESSENCE
        ])
        
        # Update markets
        mock_time.return_value = DEFAULT_MARKET_UPDATE_INTERVAL // 2
        self.economic_system.update_black_markets(DEFAULT_MARKET_UPDATE_INTERVAL)
        
        # Verify increased void essence availability
        current_void_items = len([
            item for item in self.black_market.available_goods.values()
            if item.resource_type == ResourceType.VOID_ESSENCE
        ])
        self.assertGreater(
            current_void_items,
            initial_void_items,
            "Void essence availability should increase during void market"
        )

    @patch('time.time')
    def test_astral_trading_effects(self, mock_time):
        """Test specific astral trading event effects and mechanics"""
        mock_time.return_value = 0
        
        # Create astral trading effect
        effect = self.economic_system.create_celestial_market_effect(
            MarketEvent.ASTRAL_TRADING,
            CelestialAlignment.ASTRAL,
            duration=DEFAULT_MARKET_UPDATE_INTERVAL
        )
        
        # Check astral dust price changes
        self.assertIn(ResourceType.ASTRAL_DUST, effect.price_multipliers)
        astral_multiplier = effect.price_multipliers[ResourceType.ASTRAL_DUST]
        self.assertNotEqual(
            astral_multiplier,
            1.0,
            "Astral dust prices should be affected during astral trading"
        )
        
        # Check travel cost reduction
        self.assertIn("travel_cost", effect.trade_modifiers)
        self.assertTrue(
            effect.trade_modifiers["travel_cost"] < 1.0,
            "Travel costs should be reduced during astral trading"
        )
        
        # Test effect on smuggling routes
        route = self.economic_system.create_smuggling_route(
            self.black_market_location,
            self.test_location,
            [ResourceType.ASTRAL_DUST]
        )
        initial_risk = route.risk_level
        
        # Update with astral effect active
        mock_time.return_value = DEFAULT_MARKET_UPDATE_INTERVAL // 2
        self.economic_system.update_smuggling_routes(DEFAULT_MARKET_UPDATE_INTERVAL)
        
        # Verify reduced risks during astral trading
        self.assertLess(
            route.risk_level,
            initial_risk,
            "Smuggling risks should be reduced during astral trading"
        )

    @patch('time.time')
    def test_market_status_reporting(self, mock_time):
        """Test comprehensive market status reporting and monitoring"""
        mock_time.return_value = 0
        
        # Create various market conditions
        self.economic_system.create_celestial_market_effect(
            MarketEvent.CELESTIAL_SURGE,
            CelestialAlignment.CONVERGENCE
        )
        
        route = self.economic_system.create_smuggling_route(
            self.black_market_location,
            self.test_location,
            [ResourceType.VOID_ESSENCE]
        )
        
        # Get black market status
        status = self.economic_system.get_black_market_status(self.black_market_location)
        
        # Verify status structure
        self.assertEqual(status["location"], self.black_market_location)
        self.assertIn("risk_level", status)
        self.assertIn("guard_activity", status)
        self.assertIn("items", status)
        self.assertIsInstance(status["items"], dict)
        
        # Verify item details
        for item_info in status["items"].values():
            self.assertIn("price", item_info)
            self.assertIn("quantity", item_info)
            self.assertIn("category", item_info)
            
        # Get celestial effects
        effects = self.economic_system.get_celestial_market_effects()
        self.assertIsInstance(effects, list)
        self.assertTrue(len(effects) > 0)
        
        # Verify effect details
        for effect_info in effects:
            self.assertIn("event_type", effect_info)
            self.assertIn("alignment", effect_info)
            self.assertIn("duration", effect_info)
            self.assertIn("active_markets", effect_info)

    def test_integrated_market_behavior(self):
        """Test interaction between regular markets, black markets, and celestial effects"""
        # Create celestial effect
        self.economic_system.create_celestial_market_effect(
            MarketEvent.CELESTIAL_SURGE,
            CelestialAlignment.CONVERGENCE
        )
        
        # Create smuggling route
        goods = [ResourceType.VOID_ESSENCE]
        self.economic_system.create_smuggling_route(
            self.black_market_location,
            self.test_location,
            goods
        )
        
        # Update system
        self.economic_system.update(3600)
        
        # Check effects propagation
        black_market = self.economic_system.black_markets[self.black_market_location]
        self.assertTrue(len(black_market.available_goods) > 0)
        
        # Verify celestial effects are active
        self.assertTrue(len(self.economic_system.celestial_effects) > 0) 