from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
import random
import time

from weather_system import WeatherSystem, WeatherType, CelestialPattern, MagicalStorm
from economic_system import EconomicSystem, MarketEvent, ResourceType, TradeGoodCategory

class WeatherEconomicEffect(Enum):
    TRADE_ROUTE_DISRUPTION = "trade_route_disruption"
    RESOURCE_ABUNDANCE = "resource_abundance"
    RESOURCE_SCARCITY = "resource_scarcity"
    MARKET_ISOLATION = "market_isolation"
    SMUGGLING_OPPORTUNITY = "smuggling_opportunity"
    CELESTIAL_MARKET = "celestial_market"

@dataclass
class WeatherMarketModifier:
    """Represents how weather affects market conditions"""
    price_multiplier: float
    supply_modifier: float
    demand_modifier: float
    trade_route_risk: float
    duration: float
    affected_resources: List[ResourceType]
    affected_categories: List[TradeGoodCategory]

class WeatherEconomicIntegration:
    def __init__(self, weather_system: WeatherSystem, economic_system: EconomicSystem):
        self.weather_system = weather_system
        self.economic_system = economic_system
        self.active_effects: Dict[str, List[WeatherMarketModifier]] = {}
        self.logger = self._setup_logger()
        
        # Weather effect configurations
        self.weather_effects = {
            WeatherType.STORM: WeatherMarketModifier(
                price_multiplier=1.2,
                supply_modifier=0.7,
                demand_modifier=1.1,
                trade_route_risk=1.5,
                duration=3600,
                affected_resources=[
                    ResourceType.FOOD,
                    ResourceType.WATER,
                    ResourceType.WOOD
                ],
                affected_categories=[
                    TradeGoodCategory.RAW_MATERIALS,
                    TradeGoodCategory.CONSUMABLES
                ]
            ),
            WeatherType.CLEAR: WeatherMarketModifier(
                price_multiplier=1.0,
                supply_modifier=1.2,
                demand_modifier=1.0,
                trade_route_risk=0.8,
                duration=7200,
                affected_resources=[],
                affected_categories=[]
            )
        }
        
        # Celestial weather effects
        self.celestial_effects = {
            "CELESTIAL_CONVERGENCE": WeatherMarketModifier(
                price_multiplier=2.0,
                supply_modifier=0.5,
                demand_modifier=1.5,
                trade_route_risk=1.2,
                duration=1800,
                affected_resources=[
                    ResourceType.MANA_CRYSTAL,
                    ResourceType.STARDUST,
                    ResourceType.CELESTIAL_SILVER
                ],
                affected_categories=[
                    TradeGoodCategory.CRAFTING_SUPPLIES,
                    TradeGoodCategory.LUXURY_GOODS
                ]
            ),
            "VOID_STORM": WeatherMarketModifier(
                price_multiplier=1.5,
                supply_modifier=0.3,
                demand_modifier=2.0,
                trade_route_risk=2.0,
                duration=900,
                affected_resources=[
                    ResourceType.VOID_ESSENCE,
                    ResourceType.CHAOS_FRAGMENT
                ],
                affected_categories=[
                    TradeGoodCategory.FORBIDDEN_ARTIFACTS,
                    TradeGoodCategory.RESTRICTED_MATERIALS
                ]
            )
        }

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("WeatherEconomicIntegration")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def update(self, delta_time: float):
        """Update weather effects on economy"""
        current_time = time.time()
        
        # Process regular weather effects
        for location, weather in self.weather_system.get_weather_conditions().items():
            if weather.weather_type in self.weather_effects:
                self._apply_weather_effect(location, weather.weather_type)
        
        # Process celestial patterns
        for pattern in self.weather_system.get_active_celestial_patterns():
            self._apply_celestial_effect(pattern)
        
        # Process magical storms
        for storm in self.weather_system.get_active_magical_storms():
            self._apply_magical_storm_effect(storm)
        
        # Clean up expired effects
        self._cleanup_expired_effects(current_time)

    def _apply_weather_effect(self, location: str, weather_type: WeatherType):
        """Apply weather effects to market conditions"""
        if weather_type not in self.weather_effects:
            return
            
        modifier = self.weather_effects[weather_type]
        
        # Apply to regular markets
        if location in self.economic_system.markets:
            market = self.economic_system.markets[location]
            for resource_type, item in market.items():
                if (resource_type in modifier.affected_resources or
                    item.category in modifier.affected_categories):
                    item.current_price *= modifier.price_multiplier
                    item.supply *= modifier.supply_modifier
                    item.demand *= modifier.demand_modifier
        
        # Apply to trade routes
        for route in self.economic_system.trade_routes:
            if route.source_location == location or route.destination_location == location:
                route.risk_level *= modifier.trade_route_risk
                
        # Record active effect
        if location not in self.active_effects:
            self.active_effects[location] = []
        self.active_effects[location].append(modifier)

    def _apply_celestial_effect(self, pattern: CelestialPattern):
        """Apply celestial weather effects to markets"""
        if pattern.pattern_type not in self.celestial_effects:
            return
            
        modifier = self.celestial_effects[pattern.pattern_type]
        
        # Create celestial market event
        self.economic_system.create_celestial_market_effect(
            MarketEvent.CELESTIAL_SURGE,
            pattern.alignment,
            duration=modifier.duration
        )
        
        # Apply special effects to dimensional markets
        if pattern.pattern_type in self.economic_system.dimensional_markets:
            market = self.economic_system.dimensional_markets[pattern.pattern_type]
            for resource_type, item in market.items():
                if resource_type in modifier.affected_resources:
                    item.current_price *= modifier.price_multiplier
                    item.supply *= modifier.supply_modifier
                    
        self.logger.info(f"Applied celestial effect: {pattern.pattern_type}")

    def _apply_magical_storm_effect(self, storm: MagicalStorm):
        """Apply magical storm effects to markets"""
        # Create special market opportunities
        if random.random() < 0.3:  # 30% chance
            for location in self.economic_system.markets:
                if storm.affects_location(location):
                    # Create temporary black market
                    if location not in self.economic_system.black_markets:
                        self.economic_system.create_black_market(location)
                    
                    # Add special storm-related items
                    black_market = self.economic_system.black_markets[location]
                    self.economic_system._generate_black_market_goods(
                        black_market,
                        TradeGoodCategory.FORBIDDEN_ARTIFACTS,
                        count=1
                    )
        
        # Affect existing black markets
        for location, black_market in self.economic_system.black_markets.items():
            if storm.affects_location(location):
                # Reduce guard activity during storms
                black_market.guard_activity *= 0.7
                # Increase available contraband
                black_market.raid_chance *= 0.5
                
        self.logger.info(f"Applied magical storm effect: {storm.storm_type}")

    def _cleanup_expired_effects(self, current_time: float):
        """Remove expired weather effects"""
        for location in list(self.active_effects.keys()):
            self.active_effects[location] = [
                effect for effect in self.active_effects[location]
                if current_time - effect.start_time < effect.duration
            ]
            if not self.active_effects[location]:
                del self.active_effects[location]

    def get_active_effects(self, location: str) -> List[WeatherEconomicEffect]:
        """Get active weather-economic effects for a location"""
        if location not in self.active_effects:
            return []
            
        return [
            WeatherEconomicEffect(effect.effect_type)
            for effect in self.active_effects[location]
        ]

    def get_market_weather_status(self, location: str) -> Dict[str, any]:
        """Get current weather impact on market"""
        if location not in self.economic_system.markets:
            return {"error": "Market not found"}
            
        active_effects = self.get_active_effects(location)
        weather = self.weather_system.get_weather_conditions().get(location)
        
        return {
            "location": location,
            "weather_type": weather.weather_type if weather else None,
            "active_effects": [effect.value for effect in active_effects],
            "trade_route_status": self._get_trade_route_status(location),
            "market_modifiers": self._get_market_modifiers(location)
        }

    def _get_trade_route_status(self, location: str) -> Dict[str, float]:
        """Get status of trade routes affected by weather"""
        status = {}
        for route in self.economic_system.trade_routes:
            if route.source_location == location or route.destination_location == location:
                status[f"{route.source_location}-{route.destination_location}"] = route.risk_level
        return status

    def _get_market_modifiers(self, location: str) -> Dict[str, float]:
        """Get active market modifiers from weather"""
        if location not in self.active_effects:
            return {}
            
        modifiers = {}
        for effect in self.active_effects[location]:
            modifiers.update({
                "price_multiplier": effect.price_multiplier,
                "supply_modifier": effect.supply_modifier,
                "demand_modifier": effect.demand_modifier,
                "trade_risk": effect.trade_route_risk
            })
        return modifiers 