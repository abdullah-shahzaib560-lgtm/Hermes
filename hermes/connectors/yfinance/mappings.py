from typing import Literal

YfinanceEndpoint = Literal[
    "eps_estimate",
    "revenue_estimate",
    "earnings_history",
]

YfinanceEndpoints = [
    "eps_estimate",
    "revenue_estimate",
    "earnings_history",
]

__all__ = ["YfinanceEndpoint", "YfinanceEndpoints"]
