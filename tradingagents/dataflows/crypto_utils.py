"""
Crypto-specific data utilities for TradingAgents
Uses AgentKit and crypto price oracles for blockchain data
"""

import requests
import json
from typing import Dict, List, Optional, Annotated
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
import os

# AgentKit imports
try:
    from coinbase_agentkit import AgentKit
    from coinbase_agentkit.action_providers import (
        get_token_price,
        get_token_metadata,
        get_token_balance,
        get_token_transfers,
        get_liquidity_pool_data,
        get_dex_trades,
        get_token_holders,
        get_token_supply,
        get_token_market_cap,
        get_token_volume_24h,
        get_token_price_history,
        get_defi_protocol_data,
        get_token_social_sentiment,
        get_token_news,
        get_token_technical_indicators,
    )
    AGENTKIT_AVAILABLE = True
except ImportError:
    AGENTKIT_AVAILABLE = False
    print("Warning: AgentKit not available. Install with: pip install coinbase-agentkit")

# Crypto price oracle APIs
class CryptoPriceOracle:
    """Crypto price oracle integration"""
    
    def __init__(self):
        self.coingecko_api = "https://api.coingecko.com/api/v3"
        self.binance_api = "https://api.binance.com/api/v3"
        self.defillama_api = "https://api.llama.fi"
        
    def get_token_price_coingecko(self, token_id: str, vs_currency: str = "usd") -> Dict:
        """Get token price from CoinGecko"""
        try:
            url = f"{self.coingecko_api}/simple/price"
            params = {
                "ids": token_id,
                "vs_currencies": vs_currency,
                "include_24hr_change": "true",
                "include_market_cap": "true",
                "include_24hr_vol": "true"
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"CoinGecko API error: {str(e)}"}
    
    def get_token_market_data(self, token_id: str) -> Dict:
        """Get comprehensive market data from CoinGecko"""
        try:
            url = f"{self.coingecko_api}/coins/{token_id}"
            params = {
                "localization": "false",
                "tickers": "false",
                "market_data": "true",
                "community_data": "true",
                "developer_data": "true",
                "sparkline": "false"
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"CoinGecko market data error: {str(e)}"}
    
    def get_token_price_history(self, token_id: str, days: int = 30, vs_currency: str = "usd") -> Dict:
        """Get historical price data"""
        try:
            url = f"{self.coingecko_api}/coins/{token_id}/market_chart"
            params = {
                "vs_currency": vs_currency,
                "days": days
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"CoinGecko history error: {str(e)}"}
    
    def get_defi_protocol_data(self, protocol: str) -> Dict:
        """Get DeFi protocol data from DefiLlama"""
        try:
            url = f"{self.defillama_api}/protocol/{protocol}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"DefiLlama API error: {str(e)}"}

