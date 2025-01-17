import unittest
import numpy as np
from datetime import datetime, timedelta
import time

from market_analysis import (
    MarketAnalysis,
    AnalysisTimeframe,
    TrendStrength,
    MarketIndicator
)
from economic_system import EconomicSystem, ResourceType, MarketEvent
from trading_system import TradeManager, MarketTrend

class TestMarketAnalysis(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.economic_system = EconomicSystem()
        self.trade_manager = TradeManager()
        self.market_analysis = MarketAnalysis(
            self.economic_system,
            self.trade_manager
        )
        
        # Create test market
        self.economic_system.create_market("test_market")
        
        # Initialize with test data
        self._setup_test_data()
        
    def _setup_test_data(self):
        """Set up test market data"""
        # Add price history
        history = []
        base_price = 100.0
        timestamp = time.time() - 24 * 3600  # Start 24 hours ago
        
        for i in range(24):  # 24 hours of data
            price = base_price * (1 + 0.1 * np.sin(i/4))  # Create price oscillation
            history.append((timestamp + i * 3600, price))
            
        self.economic_system.price_history["test_market"][ResourceType.CRYSTAL] = history
        
        # Add recent trades
        trades = []
        for i in range(10):
            trade_type = "buy" if i % 2 == 0 else "sell"
            trades.append({
                "type": trade_type,
                "amount": 10.0,
                "price": base_price,
                "timestamp": timestamp + i * 1800
            })
            
        self.economic_system.recent_trades["test_market"][ResourceType.CRYSTAL] = trades
        
    def test_analyze_market_conditions(self):
        """Test market condition analysis"""
        conditions = self.market_analysis.analyze_market_conditions(
            "test_market",
            ResourceType.CRYSTAL,
            AnalysisTimeframe.DAY
        )
        
        self.assertIn("trend", conditions)
        self.assertIn("strength", conditions)
        self.assertIn("volatility", conditions)
        self.assertIn("indicators", conditions)
        self.assertIn("recommendation", conditions)
        
        self.assertIsInstance(conditions["trend"], MarketTrend)
        self.assertIsInstance(conditions["strength"], TrendStrength)
        self.assertIsInstance(conditions["volatility"], float)
        self.assertIsInstance(conditions["indicators"], list)
        self.assertIsInstance(conditions["recommendation"], str)
        
    def test_get_arbitrage_opportunities(self):
        """Test arbitrage opportunity detection"""
        # Create additional test market with price difference
        self.economic_system.create_market("test_market2")
        
        # Set up price difference
        self.economic_system.markets["test_market"][ResourceType.CRYSTAL].current_price = 100.0
        self.economic_system.markets["test_market2"][ResourceType.CRYSTAL].current_price = 120.0
        
        # Create trade route
        self.economic_system.trade_routes.append({
            "source_location": "test_market",
            "destination_location": "test_market2",
            "risk_level": 0.2
        })
        
        opportunities = self.market_analysis.get_arbitrage_opportunities(
            ResourceType.CRYSTAL,
            min_profit_margin=0.1
        )
        
        self.assertTrue(len(opportunities) > 0)
        self.assertGreaterEqual(opportunities[0]["profit_margin"], 0.1)
        
    def test_predict_price_movement(self):
        """Test price movement prediction"""
        prediction = self.market_analysis.predict_price_movement(
            "test_market",
            ResourceType.CRYSTAL,
            AnalysisTimeframe.DAY
        )
        
        self.assertIn("prediction", prediction)
        self.assertIn("confidence", prediction)
        self.assertIn("factors", prediction)
        self.assertIn("estimated_change", prediction)
        
        self.assertIsInstance(prediction["confidence"], float)
        self.assertGreaterEqual(prediction["confidence"], 0.0)
        self.assertLessEqual(prediction["confidence"], 1.0)
        
    def test_get_market_sentiment(self):
        """Test market sentiment analysis"""
        sentiment = self.market_analysis.get_market_sentiment(
            "test_market",
            ResourceType.CRYSTAL
        )
        
        self.assertIn("score", sentiment)
        self.assertIn("category", sentiment)
        self.assertIn("buy_volume", sentiment)
        self.assertIn("sell_volume", sentiment)
        
        self.assertIsInstance(sentiment["score"], float)
        self.assertGreaterEqual(sentiment["score"], -1.0)
        self.assertLessEqual(sentiment["score"], 1.0)
        
    def test_technical_indicators(self):
        """Test technical indicator calculations"""
        history = self.economic_system.price_history["test_market"][ResourceType.CRYSTAL]
        indicators = self.market_analysis._calculate_technical_indicators(history)
        
        self.assertIsInstance(indicators, list)
        for indicator in indicators:
            self.assertIsInstance(indicator, MarketIndicator)
            self.assertIn(indicator.signal, ["buy", "sell", "hold"])
            self.assertGreaterEqual(indicator.confidence, 0.0)
            self.assertLessEqual(indicator.confidence, 1.0)
            
    def test_trend_analysis(self):
        """Test trend analysis"""
        history = self.economic_system.price_history["test_market"][ResourceType.CRYSTAL]
        trend, strength = self.market_analysis._analyze_trend(history)
        
        self.assertIsInstance(trend, MarketTrend)
        self.assertIsInstance(strength, TrendStrength)
        
    def test_volatility_calculation(self):
        """Test volatility calculation"""
        history = self.economic_system.price_history["test_market"][ResourceType.CRYSTAL]
        volatility = self.market_analysis._calculate_volatility(history)
        
        self.assertIsInstance(volatility, float)
        self.assertGreaterEqual(volatility, 0.0)
        
    def test_recommendation_generation(self):
        """Test trading recommendation generation"""
        # Test with different combinations of trends and indicators
        test_cases = [
            {
                "trend": MarketTrend.BOOMING,
                "strength": TrendStrength.STRONG,
                "volatility": 0.2,
                "indicators": [
                    MarketIndicator("test", 1.0, "buy", 0.8, time.time()),
                    MarketIndicator("test2", 1.0, "buy", 0.7, time.time())
                ]
            },
            {
                "trend": MarketTrend.CRASHING,
                "strength": TrendStrength.VERY_STRONG,
                "volatility": 0.2,
                "indicators": [
                    MarketIndicator("test", 1.0, "sell", 0.8, time.time()),
                    MarketIndicator("test2", 1.0, "sell", 0.7, time.time())
                ]
            },
            {
                "trend": MarketTrend.STABLE,
                "strength": TrendStrength.WEAK,
                "volatility": 0.4,  # High volatility
                "indicators": [
                    MarketIndicator("test", 1.0, "buy", 0.8, time.time()),
                    MarketIndicator("test2", 1.0, "sell", 0.7, time.time())
                ]
            }
        ]
        
        for case in test_cases:
            recommendation = self.market_analysis._generate_recommendation(
                case["trend"],
                case["strength"],
                case["volatility"],
                case["indicators"]
            )
            
            self.assertIn(
                recommendation,
                ["strong_buy", "buy", "hold", "sell", "strong_sell"]
            )
            
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Test with empty history
        conditions = self.market_analysis.analyze_market_conditions(
            "nonexistent_market",
            ResourceType.CRYSTAL,
            AnalysisTimeframe.DAY
        )
        self.assertEqual(conditions["recommendation"], "insufficient_data")
        
        # Test with single price point
        self.economic_system.price_history["test_market2"] = {
            ResourceType.CRYSTAL: [(time.time(), 100.0)]
        }
        conditions = self.market_analysis.analyze_market_conditions(
            "test_market2",
            ResourceType.CRYSTAL,
            AnalysisTimeframe.DAY
        )
        self.assertIsInstance(conditions["volatility"], float)
        
        # Test with invalid resource type
        sentiment = self.market_analysis.get_market_sentiment(
            "test_market",
            ResourceType.GOLD  # Assuming no data for GOLD
        )
        self.assertEqual(sentiment["score"], 0.0)
        
    def test_performance_benchmarks(self):
        """Test performance of analysis operations"""
        import time
        
        # Test analysis performance
        start_time = time.time()
        for _ in range(100):
            self.market_analysis.analyze_market_conditions(
                "test_market",
                ResourceType.CRYSTAL,
                AnalysisTimeframe.DAY
            )
        analysis_time = time.time() - start_time
        self.assertLess(analysis_time, 1.0)  # Should complete within 1 second
        
        # Test prediction performance
        start_time = time.time()
        for _ in range(100):
            self.market_analysis.predict_price_movement(
                "test_market",
                ResourceType.CRYSTAL,
                AnalysisTimeframe.DAY
            )
        prediction_time = time.time() - start_time
        self.assertLess(prediction_time, 1.0)
        
        # Test sentiment analysis performance
        start_time = time.time()
        for _ in range(100):
            self.market_analysis.get_market_sentiment(
                "test_market",
                ResourceType.CRYSTAL
            )
        sentiment_time = time.time() - start_time
        self.assertLess(sentiment_time, 1.0)

if __name__ == '__main__':
    unittest.main() 