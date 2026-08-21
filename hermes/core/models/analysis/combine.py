from dataclasses import dataclass

from hermes.core.models.analysis.fundamental import CompanyFundamental
from hermes.core.models.analysis.technical import TechnicalSnapshot

@dataclass
class TechnicalScore:
    symbol: str
    trend_score: float          # 0–100
    momentum_score: float       # 0–100
    volatility_score: float     # 0–100 (or risk-adjusted)
    volume_score: float         # 0–100
    overall_score: float        # 0–100
    snapshot: TechnicalSnapshot

@dataclass
class FundamentalScore:
    symbol: str
    financial_quality_score: float  # 0–100
    growth_score: float
    profitability_score: float
    balance_sheet_score: float
    valuation_score: float
    overall_score: float            # 0–100
    fundamental: CompanyFundamental

@dataclass
class CombinedAnalysis:
    symbol: str
    fundamental_score: FundamentalScore
    technical_score: TechnicalScore
    overall_score: float
    signal: str  # "BULLISH", "BEARISH", "NEUTRAL"