class OnchainAnalytics:
    """Onchain analytics using AgentKit and blockchain data"""
    
    def __init__(self, network: str = "ethereum"):
        self.network = network
        self.agentkit = AgentKit() if AGENTKIT_AVAILABLE else None
        
    def get_token_onchain_data(self, token_address: str) -> Dict:
        """Get comprehensive onchain data for a token"""
        if not AGENTKIT_AVAILABLE:
            return {"error": "AgentKit not available"}
            
        try:
            # Get token metadata
            metadata = get_token_metadata(token_address, self.network)
            
            # Get price data
            price_data = get_token_price(token_address, self.network)
            
            # Get liquidity data
            liquidity_data = get_liquidity_pool_data(token_address, self.network)
            
            # Get holder data
            holders_data = get_token_holders(token_address, self.network)
            
            # Get supply data
            supply_data = get_token_supply(token_address, self.network)
            
            # Get recent transfers
            transfers_data = get_token_transfers(token_address, self.network, limit=100)
            
            # Get DEX trades
            dex_trades = get_dex_trades(token_address, self.network, limit=50)
            
            return {
                "metadata": metadata,
                "price": price_data,
                "liquidity": liquidity_data,
                "holders": holders_data,
                "supply": supply_data,
                "transfers": transfers_data,
                "dex_trades": dex_trades
            }
        except Exception as e:
            return {"error": f"Onchain data error: {str(e)}"}
    
    def analyze_liquidity_metrics(self, token_address: str) -> Dict:
        """Analyze liquidity pool metrics"""
        if not AGENTKIT_AVAILABLE:
            return {"error": "AgentKit not available"}
            
        try:
            liquidity_data = get_liquidity_pool_data(token_address, self.network)
            
            # Calculate liquidity metrics
            total_liquidity = sum(pool.get("tvl", 0) for pool in liquidity_data.get("pools", []))
            pool_count = len(liquidity_data.get("pools", []))
            
            # Analyze liquidity distribution
            liquidity_distribution = {}
            for pool in liquidity_data.get("pools", []):
                dex = pool.get("dex", "unknown")
                tvl = pool.get("tvl", 0)
                if dex not in liquidity_distribution:
                    liquidity_distribution[dex] = 0
                liquidity_distribution[dex] += tvl
            
            return {
                "total_liquidity": total_liquidity,
                "pool_count": pool_count,
                "liquidity_distribution": liquidity_distribution,
                "pools": liquidity_data.get("pools", [])
            }
        except Exception as e:
            return {"error": f"Liquidity analysis error: {str(e)}"}
    
    def analyze_holder_metrics(self, token_address: str) -> Dict:
        """Analyze token holder metrics"""
        if not AGENTKIT_AVAILABLE:
            return {"error": "AgentKit not available"}
            
        try:
            holders_data = get_token_holders(token_address, self.network)
            
            # Calculate holder metrics
            total_holders = len(holders_data.get("holders", []))
            total_supply = holders_data.get("total_supply", 0)
            
            # Analyze concentration
            top_10_holders = holders_data.get("holders", [])[:10]
            top_10_percentage = sum(holder.get("percentage", 0) for holder in top_10_holders)
            
            # Analyze whale activity
            whale_threshold = 0.01  # 1% of supply
            whales = [h for h in holders_data.get("holders", []) if h.get("percentage", 0) > whale_threshold]
            
            return {
                "total_holders": total_holders,
                "total_supply": total_supply,
                "top_10_percentage": top_10_percentage,
                "whale_count": len(whales),
                "holder_distribution": holders_data.get("holders", [])
            }
        except Exception as e:
            return {"error": f"Holder analysis error: {str(e)}"}
    
    def analyze_transaction_metrics(self, token_address: str) -> Dict:
        """Analyze transaction patterns"""
        if not AGENTKIT_AVAILABLE:
            return {"error": "AgentKit not available"}
            
        try:
            transfers_data = get_token_transfers(token_address, self.network, limit=1000)
            dex_trades = get_dex_trades(token_address, self.network, limit=500)
            
            # Analyze transfer patterns
            transfers = transfers_data.get("transfers", [])
            total_transfers = len(transfers)
            total_volume = sum(t.get("value", 0) for t in transfers)
            
            # Analyze trade patterns
            trades = dex_trades.get("trades", [])
            total_trades = len(trades)
            total_trade_volume = sum(t.get("value", 0) for t in trades)
            
            # Calculate metrics
            avg_transfer_size = total_volume / total_transfers if total_transfers > 0 else 0
            avg_trade_size = total_trade_volume / total_trades if total_trades > 0 else 0
            
            return {
                "total_transfers": total_transfers,
                "total_transfer_volume": total_volume,
                "avg_transfer_size": avg_transfer_size,
                "total_trades": total_trades,
                "total_trade_volume": total_trade_volume,
                "avg_trade_size": avg_trade_size,
                "recent_transfers": transfers[:50],
                "recent_trades": trades[:50]
            }
        except Exception as e:
            return {"error": f"Transaction analysis error: {str(e)}"}

