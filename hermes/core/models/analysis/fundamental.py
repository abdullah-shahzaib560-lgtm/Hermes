from dataclasses import dataclass, field
from datetime import date


@dataclass
class CompanyFundamental:

    symbol: str
    filing_date: date
    fiscal_period: str
    fiscal_year: int
    filing_type: str

    revenue: int
    cost_of_revenue: int
    gross_profit: int
    operating_expenses: int
    operating_income: int
    interest_expense: int | None
    pre_tax_income: int
    income_tax_expense: int
    net_income: int
    eps_basic: float
    eps_diluted: float

    cash: int
    short_term_investments: int | None
    accounts_receivable: int
    inventory: int | None
    current_assets: int
    total_assets: int
    current_liabilities: int
    short_term_debt: int | None
    long_term_debt: int
    total_liabilities: int
    equity: int

    operating_cash_flow: int
    investing_cash_flow: int
    financing_cash_flow: int
    capital_expenditure: int

    shares_outstanding: int
    weighted_average_shares: int

    current_price: float
    market_cap: int

    earnings: float
    eps_estimates: float
    revenue_estimates: int
    earnings_surprise: float
    revenue_surprise: float


    macro_gdp: int
    macro_gdp_growth: float
    macro_inflation: float
    macro_interest_rates: float
    macro_unemployment: float
    macro_government_debt: float

    macro_exchange_rates: dict[str, float] = field(default_factory=dict)
    company_peers: list[str] = field(default_factory=list)
    dividends: int | None = 0
    buybacks: int | None = 0
    pe_ratio: float | None = field(default=None, metadata={"alias": "P/E"})
    ps_ratio: float | None = field(default=None, metadata={"alias": "P/S"})
    pb_ratio: float | None = field(default=None, metadata={"alias": "P/B"})
    ev_ebitda: float | None = field(default=None, metadata={"alias": "EV/EBITDA"})
    roe: float | None = field(default=None, metadata={"alias": "ROE"})
    roa: float | None = field(default=None, metadata={"alias": "ROA"})
    debt_equity: float | None = field(default=None, metadata={"alias": "Debt/Equity"})
