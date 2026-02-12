"""
Configuration management for the arbitrage detection system.
"""
import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


class RiskConfig(BaseModel):
    """Risk tolerance configuration for future automated trading."""
    tolerance: str = Field(default="medium", description="Risk tolerance level: low, medium, high")
    max_position_size_usd: float = Field(default=500.0, description="Maximum position size in USD")
    auto_trade_enabled: bool = Field(default=False, description="Enable automatic trade execution")
    
    @property
    def risk_multiplier(self) -> float:
        """Return risk multiplier based on tolerance level."""
        multipliers = {"low": 0.5, "medium": 1.0, "high": 2.0}
        return multipliers.get(self.tolerance.lower(), 1.0)


class AlertConfig(BaseModel):
    """Alert system configuration."""
    email: Optional[str] = Field(default=None, description="Email address for alerts")
    webhook_url: Optional[str] = Field(default=None, description="Webhook URL for alerts")
    console_enabled: bool = Field(default=True, description="Enable console alerts")


class ArbitrageConfig(BaseModel):
    """Arbitrage detection configuration."""
    min_profit_percentage: float = Field(default=1.0, description="Minimum profit percentage to trigger alert")
    update_interval_seconds: int = Field(default=30, description="Update interval in seconds")
    max_stake_usd: float = Field(default=1000.0, description="Maximum stake for arbitrage calculation")


class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.risk = RiskConfig(
            tolerance=os.getenv("RISK_TOLERANCE", "medium"),
            max_position_size_usd=float(os.getenv("MAX_POSITION_SIZE_USD", "500")),
            auto_trade_enabled=os.getenv("AUTO_TRADE_ENABLED", "false").lower() == "true"
        )
        
        self.alerts = AlertConfig(
            email=os.getenv("ALERT_EMAIL"),
            webhook_url=os.getenv("WEBHOOK_URL"),
            console_enabled=True
        )
        
        self.arbitrage = ArbitrageConfig(
            min_profit_percentage=float(os.getenv("MIN_PROFIT_PERCENTAGE", "1.0")),
            update_interval_seconds=int(os.getenv("UPDATE_INTERVAL_SECONDS", "30")),
            max_stake_usd=float(os.getenv("MAX_STAKE_USD", "1000"))
        )
        
        # API Keys
        self.polymarket_api_key = os.getenv("POLYMARKET_API_KEY")
        self.kalshi_api_key = os.getenv("KALSHI_API_KEY")
        self.predictit_api_key = os.getenv("PREDICTIT_API_KEY")
    
    def validate(self) -> bool:
        """Validate configuration."""
        if self.arbitrage.min_profit_percentage <= 0:
            raise ValueError("MIN_PROFIT_PERCENTAGE must be positive")
        if self.arbitrage.update_interval_seconds <= 0:
            raise ValueError("UPDATE_INTERVAL_SECONDS must be positive")
        return True


# Global config instance
config = Config()
