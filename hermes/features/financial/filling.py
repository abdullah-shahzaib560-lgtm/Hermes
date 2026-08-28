import logging

import numpy as np
import pandas as pd

from hermes.connectors.finnhub import FINNHUB
from hermes.connectors.sec import SECEDGAR
from hermes.connectors.sec.tags import SEC_TAG_MAP
from hermes.connectors.yfinance import Yfinance

logger = logging.getLogger(__name__)


def _to_float(value: object) -> float:
    return float(value)  # type: ignore


def _extract_periods(facts: dict, quarters: int) -> list[dict]:
    seen_periods: set[tuple[int, str]] = set()
    rows: list[dict] = []

    for field, tags in SEC_TAG_MAP.items():
        for tag in tags:
            if tag not in facts:
                continue
            tag_data = facts[tag]
            units = tag_data.get("units", {})
            for unit_type, entries in units.items():
                for entry in entries:
                    fy = entry.get("fy")
                    fp = entry.get("fp")
                    if fy is None or fp is None:
                        continue
                    period_key = (fy, fp)
                    if period_key in seen_periods:
                        continue
                    seen_periods.add(period_key)
                    rows.append(
                        {
                            "fiscal_year": fy,
                            "fiscal_period": fp,
                            "filing_date": entry.get("filed"),
                            "filing_type": entry.get("form"),
                        }
                    )
                break
            if rows:
                break
        if rows:
            break

    rows.sort(key=lambda r: (r["fiscal_year"], r["fiscal_period"]), reverse=True)
    return rows[:quarters]


def _extract_funds_per_period(facts: dict, periods: list[dict], symbol: str) -> list[dict]:
    result_rows: list[dict] = []

    for period in periods:
        period_facts: dict[str, object] = {}
        for field, tags in SEC_TAG_MAP.items():
            period_facts[field] = None
            for tag in tags:
                if tag not in facts:
                    continue
                tag_data = facts[tag]
                units = tag_data.get("units", {})
                for unit_type, entries in units.items():
                    for entry in entries:
                        if entry.get("fy") == period["fiscal_year"] and entry.get("fp") == period["fiscal_period"]:
                            period_facts[field] = entry.get("val")
                            break
                    if period_facts[field] is not None:
                        break
                if period_facts[field] is not None:
                    break

        r = period_facts.get("revenue")
        cor = period_facts.get("cost_of_revenue")
        oi = period_facts.get("operating_income")
        gp = period_facts.get("gross_profit")

        if gp is None and r is not None and cor is not None:
            try:
                period_facts["gross_profit"] = _to_float(r) - _to_float(cor)
            except (TypeError, ValueError):
                pass

        gp = period_facts.get("gross_profit")
        if period_facts.get("operating_expenses") is None and gp is not None and oi is not None:
            try:
                period_facts["operating_expenses"] = _to_float(gp) - _to_float(oi)
            except (TypeError, ValueError):
                pass

        result_rows.append(
            {
                "ticker": symbol,
                "filing_date": period["filing_date"],
                "fiscal_period": period["fiscal_period"],
                "fiscal_year": period["fiscal_year"],
                "filing_type": period["filing_type"],
                **period_facts,
            }
        )

    return result_rows


