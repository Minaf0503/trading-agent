from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel


class AnalystType(str, Enum):
    MARKET = "market"
    SOCIAL = "social"
    NEWS = "news"
    FUNDAMENTALS = "fundamentals"
    CRYPTO_MARKET = "crypto_market"
    CRYPTO_ONCHAIN = "crypto_onchain"
    CRYPTO_DEFI = "crypto_defi"
