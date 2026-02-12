"""
Data models for prediction markets and arbitrage opportunities.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum


class MarketType(Enum):
    """Type of prediction market."""
    BINARY = "binary"
    CATEGORICAL = "categorical"


class MarketSource(Enum):
    """Source of market data."""
    POLYMARKET = "polymarket"
    KALSHI = "kalshi"
    PREDICTIT = "predictit"
    MOCK = "mock"  # For testing


@dataclass
class MarketOutcome:
    """Represents a single outcome in a prediction market."""
    outcome_id: str
    outcome_name: str
    price: float  # Probability price (0-1)
    volume: float
    liquidity: float


@dataclass
class Market:
    """Represents a prediction market."""
    market_id: str
    source: MarketSource
    question: str
    market_type: MarketType
    outcomes: List[MarketOutcome]
    end_date: Optional[datetime] = None
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


@dataclass
class ArbitrageOpportunity:
    """Represents an arbitrage opportunity between markets."""
    opportunity_id: str
    market_a: Market
    market_b: Market
    outcome_a: MarketOutcome
    outcome_b: MarketOutcome
    profit_percentage: float
    guaranteed_profit_usd: float
    stake_required_usd: float
    detected_at: datetime
    
    def __post_init__(self):
        if self.detected_at is None:
            self.detected_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "opportunity_id": self.opportunity_id,
            "detected_at": self.detected_at.isoformat(),
            "profit_percentage": round(self.profit_percentage, 2),
            "guaranteed_profit_usd": round(self.guaranteed_profit_usd, 2),
            "stake_required_usd": round(self.stake_required_usd, 2),
            "market_a": {
                "source": self.market_a.source.value,
                "question": self.market_a.question,
                "outcome": self.outcome_a.outcome_name,
                "price": round(self.outcome_a.price, 4)
            },
            "market_b": {
                "source": self.market_b.source.value,
                "question": self.market_b.question,
                "outcome": self.outcome_b.outcome_name,
                "price": round(self.outcome_b.price, 4)
            }
        }
