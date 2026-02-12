#!/usr/bin/env python3
"""
Example demonstrating manual use of arbitrage detection components.
"""
import asyncio
from datetime import datetime, timedelta

from models import Market, MarketOutcome, MarketSource, MarketType
from arbitrage_detector import ArbitrageDetector


async def demo_arbitrage_detection():
    """Demonstrate arbitrage detection with example markets."""
    
    print("=" * 80)
    print("Arbitrage Detection Demo")
    print("=" * 80)
    print("\nCreating example markets...\n")
    
    # Create two markets about the same event with different prices
    market_a = Market(
        market_id="demo_market_a",
        source=MarketSource.POLYMARKET,
        question="Will it rain tomorrow?",
        market_type=MarketType.BINARY,
        outcomes=[
            MarketOutcome(
                outcome_id="yes_a",
                outcome_name="Yes",
                price=0.40,  # 40 cents for Yes
                volume=50000,
                liquidity=25000
            ),
            MarketOutcome(
                outcome_id="no_a",
                outcome_name="No",
                price=0.60,  # 60 cents for No
                volume=50000,
                liquidity=25000
            )
        ],
        end_date=datetime.now() + timedelta(days=1)
    )
    
    market_b = Market(
        market_id="demo_market_b",
        source=MarketSource.KALSHI,
        question="Will it rain tomorrow?",
        market_type=MarketType.BINARY,
        outcomes=[
            MarketOutcome(
                outcome_id="yes_b",
                outcome_name="Yes",
                price=0.45,  # 45 cents for Yes
                volume=60000,
                liquidity=30000
            ),
            MarketOutcome(
                outcome_id="no_b",
                outcome_name="No",
                price=0.50,  # 50 cents for No - ARBITRAGE OPPORTUNITY!
                volume=60000,
                liquidity=30000
            )
        ],
        end_date=datetime.now() + timedelta(days=1)
    )
    
    print(f"Market A ({market_a.source.value}):")
    print(f"  {market_a.question}")
    print(f"  Yes: ${market_a.outcomes[0].price:.2f}")
    print(f"  No:  ${market_a.outcomes[1].price:.2f}")
    print(f"  Total: ${market_a.outcomes[0].price + market_a.outcomes[1].price:.2f}")
    
    print(f"\nMarket B ({market_b.source.value}):")
    print(f"  {market_b.question}")
    print(f"  Yes: ${market_b.outcomes[0].price:.2f}")
    print(f"  No:  ${market_b.outcomes[1].price:.2f}")
    print(f"  Total: ${market_b.outcomes[0].price + market_b.outcomes[1].price:.2f}")
    
    # Detect arbitrage
    detector = ArbitrageDetector(min_profit_percentage=0.5, max_stake_usd=1000)
    opportunities = detector.detect_opportunities([market_a, market_b])
    
    print(f"\n{'=' * 80}")
    print(f"Arbitrage Analysis")
    print(f"{'=' * 80}\n")
    
    if opportunities:
        print(f"✅ Found {len(opportunities)} arbitrage opportunity!\n")
        
        for opp in opportunities:
            print(f"Strategy: Buy {opp.outcome_a.outcome_name} on {opp.market_a.source.value} "
                  f"at ${opp.outcome_a.price:.2f}")
            print(f"          Buy {opp.outcome_b.outcome_name} on {opp.market_b.source.value} "
                  f"at ${opp.outcome_b.price:.2f}")
            print(f"\nTotal Cost: ${opp.outcome_a.price + opp.outcome_b.price:.2f}")
            print(f"Guaranteed Payout: $1.00 (winner pays $1.00)")
            print(f"Guaranteed Profit: ${1.0 - (opp.outcome_a.price + opp.outcome_b.price):.2f}")
            print(f"\nWith ${opp.stake_required_usd:.2f} stake:")
            print(f"  💰 Profit: ${opp.guaranteed_profit_usd:.2f} ({opp.profit_percentage:.2f}%)")
    else:
        print("❌ No arbitrage opportunities found.")
    
    print(f"\n{'=' * 80}\n")


if __name__ == "__main__":
    asyncio.run(demo_arbitrage_detection())
