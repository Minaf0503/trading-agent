# TradingAgents Crypto Modifications

This document outlines the modifications made to TradingAgents to support cryptocurrency analysis using Coinbase's AgentKit and crypto-specific data sources.

## Overview

The TradingAgents project has been enhanced to analyze crypto assets instead of traditional stocks. The modifications include:

1. **Crypto Price Oracles** - Integration with CoinGecko, DefiLlama, and other crypto data sources
2. **Onchain Analytics** - Blockchain data analysis using AgentKit
3. **Crypto-Specific Analyst Teams** - Specialized analysts for crypto markets
4. **DeFi Protocol Analysis** - Analysis of DeFi ecosystem metrics

## New Data Sources

### 1. Crypto Price Oracles (`tradingagents/dataflows/crypto_utils.py`)

**CryptoPriceOracle Class:**
- **CoinGecko API** - Real-time crypto prices, market data, and historical data
- **DefiLlama API** - DeFi protocol TVL and metrics
- **Binance API** - Additional price data source

**Key Features:**
- Real-time price data for 1000+ cryptocurrencies
- Historical price data for technical analysis
- Market cap, volume, and supply data
- DeFi protocol metrics

### 2. Onchain Analytics (`OnchainAnalytics Class`)

**Blockchain Data Analysis:**
- **Liquidity Pool Analysis** - TVL, distribution across DEXs, concentration risks
- **Holder Analysis** - Holder distribution, whale activity, concentration metrics
- **Transaction Analysis** - Transfer patterns, DEX trading activity, volume analysis
- **Supply Analysis** - Circulating vs total supply, vesting schedules

**AgentKit Integration:**
- Token metadata and price data
- Liquidity pool data from multiple DEXs
- Holder and transaction data
- Cross-chain analytics support

### 3. DeFi Protocol Analysis

**Protocol Metrics:**
- Total Value Locked (TVL) and trends
- Yield opportunities and APY/APR rates
- Governance token analysis
- Risk assessment for DeFi protocols

## New Analyst Teams

### 1. Crypto Market Analyst (`crypto_market_analyst.py`)

**Focus Areas:**
- **Technical Analysis** - RSI, MACD, Bollinger Bands, moving averages
- **Market Metrics** - Market cap, volume, supply dynamics
- **Crypto-Specific Indicators** - Fear & Greed Index, network activity
- **Risk Assessment** - Volatility, liquidity, regulatory risks

**Data Sources:**
- CoinGecko price and market data
- Technical indicators calculated from historical data
- Crypto-specific sentiment and social data

### 2. Crypto Onchain Analyst (`crypto_onchain_analyst.py`)

**Focus Areas:**
- **Liquidity Analysis** - DEX liquidity, concentration risks, depth analysis
- **Holder Analysis** - Distribution, whale activity, growth trends
- **Transaction Analysis** - Volume patterns, transfer behavior, DEX activity
- **Supply Analysis** - Tokenomics, vesting, inflation/deflation

**Data Sources:**
- AgentKit blockchain data
- Onchain transaction analysis
- Liquidity pool metrics
- Holder distribution data

### 3. Crypto DeFi Analyst (`crypto_defi_analyst.py`)

**Focus Areas:**
- **Protocol Fundamentals** - TVL, revenue, user growth
- **Yield Opportunities** - APY/APR, farming rewards, staking
- **Governance Analysis** - Token distribution, voting power, proposals
- **Risk Assessment** - Smart contract risks, oracle risks, competition

**Data Sources:**
- DefiLlama protocol data
- DeFi ecosystem metrics
- Governance token analysis
- Cross-protocol integration data

## Enhanced Toolkit

### New Crypto Tools (`agent_utils.py`)

**Price & Market Tools:**
- `get_crypto_price_data()` - Real-time price data from CoinGecko
- `get_crypto_technical_indicators()` - Technical analysis for crypto
- `get_crypto_market_metrics()` - Comprehensive market data
- `get_crypto_volume_analysis()` - Volume and market cap analysis

**Onchain Tools:**
- `get_onchain_liquidity_data()` - Liquidity pool analysis
- `get_onchain_holder_data()` - Holder distribution analysis
- `get_onchain_transaction_data()` - Transaction pattern analysis
- `get_onchain_supply_data()` - Supply and tokenomics analysis

**DeFi Tools:**
- `get_defi_protocol_data()` - Protocol fundamentals
- `get_defi_yield_data()` - Yield opportunities
- `get_defi_tvl_data()` - TVL analysis
- `get_defi_governance_data()` - Governance analysis
- `get_defi_risk_data()` - Risk assessment

## Installation & Setup

### 1. Install Dependencies

```bash
# Install AgentKit and crypto dependencies
pip install coinbase-agentkit requests pandas

# Or update requirements.txt and install all
pip install -r requirements.txt
```

### 2. Configure API Keys (Optional)

For enhanced functionality, you can set up API keys:

```bash
# Set environment variables for additional APIs
export COINGECKO_API_KEY="your_api_key"  # Optional, for higher rate limits
export DEFILLAMA_API_KEY="your_api_key"   # Optional
```

### 3. Run Crypto Analysis

```bash
# Run analysis with crypto analysts
python -m cli.main analyze

# Select crypto analysts when prompted:
# - Crypto Market Analyst
# - Crypto Onchain Analyst  
# - Crypto DeFi Analyst
```

## Usage Examples

### 1. Basic Crypto Analysis

