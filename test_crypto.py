#!/usr/bin/env python3
"""
Test script for TradingAgents crypto functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradingagents.dataflows.crypto_utils import CryptoDataProvider, OnchainAnalytics
import json

def test_crypto_data_provider():
    """Test the crypto data provider functionality"""
    print("🔍 Testing Crypto Data Provider...")
    
    # Initialize crypto data provider
    crypto_provider = CryptoDataProvider()
    
    # Test with Bitcoin
    print("\n📊 Testing Bitcoin (BTC) analysis...")
    try:
        btc_data = crypto_provider.get_crypto_market_data("BTC")
        print(f"✅ Bitcoin market data retrieved successfully")
        print(f"   - Price data available: {'price_data' in btc_data}")
        print(f"   - Market data available: {'market_data' in btc_data}")
        print(f"   - Price history available: {'price_history' in btc_data}")
    except Exception as e:
        print(f"❌ Error getting Bitcoin data: {e}")
    
    # Test with Ethereum
    print("\n📊 Testing Ethereum (ETH) analysis...")
    try:
        eth_data = crypto_provider.get_crypto_market_data("ETH")
        print(f"✅ Ethereum market data retrieved successfully")
        print(f"   - Price data available: {'price_data' in eth_data}")
        print(f"   - Market data available: {'market_data' in eth_data}")
        print(f"   - Price history available: {'price_history' in eth_data}")
    except Exception as e:
        print(f"❌ Error getting Ethereum data: {e}")
    
    # Test technical analysis
    print("\n📈 Testing technical analysis...")
    try:
        btc_technical = crypto_provider.get_crypto_technical_analysis("BTC")
        if "error" not in btc_technical:
            print(f"✅ Technical analysis successful")
            print(f"   - Current price: ${btc_technical.get('current_price', 'N/A'):,.2f}")
            print(f"   - RSI: {btc_technical.get('rsi', 'N/A'):.2f}")
            print(f"   - MACD: {btc_technical.get('macd', 'N/A'):.4f}")
        else:
            print(f"⚠️  Technical analysis warning: {btc_technical['error']}")
    except Exception as e:
        print(f"❌ Error in technical analysis: {e}")
    
    # Test DeFi protocol analysis
    print("\n🏦 Testing DeFi protocol analysis...")
    try:
        uniswap_data = crypto_provider.get_defi_protocol_analysis("uniswap")
        if "error" not in uniswap_data:
            print(f"✅ Uniswap protocol data retrieved successfully")
            print(f"   - TVL: ${uniswap_data.get('tvl', 0):,.0f}")
            print(f"   - 1d change: {uniswap_data.get('tvl_change_1d', 0):.2f}%")
            print(f"   - 7d change: {uniswap_data.get('tvl_change_7d', 0):.2f}%")
        else:
            print(f"⚠️  DeFi protocol warning: {uniswap_data['error']}")
    except Exception as e:
        print(f"❌ Error in DeFi protocol analysis: {e}")

def test_onchain_analytics():
    """Test the onchain analytics functionality"""
    print("\n🔗 Testing Onchain Analytics...")
    
    # Initialize onchain analytics
    onchain_analytics = OnchainAnalytics("ethereum")
    
    # Test with UNI token (Uniswap)
    print("\n📊 Testing UNI token onchain analysis...")
    uni_address = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"  # UNI token
    
    try:
        onchain_data = onchain_analytics.get_token_onchain_data(uni_address)
        if "error" not in onchain_data:
            print(f"✅ UNI onchain data retrieved successfully")
            print(f"   - Metadata available: {'metadata' in onchain_data}")
            print(f"   - Price data available: {'price' in onchain_data}")
            print(f"   - Liquidity data available: {'liquidity' in onchain_data}")
            print(f"   - Holder data available: {'holders' in onchain_data}")
        else:
            print(f"⚠️  Onchain data warning: {onchain_data['error']}")
    except Exception as e:
        print(f"❌ Error getting onchain data: {e}")
    
    # Test liquidity analysis
    print("\n💧 Testing liquidity analysis...")
    try:
        liquidity_metrics = onchain_analytics.analyze_liquidity_metrics(uni_address)
        if "error" not in liquidity_metrics:
            print(f"✅ Liquidity analysis successful")
            print(f"   - Total liquidity: ${liquidity_metrics.get('total_liquidity', 0):,.0f}")
            print(f"   - Pool count: {liquidity_metrics.get('pool_count', 0)}")
        else:
            print(f"⚠️  Liquidity analysis warning: {liquidity_metrics['error']}")
    except Exception as e:
        print(f"❌ Error in liquidity analysis: {e}")
    
    # Test holder analysis
    print("\n👥 Testing holder analysis...")
    try:
        holder_metrics = onchain_analytics.analyze_holder_metrics(uni_address)
        if "error" not in holder_metrics:
            print(f"✅ Holder analysis successful")
            print(f"   - Total holders: {holder_metrics.get('total_holders', 0):,}")
            print(f"   - Top 10 percentage: {holder_metrics.get('top_10_percentage', 0):.2f}%")
            print(f"   - Whale count: {holder_metrics.get('whale_count', 0)}")
        else:
            print(f"⚠️  Holder analysis warning: {holder_metrics['error']}")
    except Exception as e:
        print(f"❌ Error in holder analysis: {e}")

def test_crypto_analysts():
    """Test the crypto analyst functionality"""
    print("\n🤖 Testing Crypto Analysts...")
    
    # Test crypto market analyst
    print("\n📊 Testing Crypto Market Analyst...")
    try:
        from tradingagents.agents.analysts.crypto_market_analyst import create_crypto_market_analyst
        print("✅ Crypto Market Analyst module imported successfully")
    except Exception as e:
        print(f"❌ Error importing Crypto Market Analyst: {e}")
    
    # Test crypto onchain analyst
    print("\n🔗 Testing Crypto Onchain Analyst...")
    try:
        from tradingagents.agents.analysts.crypto_onchain_analyst import create_crypto_onchain_analyst
        print("✅ Crypto Onchain Analyst module imported successfully")
    except Exception as e:
        print(f"❌ Error importing Crypto Onchain Analyst: {e}")
    
    # Test crypto DeFi analyst
    print("\n🏦 Testing Crypto DeFi Analyst...")
    try:
        from tradingagents.agents.analysts.crypto_defi_analyst import create_crypto_defi_analyst
        print("✅ Crypto DeFi Analyst module imported successfully")
    except Exception as e:
        print(f"❌ Error importing Crypto DeFi Analyst: {e}")

def test_toolkit():
    """Test the crypto toolkit functionality"""
    print("\n🛠️  Testing Crypto Toolkit...")
    
    try:
        from tradingagents.agents.utils.agent_utils import Toolkit
        toolkit = Toolkit()
        print("✅ Toolkit initialized successfully")
        
        # Test crypto tools
        crypto_tools = [
            'get_crypto_price_data',
            'get_crypto_technical_indicators',
            'get_crypto_market_metrics',
            'get_crypto_volume_analysis',
            'get_onchain_liquidity_data',
            'get_onchain_holder_data',
            'get_onchain_transaction_data',
            'get_onchain_supply_data',
            'get_defi_protocol_data',
            'get_defi_yield_data',
            'get_defi_tvl_data',
            'get_defi_governance_data',
            'get_defi_risk_data',
        ]
        
        available_tools = []
        for tool_name in crypto_tools:
            if hasattr(toolkit, tool_name):
                available_tools.append(tool_name)
                print(f"   ✅ {tool_name}")
            else:
                print(f"   ❌ {tool_name} - Not found")
        
        print(f"\n📊 Crypto tools available: {len(available_tools)}/{len(crypto_tools)}")
        
    except Exception as e:
        print(f"❌ Error testing toolkit: {e}")

def main():
    """Run all crypto tests"""
    print("🚀 TradingAgents Crypto Functionality Test")
    print("=" * 50)
    
    # Test crypto data provider
    test_crypto_data_provider()
    
    # Test onchain analytics
    test_onchain_analytics()
    
    # Test crypto analysts
    test_crypto_analysts()
    
    # Test toolkit
    test_toolkit()
    
    print("\n" + "=" * 50)
    print("✅ Crypto functionality test completed!")
    print("\n📝 Next steps:")
    print("   1. Set your OPENAI_API_KEY environment variable")
    print("   2. Run: python -m cli.main analyze")
    print("   3. Select crypto analysts when prompted")
    print("   4. Enter a crypto token symbol (e.g., BTC, ETH, UNI)")

if __name__ == "__main__":
    main() 