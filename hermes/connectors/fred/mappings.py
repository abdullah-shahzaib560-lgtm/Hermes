fred_series = [
    # Growth
    "GDPC1",  # Real GDP
    "A191RL1Q225SBEA",  # GDP growth
    "INDPRO",  # Industrial Production
    # Inflation
    "CPIAUCSL",  # CPI
    "CPILFESL",  # Core CPI
    "PCEPI",  # PCE
    "PCEPILFE",  # Core PCE
    # Employment
    "UNRATE",  # Unemployment
    "PAYEMS",  # Nonfarm Payrolls
    "CIVPART",  # Labor Force Participation
    # Interest rates
    "FEDFUNDS",  # Fed Funds Rate
    "DGS10",  # 10Y Treasury
    "DGS2",  # 2Y Treasury
    "DGS3MO",  # 3M Treasury
    # Yield curve
    "T10Y2Y",  # 10Y - 2Y
    "T10Y3M",  # 10Y - 3M
    # Money/credit
    "M2SL",  # M2
    "TOTBKCR",  # Bank Credit
    # Housing
    "HOUST",  # Housing Starts
    "EXHOSLUSM495S",  # Existing Home Sales
    # Markets
    "SP500",  # S&P 500
    "VIXCLS",  # VIX
    # Dollar
    "DTWEXBGS",  # USD Index
]

# https://api.stlouisfed.org/fred/series/observations?series_id=GNPCA&api_key={api}&file_type=json

__all__ = ["fred_series"]