class CryptoDataProvider:
    """Main crypto data provider combining multiple sources"""
    
    def __init__(self, network: str = "ethereum"):
        self.network = network
        self.price_oracle = CryptoPriceOracle()
        self.onchain_analytics = OnchainAnalytics(network)
        
    def get_crypto_market_data(self, token_symbol: str, token_address: str = None) -> Dict:
        """Get comprehensive crypto market data"""
        # Map common symbols to CoinGecko IDs
        symbol_to_id = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "USDC": "usd-coin",
            "USDT": "tether",
            "DAI": "dai",
            "UNI": "uniswap",
            "LINK": "chainlink",
            "AAVE": "aave",
            "COMP": "compound-governance-token",
            "CRV": "curve-dao-token",
            "SUSHI": "sushi",
            "YFI": "yearn-finance",
            "BAL": "balancer",
            "SNX": "havven",
            "MKR": "maker",
            "REN": "republic-protocol",
            "BAND": "band-protocol",
            "ZRX": "0x",
            "BAT": "basic-attention-token",
            "REP": "augur",
        }
        
        token_id = symbol_to_id.get(token_symbol.upper(), token_symbol.lower())
        
        # Get price data
        price_data = self.price_oracle.get_token_price_coingecko(token_id)
        market_data = self.price_oracle.get_token_market_data(token_id)
        price_history = self.price_oracle.get_token_price_history(token_id, days=30)
        
        # Get onchain data if address provided
        onchain_data = {}
        if token_address:
            onchain_data = self.onchain_analytics.get_token_onchain_data(token_address)
        
        return {
            "symbol": token_symbol,
            "token_id": token_id,
            "price_data": price_data,
            "market_data": market_data,
            "price_history": price_history,
            "onchain_data": onchain_data
        }
    
    def get_crypto_technical_analysis(self, token_symbol: str) -> Dict:
        """Get technical analysis for crypto"""
        token_id = token_symbol.lower()
        
        # Get price history for technical analysis
        price_history = self.price_oracle.get_token_price_history(token_id, days=90)
        
        if "error" in price_history:
            return price_history
        
        # Calculate technical indicators
        prices = price_history.get("prices", [])
        if not prices:
            return {"error": "No price data available"}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        
        # Calculate moving averages
        df["sma_20"] = df["price"].rolling(window=20).mean()
        df["sma_50"] = df["price"].rolling(window=50).mean()
        df["ema_12"] = df["price"].ewm(span=12).mean()
        df["ema_26"] = df["price"].ewm(span=26).mean()
        
        # Calculate RSI
        delta = df["price"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))
        
        # Calculate Bollinger Bands
        df["bb_middle"] = df["price"].rolling(window=20).mean()
        bb_std = df["price"].rolling(window=20).std()
        df["bb_upper"] = df["bb_middle"] + (bb_std * 2)
        df["bb_lower"] = df["bb_middle"] - (bb_std * 2)
        
        # Calculate MACD
        df["macd"] = df["ema_12"] - df["ema_26"]
        df["macd_signal"] = df["macd"].ewm(span=9).mean()
        df["macd_histogram"] = df["macd"] - df["macd_signal"]
        
        # Get latest values
        latest = df.iloc[-1]
        
        return {
            "current_price": latest["price"],
            "sma_20": latest["sma_20"],
            "sma_50": latest["sma_50"],
            "rsi": latest["rsi"],
            "bb_upper": latest["bb_upper"],
            "bb_middle": latest["bb_middle"],
            "bb_lower": latest["bb_lower"],
            "macd": latest["macd"],
            "macd_signal": latest["macd_signal"],
            "macd_histogram": latest["macd_histogram"],
            "price_data": df.tail(30).to_dict("records")
        }
    
    def get_defi_protocol_analysis(self, protocol: str) -> Dict:
        """Analyze DeFi protocol data"""
        protocol_data = self.price_oracle.get_defi_protocol_data(protocol)
        
        if "error" in protocol_data:
            return protocol_data
        
        # Extract key metrics
        tvl = protocol_data.get("tvl", 0)
        tvl_change_1d = protocol_data.get("change_1d", 0)
        tvl_change_7d = protocol_data.get("change_7d", 0)
        
        return {
            "protocol": protocol,
            "tvl": tvl,
            "tvl_change_1d": tvl_change_1d,
            "tvl_change_7d": tvl_change_7d,
            "protocol_data": protocol_data
        } 