import unittest
from unittest.mock import Mock, patch
import time
from typing import Dict, List

from weather_system import WeatherSystem, WeatherType, CelestialPattern, MagicalStorm
from economic_system import EconomicSystem, ResourceType, TradeGoodCategory, MarketItem, MarketEvent
from weather_economic_integration import (
    WeatherEconomicIntegration,
    WeatherEconomicEffect,
    WeatherMarketModifier
)

class TestWeatherEconomicIntegration(unittest.TestCase):
    def setUp(self):
        self.weather_system = Mock(spec=WeatherSystem)
        self.economic_system = Mock(spec=EconomicSystem)
        self.integration = WeatherEconomicIntegration(
            self.weather_system,
            self.economic_system
        )
        
        # Test location
        self.test_location = "test_market"
        
        # Setup mock market
        self.market_items = {
            ResourceType.FOOD: MarketItem(
                resource_type=ResourceType.FOOD,
                base_price=100,
                current_price=100,
                quantity=10,
                demand=1.0,
                supply=1.0,
                category=TradeGoodCategory.CONSUMABLES,
                quality=1.0,
                last_update=time.time()
            )
        }
        self.economic_system.markets = {self.test_location: self.market_items}

    def test_weather_effect_application(self):
        """Test application of weather effects to markets"""
        # Setup weather conditions
        self.weather_system.get_weather_conditions.return_value = {
            self.test_location: Mock(weather_type=WeatherType.STORM)
        }
        
        # Initial price
        initial_price = self.market_items[ResourceType.FOOD].current_price
        
        # Update integration
        self.integration.update(1.0)
        
        # Check price modification
        self.assertNotEqual(
            self.market_items[ResourceType.FOOD].current_price,
            initial_price
        )
        self.assertTrue(
            self.market_items[ResourceType.FOOD].current_price >
            initial_price
        )

    def test_celestial_pattern_effects(self):
        """Test celestial pattern effects on markets"""
        # Setup celestial pattern
        pattern = Mock(
            pattern_type="CELESTIAL_CONVERGENCE",
            alignment="CONVERGENCE"
        )
        self.weather_system.get_active_celestial_patterns.return_value = [pattern]
        
        # Update integration
        self.integration.update(1.0)
        
        # Verify celestial market effect creation
        self.economic_system.create_celestial_market_effect.assert_called_once()

    def test_magical_storm_effects(self):
        """Test magical storm effects on black markets"""
        # Setup magical storm
        storm = Mock(
            storm_type="CHAOS_STORM",
            affects_location=lambda x: True
        )
        self.weather_system.get_active_magical_storms.return_value = [storm]
        
        # Setup black market
        black_market = Mock(
            guard_activity=1.0,
            raid_chance=0.5
        )
        self.economic_system.black_markets = {
            self.test_location: black_market
        }
        
        # Update integration
        self.integration.update(1.0)
        
        # Verify black market modifications
        self.assertTrue(black_market.guard_activity < 1.0)
        self.assertTrue(black_market.raid_chance < 0.5)

    def test_trade_route_modification(self):
        """Test weather effects on trade routes"""
        # Setup weather
        self.weather_system.get_weather_conditions.return_value = {
            self.test_location: Mock(weather_type=WeatherType.STORM)
        }
        
        # Setup trade route
        route = Mock(
            source_location=self.test_location,
            destination_location="other_market",
            risk_level=1.0
        )
        self.economic_system.trade_routes = [route]
        
        # Update integration
        self.integration.update(1.0)
        
        # Verify risk level increase
        self.assertTrue(route.risk_level > 1.0)

    def test_market_weather_status(self):
        """Test market weather status reporting"""
        # Setup weather conditions
        weather = Mock(weather_type=WeatherType.STORM)
        self.weather_system.get_weather_conditions.return_value = {
            self.test_location: weather
        }
        
        # Get status
        status = self.integration.get_market_weather_status(self.test_location)
        
        # Verify status content
        self.assertEqual(status["location"], self.test_location)
        self.assertEqual(status["weather_type"], WeatherType.STORM)
        self.assertIn("active_effects", status)
        self.assertIn("trade_route_status", status)
        self.assertIn("market_modifiers", status)

    def test_effect_cleanup(self):
        """Test cleanup of expired effects"""
        # Add test effect
        modifier = WeatherMarketModifier(
            price_multiplier=1.2,
            supply_modifier=0.7,
            demand_modifier=1.1,
            trade_route_risk=1.5,
            duration=1,  # Short duration
            affected_resources=[ResourceType.FOOD],
            affected_categories=[TradeGoodCategory.CONSUMABLES]
        )
        self.integration.active_effects[self.test_location] = [modifier]
        
        # Wait for effect to expire
        time.sleep(2)
        
        # Update integration
        self.integration.update(1.0)
        
        # Verify effect cleanup
        self.assertNotIn(self.test_location, self.integration.active_effects)

    def test_void_market_creation(self):
        """Test void market creation during void storms"""
        # Setup void storm
        pattern = Mock(
            pattern_type="VOID_STORM",
            alignment="VOID"
        )
        self.weather_system.get_active_celestial_patterns.return_value = [pattern]
        
        # Update integration
        self.integration.update(1.0)
        
        # Verify void market effect
        self.economic_system.create_celestial_market_effect.assert_called_with(
            MarketEvent.CELESTIAL_SURGE,
            "VOID",
            duration=900
        )

    def test_weather_effect_stacking(self):
        """Test stacking of multiple weather effects"""
        # Setup multiple weather conditions
        self.weather_system.get_weather_conditions.return_value = {
            self.test_location: Mock(weather_type=WeatherType.STORM)
        }
        pattern = Mock(
            pattern_type="CELESTIAL_CONVERGENCE",
            alignment="CONVERGENCE"
        )
        self.weather_system.get_active_celestial_patterns.return_value = [pattern]
        
        # Initial price
        initial_price = self.market_items[ResourceType.FOOD].current_price
        
        # Update integration multiple times
        self.integration.update(1.0)
        self.integration.update(1.0)
        
        # Verify cumulative effect
        final_price = self.market_items[ResourceType.FOOD].current_price
        self.assertTrue(final_price > initial_price)

    def test_market_isolation(self):
        """Test market isolation during severe weather"""
        # Setup severe weather
        self.weather_system.get_weather_conditions.return_value = {
            self.test_location: Mock(
                weather_type=WeatherType.STORM,
                severity=1.0
            )
        }
        
        # Setup trade routes
        route = Mock(
            source_location=self.test_location,
            destination_location="other_market",
            risk_level=1.0,
            active=True
        )
        self.economic_system.trade_routes = [route]
        
        # Update integration
        self.integration.update(1.0)
        
        # Verify trade route risk increase
        self.assertTrue(route.risk_level > 1.5)

    def test_resource_scarcity(self):
        """Test resource scarcity during weather events"""
        # Setup weather
        self.weather_system.get_weather_conditions.return_value = {
            self.test_location: Mock(weather_type=WeatherType.STORM)
        }
        
        # Initial supply
        initial_supply = self.market_items[ResourceType.FOOD].supply
        
        # Update integration
        self.integration.update(1.0)
        
        # Verify supply reduction
        self.assertTrue(
            self.market_items[ResourceType.FOOD].supply <
            initial_supply
        ) 