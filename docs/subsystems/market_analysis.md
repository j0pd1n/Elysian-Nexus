# Market Analysis System Documentation

## Overview
The Market Analysis System in Elysian Nexus provides sophisticated market analysis tools and trading strategies for the game's economic simulation. It integrates with the Economic System and Trading System to provide detailed market insights, predictions, and trading opportunities.

## Core Components

### Market Analysis Tools
1. **Technical Indicators**
   - Simple Moving Average (SMA)
   - Relative Strength Index (RSI)
   - Moving Average Convergence Divergence (MACD)
   - Price Momentum
   - Volatility Calculations

2. **Market Sentiment Analysis**
   - Buy/Sell Volume Analysis
   - Event Impact Assessment
   - Sentiment Scoring (-1.0 to 1.0)
   - Sentiment Categories (very_bullish to very_bearish)

### Analysis Timeframes
- Hour (1h)
- Day (1d)
- Week (1w)
- Month (1m)

### Trend Analysis
**Trend Strengths:**
- Very Weak
- Weak
- Moderate
- Strong
- Very Strong

## Key Features

### 1. Market Condition Analysis
- Comprehensive market analysis for specific resources and locations
- Technical indicator calculations
- Trend and strength determination
- Volatility assessment
- Trading recommendations

### 2. Arbitrage Opportunities
- Cross-market price comparison
- Profit margin calculation
- Risk-adjusted profit assessment
- Trade route analysis
- Minimum profit margin filtering

### 3. Price Movement Prediction
- Historical data analysis
- Trend indicator integration
- Market event consideration
- Supply/demand factor analysis
- Confidence-based predictions

### 4. Market Sentiment Analysis
- Trading activity analysis
- Event impact assessment
- Volume-based sentiment scoring
- Categorical sentiment classification
- Recent event tracking

## Technical Implementation

### MarketIndicator Class
```python
@dataclass
class MarketIndicator:
    name: str
    value: float
    signal: str  # "buy", "sell", or "hold"
    confidence: float  # 0.0 to 1.0
    timestamp: float
```

### Key Methods
1. `analyze_market_conditions()`: Comprehensive market analysis
2. `get_arbitrage_opportunities()`: Find profitable trading opportunities
3. `predict_price_movement()`: Future price movement prediction
4. `get_market_sentiment()`: Analyze current market sentiment

## Integration Points
- Economic System: Price history and market events
- Trading System: Market trends and trade management
- Resource Management: Supply and demand tracking

## Best Practices
1. Regular market condition monitoring
2. Risk assessment before trading
3. Consider multiple timeframes for analysis
4. Monitor sentiment changes for market shifts
5. Validate arbitrage opportunities before trading 