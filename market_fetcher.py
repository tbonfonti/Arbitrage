"""
Market data fetcher for prediction markets.
Provides a unified interface for fetching data from multiple sources.
"""
import asyncio
import random
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from models import Market, MarketOutcome, MarketSource, MarketType

logger = logging.getLogger(__name__)


class MarketFetcher(ABC):
    """Abstract base class for market data fetchers."""
    
    @abstractmethod
    async def fetch_markets(self) -> List[Market]:
        """Fetch markets from the source."""
        pass


class MockMarketFetcher(MarketFetcher):
    """Mock market fetcher for testing and demonstration."""
    
    def __init__(self, source: MarketSource = MarketSource.MOCK):
        self.source = source
    
    async def fetch_markets(self) -> List[Market]:
        """Generate mock market data."""
        # Simulate API delay
        await asyncio.sleep(0.1)
        
        markets = []
        
        # Generate some mock binary markets with varying prices
        questions = [
            "Will candidate A win the election?",
            "Will the stock market go up tomorrow?",
            "Will it rain next week?",
            "Will the team win the championship?",
        ]
        
        for i, question in enumerate(questions):
            # Add some randomness to prices to simulate real market movements
            base_yes_price = 0.3 + (i * 0.15) + random.uniform(-0.05, 0.05)
            base_yes_price = max(0.1, min(0.9, base_yes_price))
            
            market = Market(
                market_id=f"{self.source.value}_market_{i}",
                source=self.source,
                question=question,
                market_type=MarketType.BINARY,
                outcomes=[
                    MarketOutcome(
                        outcome_id=f"yes_{i}",
                        outcome_name="Yes",
                        price=base_yes_price,
                        volume=random.uniform(10000, 100000),
                        liquidity=random.uniform(5000, 50000)
                    ),
                    MarketOutcome(
                        outcome_id=f"no_{i}",
                        outcome_name="No",
                        price=1.0 - base_yes_price,
                        volume=random.uniform(10000, 100000),
                        liquidity=random.uniform(5000, 50000)
                    )
                ],
                end_date=datetime.now() + timedelta(days=random.randint(1, 30)),
                last_updated=datetime.now()
            )
            markets.append(market)
        
        logger.info(f"Fetched {len(markets)} mock markets from {self.source.value}")
        return markets


class PolymarketFetcher(MarketFetcher):
    """Fetcher for Polymarket data."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.source = MarketSource.POLYMARKET
    
    async def fetch_markets(self) -> List[Market]:
        """
        Fetch markets from Polymarket.
        This is a placeholder for actual API integration.
        """
        logger.warning("Polymarket API integration not implemented. Using mock data.")
        # In production, implement actual API calls here
        # For now, return empty list or use mock data
        return []


class KalshiFetcher(MarketFetcher):
    """Fetcher for Kalshi data."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.source = MarketSource.KALSHI
    
    async def fetch_markets(self) -> List[Market]:
        """
        Fetch markets from Kalshi.
        This is a placeholder for actual API integration.
        """
        logger.warning("Kalshi API integration not implemented. Using mock data.")
        # In production, implement actual API calls here
        return []


class PredictItFetcher(MarketFetcher):
    """Fetcher for PredictIt data."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.source = MarketSource.PREDICTIT
    
    async def fetch_markets(self) -> List[Market]:
        """
        Fetch markets from PredictIt.
        This is a placeholder for actual API integration.
        """
        logger.warning("PredictIt API integration not implemented. Using mock data.")
        # In production, implement actual API calls here
        return []


class MarketAggregator:
    """Aggregates market data from multiple sources."""
    
    def __init__(self, fetchers: List[MarketFetcher]):
        self.fetchers = fetchers
    
    async def fetch_all_markets(self) -> List[Market]:
        """Fetch markets from all sources concurrently."""
        tasks = [fetcher.fetch_markets() for fetcher in self.fetchers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_markets = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error fetching from {self.fetchers[i]}: {result}")
            else:
                all_markets.extend(result)
        
        logger.info(f"Fetched total of {len(all_markets)} markets from {len(self.fetchers)} sources")
        return all_markets
