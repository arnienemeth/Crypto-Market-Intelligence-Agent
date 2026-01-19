# services/crypto_api.py
"""
Real-time Cryptocurrency Data Service
Fetches live market data from CoinGecko API (free, no API key required)
"""

import requests
from typing import Optional
from datetime import datetime


class CryptoAPIService:
    """Service for fetching real-time cryptocurrency data"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    # Mapping common symbols to CoinGecko IDs
    SYMBOL_TO_ID = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "BNB": "binancecoin",
        "XRP": "ripple",
        "ADA": "cardano",
        "DOGE": "dogecoin",
        "SOL": "solana",
        "DOT": "polkadot",
        "MATIC": "matic-network",
        "LTC": "litecoin",
        "AVAX": "avalanche-2",
        "LINK": "chainlink",
        "UNI": "uniswap",
        "ATOM": "cosmos",
        "XLM": "stellar",
    }
    
    @classmethod
    def get_coin_id(cls, symbol: str) -> str:
        """Convert symbol to CoinGecko ID"""
        return cls.SYMBOL_TO_ID.get(symbol.upper(), symbol.lower())
    
    @classmethod
    def get_current_price(cls, symbol: str) -> dict:
        """Get current price with 24h change"""
        coin_id = cls.get_coin_id(symbol)
        
        try:
            response = requests.get(
                f"{cls.BASE_URL}/simple/price",
                params={
                    "ids": coin_id,
                    "vs_currencies": "usd,eur",
                    "include_24hr_vol": "true",
                    "include_24hr_change": "true",
                    "include_market_cap": "true",
                    "include_last_updated_at": "true"
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if coin_id in data:
                return {
                    "symbol": symbol.upper(),
                    "coin_id": coin_id,
                    "price_usd": data[coin_id].get("usd"),
                    "price_eur": data[coin_id].get("eur"),
                    "change_24h_percent": round(data[coin_id].get("usd_24h_change", 0), 2),
                    "volume_24h_usd": data[coin_id].get("usd_24h_vol"),
                    "market_cap_usd": data[coin_id].get("usd_market_cap"),
                    "last_updated": datetime.fromtimestamp(
                        data[coin_id].get("last_updated_at", 0)
                    ).isoformat(),
                    "status": "success"
                }
            else:
                return {"status": "error", "message": f"Coin {symbol} not found"}
                
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    @classmethod
    def get_detailed_market_data(cls, symbol: str) -> dict:
        """Get comprehensive market data for analysis"""
        coin_id = cls.get_coin_id(symbol)
        
        try:
            response = requests.get(
                f"{cls.BASE_URL}/coins/{coin_id}",
                params={
                    "localization": "false",
                    "tickers": "false",
                    "community_data": "false",
                    "developer_data": "false"
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            market_data = data.get("market_data", {})
            
            return {
                "symbol": symbol.upper(),
                "name": data.get("name"),
                "current_price_usd": market_data.get("current_price", {}).get("usd"),
                "current_price_eur": market_data.get("current_price", {}).get("eur"),
                "market_cap_usd": market_data.get("market_cap", {}).get("usd"),
                "market_cap_rank": data.get("market_cap_rank"),
                "total_volume_24h": market_data.get("total_volume", {}).get("usd"),
                "high_24h": market_data.get("high_24h", {}).get("usd"),
                "low_24h": market_data.get("low_24h", {}).get("usd"),
                "price_change_24h": market_data.get("price_change_24h"),
                "price_change_percentage_24h": round(market_data.get("price_change_percentage_24h", 0), 2),
                "price_change_percentage_7d": round(market_data.get("price_change_percentage_7d", 0), 2),
                "price_change_percentage_30d": round(market_data.get("price_change_percentage_30d", 0), 2),
                "ath": market_data.get("ath", {}).get("usd"),
                "ath_change_percentage": round(market_data.get("ath_change_percentage", {}).get("usd", 0), 2),
                "atl": market_data.get("atl", {}).get("usd"),
                "circulating_supply": market_data.get("circulating_supply"),
                "total_supply": market_data.get("total_supply"),
                "max_supply": market_data.get("max_supply"),
                "last_updated": market_data.get("last_updated"),
                "status": "success"
            }
            
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    @classmethod
    def get_market_overview(cls, limit: int = 10) -> dict:
        """Get top cryptocurrencies by market cap"""
        try:
            response = requests.get(
                f"{cls.BASE_URL}/coins/markets",
                params={
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": limit,
                    "page": 1,
                    "sparkline": "false",
                    "price_change_percentage": "24h,7d"
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            coins = []
            for coin in data:
                coins.append({
                    "rank": coin.get("market_cap_rank"),
                    "symbol": coin.get("symbol", "").upper(),
                    "name": coin.get("name"),
                    "price_usd": coin.get("current_price"),
                    "change_24h": round(coin.get("price_change_percentage_24h", 0), 2),
                    "change_7d": round(coin.get("price_change_percentage_7d_in_currency", 0) or 0, 2),
                    "volume_24h": coin.get("total_volume"),
                    "market_cap": coin.get("market_cap")
                })
            
            return {
                "timestamp": datetime.now().isoformat(),
                "count": len(coins),
                "coins": coins,
                "status": "success"
            }
            
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    @classmethod
    def get_fear_greed_index(cls) -> dict:
        """Get Fear & Greed Index from alternative.me"""
        try:
            response = requests.get(
                "https://api.alternative.me/fng/",
                params={"limit": 1},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("data"):
                fng = data["data"][0]
                return {
                    "value": int(fng.get("value", 0)),
                    "classification": fng.get("value_classification"),
                    "timestamp": fng.get("timestamp"),
                    "status": "success"
                }
            return {"status": "error", "message": "No data available"}
            
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}


# ============================================
# LangChain Tool Functions
# ============================================

def get_market_data(symbol: str) -> str:
    """
    Get real-time market data for a cryptocurrency.
    Use this tool to fetch current price, 24h change, volume, and market cap.
    Input: cryptocurrency symbol (e.g., 'BTC', 'ETH', 'SOL')
    """
    data = CryptoAPIService.get_detailed_market_data(symbol)
    
    if data.get("status") == "error":
        return f"Error fetching data for {symbol}: {data.get('message')}"
    
    # Format response for the agent
    response = f"""
