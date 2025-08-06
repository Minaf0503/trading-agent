from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, AIMessage
from typing import List
from typing import Annotated
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import RemoveMessage
from langchain_core.tools import tool
from datetime import date, timedelta, datetime
import functools
import pandas as pd
import os
from dateutil.relativedelta import relativedelta
from langchain_openai import ChatOpenAI
import tradingagents.dataflows.interface as interface
from tradingagents.dataflows.crypto_utils import CryptoDataProvider, OnchainAnalytics
from tradingagents.default_config import DEFAULT_CONFIG
from langchain_core.messages import HumanMessage


def create_msg_delete():
    def delete_messages(state):
        """Clear messages and add placeholder for Anthropic compatibility"""
        messages = state["messages"]
        
        # Remove all messages
        removal_operations = [RemoveMessage(id=m.id) for m in messages]
        
        # Add a minimal placeholder message
        placeholder = HumanMessage(content="Continue")
        
        return {"messages": removal_operations + [placeholder]}
    
    return delete_messages


class Toolkit:
    _config = DEFAULT_CONFIG.copy()

    @classmethod
    def update_config(cls, config):
        """Update the class-level configuration."""
        cls._config.update(config)

    @property
    def config(self):
        """Access the configuration."""
        return self._config

    def __init__(self, config=None):
        if config:
            self.update_config(config)

    @staticmethod
    @tool
    def get_reddit_news(
        curr_date: Annotated[str, "Date you want to get news for in yyyy-mm-dd format"],
    ) -> str:
        """
        Retrieve global news from Reddit within a specified time frame.
        Args:
            curr_date (str): Date you want to get news for in yyyy-mm-dd format
        Returns:
            str: A formatted dataframe containing the latest global news from Reddit in the specified time frame.
        """
        
        global_news_result = interface.get_reddit_global_news(curr_date, 7, 5)

        return global_news_result

    @staticmethod
    @tool
    def get_finnhub_news(
        ticker: Annotated[
            str,
            "Search query of a company, e.g. 'AAPL, TSM, etc.",
        ],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    ):
        """
        Retrieve the latest news about a given stock from Finnhub within a date range
        Args:
            ticker (str): Ticker of a company. e.g. AAPL, TSM
            start_date (str): Start date in yyyy-mm-dd format
            end_date (str): End date in yyyy-mm-dd format
        Returns:
            str: A formatted dataframe containing news about the company within the date range from start_date to end_date
        """

        end_date_str = end_date

        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        look_back_days = (end_date - start_date).days

        finnhub_news_result = interface.get_finnhub_news(
            ticker, end_date_str, look_back_days
        )

        return finnhub_news_result

    @staticmethod
    @tool
    def get_reddit_stock_info(
        ticker: Annotated[
            str,
            "Ticker of a company. e.g. AAPL, TSM",
        ],
        curr_date: Annotated[str, "Current date you want to get news for"],
    ) -> str:
        """
        Retrieve the latest news about a given stock from Reddit, given the current date.
        Args:
            ticker (str): Ticker of a company. e.g. AAPL, TSM
            curr_date (str): current date in yyyy-mm-dd format to get news for
        Returns:
            str: A formatted dataframe containing the latest news about the company on the given date
        """

        stock_news_results = interface.get_reddit_company_news(ticker, curr_date, 7, 5)

        return stock_news_results

    @staticmethod
    @tool
    def get_YFin_data(
        symbol: Annotated[str, "ticker symbol of the company"],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    ) -> str:
        """
        Retrieve the stock price data for a given ticker symbol from Yahoo Finance.
        Args:
            symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
            start_date (str): Start date in yyyy-mm-dd format
            end_date (str): End date in yyyy-mm-dd format
        Returns:
            str: A formatted dataframe containing the stock price data for the specified ticker symbol in the specified date range.
        """

        result_data = interface.get_YFin_data(symbol, start_date, end_date)

        return result_data

    @staticmethod
    @tool
    def get_YFin_data_online(
        symbol: Annotated[str, "ticker symbol of the company"],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    ) -> str:
        """
        Retrieve the stock price data for a given ticker symbol from Yahoo Finance.
        Args:
            symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
            start_date (str): Start date in yyyy-mm-dd format
            end_date (str): End date in yyyy-mm-dd format
        Returns:
            str: A formatted dataframe containing the stock price data for the specified ticker symbol in the specified date range.
        """

        result_data = interface.get_YFin_data_online(symbol, start_date, end_date)

        return result_data

    @staticmethod
    @tool
    def get_stockstats_indicators_report(
        symbol: Annotated[str, "ticker symbol of the company"],
        indicator: Annotated[
            str, "technical indicator to get the analysis and report of"
        ],
        curr_date: Annotated[
            str, "The current trading date you are trading on, YYYY-mm-dd"
        ],
        look_back_days: Annotated[int, "how many days to look back"] = 30,
    ) -> str:
        """
        Retrieve stock stats indicators for a given ticker symbol and indicator.
        Args:
            symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
            indicator (str): Technical indicator to get the analysis and report of
            curr_date (str): The current trading date you are trading on, YYYY-mm-dd
            look_back_days (int): How many days to look back, default is 30
        Returns:
            str: A formatted dataframe containing the stock stats indicators for the specified ticker symbol and indicator.
        """

        result_stockstats = interface.get_stock_stats_indicators_window(
            symbol, indicator, curr_date, look_back_days, False
        )

        return result_stockstats

    @staticmethod
    @tool
    def get_stockstats_indicators_report_online(
        symbol: Annotated[str, "ticker symbol of the company"],
        indicator: Annotated[
            str, "technical indicator to get the analysis and report of"
        ],
        curr_date: Annotated[
            str, "The current trading date you are trading on, YYYY-mm-dd"
        ],
        look_back_days: Annotated[int, "how many days to look back"] = 30,
    ) -> str:
        """
        Retrieve stock stats indicators for a given ticker symbol and indicator.
        Args:
            symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
            indicator (str): Technical indicator to get the analysis and report of
            curr_date (str): The current trading date you are trading on, YYYY-mm-dd
            look_back_days (int): How many days to look back, default is 30
        Returns:
            str: A formatted dataframe containing the stock stats indicators for the specified ticker symbol and indicator.
        """

        result_stockstats = interface.get_stock_stats_indicators_window(
            symbol, indicator, curr_date, look_back_days, True
        )

        return result_stockstats

    @staticmethod
    @tool
    def get_finnhub_company_insider_sentiment(
        ticker: Annotated[str, "ticker symbol for the company"],
        curr_date: Annotated[
            str,
            "current date of you are trading at, yyyy-mm-dd",
        ],
    ):
        """
        Retrieve insider sentiment information about a company (retrieved from public SEC information) for the past 30 days
        Args:
            ticker (str): ticker symbol of the company
            curr_date (str): current date you are trading at, yyyy-mm-dd
        Returns:
            str: a report of the sentiment in the past 30 days starting at curr_date
        """

        data_sentiment = interface.get_finnhub_company_insider_sentiment(
            ticker, curr_date, 30
        )

        return data_sentiment

    @staticmethod
    @tool
    def get_finnhub_company_insider_transactions(
        ticker: Annotated[str, "ticker symbol"],
        curr_date: Annotated[
            str,
            "current date you are trading at, yyyy-mm-dd",
        ],
    ):
        """
        Retrieve insider transaction information about a company (retrieved from public SEC information) for the past 30 days
        Args:
            ticker (str): ticker symbol of the company
            curr_date (str): current date you are trading at, yyyy-mm-dd
        Returns:
            str: a report of the company's insider transactions/trading information in the past 30 days
        """

        data_trans = interface.get_finnhub_company_insider_transactions(
            ticker, curr_date, 30
        )

        return data_trans

    @staticmethod
    @tool
    def get_simfin_balance_sheet(
        ticker: Annotated[str, "ticker symbol"],
        freq: Annotated[
            str,
            "reporting frequency of the company's financial history: annual/quarterly",
        ],
        curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
    ):
        """
        Retrieve the most recent balance sheet of a company
        Args:
            ticker (str): ticker symbol of the company
            freq (str): reporting frequency of the company's financial history: annual / quarterly
            curr_date (str): current date you are trading at, yyyy-mm-dd
        Returns:
            str: a report of the company's most recent balance sheet
        """

        data_balance_sheet = interface.get_simfin_balance_sheet(ticker, freq, curr_date)

        return data_balance_sheet

    @staticmethod
    @tool
    def get_simfin_cashflow(
        ticker: Annotated[str, "ticker symbol"],
        freq: Annotated[
            str,
            "reporting frequency of the company's financial history: annual/quarterly",
        ],
        curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
    ):
        """
        Retrieve the most recent cash flow statement of a company
        Args:
            ticker (str): ticker symbol of the company
            freq (str): reporting frequency of the company's financial history: annual / quarterly
            curr_date (str): current date you are trading at, yyyy-mm-dd
        Returns:
                str: a report of the company's most recent cash flow statement
        """

        data_cashflow = interface.get_simfin_cashflow(ticker, freq, curr_date)

        return data_cashflow

    @staticmethod
    @tool
    def get_simfin_income_stmt(
        ticker: Annotated[str, "ticker symbol"],
        freq: Annotated[
            str,
            "reporting frequency of the company's financial history: annual/quarterly",
        ],
        curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
    ):
        """
        Retrieve the most recent income statement of a company
        Args:
            ticker (str): ticker symbol of the company
            freq (str): reporting frequency of the company's financial history: annual / quarterly
            curr_date (str): current date you are trading at, yyyy-mm-dd
        Returns:
                str: a report of the company's most recent income statement
        """

        data_income_stmt = interface.get_simfin_income_statements(
            ticker, freq, curr_date
        )

        return data_income_stmt

    @staticmethod
    @tool
    def get_google_news(
        query: Annotated[str, "Query to search with"],
        curr_date: Annotated[str, "Curr date in yyyy-mm-dd format"],
    ):
        """
        Retrieve the latest news from Google News based on a query and date range.
        Args:
            query (str): Query to search with
            curr_date (str): Current date in yyyy-mm-dd format
            look_back_days (int): How many days to look back
        Returns:
            str: A formatted string containing the latest news from Google News based on the query and date range.
        """

        google_news_results = interface.get_google_news(query, curr_date, 7)

        return google_news_results

    # Crypto-specific tools
    @staticmethod
    @tool
    def get_crypto_price_data(
        token_symbol: Annotated[str, "Token symbol (e.g., BTC, ETH, UNI)"],
        vs_currency: Annotated[str, "Quote currency (e.g., USD, EUR)"] = "usd",
    ):
        """
        Get current crypto price data from CoinGecko
        Args:
            token_symbol (str): Token symbol (e.g., BTC, ETH, UNI)
            vs_currency (str): Quote currency (e.g., USD, EUR)
        Returns:
            str: Current price data and market metrics
        """
        crypto_provider = CryptoDataProvider()
        market_data = crypto_provider.get_crypto_market_data(token_symbol)
        
        if "error" in market_data.get("price_data", {}):
            return f"Error getting price data for {token_symbol}: {market_data['price_data']['error']}"
        
        price_data = market_data["price_data"]
        return f"Price data for {token_symbol}: {json.dumps(price_data, indent=2)}"

    @staticmethod
    @tool
    def get_crypto_technical_indicators(
        token_symbol: Annotated[str, "Token symbol (e.g., BTC, ETH, UNI)"],
    ):
        """
        Get technical indicators for crypto token
        Args:
            token_symbol (str): Token symbol (e.g., BTC, ETH, UNI)
        Returns:
            str: Technical analysis data
        """
        crypto_provider = CryptoDataProvider()
        technical_data = crypto_provider.get_crypto_technical_analysis(token_symbol)
        
        if "error" in technical_data:
            return f"Error getting technical data for {token_symbol}: {technical_data['error']}"
        
        return f"Technical analysis for {token_symbol}: {json.dumps(technical_data, indent=2)}"

    @staticmethod
    @tool
    def get_crypto_market_metrics(
        token_symbol: Annotated[str, "Token symbol (e.g., BTC, ETH, UNI)"],
    ):
        """
        Get comprehensive market metrics for crypto token
        Args:
            token_symbol (str): Token symbol (e.g., BTC, ETH, UNI)
        Returns:
            str: Market metrics data
        """
        crypto_provider = CryptoDataProvider()
        market_data = crypto_provider.get_crypto_market_data(token_symbol)
        
        if "error" in market_data.get("market_data", {}):
            return f"Error getting market data for {token_symbol}: {market_data['market_data']['error']}"
        
        return f"Market metrics for {token_symbol}: {json.dumps(market_data['market_data'], indent=2)}"

    @staticmethod
    @tool
    def get_crypto_volume_analysis(
        token_symbol: Annotated[str, "Token symbol (e.g., BTC, ETH, UNI)"],
    ):
        """
        Get volume analysis for crypto token
        Args:
            token_symbol (str): Token symbol (e.g., BTC, ETH, UNI)
        Returns:
            str: Volume analysis data
        """
        crypto_provider = CryptoDataProvider()
        market_data = crypto_provider.get_crypto_market_data(token_symbol)
        
        if "error" in market_data.get("price_data", {}):
            return f"Error getting volume data for {token_symbol}: {market_data['price_data']['error']}"
        
        price_data = market_data["price_data"]
        volume_24h = price_data.get("usd_24h_vol", 0)
        market_cap = price_data.get("usd_market_cap", 0)
        
        return f"Volume analysis for {token_symbol}: 24h Volume: ${volume_24h:,.0f}, Market Cap: ${market_cap:,.0f}"

    @staticmethod
    @tool
    def get_onchain_liquidity_data(
        token_address: Annotated[str, "Token contract address"],
        network: Annotated[str, "Blockchain network (e.g., ethereum, polygon)"] = "ethereum",
    ):
        """
        Get onchain liquidity data for token
        Args:
            token_address (str): Token contract address
            network (str): Blockchain network
        Returns:
            str: Liquidity analysis data
        """
        onchain_analytics = OnchainAnalytics(network)
        liquidity_data = onchain_analytics.analyze_liquidity_metrics(token_address)
        
        if "error" in liquidity_data:
            return f"Error getting liquidity data: {liquidity_data['error']}"
        
        return f"Liquidity analysis: {json.dumps(liquidity_data, indent=2)}"

    @staticmethod
    @tool
    def get_onchain_holder_data(
        token_address: Annotated[str, "Token contract address"],
        network: Annotated[str, "Blockchain network (e.g., ethereum, polygon)"] = "ethereum",
    ):
        """
        Get onchain holder data for token
        Args:
            token_address (str): Token contract address
            network (str): Blockchain network
        Returns:
            str: Holder analysis data
        """
        onchain_analytics = OnchainAnalytics(network)
        holder_data = onchain_analytics.analyze_holder_metrics(token_address)
        
        if "error" in holder_data:
            return f"Error getting holder data: {holder_data['error']}"
        
        return f"Holder analysis: {json.dumps(holder_data, indent=2)}"

    @staticmethod
    @tool
    def get_onchain_transaction_data(
        token_address: Annotated[str, "Token contract address"],
        network: Annotated[str, "Blockchain network (e.g., ethereum, polygon)"] = "ethereum",
    ):
        """
        Get onchain transaction data for token
        Args:
            token_address (str): Token contract address
            network (str): Blockchain network
        Returns:
            str: Transaction analysis data
        """
        onchain_analytics = OnchainAnalytics(network)
        transaction_data = onchain_analytics.analyze_transaction_metrics(token_address)
        
        if "error" in transaction_data:
            return f"Error getting transaction data: {transaction_data['error']}"
        
        return f"Transaction analysis: {json.dumps(transaction_data, indent=2)}"

    @staticmethod
    @tool
    def get_onchain_supply_data(
        token_address: Annotated[str, "Token contract address"],
        network: Annotated[str, "Blockchain network (e.g., ethereum, polygon)"] = "ethereum",
    ):
        """
        Get onchain supply data for token
        Args:
            token_address (str): Token contract address
            network (str): Blockchain network
        Returns:
            str: Supply analysis data
        """
        onchain_analytics = OnchainAnalytics(network)
        onchain_data = onchain_analytics.get_token_onchain_data(token_address)
        
        if "error" in onchain_data:
            return f"Error getting supply data: {onchain_data['error']}"
        
        supply_data = onchain_data.get("supply", {})
        return f"Supply analysis: {json.dumps(supply_data, indent=2)}"

    @staticmethod
    @tool
    def get_defi_protocol_data(
        protocol: Annotated[str, "DeFi protocol name (e.g., uniswap, aave, compound)"],
    ):
        """
        Get DeFi protocol data
        Args:
            protocol (str): DeFi protocol name
        Returns:
            str: Protocol analysis data
        """
        crypto_provider = CryptoDataProvider()
        protocol_data = crypto_provider.get_defi_protocol_analysis(protocol)
        
        if "error" in protocol_data:
            return f"Error getting protocol data for {protocol}: {protocol_data['error']}"
        
        return f"Protocol analysis for {protocol}: {json.dumps(protocol_data, indent=2)}"

    @staticmethod
    @tool
    def get_defi_yield_data(
        protocol: Annotated[str, "DeFi protocol name (e.g., uniswap, aave, compound)"],
    ):
        """
        Get DeFi yield opportunities
        Args:
            protocol (str): DeFi protocol name
        Returns:
            str: Yield analysis data
        """
        crypto_provider = CryptoDataProvider()
        protocol_data = crypto_provider.get_defi_protocol_analysis(protocol)
        
        if "error" in protocol_data:
            return f"Error getting yield data for {protocol}: {protocol_data['error']}"
        
        return f"Yield analysis for {protocol}: {json.dumps(protocol_data, indent=2)}"

    @staticmethod
    @tool
    def get_defi_tvl_data(
        protocol: Annotated[str, "DeFi protocol name (e.g., uniswap, aave, compound)"],
    ):
        """
        Get DeFi TVL data
        Args:
            protocol (str): DeFi protocol name
        Returns:
            str: TVL analysis data
        """
        crypto_provider = CryptoDataProvider()
        protocol_data = crypto_provider.get_defi_protocol_analysis(protocol)
        
        if "error" in protocol_data:
            return f"Error getting TVL data for {protocol}: {protocol_data['error']}"
        
        tvl = protocol_data.get("tvl", 0)
        tvl_change_1d = protocol_data.get("tvl_change_1d", 0)
        tvl_change_7d = protocol_data.get("tvl_change_7d", 0)
        
        return f"TVL analysis for {protocol}: Current TVL: ${tvl:,.0f}, 1d change: {tvl_change_1d:.2f}%, 7d change: {tvl_change_7d:.2f}%"

    @staticmethod
    @tool
    def get_defi_governance_data(
        protocol: Annotated[str, "DeFi protocol name (e.g., uniswap, aave, compound)"],
    ):
        """
        Get DeFi governance data
        Args:
            protocol (str): DeFi protocol name
        Returns:
            str: Governance analysis data
        """
        crypto_provider = CryptoDataProvider()
        protocol_data = crypto_provider.get_defi_protocol_analysis(protocol)
        
        if "error" in protocol_data:
            return f"Error getting governance data for {protocol}: {protocol_data['error']}"
        
        return f"Governance analysis for {protocol}: {json.dumps(protocol_data, indent=2)}"

    @staticmethod
    @tool
    def get_defi_risk_data(
        protocol: Annotated[str, "DeFi protocol name (e.g., uniswap, aave, compound)"],
    ):
        """
        Get DeFi risk assessment
        Args:
            protocol (str): DeFi protocol name
        Returns:
            str: Risk analysis data
        """
        crypto_provider = CryptoDataProvider()
        protocol_data = crypto_provider.get_defi_protocol_analysis(protocol)
        
        if "error" in protocol_data:
            return f"Error getting risk data for {protocol}: {protocol_data['error']}"
        
        return f"Risk analysis for {protocol}: {json.dumps(protocol_data, indent=2)}"

    @staticmethod
    @tool
    def get_stock_news_openai(
        ticker: Annotated[str, "the company's ticker"],
        curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    ):
        """
        Retrieve the latest news about a given stock by using OpenAI's news API.
        Args:
            ticker (str): Ticker of a company. e.g. AAPL, TSM
            curr_date (str): Current date in yyyy-mm-dd format
        Returns:
            str: A formatted string containing the latest news about the company on the given date.
        """

        openai_news_results = interface.get_stock_news_openai(ticker, curr_date)

        return openai_news_results

    @staticmethod
    @tool
    def get_global_news_openai(
        curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    ):
        """
        Retrieve the latest macroeconomics news on a given date using OpenAI's macroeconomics news API.
        Args:
            curr_date (str): Current date in yyyy-mm-dd format
        Returns:
            str: A formatted string containing the latest macroeconomic news on the given date.
        """

        openai_news_results = interface.get_global_news_openai(curr_date)

        return openai_news_results

    @staticmethod
    @tool
    def get_fundamentals_openai(
        ticker: Annotated[str, "the company's ticker"],
        curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    ):
        """
        Retrieve the latest fundamental information about a given stock on a given date by using OpenAI's news API.
        Args:
            ticker (str): Ticker of a company. e.g. AAPL, TSM
            curr_date (str): Current date in yyyy-mm-dd format
        Returns:
            str: A formatted string containing the latest fundamental information about the company on the given date.
        """

        openai_fundamentals_results = interface.get_fundamentals_openai(
            ticker, curr_date
        )

        return openai_fundamentals_results
