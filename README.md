# Arbitrage Opportunity Detection System

Real-time arbitrage opportunity detection for prediction markets with automated alerts.

## 🎯 Overview

This application continuously monitors multiple prediction markets (Polymarket, Kalshi, PredictIt) to identify arbitrage opportunities where you can guarantee a profit regardless of the outcome by placing bets on opposite outcomes across different markets.

### Key Features

- **Real-time Monitoring**: Continuously scans multiple prediction markets
- **Arbitrage Detection**: Identifies opportunities where opposite outcomes can be bought at favorable prices
- **Multi-channel Alerts**: Console, email, and webhook notifications
- **Risk Management**: Built-in risk tolerance configuration for future automated trading
- **Extensible Architecture**: Modular design allows easy addition of new markets and features
- **Future-Ready**: Infrastructure designed to support fully automated trading

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/tbonfonti/Arbitrage.git
cd Arbitrage
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the application:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run the application:
```bash
python main.py
```

## ⚙️ Configuration

Edit the `.env` file to customize the application behavior:

### Market API Keys (Optional)
```bash
POLYMARKET_API_KEY=your_api_key_here
KALSHI_API_KEY=your_api_key_here
PREDICTIT_API_KEY=your_api_key_here
```

### Alert Settings
```bash
ALERT_EMAIL=your_email@example.com        # Email for alerts
WEBHOOK_URL=https://your-webhook.com      # Webhook URL for alerts
```

### Arbitrage Detection
```bash
MIN_PROFIT_PERCENTAGE=1.0                 # Minimum profit % to trigger alert
UPDATE_INTERVAL_SECONDS=30                # How often to scan markets
MAX_STAKE_USD=1000                        # Maximum stake for calculations
```

### Risk Tolerance (Future Automated Trading)
```bash
RISK_TOLERANCE=medium                     # low, medium, or high
MAX_POSITION_SIZE_USD=500                 # Maximum position size
AUTO_TRADE_ENABLED=false                  # Enable automatic trading (future feature)
```

## 📊 How It Works

### Arbitrage Detection Algorithm

The system identifies arbitrage opportunities in binary prediction markets:

1. **Market Scanning**: Fetches current prices from multiple prediction markets
2. **Opportunity Detection**: Finds pairs of markets where opposite outcomes can be bought
3. **Profit Calculation**: Calculates guaranteed profit accounting for stake allocation
4. **Alert Triggering**: Sends alerts when opportunities exceed minimum profit threshold

### Example Arbitrage

**Market A (Polymarket)**: "Will it rain tomorrow?"
- Yes: $0.40

**Market B (Kalshi)**: "Will it rain tomorrow?"
- No: $0.55

**Arbitrage Strategy**:
- Buy Yes on Market A for $0.40
- Buy No on Market B for $0.55
- Total cost: $0.95
- Guaranteed payout: $1.00 (winner pays $1.00)
- **Guaranteed profit: $0.05 (5.26%)**

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                      Main Application                       │
│                        (main.py)                            │
└────────────┬────────────────────────────────────────────────┘
             │
             ├──► Market Fetcher (market_fetcher.py)
             │    └─ Aggregates data from multiple sources
             │       ├─ Polymarket
             │       ├─ Kalshi
             │       └─ PredictIt
             │
             ├──► Arbitrage Detector (arbitrage_detector.py)
             │    └─ Identifies profitable opportunities
             │
             ├──► Alert System (alert_system.py)
             │    └─ Sends notifications
             │       ├─ Console
             │       ├─ Email
             │       └─ Webhook
             │
             └──► Configuration (config.py)
                  └─ Manages settings and risk tolerance
```

### Data Models

- **Market**: Represents a prediction market with outcomes and prices
- **MarketOutcome**: Individual outcome within a market
- **ArbitrageOpportunity**: Detected arbitrage with profit calculations

### Extensibility

The modular architecture supports future enhancements:

1. **Automated Trading**: Risk tolerance settings are already configured
2. **Additional Markets**: Easily add new market sources by implementing `MarketFetcher`
3. **Advanced Strategies**: Detection algorithm can be extended for categorical markets
4. **Custom Alerts**: Add new alert handlers by implementing `AlertHandler`

## 📝 Usage Examples

### Basic Usage

Run with default settings:
```bash
python main.py
```

### Custom Configuration

Use environment variables to override settings:
```bash
MIN_PROFIT_PERCENTAGE=2.0 UPDATE_INTERVAL_SECONDS=60 python main.py
```

### Output Example

```
================================================================================
🚨 ARBITRAGE OPPORTUNITY DETECTED 🚨
================================================================================
Opportunity ID: 550e8400-e29b-41d4-a716-446655440000
Detected at: 2026-02-12 14:30:00

💰 Profit: $5.26 (5.26%)
💵 Stake Required: $100.00

📊 Market A (polymarket):
   Question: Will it rain tomorrow?
   Bet on: Yes
   Price: 0.4000

📊 Market B (kalshi):
   Question: Will it rain tomorrow?
   Bet on: No
   Price: 0.5500
================================================================================
```

## 🔒 Security & Risk Management

### Current Features

- Configurable profit thresholds to avoid false positives
- Maximum stake limits to control exposure
- Risk tolerance settings for different trading profiles
- Alert-only mode (no automatic trading)

### Future Automated Trading

When enabled (future feature), the system will:
- Respect risk tolerance settings (low/medium/high)
- Enforce maximum position sizes
- Require user approval for trades above thresholds
- Maintain detailed trade logs
- Support stop-loss and take-profit rules

## 🧪 Testing

The application includes mock market fetchers for testing without API keys:

```bash
# Run with mock data (default behavior without API keys)
python main.py
```

The mock fetchers generate realistic market data with varying prices to simulate real market conditions.

## 📚 API Integration

### Adding Real Market APIs

To integrate real prediction market APIs:

1. Obtain API keys from market providers
2. Add keys to `.env` file
3. Implement API calls in respective fetcher classes:
   - `PolymarketFetcher.fetch_markets()`
   - `KalshiFetcher.fetch_markets()`
   - `PredictItFetcher.fetch_markets()`

### Example API Implementation

```python
class PolymarketFetcher(MarketFetcher):
    async def fetch_markets(self) -> List[Market]:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with session.get(API_URL, headers=headers) as response:
                data = await response.json()
                return self._parse_markets(data)
```

## 🐛 Troubleshooting

### No opportunities detected
- Lower `MIN_PROFIT_PERCENTAGE` threshold
- Increase `UPDATE_INTERVAL_SECONDS` to capture more market movements
- Ensure multiple market sources are active

### API Errors
- Verify API keys are correct in `.env`
- Check API rate limits
- Review logs in `arbitrage_detector.log`

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Real API integrations for prediction markets
- Advanced matching algorithms for similar markets
- Machine learning for opportunity prediction
- Web dashboard for monitoring
- Mobile app for alerts
- Automated trade execution

## ⚠️ Disclaimer

This software is for educational and research purposes. Trading involves risk. Always verify opportunities manually before placing real trades. The developers are not responsible for any financial losses.