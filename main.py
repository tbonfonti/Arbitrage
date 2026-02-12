#!/usr/bin/env python3
"""
Main application for arbitrage opportunity detection.

This application monitors prediction markets in real-time and alerts users
when arbitrage opportunities are detected.
"""
import asyncio
import logging
import sys
from datetime import datetime

from config import config
from models import MarketSource
from market_fetcher import (
    MarketAggregator,
    MockMarketFetcher,
    PolymarketFetcher,
    KalshiFetcher,
    PredictItFetcher
)
from arbitrage_detector import ArbitrageDetector
from alert_system import AlertSystem, ConsoleAlertHandler, EmailAlertHandler, WebhookAlertHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('arbitrage_detector.log')
    ]
)

logger = logging.getLogger(__name__)


class ArbitrageApp:
    """Main application class for arbitrage detection."""
    
    def __init__(self):
        self.config = config
        self.running = False
        
        # Validate configuration
        try:
            self.config.validate()
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            sys.exit(1)
        
        # Initialize components
        self.market_aggregator = self._setup_market_fetchers()
        self.arbitrage_detector = ArbitrageDetector(
            min_profit_percentage=self.config.arbitrage.min_profit_percentage,
            max_stake_usd=self.config.arbitrage.max_stake_usd
        )
        self.alert_system = self._setup_alert_system()
        
        logger.info("ArbitrageApp initialized")
    
    def _setup_market_fetchers(self) -> MarketAggregator:
        """Set up market data fetchers based on configuration."""
        fetchers = []
        
        # Add mock fetchers for demonstration (simulating different markets)
        # In production, these would be replaced with real API fetchers
        fetchers.append(MockMarketFetcher(MarketSource.POLYMARKET))
        fetchers.append(MockMarketFetcher(MarketSource.KALSHI))
        fetchers.append(MockMarketFetcher(MarketSource.PREDICTIT))
        
        # Uncomment these when API keys are configured and APIs are implemented
        # if self.config.polymarket_api_key:
        #     fetchers.append(PolymarketFetcher(self.config.polymarket_api_key))
        # if self.config.kalshi_api_key:
        #     fetchers.append(KalshiFetcher(self.config.kalshi_api_key))
        # if self.config.predictit_api_key:
        #     fetchers.append(PredictItFetcher(self.config.predictit_api_key))
        
        logger.info(f"Configured {len(fetchers)} market fetchers")
        return MarketAggregator(fetchers)
    
    def _setup_alert_system(self) -> AlertSystem:
        """Set up alert system based on configuration."""
        alert_system = AlertSystem()
        
        # Always enable console alerts
        if self.config.alerts.console_enabled:
            alert_system.add_handler(ConsoleAlertHandler())
        
        # Add email alerts if configured
        if self.config.alerts.email:
            alert_system.add_handler(EmailAlertHandler(self.config.alerts.email))
        
        # Add webhook alerts if configured
        if self.config.alerts.webhook_url:
            alert_system.add_handler(WebhookAlertHandler(self.config.alerts.webhook_url))
        
        return alert_system
    
    async def scan_once(self):
        """Perform a single scan for arbitrage opportunities."""
        logger.info("Starting market scan...")
        
        # Fetch markets
        markets = await self.market_aggregator.fetch_all_markets()
        logger.info(f"Fetched {len(markets)} markets")
        
        if not markets:
            logger.warning("No markets fetched, skipping scan")
            return
        
        # Detect arbitrage opportunities
        opportunities = self.arbitrage_detector.detect_opportunities(markets)
        logger.info(f"Detected {len(opportunities)} arbitrage opportunities")
        
        # Send alerts
        if opportunities:
            await self.alert_system.send_alerts(opportunities)
        else:
            logger.info("No arbitrage opportunities found in this scan")
    
    async def run(self):
        """Main application loop."""
        self.running = True
        logger.info("=" * 80)
        logger.info("Arbitrage Detection System Started")
        logger.info("=" * 80)
        logger.info(f"Update interval: {self.config.arbitrage.update_interval_seconds} seconds")
        logger.info(f"Minimum profit threshold: {self.config.arbitrage.min_profit_percentage}%")
        logger.info(f"Maximum stake: ${self.config.arbitrage.max_stake_usd}")
        logger.info(f"Risk tolerance: {self.config.risk.tolerance}")
        logger.info(f"Auto-trade enabled: {self.config.risk.auto_trade_enabled}")
        logger.info("=" * 80)
        
        if self.config.risk.auto_trade_enabled:
            logger.warning("⚠️  AUTO-TRADE is ENABLED - This is a future feature not yet implemented")
        
        scan_count = 0
        
        try:
            while self.running:
                scan_count += 1
                logger.info("--- Scan #%d at %s ---", scan_count, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                
                try:
                    await self.scan_once()
                except Exception as e:
                    logger.error(f"Error during scan: {e}", exc_info=True)
                
                # Wait for next update
                logger.info(f"Waiting {self.config.arbitrage.update_interval_seconds} seconds until next scan...")
                await asyncio.sleep(self.config.arbitrage.update_interval_seconds)
        
        except KeyboardInterrupt:
            logger.info("\nShutdown requested by user")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
        finally:
            self.running = False
            logger.info("Arbitrage Detection System stopped")
    
    def stop(self):
        """Stop the application."""
        self.running = False


async def main():
    """Main entry point."""
    app = ArbitrageApp()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