📊 **{data['name']} ({data['symbol']}) Market Data**

💰 **Current Price:** ${data['current_price_usd']:,.2f} (€{data['current_price_eur']:,.2f})
📈 **24h Change:** {data['price_change_percentage_24h']:+.2f}%
📊 **7d Change:** {data['price_change_percentage_7d']:+.2f}%
📉 **30d Change:** {data['price_change_percentage_30d']:+.2f}%

📊 **24h Range:** ${data['low_24h']:,.2f} - ${data['high_24h']:,.2f}
💎 **Market Cap:** ${data['market_cap_usd']:,.0f} (Rank #{data['market_cap_rank']})
📈 **24h Volume:** ${data['total_volume_24h']:,.0f}

🏆 **All-Time High:** ${data['ath']:,.2f} ({data['ath_change_percentage']:+.2f}% from ATH)
📉 **All-Time Low:** ${data['atl']:,.2f}

⏰ **Last Updated:** {data['last_updated']}

**Trend Analysis:**
- 24h: {"🟢 BULLISH" if data['price_change_percentage_24h'] > 0 else "🔴 BEARISH"}
- 7d: {"🟢 BULLISH" if data['price_change_percentage_7d'] > 0 else "🔴 BEARISH"}
- 30d: {"🟢 BULLISH" if data['price_change_percentage_30d'] > 0 else "🔴 BEARISH"}
"""
    return response


def get_market_overview(query: str = "") -> str:
    """
    Get overview of top cryptocurrencies by market cap.
    Use this to see the overall market state and top performers.
    Input: optional, can be empty or 'top 10', 'market overview'
    """
    data = CryptoAPIService.get_market_overview(limit=10)
    
    if data.get("status") == "error":
        return f"Error fetching market overview: {data.get('message')}"
    
    response = f"📊 **Top 10 Cryptocurrencies by Market Cap**\n"
    response += f"⏰ {data['timestamp']}\n\n"
    
    for coin in data['coins']:
        trend_24h = "🟢" if coin['change_24h'] > 0 else "🔴"
        response += f"**#{coin['rank']} {coin['symbol']}** ({coin['name']})\n"
        response += f"   💰 ${coin['price_usd']:,.2f} | {trend_24h} {coin['change_24h']:+.2f}% (24h)\n\n"
    
    return response


def get_fear_greed(query: str = "") -> str:
    """
    Get the current Crypto Fear & Greed Index.
    This indicates market sentiment: Extreme Fear (0-25), Fear (25-45), 
    Neutral (45-55), Greed (55-75), Extreme Greed (75-100).
    Input: optional, can be empty
    """
    data = CryptoAPIService.get_fear_greed_index()
    
    if data.get("status") == "error":
        return f"Error fetching Fear & Greed Index: {data.get('message')}"
    
    value = data['value']
    
    # Emoji based on value
    if value <= 25:
        emoji = "😱"
        recommendation = "Extreme fear often indicates buying opportunities"
    elif value <= 45:
        emoji = "😰"
        recommendation = "Market is fearful, potential accumulation zone"
    elif value <= 55:
        emoji = "😐"
        recommendation = "Market sentiment is neutral"
    elif value <= 75:
        emoji = "😀"
        recommendation = "Greed in the market, consider taking some profits"
    else:
        emoji = "🤑"
        recommendation = "Extreme greed often precedes corrections"
    
    response = f"""
📊 **Crypto Fear & Greed Index**

{emoji} **Current Value:** {value}/100
📌 **Classification:** {data['classification']}

💡 **Interpretation:** {recommendation}

The Fear & Greed Index measures market sentiment:
- 0-25: Extreme Fear
- 25-45: Fear  
- 45-55: Neutral
- 55-75: Greed
- 75-100: Extreme Greed
"""
    return response


# ============================================
# Test the service
# ============================================

if __name__ == "__main__":
    print("Testing CryptoAPIService...\n")
    
    # Test current price
    print("=== BTC Current Price ===")
    print(get_market_data("BTC"))
    
    print("\n=== Market Overview ===")
    print(get_market_overview())
    
    print("\n=== Fear & Greed Index ===")
    print(get_fear_greed())
