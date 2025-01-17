from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, NamedTuple
from dataclasses import dataclass
import random
from visual_system import VisualSystem, TextColor
from faction_system import FactionType, FactionAlignment

class MarketTrend(Enum):
    """Market trends affecting item prices"""
    CRASHING = "Crashing"     # 📉
    DECLINING = "Declining"   # ↘️
    STABLE = "Stable"         # ➡️
    GROWING = "Growing"       # ↗️
    BOOMING = "Booming"       # 📈

@dataclass
class ItemDurability:
    """Tracks item condition and repair costs"""
    max_durability: int
    current_durability: int
    repair_cost_multiplier: float = 1.0

    @property
    def durability_percentage(self) -> float:
        return (self.current_durability / self.max_durability) * 100

    @property
    def value_modifier(self) -> float:
        """Calculate how durability affects item value"""
        if self.durability_percentage >= 90:
            return 1.0
        elif self.durability_percentage >= 75:
            return 0.9
        elif self.durability_percentage >= 50:
            return 0.7
        elif self.durability_percentage >= 25:
            return 0.5
        else:
            return 0.3

@dataclass
class BundleDeal:
    """Represents a collection of items sold together at a discount"""
    name: str
    items: Dict[str, int]  # item_id: quantity
    discount: float  # percentage off total price
    duration: int  # in game hours
    theme_bonus: float = 0.0  # additional discount for themed items

@dataclass
class EconomicCrisis:
    """Represents a major market event affecting prices and availability"""
    name: str
    duration: int
    effects: Dict[str, float]  # effect_type: modifier
    affected_regions: Set[str]
    affected_items: Set[str]

    def __post_init__(self):
        if not self.affected_regions:
            self.affected_regions = set()
        if not self.affected_items:
            self.affected_items = set()

@dataclass
class TradeItem:
    """An item that can be traded"""
    id: str
    name: str
    type: TradeItemType
    base_price: int
    quality_level: int = 1  # 1-5, affects value and effectiveness
    rarity: float = 1.0  # Multiplier for base price and availability
    durability: Optional[ItemDurability] = None
    repair_difficulty: float = 1.0  # Multiplier for repair costs
    usage_degradation: float = 1.0  # How quickly item loses durability
    bundle_eligible: bool = True
    crisis_sensitive: bool = False  # Whether item is affected by economic crises
    discovery_chance: float = 1.0  # Chance to appear in merchant's hidden inventory
    barter_value_modifier: float = 1.0  # Affects value in barter trades

    @property
    def current_price(self) -> int:
        """Calculate current price based on quality and durability"""
        price = self.base_price * self.quality_level * self.rarity
        if self.durability:
            price *= self.durability.value_modifier
        return int(price)

@dataclass
class TradeRoute:
    """A trade route between two locations"""
    start_location: str
    end_location: str
    distance: int  # in game hours
    risk_level: float  # 0.0 to 1.0
    banned_items: Set[str]
    faction_control: Optional[FactionType] = None
    caravan_capacity: int = 100
    maintenance_cost: float = 1.0
    seasonal_modifiers: Dict[str, float] = None
    active_events: List[str] = None
    
    def __post_init__(self):
        """Initialize default values for seasonal modifiers and active events"""
        if self.seasonal_modifiers is None:
            self.seasonal_modifiers = {
                "spring": 1.0,  # Standard travel conditions
                "summer": 1.0,  # Standard travel conditions
                "autumn": 1.2,  # Better for land travel
                "winter": 1.5   # Harder to traverse
            }
        if self.active_events is None:
            self.active_events = []

class CurrencyType(Enum):
    GOLD = "Gold"       # 💰
    SILVER = "Silver"   # 🪙
    GEMS = "Gems"       # 💎
    TOKENS = "Tokens"   # 🎫
    FACTION_MARKS = "Faction Marks" # ⚜️

class TradeItemType(Enum):
    WEAPON = "Weapon"     # ⚔️
    ARMOR = "Armor"       # 🛡️
    POTION = "Potion"    # 🧃
    FOOD = "Food"        # 🍞
    MATERIAL = "Material" # 📦
    ARTIFACT = "Artifact" # 🎁
    SCROLL = "Scroll"    # 📜
    GEM = "Gem"         # 💎
    RELIC = "Relic"     # 🏺
    ESSENCE = "Essence"  # ✨ 

