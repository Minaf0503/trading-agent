"""
Crypto DeFi Analyst for TradingAgents
Analyzes DeFi protocol data, yield opportunities, and ecosystem metrics
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from tradingagents.dataflows.crypto_utils import CryptoDataProvider

def create_crypto_defi_analyst(llm, toolkit):
    """Create a crypto DeFi analyst that focuses on DeFi ecosystem analysis"""
    
    def crypto_defi_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]  # This will be the token symbol
        
        # Initialize crypto data provider
        crypto_provider = CryptoDataProvider()
        
        # Get DeFi protocol data
        defi_data = crypto_provider.get_defi_protocol_analysis(ticker.lower())
        
        # Create tools for the analyst
        tools = [
            toolkit.get_defi_protocol_data,
            toolkit.get_defi_yield_data,
            toolkit.get_defi_tvl_data,
            toolkit.get_defi_governance_data,
            toolkit.get_defi_risk_data,
        ]
        
        system_message = (
            """You are a crypto DeFi analyst specializing in decentralized finance protocol analysis. Your role is to analyze DeFi ecosystem metrics and provide insights for DeFi investment decisions.

Key areas to analyze:

1. **Protocol Fundamentals:**
   - Total Value Locked (TVL)
   - TVL growth/decline trends
   - Protocol revenue and fees
   - User growth and retention
   - Market share in DeFi ecosystem

2. **Yield Opportunities:**
   - Current APY/APR rates
   - Yield farming opportunities
   - Liquidity mining rewards
   - Staking rewards
   - Risk-adjusted returns

3. **Liquidity Analysis:**
   - Liquidity depth across DEXs
   - Liquidity provider incentives
   - Impermanent loss risks
   - Liquidity concentration
   - Cross-chain liquidity

4. **Governance & Tokenomics:**
   - Governance token distribution
   - Voting power concentration
   - Proposal activity
   - Token utility and demand
   - Vesting schedules

5. **Risk Assessment:**
   - Smart contract risks
   - Oracle risks
   - Liquidation risks
   - Regulatory risks
   - Competition risks

6. **Ecosystem Integration:**
   - Cross-protocol integrations
   - Partnership opportunities
   - Developer activity
   - Community growth
   - Innovation pipeline

7. **Market Positioning:**
   - Competitive advantages
   - Market differentiation
   - Growth potential
   - Adoption barriers
   - Network effects

Please provide a comprehensive analysis focusing on:
- Protocol health and sustainability
- Yield opportunities and risks
- Governance effectiveness
- Ecosystem integration
- Competitive positioning
- Investment recommendations

Make sure to append a Markdown table at the end organizing key DeFi metrics and insights."""
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
            "crypto_defi_report": report,
        }
    
    return crypto_defi_analyst_node 