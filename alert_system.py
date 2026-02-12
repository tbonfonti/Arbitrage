"""
Alert system for notifying users of arbitrage opportunities.
"""
import logging
import json
from typing import List
from datetime import datetime
from abc import ABC, abstractmethod

from models import ArbitrageOpportunity

logger = logging.getLogger(__name__)


class AlertHandler(ABC):
    """Abstract base class for alert handlers."""
    
    @abstractmethod
    async def send_alert(self, opportunity: ArbitrageOpportunity) -> bool:
        """Send an alert for an arbitrage opportunity."""
        pass


class ConsoleAlertHandler(AlertHandler):
    """Sends alerts to the console."""
    
    async def send_alert(self, opportunity: ArbitrageOpportunity) -> bool:
        """Print alert to console."""
        print("\n" + "=" * 80)
        print("🚨 ARBITRAGE OPPORTUNITY DETECTED 🚨")
        print("=" * 80)
        print(f"Opportunity ID: {opportunity.opportunity_id}")
        print(f"Detected at: {opportunity.detected_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n💰 Profit: ${opportunity.guaranteed_profit_usd:.2f} ({opportunity.profit_percentage:.2f}%)")
        print(f"💵 Stake Required: ${opportunity.stake_required_usd:.2f}")
        print(f"\n📊 Market A ({opportunity.market_a.source.value}):")
        print(f"   Question: {opportunity.market_a.question}")
        print(f"   Bet on: {opportunity.outcome_a.outcome_name}")
        print(f"   Price: {opportunity.outcome_a.price:.4f}")
        print(f"\n📊 Market B ({opportunity.market_b.source.value}):")
        print(f"   Question: {opportunity.market_b.question}")
        print(f"   Bet on: {opportunity.outcome_b.outcome_name}")
        print(f"   Price: {opportunity.outcome_b.price:.4f}")
        print("=" * 80 + "\n")
        
        logger.info(f"Console alert sent for opportunity {opportunity.opportunity_id}")
        return True


class EmailAlertHandler(AlertHandler):
    """Sends alerts via email."""
    
    def __init__(self, email_address: str):
        self.email_address = email_address
    
    async def send_alert(self, opportunity: ArbitrageOpportunity) -> bool:
        """
        Send alert via email.
        This is a placeholder for actual email integration.
        """
        logger.info(f"[PLACEHOLDER] Would send email to {self.email_address} for opportunity {opportunity.opportunity_id}")
        # In production, implement actual email sending using SMTP or email service
        # Example: use smtplib or services like SendGrid, AWS SES, etc.
        return True


class WebhookAlertHandler(AlertHandler):
    """Sends alerts to a webhook URL."""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def send_alert(self, opportunity: ArbitrageOpportunity) -> bool:
        """
        Send alert to webhook.
        This is a placeholder for actual webhook integration.
        """
        logger.info(f"[PLACEHOLDER] Would send webhook to {self.webhook_url} for opportunity {opportunity.opportunity_id}")
        # In production, implement actual HTTP POST to webhook
        # Example using aiohttp:
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(self.webhook_url, json=opportunity.to_dict()) as response:
        #         return response.status == 200
        return True


class AlertSystem:
    """Manages multiple alert handlers and sends notifications."""
    
    def __init__(self):
        self.handlers: List[AlertHandler] = []
        self.sent_opportunities = set()  # Track sent alerts to avoid duplicates
    
    def add_handler(self, handler: AlertHandler):
        """Add an alert handler."""
        self.handlers.append(handler)
        logger.info(f"Added alert handler: {handler.__class__.__name__}")
    
    async def send_alerts(self, opportunities: List[ArbitrageOpportunity]):
        """Send alerts for all new opportunities."""
        new_opportunities = [
            opp for opp in opportunities 
            if opp.opportunity_id not in self.sent_opportunities
        ]
        
        if not new_opportunities:
            logger.debug("No new opportunities to alert")
            return
        
        logger.info(f"Sending alerts for {len(new_opportunities)} new opportunities")
        
        for opportunity in new_opportunities:
            for handler in self.handlers:
                try:
                    success = await handler.send_alert(opportunity)
                    if success:
                        self.sent_opportunities.add(opportunity.opportunity_id)
                except Exception as e:
                    logger.error(f"Error sending alert via {handler.__class__.__name__}: {e}")
    
    def clear_history(self):
        """Clear the history of sent opportunities."""
        self.sent_opportunities.clear()
        logger.info("Cleared alert history")
