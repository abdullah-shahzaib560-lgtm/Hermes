# hermes/core/models/analysis/fundamental.py
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import date


@dataclass
class CompanyFundamental:
    symbol: str

    # Identity
    name: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None

    # Market data (point-in-time)
    market_cap: Optional[float] = None
    shares_outstanding: Optional[float] = None
    price: Optional[float] = None  

    revenue: Optional[float] = None
    revenue_growth_yoy: Optional[float] = None
    gross_profit: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_income: Optional[float] = None
    operating_margin: Optional[float] = None
    net_income: Optional[float] = None
    net_margin: Optional[float] = None
    eps_ttm: Optional[float] = None
    eps_growth_yoy: Optional[float] = None

    # Cash flow
    operating_cash_flow: Optional[float] = None
    capex: Optional[float] = None
    free_cash_flow: Optional[float] = None

    # Balance sheet
    total_debt: Optional[float] = None
    cash_and_equivalents: Optional[float] = None
    total_assets: Optional[float] = None
    total_equity: Optional[float] = None
    current_assets: Optional[float] = None
    current_liabilities: Optional[float] = None
    interest_expense: Optional[float] = None
    ebit: Optional[float] = None

    # Derived ratios
    roe: Optional[float] = None
    roic: Optional[float] = None
    roa: Optional[float] = None
    current_ratio: Optional[float] = None
    debt_to_equity: Optional[float] = None
    interest_coverage: Optional[float] = None

    # Valuation
    pe_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    ev_ebitda: Optional[float] = None
    peg_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    fcf_yield: Optional[float] = None

    earnings_quality_score: Optional[float] = None

    source_map: Dict[str, List[str]] = field(default_factory=dict)
    as_of_date: Optional[date] = None