```python
from tradingagents.dataflows.crypto_utils import CryptoDataProvider

# Initialize crypto data provider
crypto_provider = CryptoDataProvider()

# Get market data for Bitcoin
btc_data = crypto_provider.get_crypto_market_data("BTC")

# Get technical analysis
btc_technical = crypto_provider.get_crypto_technical_analysis("BTC")

# Get DeFi protocol data
uniswap_data = crypto_provider.get_defi_protocol_analysis("uniswap")
```

### 2. Onchain Analysis

```python
from tradingagents.dataflows.crypto_utils import OnchainAnalytics

# Initialize onchain analytics
onchain_analytics = OnchainAnalytics("ethereum")

# Get comprehensive onchain data
token_address = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"  # UNI token
onchain_data = onchain_analytics.get_token_onchain_data(token_address)

# Analyze liquidity metrics
liquidity_metrics = onchain_analytics.analyze_liquidity_metrics(token_address)

# Analyze holder metrics
holder_metrics = onchain_analytics.analyze_holder_metrics(token_address)
```

### 3. CLI Analysis

```bash
# Analyze Bitcoin with crypto analysts
python -m cli.main analyze
# Enter: BTC
# Select: Crypto Market Analyst, Crypto Onchain Analyst, Crypto DeFi Analyst

# Analyze Ethereum DeFi token
python -m cli.main analyze
# Enter: UNI
# Select: Crypto Market Analyst, Crypto Onchain Analyst, Crypto DeFi Analyst
```

## Supported Tokens

### Major Cryptocurrencies
- **BTC** - Bitcoin
- **ETH** - Ethereum
- **USDC** - USD Coin
- **USDT** - Tether
- **DAI** - Dai

### DeFi Tokens
- **UNI** - Uniswap
- **LINK** - Chainlink
- **AAVE** - Aave
- **COMP** - Compound
- **CRV** - Curve DAO
- **SUSHI** - SushiSwap
- **YFI** - Yearn Finance
- **BAL** - Balancer
- **SNX** - Synthetix
- **MKR** - Maker

### Networks Supported
- **Ethereum** - Mainnet and testnets
- **Polygon** - Layer 2 scaling
- **Base** - Coinbase's L2
- **Solana** - High-performance blockchain

## Report Structure

### Crypto Analysis Reports

Reports are saved in the same structure as traditional analysis:

```
results/
└── {TOKEN_SYMBOL}/
    └── {DATE}/
        ├── complete_report_YYYYMMDD_HHMMSS.md
        ├── analysis_summary_YYYYMMDD_HHMMSS.json
        └── reports/
            ├── crypto_market_report.md      # Technical & market analysis
            ├── crypto_onchain_report.md     # Blockchain data analysis
            └── crypto_defi_report.md        # DeFi ecosystem analysis
```

### Report Content

**Crypto Market Report:**
- Current price and 24h change
- Technical indicators (RSI, MACD, Bollinger Bands)
- Market metrics (market cap, volume, supply)
- Risk assessment and trading recommendations

**Crypto Onchain Report:**
- Liquidity analysis across DEXs
- Holder distribution and whale activity
- Transaction patterns and volume analysis
- Supply dynamics and tokenomics

**Crypto DeFi Report:**
- Protocol TVL and growth metrics
- Yield opportunities and APY analysis
- Governance token analysis
- Risk assessment for DeFi protocols

## Integration with AgentKit

### AgentKit Features Used

1. **Action Providers** - 50+ blockchain actions
2. **Wallet Providers** - CDP, Privy, ViEM integration
3. **Protocol Support** - Compound, DefiLlama, Jupiter, etc.
4. **Network Support** - Base, Ethereum, Solana

### Key AgentKit Actions

```python
from coinbase_agentkit.action_providers import (
    get_token_price,
    get_token_metadata,
    get_liquidity_pool_data,
    get_dex_trades,
    get_token_holders,
    get_token_supply,
    get_defi_protocol_data,
)
```

## Future Enhancements

### Planned Features

1. **Cross-Chain Analysis** - Multi-chain token analysis
2. **NFT Analytics** - NFT market and collection analysis
3. **MEV Analysis** - Miner extractable value analysis
4. **Social Sentiment** - Crypto-specific social media analysis
5. **Regulatory Analysis** - Regulatory risk assessment

### Potential Integrations

1. **The Graph** - Subgraph data integration
2. **Dune Analytics** - Custom blockchain queries
3. **Messari** - Institutional-grade crypto data
4. **Glassnode** - Onchain analytics platform
5. **Santiment** - Social sentiment data

## Troubleshooting

### Common Issues

1. **AgentKit Import Errors**
   ```bash
   pip install coinbase-agentkit --upgrade
   ```

2. **API Rate Limits**
   - Use API keys for higher limits
   - Implement rate limiting in data providers

3. **Network Connectivity**
   - Check internet connection
   - Verify API endpoints are accessible

4. **Token Address Issues**
   - Ensure correct contract addresses
   - Verify network compatibility

### Debug Mode

Enable debug mode for detailed logging:

```python
# Set debug flag in configuration
config["debug"] = True
```

## Contributing

### Adding New Crypto Data Sources

1. Create new data provider class
2. Add corresponding tools to toolkit
3. Update analyst prompts
4. Add tests and documentation

### Adding New Analyst Types

1. Create analyst module
2. Add to CLI models and utils
3. Update graph setup
4. Add tool nodes

## License

This crypto modification maintains the same license as the original TradingAgents project.

## Acknowledgments

- **Coinbase AgentKit** - For blockchain data integration
- **CoinGecko** - For comprehensive crypto market data
- **DefiLlama** - For DeFi protocol metrics
- **Ethereum Foundation** - For blockchain infrastructure 