class MerchantPersonality(Enum):
    """Merchant personality types affecting trading behavior"""
    FRIENDLY = "Friendly"      # 😊
    SHREWD = "Shrewd"         # 🧐
    GENEROUS = "Generous"     # 🤝
    COLLECTOR = "Collector"   # 🏺
    MYSTERIOUS = "Mysterious" # 🔮
    MENTOR = "Mentor"        # 📚

@dataclass
class Merchant:
    """A merchant that trades items with players"""
    id: str
    name: str
    specialization: MerchantSpecialization
    personality: MerchantPersonality
    inventory: Dict[str, int]  # item_id: quantity
    faction_alignment: FactionAlignment
    market_influence: float
    specialty_crafting: Dict[TradeItemType, float] = None
    repair_skills: Dict[TradeItemType, float] = None  # type: skill_level
    trade_knowledge: Dict[str, float] = None  # item_id: knowledge_level
    active_bundles: Dict[str, BundleDeal] = None
    specialization_experience: Dict[MerchantSpecialization, float] = None
    learned_techniques: Set[str] = None
    hidden_inventory: Dict[str, int] = None  # Rare/special items
    rival_merchants: Set[str] = None
    special_deals: Dict[str, float] = None  # item_id: price_modifier
    barter_threshold: float = 0.8  # Minimum satisfaction to accept barter
    item_qualities: Dict[str, int] = None  # item_id: quality_level
    item_prices: Dict[str, int] = None  # item_id: custom_price

    def __post_init__(self):
        """Initialize default values for collections"""
        if self.specialty_crafting is None:
            self.specialty_crafting = {}
        if self.repair_skills is None:
            self.repair_skills = {}
        if self.trade_knowledge is None:
            self.trade_knowledge = {}
        if self.active_bundles is None:
            self.active_bundles = {}
        if self.specialization_experience is None:
            self.specialization_experience = {}
        if self.learned_techniques is None:
            self.learned_techniques = set()
        if self.hidden_inventory is None:
            self.hidden_inventory = {}
        if self.rival_merchants is None:
            self.rival_merchants = set()
        if self.special_deals is None:
            self.special_deals = {}
        if self.item_qualities is None:
            self.item_qualities = {}
        if self.item_prices is None:
            self.item_prices = {} 

