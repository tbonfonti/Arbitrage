"""
Arbitrage opportunity detection engine.
"""
import logging
from typing import List, Optional
from datetime import datetime
import uuid

from models import Market, ArbitrageOpportunity, MarketType

logger = logging.getLogger(__name__)


class ArbitrageDetector:
    """Detects arbitrage opportunities across prediction markets."""
    
    def __init__(self, min_profit_percentage: float = 1.0, max_stake_usd: float = 1000.0):
        self.min_profit_percentage = min_profit_percentage
        self.max_stake_usd = max_stake_usd
    
    def detect_opportunities(self, markets: List[Market]) -> List[ArbitrageOpportunity]:
        """
        Detect arbitrage opportunities across markets.
        
        For binary markets, an arbitrage exists when you can bet on opposite outcomes
        on different markets such that you profit regardless of the outcome.
        
        Example: Market A has Yes at 0.40, Market B has No at 0.55
        You can buy Yes on A and No on B:
        - If Yes happens: you win on A (1/0.40 = 2.5x)
        - If No happens: you win on B (1/0.55 = 1.82x)
        - If total cost < guaranteed return, it's an arbitrage
        """
        opportunities = []
        
        # Group markets by similar questions (in production, use NLP/matching)
        market_groups = self._group_similar_markets(markets)
        
        for group in market_groups:
            if len(group) < 2:
                continue
            
            # Check all pairs in the group
            for i, market_a in enumerate(group):
                for market_b in group[i+1:]:
                    opps = self._check_market_pair(market_a, market_b)
                    opportunities.extend(opps)
        
        # Filter by minimum profit percentage
        opportunities = [
            opp for opp in opportunities 
            if opp.profit_percentage >= self.min_profit_percentage
        ]
        
        logger.info(f"Detected {len(opportunities)} arbitrage opportunities")
        return opportunities
    
    def _group_similar_markets(self, markets: List[Market]) -> List[List[Market]]:
        """
        Group markets that are likely about the same event.
        For simplicity, we group binary markets with similar questions.
        In production, use more sophisticated matching.
        """
        groups = []
        
        # Simple grouping by question similarity (first word matching)
        grouped = {}
        for market in markets:
            if market.market_type != MarketType.BINARY:
                continue
            
            # Simple key: first 3 words of question
            words = market.question.lower().split()[:3]
            key = " ".join(words)
            
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(market)
        
        # Only keep groups with multiple markets
        groups = [markets for markets in grouped.values() if len(markets) >= 2]
        
        return groups
    
    def _check_market_pair(self, market_a: Market, market_b: Market) -> List[ArbitrageOpportunity]:
        """Check a pair of markets for arbitrage opportunities."""
        opportunities = []
        
        # For binary markets, check if buying opposite outcomes creates arbitrage
        if market_a.market_type == MarketType.BINARY and market_b.market_type == MarketType.BINARY:
            if len(market_a.outcomes) >= 2 and len(market_b.outcomes) >= 2:
                opportunities.extend(self._check_binary_arbitrage(market_a, market_b))
        
        return opportunities
    
    def _check_binary_arbitrage(self, market_a: Market, market_b: Market) -> List[ArbitrageOpportunity]:
        """
        Check for arbitrage in binary markets.
        
        Strategy: Buy outcome A in market 1 and opposite outcome B in market 2.
        If sum of prices < 1.0, there's guaranteed profit.
        """
        opportunities = []
        
        # Get outcomes from each market
        outcomes_a = market_a.outcomes
        outcomes_b = market_b.outcomes
        
        # Check all combinations
        for outcome_a in outcomes_a:
            for outcome_b in outcomes_b:
                # Skip if same outcome (we want opposite outcomes)
                if outcome_a.outcome_name.lower() == outcome_b.outcome_name.lower():
                    continue
                
                # Calculate arbitrage
                price_a = outcome_a.price
                price_b = outcome_b.price
                
                # Total cost to buy one unit of each
                total_cost = price_a + price_b
                
                # If total cost < 1.0, we have arbitrage (guaranteed payout is 1.0)
                if total_cost < 1.0:
                    # Calculate actual profit with real stake
                    stake = min(self.max_stake_usd, outcome_a.liquidity, outcome_b.liquidity)
                    
                    # Allocate stake proportionally
                    stake_a = stake * (price_a / total_cost)
                    stake_b = stake * (price_b / total_cost)
                    
                    # Guaranteed payout (winner pays 1.0 per unit)
                    units_a = stake_a / price_a
                    units_b = stake_b / price_b
                    
                    # Minimum payout (regardless of outcome)
                    guaranteed_payout = min(units_a, units_b)
                    total_stake = stake_a + stake_b
                    guaranteed_profit = guaranteed_payout - total_stake
                    
                    profit_percentage = (guaranteed_profit / total_stake) * 100
                    
                    if profit_percentage > 0:
                        opportunity = ArbitrageOpportunity(
                            opportunity_id=str(uuid.uuid4()),
                            market_a=market_a,
                            market_b=market_b,
                            outcome_a=outcome_a,
                            outcome_b=outcome_b,
                            profit_percentage=profit_percentage,
                            guaranteed_profit_usd=guaranteed_profit,
                            stake_required_usd=total_stake,
                            detected_at=datetime.now()
                        )
                        opportunities.append(opportunity)
        
        return opportunities
