from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass

class ResourceType(Enum):
    GOLD = "gold"
    WOOD = "wood"
    STONE = "stone"
    IRON = "iron"
    FOOD = "food"
    HERBS = "herbs"

class MarketEvent(Enum):
    PRICE_INCREASE = "price_increase"
    PRICE_DECREASE = "price_decrease"
    SHORTAGE = "shortage"
    SURPLUS = "surplus"
    TRADE_OPPORTUNITY = "trade_opportunity"

@dataclass
class MarketData:
    resource_type: ResourceType
    base_price: float
    current_price: float
    supply: int
    demand: int
    modifiers: Dict[str, float]

class EconomicSystem:
    def __init__(self):
        self.market_data: Dict[ResourceType, MarketData] = {}
        self.active_events: List[MarketEvent] = []
        self.transaction_history: List[Dict] = []
        
    def update_market(self, game_time: int):
        """Update market prices and conditions"""
        # Market update logic here
        pass 