@dataclass
class TradeManager:
    """Manages all trading-related functionality"""
    visual_system: VisualSystem
    merchants: Dict[str, Merchant] = None
    items: Dict[str, TradeItem] = None
    trade_network: Dict[str, TradeRoute] = None
    active_crises: List[EconomicCrisis] = None
    bundle_themes: Dict[str, Set[str]] = None
    market_state: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize collections and load initial data"""
        if self.merchants is None:
            self.merchants = {}
        if self.items is None:
            self.items = {}
        if self.trade_network is None:
            self.trade_network = {}
        if self.active_crises is None:
            self.active_crises = []
        if self.bundle_themes is None:
            self.bundle_themes = {
                "warrior": {"sword", "shield", "armor", "potion"},
                "mage": {"staff", "robe", "scroll", "mana_potion"},
                "adventurer": {"backpack", "map", "compass", "rations"}
            }
        if self.market_state is None:
            self.market_state = {
                "price_trends": {},
                "current_events": [],
                "supply_demand": {}
            }

    def calculate_repair_cost(self, item_id: str, merchant_id: str) -> Optional[int]:
        """Calculate cost to repair an item"""
        if item_id not in self.items or merchant_id not in self.merchants:
            return None

        item = self.items[item_id]
        merchant = self.merchants[merchant_id]

        if not item.durability:
            return None

        # Base repair cost
        missing_durability = item.durability.max_durability - item.durability.current_durability
        base_cost = (missing_durability / item.durability.max_durability) * item.base_price

        # Apply merchant's repair skill modifier
        skill_modifier = merchant.repair_skills.get(item.type, 1.0)
        repair_cost = base_cost * item.repair_difficulty * skill_modifier

        return int(repair_cost)

    def repair_item(self, item_id: str, merchant_id: str) -> Tuple[bool, str, int]:
        """Attempt to repair an item"""
        repair_cost = self.calculate_repair_cost(item_id, merchant_id)
        if not repair_cost:
            return False, "Item cannot be repaired", 0

        item = self.items[item_id]
        merchant = self.merchants[merchant_id]

        # Chance for merchant to gain repair experience
        if random.random() < 0.3:  # 30% chance
            current_skill = merchant.repair_skills.get(item.type, 1.0)
            merchant.repair_skills[item.type] = min(current_skill + 0.05, 2.0)

        item.durability.current_durability = item.durability.max_durability
        return True, "Item repaired successfully", repair_cost

    def create_bundle_deal(self, merchant_id: str, theme: str = None) -> Optional[BundleDeal]:
        """Create a themed bundle deal"""
        if merchant_id not in self.merchants:
            return None

        merchant = self.merchants[merchant_id]
        available_items = {
            item_id: qty for item_id, qty in merchant.inventory.items()
            if self.items[item_id].bundle_eligible
        }

        if not available_items:
            return None

        # Select items for bundle
        bundle_items = {}
        if theme and theme in self.bundle_themes:
            # Select themed items
            themed_items = {
                item_id: qty for item_id, qty in available_items.items()
                if any(tag in item_id for tag in self.bundle_themes[theme])
            }
            if themed_items:
                selected_items = random.sample(
                    list(themed_items.keys()),
                    min(3, len(themed_items))
                )
                for item_id in selected_items:
                    bundle_items[item_id] = random.randint(1, themed_items[item_id])
        else:
            # Random bundle
            selected_items = random.sample(
                list(available_items.keys()),
                min(3, len(available_items))
            )
            for item_id in selected_items:
                bundle_items[item_id] = random.randint(1, available_items[item_id])

        # Calculate discount
        base_discount = 0.1  # 10% base discount
        if theme:
            base_discount += 0.05  # Additional 5% for themed bundles

        return BundleDeal(
            name=f"{theme.title() if theme else 'Mixed'} Bundle",
            items=bundle_items,
            discount=base_discount,
            duration=24  # 24 game hours
        )

    def generate_economic_crisis(self) -> Optional[EconomicCrisis]:
        """Generate a random economic crisis event"""
        crisis_types = [
            {
                "name": "Supply Chain Disruption",
                "duration": 72,  # 3 days
                "effects": {
                    "supply": 0.5,  # 50% reduction in supply
                    "price": 2.0,   # 100% price increase
                    "quality": 0.8   # 20% quality reduction
                }
            },
            {
                "name": "Currency Devaluation",
                "duration": 96,  # 4 days
                "effects": {
                    "currency_value": 0.7,  # 30% currency value loss
                    "foreign_prices": 1.5,  # 50% increase in foreign goods
                    "local_prices": 0.8     # 20% decrease in local goods
                }
            },
            {
                "name": "Trade Route Collapse",
                "duration": 48,  # 2 days
                "effects": {
                    "route_safety": 0.5,    # 50% reduced safety
                    "transport_cost": 2.0,  # 100% increased transport cost
                    "availability": 0.6     # 40% reduced availability
                }
            }
        ]

        if random.random() < 0.05:  # 5% chance of crisis
            crisis_data = random.choice(crisis_types)
            crisis = EconomicCrisis(
                name=crisis_data["name"],
                duration=crisis_data["duration"],
                effects=crisis_data["effects"],
                affected_regions=set(),
                affected_items=set()
            )
            
            # Determine affected regions and items
            num_regions = random.randint(1, 3)
            all_regions = set(
                route.start_location for route in self.trade_network.values()
            ) | set(
                route.end_location for route in self.trade_network.values()
            )
            crisis.affected_regions = set(random.sample(list(all_regions), num_regions))
            
            # Select affected items
            crisis_sensitive_items = {
                item_id for item_id, item in self.items.items()
                if item.crisis_sensitive
            }
            num_items = random.randint(
                len(crisis_sensitive_items) // 4,
                len(crisis_sensitive_items) // 2
            )
            crisis.affected_items = set(
                random.sample(list(crisis_sensitive_items), num_items)
            )
            
            return crisis
        return None

    def update_merchant_specialization(self, merchant_id: str, successful_trade: Dict[str, int]):
        """Update merchant's specialization based on successful trades"""
        if merchant_id not in self.merchants:
            return

        merchant = self.merchants[merchant_id]
        
        # Calculate experience gained for relevant specializations
        for item_id, quantity in successful_trade.items():
            if item_id in self.items:
                item = self.items[item_id]
                relevant_specs = self._get_relevant_specializations(item.type)
                
                for spec in relevant_specs:
                    current_exp = merchant.specialization_experience.get(spec, 0.0)
                    # More experience for higher quality/value items
                    exp_gain = 0.01 * quantity * (item.quality_level / 5.0)
                    merchant.specialization_experience[spec] = min(
                        current_exp + exp_gain,
                        1.0
                    )

        # Check for specialization shifts
        primary_spec = max(
            merchant.specialization_experience.items(),
            key=lambda x: x[1],
            default=(merchant.specialization, 0.0)
        )[0]

        if (primary_spec != merchant.specialization and
            merchant.specialization_experience.get(primary_spec, 0.0) > 0.7):
            # Merchant shifts specialization
            merchant.specialization = primary_spec
            # Update trade knowledge and skills accordingly
            self._update_merchant_skills(merchant)

    def _update_merchant_skills(self, merchant: Merchant):
        """Update merchant's skills based on specialization"""
        # Reset non-primary skills
        merchant.repair_skills.clear()
        merchant.trade_knowledge.clear()
        
        # Set base skills for new specialization
        base_skill = 1.2  # 20% bonus in specialized areas
        if merchant.specialization == MerchantSpecialization.WEAPONSMITH:
            merchant.repair_skills[TradeItemType.WEAPON] = base_skill
            merchant.trade_knowledge["weapon_crafting"] = base_skill
        elif merchant.specialization == MerchantSpecialization.ARMORSMITH:
            merchant.repair_skills[TradeItemType.ARMOR] = base_skill
            merchant.trade_knowledge["armor_crafting"] = base_skill
        # ... add other specialization updates

    def _get_relevant_specializations(self, item_type: TradeItemType) -> Set[MerchantSpecialization]:
        """Get specializations relevant to an item type"""
        specialization_map = {
            TradeItemType.WEAPON: {
                MerchantSpecialization.WEAPONSMITH,
                MerchantSpecialization.ARTIFICER
            },
            TradeItemType.ARMOR: {
                MerchantSpecialization.ARMORSMITH,
                MerchantSpecialization.ARTIFICER
            },
            TradeItemType.POTION: {
                MerchantSpecialization.ALCHEMIST,
                MerchantSpecialization.MYSTIC
            }
            # ... add mappings for other item types
        }
        return specialization_map.get(item_type, {MerchantSpecialization.TRADER}) 

    def update_market_conditions(self, game_time: int):
        """Enhanced market condition updates"""
        # Update base supply and demand
        for item_type in TradeItemType:
            # Calculate trend
            current_trend = self._calculate_market_trend(item_type)
            
            # Apply trend-based modification
            base_fluctuation = self._get_trend_fluctuation(current_trend)
            seasonal_modifier = self._get_seasonal_modifier(game_time, item_type)
            event_modifier = self._get_event_modifier(item_type)
            
            final_modifier = base_fluctuation * seasonal_modifier * event_modifier
            self.market_state["supply_demand"][item_type] = final_modifier
            
            # Store trend for history
            if item_type not in self.market_state["price_trends"]:
                self.market_state["price_trends"][item_type] = []
            self.market_state["price_trends"][item_type].append(final_modifier)
            
            # Keep only last 30 data points
            if len(self.market_state["price_trends"][item_type]) > 30:
                self.market_state["price_trends"][item_type].pop(0)

    def _calculate_market_trend(self, item_type: TradeItemType) -> MarketTrend:
        """Calculate market trend based on price history"""
        if item_type not in self.market_state["price_trends"]:
            return MarketTrend.STABLE
            
        history = self.market_state["price_trends"][item_type]
        if len(history) < 5:
            return MarketTrend.STABLE
            
        # Calculate recent price changes
        recent_changes = [
            (history[i] - history[i-1]) / history[i-1]
            for i in range(1, len(history))
        ]
        avg_change = sum(recent_changes) / len(recent_changes)
        
        if avg_change < -0.2:
            return MarketTrend.CRASHING
        elif avg_change < -0.1:
            return MarketTrend.DECLINING
        elif avg_change > 0.2:
            return MarketTrend.BOOMING
        elif avg_change > 0.1:
            return MarketTrend.GROWING
        else:
            return MarketTrend.STABLE

    def _get_trend_fluctuation(self, trend: MarketTrend) -> float:
        """Get price fluctuation based on market trend"""
        fluctuations = {
            MarketTrend.CRASHING: 0.6,
            MarketTrend.DECLINING: 0.8,
            MarketTrend.STABLE: 1.0,
            MarketTrend.GROWING: 1.2,
            MarketTrend.BOOMING: 1.4
        }
        return fluctuations.get(trend, 1.0)

    def _get_seasonal_modifier(self, game_time: int, item_type: TradeItemType) -> float:
        """Get seasonal price modifier"""
        season = self._get_current_season(game_time)
        
        # Define seasonal effects on different item types
        seasonal_effects = {
            "spring": {
                TradeItemType.ESSENCE: 1.2,
                TradeItemType.GEM: 0.9,
                TradeItemType.MATERIAL: 0.8
            },
            "summer": {
                TradeItemType.WEAPON: 0.9,
                TradeItemType.ARMOR: 0.9,
                TradeItemType.POTION: 1.1
            },
            "autumn": {
                TradeItemType.FOOD: 0.7,
                TradeItemType.MATERIAL: 1.2,
                TradeItemType.SCROLL: 1.1
            },
            "winter": {
                TradeItemType.FOOD: 1.3,
                TradeItemType.ESSENCE: 0.8,
                TradeItemType.ARTIFACT: 1.2
            }
        }
        
        return seasonal_effects.get(season, {}).get(item_type, 1.0)

    def _get_event_modifier(self, item_type: TradeItemType) -> float:
        """Get event-based price modifier"""
        modifier = 1.0
        
        for event in self.market_state["current_events"]:
            if item_type in event.modifiers:
                modifier *= event.modifiers[item_type]
                
        return modifier

    def _get_current_season(self, game_time: int) -> str:
        """Calculate current season based on game time"""
        # Assuming 1 year = 365 game days
        day_of_year = game_time % 365
        
        if day_of_year < 90:  # Spring: days 0-89
            return "spring"
        elif day_of_year < 180:  # Summer: days 90-179
            return "summer"
        elif day_of_year < 270:  # Autumn: days 180-269
            return "autumn"
        else:  # Winter: days 270-364
            return "winter"

    def update_trade_routes(self, game_time: int):
        """Update trade route conditions and apply seasonal effects"""
        current_season = self._get_current_season(game_time)
        
        for route in self.trade_network.values():
            # Apply seasonal modifiers
            route.maintenance_cost *= route.seasonal_modifiers.get(current_season, 1.0)
            
            # Check for active crises affecting the route
            for crisis in self.active_crises:
                if (route.start_location in crisis.affected_regions or
                    route.end_location in crisis.affected_regions):
                    route.risk_level *= crisis.effects.get("route_safety", 1.0)
                    route.maintenance_cost *= crisis.effects.get("transport_cost", 1.0)

    def calculate_route_profit(self, route_id: str, cargo: Dict[str, int]) -> float:
        """Calculate potential profit for a trade route"""
        if route_id not in self.trade_network:
            return 0.0
            
        route = self.trade_network[route_id]
        
        # Calculate base revenue
        start_prices = self._get_location_prices(route.start_location)
        end_prices = self._get_location_prices(route.end_location)
        
        revenue = sum(
            (end_prices.get(item_id, 0) - start_prices.get(item_id, 0)) * qty
            for item_id, qty in cargo.items()
        )
        
        # Calculate costs
        transport_cost = route.maintenance_cost * sum(cargo.values())
        risk_cost = route.risk_level * revenue * 0.1  # 10% of revenue at risk
        
        return revenue - transport_cost - risk_cost

    def _get_location_prices(self, location: str) -> Dict[str, int]:
        """Get current prices at a location"""
        prices = {}
        for merchant_id, merchant in self.merchants.items():
            if merchant.location == location:
                prices.update(merchant.item_prices)
        return prices 