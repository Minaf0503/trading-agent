"""
Crypto Market Analyst for TradingAgents
Analyzes crypto market data using price oracles and technical indicators
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from tradingagents.dataflows.crypto_utils import CryptoDataProvider

def create_crypto_market_analyst(llm, toolkit):
    """Create a crypto market analyst that focuses on crypto-specific metrics"""
    
    def crypto_market_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]  # This will be the token symbol
        
        # Initialize crypto data provider
        crypto_provider = CryptoDataProvider()
        
        # Get crypto market data
        market_data = crypto_provider.get_crypto_market_data(ticker)
        technical_data = crypto_provider.get_crypto_technical_analysis(ticker)
        
        # Create tools for the analyst
        tools = [
            toolkit.get_crypto_price_data,
            toolkit.get_crypto_technical_indicators,
            toolkit.get_crypto_market_metrics,
            toolkit.get_crypto_volume_analysis,
        ]
        
        system_message = (
            """You are a crypto market analyst specializing in cryptocurrency trading analysis. Your role is to analyze crypto-specific metrics and provide insights for trading decisions.

Key areas to analyze:

1. **Price Action & Technical Analysis:**
   - Current price and 24h change
   - Moving averages (SMA, EMA)
   - RSI for overbought/oversold conditions
   - Bollinger Bands for volatility
   - MACD for momentum signals
   - Support and resistance levels

2. **Market Metrics:**
   - Market capitalization
   - 24h trading volume
   - Circulating supply vs total supply
   - Market dominance
   - Price correlation with BTC/ETH

3. **Crypto-Specific Indicators:**
   - Fear & Greed Index
   - Network activity (transactions, active addresses)
   - Exchange flows (inflows/outflows)
   - Social sentiment
   - Developer activity

4. **Risk Assessment:**
   - Volatility analysis
   - Liquidity assessment
   - Market manipulation risks
   - Regulatory considerations

Please provide a comprehensive analysis focusing on:
- Current market position and trend
- Key technical levels and signals
- Risk/reward assessment
- Short-term and medium-term outlook
- Trading recommendations with clear entry/exit points

Make sure to append a Markdown table at the end organizing key metrics and insights."""
        )
        
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. The crypto token we want to analyze is {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        
        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)
        
        chain = prompt | llm.bind_tools(tools)
        
        result = chain.invoke(state["messages"])
        
        report = ""
        
        if len(result.tool_calls) == 0:
            report = result.content
        
        return {
            "messages": [result],
            "crypto_market_report": report,
        }
    
    return crypto_market_analyst_node 