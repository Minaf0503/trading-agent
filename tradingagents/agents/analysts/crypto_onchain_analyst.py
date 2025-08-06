"""
Crypto Onchain Analyst for TradingAgents
Analyzes blockchain data including transactions, liquidity pools, and holder metrics
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from tradingagents.dataflows.crypto_utils import OnchainAnalytics

def create_crypto_onchain_analyst(llm, toolkit):
    """Create a crypto onchain analyst that focuses on blockchain data"""
    
    def crypto_onchain_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]  # This will be the token symbol
        token_address = state.get("token_address", None)  # Token contract address
        
        # Initialize onchain analytics
        onchain_analytics = OnchainAnalytics()
        
        # Get onchain data if address is available
        onchain_data = {}
        if token_address:
            onchain_data = onchain_analytics.get_token_onchain_data(token_address)
            liquidity_metrics = onchain_analytics.analyze_liquidity_metrics(token_address)
            holder_metrics = onchain_analytics.analyze_holder_metrics(token_address)
            transaction_metrics = onchain_analytics.analyze_transaction_metrics(token_address)
        else:
            # Fallback to basic analysis without onchain data
            onchain_data = {"error": "No token address provided"}
            liquidity_metrics = {"error": "No token address provided"}
            holder_metrics = {"error": "No token address provided"}
            transaction_metrics = {"error": "No token address provided"}
        
        # Create tools for the analyst
        tools = [
            toolkit.get_onchain_liquidity_data,
            toolkit.get_onchain_holder_data,
            toolkit.get_onchain_transaction_data,
            toolkit.get_onchain_supply_data,
            toolkit.get_defi_protocol_data,
        ]
        
        system_message = (
            """You are a crypto onchain analyst specializing in blockchain data analysis. Your role is to analyze onchain metrics and provide insights based on blockchain activity.

Key areas to analyze:

1. **Liquidity Analysis:**
   - Total liquidity across all DEXs
   - Liquidity distribution by DEX
   - Liquidity depth and slippage
   - Liquidity concentration risks
   - New liquidity additions/removals

2. **Holder Analysis:**
   - Total number of holders
   - Holder concentration (top 10, top 100)
   - Whale activity and large transactions
   - Holder growth/decline trends
   - Average holding size

3. **Transaction Analysis:**
   - Transaction volume and frequency
   - Average transaction size
   - Large transaction patterns
   - DEX trading activity
   - Transfer patterns (inflows/outflows)

4. **Supply Analysis:**
   - Circulating vs total supply
   - Supply distribution
   - Token burning/minting events
   - Vesting schedules
   - Inflation/deflation mechanisms

5. **DeFi Integration:**
   - Protocol TVL and usage
   - Yield farming opportunities
   - Lending/borrowing activity
   - Governance participation
   - Cross-protocol integration

6. **Risk Assessment:**
   - Liquidity risks
   - Concentration risks
   - Smart contract risks
   - Regulatory risks
   - Market manipulation risks

Please provide a comprehensive analysis focusing on:
- Onchain activity trends
- Liquidity health and risks
- Holder behavior patterns
- Supply dynamics
- DeFi ecosystem integration
- Risk factors and mitigation strategies

Make sure to append a Markdown table at the end organizing key onchain metrics and insights."""
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
            "crypto_onchain_report": report,
        }
    
    return crypto_onchain_analyst_node 