class CompanyFiling:
    def __init__(
        self,
        finnhub_api: str,
        sec_email: str,
        sec_username: str,
        fred_api: str,
    ):
        self.finn = FINNHUB(api=finnhub_api)
        self.sec = SECEDGAR(username=sec_username, email=sec_email)
        self.yf = Yfinance()

    async def get_candle_history(
        self,
        symbol: str,
        interval: str = "1d",
        years: int = 2,
    ) -> pd.DataFrame:
        from hermes.constants import FINNHUB_RESOLUTION_MAP, SUPPORTED_STOCK_FREQS

        if interval not in SUPPORTED_STOCK_FREQS:
            raise ValueError(f"Interval {interval!r} not supported for stocks. Supported: {SUPPORTED_STOCK_FREQS}")

        resolution = FINNHUB_RESOLUTION_MAP[interval]

        df_finn = await self.finn.fetch_candles_history(
            symbol=symbol,
            resolution=resolution,
            years=years,
        )

        if not df_finn.empty and len(df_finn) > 100:
            df_finn["symbol"] = symbol
            df_finn["interval"] = interval
            return df_finn

        logger.info(f"Finnhub returned {len(df_finn)} rows for {symbol}, falling back to yfinance")

        df_yf = await self.yf.fetch_history(
            symbol=symbol,
            interval=interval,
            years=years,
        )

        if not df_yf.empty:
            df_yf["symbol"] = symbol
            df_yf["interval"] = interval

        return df_yf

    async def get_history(
        self,
        quarters: int = 8,
        symbols: list[str] | None = None,
    ) -> pd.DataFrame:
        from hermes.constants import TICKERS

        symbols = symbols or TICKERS
        all_dfs: list[pd.DataFrame] = []

        for symbol in symbols:
            try:
                raw = await self.sec.fetch(symbol=symbol)
            except Exception:
                logger.warning(f"Failed to fetch SEC data for {symbol}")
                continue

            if raw is None or "facts" not in raw:
                continue

            facts = raw["facts"].get("us-gaap")
            if not facts:
                continue

            periods = _extract_periods(facts, quarters)
            if not periods:
                continue

            rows = _extract_funds_per_period(facts, periods, symbol)
            if rows:
                df_sym = pd.DataFrame(rows)
                df_sym = CompanyFiling._compute_fundamental_features(df_sym)
                all_dfs.append(df_sym)

        if not all_dfs:
            return pd.DataFrame()

        return pd.concat(all_dfs, ignore_index=True)

    @staticmethod
    def _compute_fundamental_features(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or len(df) < 2:
            return df

        df = df.sort_values(["fiscal_year", "fiscal_period"]).reset_index(drop=True)

        period_order = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4, "FY": 5}
        df["_period_num"] = df["fiscal_period"].map(period_order)

        def _safe_div(a: pd.Series, b: pd.Series) -> pd.Series:
            return np.where(b > 0, a / b, np.nan)

        def _yoy_growth(current: pd.Series, periods_back: int) -> pd.Series:
            shifted = current.shift(periods_back)
            return np.where(shifted.abs() > 0, (current - shifted) / shifted.abs(), np.nan)

        r = df["revenue"].astype(float)
        gp = df["gross_profit"].astype(float)
        oi = df["operating_income"].astype(float)
        ni = df["net_income"].astype(float)
        ocf = df["operating_cash_flow"].astype(float)
        ca = df["current_assets"].astype(float)
        cl = df["current_liabilities"].astype(float)
        ta = df["total_assets"].astype(float)
        eq = df["equity"].astype(float)
        cash = df["cash"].astype(float)
        inv = df["inventory"].astype(float)
        ar = df["accounts_receivable"].astype(float)
        ltd = df["long_term_debt"].astype(float)
        std_ = df["short_term_debt"].astype(float)
        capex = df["capital_expenditure"].astype(float)
        ie = df["interest_expense"].astype(float).fillna(0)
        eps_d = df["eps_diluted"].astype(float)
        shares = df["shares_outstanding"].astype(float)
        divs = df["dividends"].astype(float).fillna(0)
        bbs = df["buybacks"].astype(float).fillna(0)
        total_debt = std_ + ltd

        prev_yoy_idx = np.full(len(df), -1, dtype=int)
        for i in range(len(df)):
            fy = df.iloc[i]["fiscal_year"]
            fp = df.iloc[i]["fiscal_period"]
            match = df[(df["fiscal_year"] == fy - 1) & (df["fiscal_period"] == fp)]
            if not match.empty:
                prev_yoy_idx[i] = match.index[0]

        has_prev = prev_yoy_idx >= 0

        def _yoy(col: pd.Series) -> np.ndarray:
            result = np.full(len(df), np.nan)
            vals = col.values.astype(float)
            for i in range(len(df)):
                if has_prev[i]:
                    pi = prev_yoy_idx[i]
                    if vals[pi] != 0 and not np.isnan(vals[pi]):
                        result[i] = (vals[i] - vals[pi]) / abs(vals[pi])
            return result

        # Growth rates
        df["revenue_growth_yoy"] = _yoy(r)
        df["gross_profit_growth_yoy"] = _yoy(gp)
        df["operating_income_growth_yoy"] = _yoy(oi)
        df["net_income_growth_yoy"] = _yoy(ni)
        df["eps_growth_yoy"] = _yoy(eps_d)
        df["operating_cash_flow_growth_yoy"] = _yoy(ocf)

        # Margins
        df["gross_margin"] = _safe_div(gp, r)
        df["operating_margin"] = _safe_div(oi, r)
        df["net_margin"] = _safe_div(ni, r)
        df["ocf_margin"] = _safe_div(ocf, r)

        # Liquidity
        df["current_ratio"] = _safe_div(ca, cl)
        df["quick_ratio"] = _safe_div(ca - inv, cl)
        df["cash_ratio"] = _safe_div(cash, cl)

        # Leverage
        df["cash_to_assets"] = _safe_div(cash, ta)
        df["debt_to_equity"] = _safe_div(total_debt, eq)
        df["debt_to_assets"] = _safe_div(total_debt, ta)
        df["debt_to_capital"] = _safe_div(total_debt, total_debt + eq)
        df["net_debt"] = total_debt - cash
        df["net_debt_to_equity"] = _safe_div(total_debt - cash, eq)
        df["debt_growth_yoy"] = _yoy(total_debt)
        df["short_term_debt_ratio"] = _safe_div(std_, total_debt)
        df["long_term_debt_ratio"] = _safe_div(ltd, total_debt)

        # Cash flow quality
        fcf = ocf - capex
        df["free_cash_flow"] = fcf
        df["fcf_margin"] = _safe_div(fcf, r)
        df["capex_to_revenue"] = _safe_div(capex, r)
        df["ocf_to_net_income"] = _safe_div(ocf, ni)

        # Efficiency
        df["receivables_to_revenue"] = _safe_div(ar, r)
        df["inventory_to_revenue"] = _safe_div(inv, r)
        df["receivables_growth_yoy"] = _yoy(ar)
        df["inventory_growth_yoy"] = _yoy(inv)
        df["working_capital"] = ca - cl
        df["working_capital_to_revenue"] = _safe_div(ca - cl, r)

        # Balance sheet growth
        df["asset_growth_yoy"] = _yoy(ta)
        df["equity_growth_yoy"] = _yoy(eq)
        df["cash_growth_yoy"] = _yoy(cash)
        df["capex_growth_yoy"] = _yoy(capex)
        df["free_cash_flow_growth_yoy"] = _yoy(pd.Series(fcf))

        # Shareholder
        df["share_count_change_yoy"] = _yoy(shares)
        df["buyback_change_yoy"] = _yoy(bbs)
        df["dividend_change_yoy"] = _yoy(divs)
        df["buyback_to_net_income"] = _safe_div(bbs, ni)
        df["dividend_to_net_income"] = _safe_div(divs, ni)

        # Coverage
        df["interest_coverage"] = _safe_div(oi, ie)

        df = df.drop(columns=["_period_num"])

        return df
