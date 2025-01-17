from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np
from datetime import datetime, timedelta
import logging

from economic_system import ResourceType, MarketEvent, EconomicSystem
from trading_system import MarketTrend, TradeManager

class AnalysisTimeframe(Enum):
    HOUR = "1h"
    DAY = "1d"
    WEEK = "1w"
    MONTH = "1m"

class TrendStrength(Enum):
    VERY_WEAK = "very_weak"
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"

@dataclass
class MarketIndicator:
    """Represents a market technical indicator"""
    name: str
    value: float
    signal: str  # "buy", "sell", or "hold"
    confidence: float  # 0.0 to 1.0
    timestamp: float

@dataclass
class MarketAnalysis:
    """Handles advanced market analysis and trading strategies"""
    economic_system: EconomicSystem
    trade_manager: TradeManager
    
    def __post_init__(self):
        """Initialize analysis components"""
        self.logger = logging.getLogger("MarketAnalysis")
        self.indicator_history: Dict[str, List[MarketIndicator]] = {}
        self.trend_cache: Dict[Tuple[str, ResourceType], List[Tuple[float, float]]] = {}
        
    def analyze_market_conditions(
        self,
        location: str,
        resource_type: ResourceType,
        timeframe: AnalysisTimeframe = AnalysisTimeframe.DAY
    ) -> Dict[str, any]:
        """Analyze current market conditions for a resource"""
        # Get price history
        history = self.economic_system.get_price_history(
            location,
            resource_type,
            self._get_hours_for_timeframe(timeframe)
        )
        
        if not history:
            return {
                "trend": MarketTrend.STABLE,
                "strength": TrendStrength.VERY_WEAK,
                "volatility": 0.0,
                "indicators": [],
                "recommendation": "insufficient_data"
            }
            
        # Calculate technical indicators
        indicators = self._calculate_technical_indicators(history)
        
        # Determine trend and strength
        trend, strength = self._analyze_trend(history)
        
        # Calculate volatility
        volatility = self._calculate_volatility(history)
        
        # Generate trading recommendation
        recommendation = self._generate_recommendation(
            trend,
            strength,
            volatility,
            indicators
        )
        
        return {
            "trend": trend,
            "strength": strength,
            "volatility": volatility,
            "indicators": indicators,
            "recommendation": recommendation
        }
        
    def get_arbitrage_opportunities(
        self,
        resource_type: ResourceType,
        min_profit_margin: float = 0.1
    ) -> List[Dict[str, any]]:
        """Find arbitrage opportunities across different markets"""
        opportunities = []
        markets = self.economic_system.markets
        
        for source_loc, source_market in markets.items():
            if resource_type not in source_market:
                continue
                
            source_price = source_market[resource_type].current_price
            
            for dest_loc, dest_market in markets.items():
                if dest_loc == source_loc or resource_type not in dest_market:
                    continue
                    
                dest_price = dest_market[resource_type].current_price
                profit_margin = (dest_price - source_price) / source_price
                
                if profit_margin >= min_profit_margin:
                    route = self._find_trade_route(source_loc, dest_loc)
                    if route:
                        opportunities.append({
                            "source": source_loc,
                            "destination": dest_loc,
                            "buy_price": source_price,
                            "sell_price": dest_price,
                            "profit_margin": profit_margin,
                            "route": route,
                            "risk_adjusted_profit": profit_margin * (1 - route.risk_level)
                        })
                        
        return sorted(
            opportunities,
            key=lambda x: x["risk_adjusted_profit"],
            reverse=True
        )
        
    def predict_price_movement(
        self,
        location: str,
        resource_type: ResourceType,
        timeframe: AnalysisTimeframe
    ) -> Dict[str, any]:
        """Predict future price movement using historical data and market conditions"""
        # Get historical data
        history = self.economic_system.get_price_history(
            location,
            resource_type,
            self._get_hours_for_timeframe(timeframe)
        )
        
        if not history:
            return {
                "prediction": "unknown",
                "confidence": 0.0,
                "factors": []
            }
            
        # Convert to numpy arrays for analysis
        prices = np.array([price for _, price in history])
        timestamps = np.array([ts for ts, _ in history])
        
        # Calculate trend indicators
        sma_short = self._calculate_sma(prices, 5)
        sma_long = self._calculate_sma(prices, 20)
        momentum = self._calculate_momentum(prices)
        
        # Get market events and conditions
        events = self.economic_system.get_market_status(location)["recent_events"]
        market_conditions = self.trade_manager.market_state["supply_demand"].get(
            resource_type,
            1.0
        )
        
        # Combine factors for prediction
        prediction_factors = []
        
        # Trend analysis
        if sma_short[-1] > sma_long[-1]:
            prediction_factors.append(("trend", "bullish", 0.6))
        else:
            prediction_factors.append(("trend", "bearish", 0.6))
            
        # Momentum
        if momentum > 0:
            prediction_factors.append(("momentum", "positive", 0.4))
        else:
            prediction_factors.append(("momentum", "negative", 0.4))
            
        # Market conditions
        if market_conditions > 1.1:
            prediction_factors.append(("demand", "high", 0.5))
        elif market_conditions < 0.9:
            prediction_factors.append(("demand", "low", 0.5))
            
        # Recent events impact
        for event in events:
            if event["event"] == MarketEvent.PRICE_SPIKE.value:
                prediction_factors.append(("event", "spike", 0.3))
            elif event["event"] == MarketEvent.PRICE_CRASH.value:
                prediction_factors.append(("event", "crash", 0.3))
                
        # Calculate final prediction
        prediction = self._combine_prediction_factors(prediction_factors)
        
        return {
            "prediction": prediction["direction"],
            "confidence": prediction["confidence"],
            "factors": prediction_factors,
            "estimated_change": prediction["estimated_change"]
        }
        
    def get_market_sentiment(
        self,
        location: str,
        resource_type: ResourceType
    ) -> Dict[str, any]:
        """Analyze market sentiment based on trading activity and events"""
        # Get recent trading activity
        trades = self.economic_system.get_recent_trades(location, resource_type)
        events = self.economic_system.get_market_status(location)["recent_events"]
        
        # Analyze trade volume and direction
        buy_volume = sum(t["amount"] for t in trades if t["type"] == "buy")
        sell_volume = sum(t["amount"] for t in trades if t["type"] == "sell")
        
        # Calculate sentiment score (-1.0 to 1.0)
        if buy_volume + sell_volume == 0:
            sentiment_score = 0.0
        else:
            sentiment_score = (buy_volume - sell_volume) / (buy_volume + sell_volume)
            
        # Adjust for recent events
        for event in events:
            if event["event"] == MarketEvent.PRICE_SPIKE.value:
                sentiment_score += 0.2
            elif event["event"] == MarketEvent.PRICE_CRASH.value:
                sentiment_score -= 0.2
                
        sentiment_score = max(-1.0, min(1.0, sentiment_score))
        
        # Determine sentiment category
        if sentiment_score >= 0.6:
            category = "very_bullish"
        elif sentiment_score >= 0.2:
            category = "bullish"
        elif sentiment_score <= -0.6:
            category = "very_bearish"
        elif sentiment_score <= -0.2:
            category = "bearish"
        else:
            category = "neutral"
            
        return {
            "score": sentiment_score,
            "category": category,
            "buy_volume": buy_volume,
            "sell_volume": sell_volume,
            "recent_events": events
        }
        
    def _calculate_technical_indicators(
        self,
        history: List[Tuple[float, float]]
    ) -> List[MarketIndicator]:
        """Calculate technical indicators from price history"""
        prices = np.array([price for _, price in history])
        timestamps = np.array([ts for ts, _ in history])
        
        indicators = []
        
        # Moving Averages
        sma_short = self._calculate_sma(prices, 5)
        sma_long = self._calculate_sma(prices, 20)
        
        # RSI
        rsi = self._calculate_rsi(prices)
        
        # MACD
        macd, signal = self._calculate_macd(prices)
        
        # Create indicator objects
        current_time = timestamps[-1]
        
        # SMA Cross
        if sma_short[-1] > sma_long[-1] and sma_short[-2] <= sma_long[-2]:
            indicators.append(MarketIndicator(
                "sma_cross",
                sma_short[-1],
                "buy",
                0.7,
                current_time
            ))
        elif sma_short[-1] < sma_long[-1] and sma_short[-2] >= sma_long[-2]:
            indicators.append(MarketIndicator(
                "sma_cross",
                sma_short[-1],
                "sell",
                0.7,
                current_time
            ))
            
        # RSI
        if rsi[-1] < 30:
            indicators.append(MarketIndicator(
                "rsi",
                rsi[-1],
                "buy",
                0.8,
                current_time
            ))
        elif rsi[-1] > 70:
            indicators.append(MarketIndicator(
                "rsi",
                rsi[-1],
                "sell",
                0.8,
                current_time
            ))
            
        # MACD
        if macd[-1] > signal[-1] and macd[-2] <= signal[-2]:
            indicators.append(MarketIndicator(
                "macd",
                macd[-1],
                "buy",
                0.6,
                current_time
            ))
        elif macd[-1] < signal[-1] and macd[-2] >= signal[-2]:
            indicators.append(MarketIndicator(
                "macd",
                macd[-1],
                "sell",
                0.6,
                current_time
            ))
            
        return indicators
        
    def _calculate_sma(self, prices: np.ndarray, period: int) -> np.ndarray:
        """Calculate Simple Moving Average"""
        return np.convolve(prices, np.ones(period)/period, mode='valid')
        
    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> np.ndarray:
        """Calculate Relative Strength Index"""
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum()/period
        down = -seed[seed < 0].sum()/period
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:period] = 100. - 100./(1. + rs)
        
        for i in range(period, len(prices)):
            delta = deltas[i-1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
                
            up = (up*(period-1) + upval)/period
            down = (down*(period-1) + downval)/period
            rs = up/down
            rsi[i] = 100. - 100./(1. + rs)
            
        return rsi
        
    def _calculate_macd(
        self,
        prices: np.ndarray,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate MACD and Signal line"""
        exp1 = prices.ewm(span=fast, adjust=False).mean()
        exp2 = prices.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return macd, signal_line
        
    def _calculate_momentum(self, prices: np.ndarray, period: int = 10) -> float:
        """Calculate price momentum"""
        if len(prices) < period:
            return 0.0
        return prices[-1] - prices[-period]
        
    def _analyze_trend(
        self,
        history: List[Tuple[float, float]]
    ) -> Tuple[MarketTrend, TrendStrength]:
        """Analyze price trend and its strength"""
        prices = np.array([price for _, price in history])
        
        # Calculate price changes
        changes = np.diff(prices) / prices[:-1]
        
        # Determine trend
        avg_change = np.mean(changes)
        if avg_change > 0.02:
            trend = MarketTrend.BOOMING
        elif avg_change > 0.01:
            trend = MarketTrend.GROWING
        elif avg_change < -0.02:
            trend = MarketTrend.CRASHING
        elif avg_change < -0.01:
            trend = MarketTrend.DECLINING
        else:
            trend = MarketTrend.STABLE
            
        # Calculate trend strength
        strength_score = abs(avg_change) * 100
        if strength_score > 5:
            strength = TrendStrength.VERY_STRONG
        elif strength_score > 3:
            strength = TrendStrength.STRONG
        elif strength_score > 1:
            strength = TrendStrength.MODERATE
        elif strength_score > 0.5:
            strength = TrendStrength.WEAK
        else:
            strength = TrendStrength.VERY_WEAK
            
        return trend, strength
        
    def _calculate_volatility(self, history: List[Tuple[float, float]]) -> float:
        """Calculate price volatility"""
        prices = np.array([price for _, price in history])
        returns = np.diff(np.log(prices))
        return np.std(returns) * np.sqrt(252)  # Annualized volatility
        
    def _generate_recommendation(
        self,
        trend: MarketTrend,
        strength: TrendStrength,
        volatility: float,
        indicators: List[MarketIndicator]
    ) -> str:
        """Generate trading recommendation based on analysis"""
        # Count indicator signals
        buy_signals = sum(1 for i in indicators if i.signal == "buy")
        sell_signals = sum(1 for i in indicators if i.signal == "sell")
        
        # Consider trend
        if trend in [MarketTrend.BOOMING, MarketTrend.GROWING]:
            buy_signals += 1
        elif trend in [MarketTrend.CRASHING, MarketTrend.DECLINING]:
            sell_signals += 1
            
        # Consider strength
        if strength in [TrendStrength.STRONG, TrendStrength.VERY_STRONG]:
            if buy_signals > sell_signals:
                buy_signals += 1
            elif sell_signals > buy_signals:
                sell_signals += 1
                
        # Consider volatility
        if volatility > 0.3:  # High volatility
            return "hold"  # Recommend holding in highly volatile markets
            
        # Generate recommendation
        if buy_signals > sell_signals + 1:
            return "strong_buy"
        elif buy_signals > sell_signals:
            return "buy"
        elif sell_signals > buy_signals + 1:
            return "strong_sell"
        elif sell_signals > buy_signals:
            return "sell"
        else:
            return "hold"
            
    def _get_hours_for_timeframe(self, timeframe: AnalysisTimeframe) -> int:
        """Convert timeframe to hours"""
        return {
            AnalysisTimeframe.HOUR: 1,
            AnalysisTimeframe.DAY: 24,
            AnalysisTimeframe.WEEK: 168,
            AnalysisTimeframe.MONTH: 720
        }[timeframe]
        
    def _find_trade_route(self, source: str, destination: str) -> Optional[Dict]:
        """Find trade route between locations"""
        return next(
            (route for route in self.economic_system.trade_routes
             if route.source_location == source
             and route.destination_location == destination),
            None
        )
        
    def _combine_prediction_factors(
        self,
        factors: List[Tuple[str, str, float]]
    ) -> Dict[str, any]:
        """Combine prediction factors into final prediction"""
        total_weight = sum(weight for _, _, weight in factors)
        weighted_score = sum(
            weight * (1 if signal in ["bullish", "positive", "high", "spike"] else -1)
            for _, signal, weight in factors
        )
        
        normalized_score = weighted_score / total_weight
        
        # Determine direction and confidence
        if normalized_score > 0.3:
            direction = "up"
            confidence = min(abs(normalized_score), 1.0)
            estimated_change = normalized_score * 0.1  # 10% max estimated change
        elif normalized_score < -0.3:
            direction = "down"
            confidence = min(abs(normalized_score), 1.0)
            estimated_change = normalized_score * 0.1
        else:
            direction = "sideways"
            confidence = 1 - abs(normalized_score)
            estimated_change = 0.0
            
        return {
            "direction": direction,
            "confidence": confidence,
            "estimated_change": estimated_change
        } 