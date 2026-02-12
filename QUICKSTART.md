# Quick Start Guide

## Installation (3 steps)

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure settings** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your preferences
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## What You'll See

The application will:
- Scan prediction markets every 30 seconds (configurable)
- Display arbitrage opportunities when found
- Show profit potential and required stake
- Log all activity to `arbitrage_detector.log`

Example output:
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

## Try the Demo

Run the example script to see how arbitrage detection works:
```bash
python example.py
```

## Configuration Options

Key settings in `.env`:
- `MIN_PROFIT_PERCENTAGE=1.0` - Minimum profit % to alert
- `UPDATE_INTERVAL_SECONDS=30` - Scan frequency
- `MAX_STAKE_USD=1000` - Maximum stake for calculations

## Next Steps

1. **Get API Keys**: Obtain keys from Polymarket, Kalshi, PredictIt
2. **Configure APIs**: Add keys to `.env`
3. **Implement API Fetchers**: Replace mock fetchers in `market_fetcher.py`
4. **Enable Alerts**: Configure email or webhook in `.env`

## Troubleshooting

- **No opportunities found**: Lower `MIN_PROFIT_PERCENTAGE` or wait for market movements
- **Import errors**: Run `pip install -r requirements.txt`
- **Configuration errors**: Check `.env` file format

## Support

See [README.md](README.md) for detailed documentation.
