from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class CompanyFundamental:

    ticker: str
    filing_date: date
    fiscal_period: str 
    fiscal_year: int
    filing_type: str

    revenue: int
    cost_of_revenue: int
    gross_profit: int
    operating_expenses: int
    operating_income: int
    interest_expense: Optional[int]
    pre_tax_income: int
    income_tax_expense: int
    net_income: int
    eps_basic: float
    eps_diluted: float

    cash: int
    short_term_investments: Optional[int]
    accounts_receivable: int
    inventory: Optional[int]
    current_assets: int
    total_assets: int
    current_liabilities: int
    short_term_debt: Optional[int]
    long_term_debt: int
    total_liabilities: int
    equity: int

    operating_cash_flow: int
    investing_cash_flow: int
    financing_cash_flow: int
    capital_expenditure: int

    shares_outstanding: int
    weighted_average_shares: int
    dividends: Optional[int] = 0
    buybacks: Optional[int] = 0

    current_price: float
    market_cap: int
    pe_ratio: Optional[float] = field(default=None, metadata={"alias": "P/E"})
    ps_ratio: Optional[float] = field(default=None, metadata={"alias": "P/S"})
    pb_ratio: Optional[float] = field(default=None, metadata={"alias": "P/B"})
    ev_ebitda: Optional[float] = field(default=None, metadata={"alias": "EV/EBITDA"})
    roe: Optional[float] = field(default=None, metadata={"alias": "ROE"})
    roa: Optional[float] = field(default=None, metadata={"alias": "ROA"})
    debt_equity: Optional[float] = field(default=None, metadata={"alias": "Debt/Equity"})

    earnings: float
    eps_estimates: float
    revenue_estimates: int
    ebitda_estimates: int
    earnings_surprise: float
    revenue_surprise: float
    company_peers: List[str] = field(default_factory=list)

    macro_gdp: int
    macro_gdp_growth: float
    macro_inflation: float
    macro_interest_rates: float
    macro_unemployment: float
    macro_government_debt: float
    macro_exchange_rates: dict = field(default_factory=dict)