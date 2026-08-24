import logging

import numpy as np
import pandas as pd

from hermes.sources.binance import Binance
from hermes.sources.finnhub import FINNHUB
from hermes.sources.lib.sec_tag import SEC_TAG_MAP
from hermes.sources.sec_edgar import SECEDGAR
from hermes.sources.yf import Yfinance

logger = logging.getLogger(__name__)


class TAHistory:
    def __init__(self):
        self.binance = Binance()

    async def get_history(
        self,
        symbol: str,
        interval: str = "1d",
        market: str = "future",
        years: int = 2,
        max_concurrent: int = 10,
    ) -> pd.DataFrame:
        df = await self.binance.fetch_history(
            symbol=symbol,
            interval=interval,
            market=market,
            years=years,
            max_concurrent=max_concurrent,
        )

        if df.empty:
            return df

        df["symbol"] = symbol
        df["interval"] = interval

        df = self._compute_features(df)

        return df

    @staticmethod
    def _compute_features(df: pd.DataFrame) -> pd.DataFrame:
        c = df["close"].values.astype(float)
        o = df["open"].values.astype(float)
        hi = df["high"].values.astype(float)
        lo = df["low"].values.astype(float)
        v = df["volume"].values.astype(float)
        qv = df["quote_volume"].values.astype(float)
        tbv = df["taker_buy_volume"].values.astype(float)
        tc = df["trades_count"].values.astype(float)

        cs = pd.Series(c)
        hs = pd.Series(hi)
        ls = pd.Series(lo)
        vs = pd.Series(v)

        log_ret = np.full(len(c), np.nan)
        log_ret[1:] = np.log(c[1:] / c[:-1])
        log_ret_s = pd.Series(log_ret)

        df["ret_1b"] = log_ret
        df["ret_open_to_close"] = np.where(o > 0, c / o - 1, np.nan)
        df["ret_3b"] = log_ret_s.shift(2).values
        df["ret_5b"] = log_ret_s.shift(4).values
        df["ret_10b"] = log_ret_s.shift(9).values
        df["ret_20b"] = log_ret_s.shift(19).values
        df["ret_60b"] = log_ret_s.shift(59).values

        df["hl_range"] = np.where(c > 0, (hi - lo) / c, np.nan)
        df["body_range"] = np.where(c > 0, np.abs(c - o) / c, np.nan)

        sma20 = cs.rolling(20).mean()
        sma50 = cs.rolling(50).mean()
        sma200 = cs.rolling(200).mean()

        df["dist_sma_20"] = np.where(sma20 > 0, (c - sma20) / sma20, np.nan)
        df["dist_sma_50"] = np.where(sma50 > 0, (c - sma50) / sma50, np.nan)
        df["dist_sma_200"] = np.where(sma200 > 0, (c - sma200) / sma200, np.nan)

        ema9 = cs.ewm(span=9, adjust=False).mean()
        ema21 = cs.ewm(span=21, adjust=False).mean()
        ema50 = cs.ewm(span=50, adjust=False).mean()

        df["ema_diff_9_21"] = np.where(ema21 > 0, (ema9 - ema21) / ema21, np.nan)
        df["ema_diff_21_50"] = np.where(ema50 > 0, (ema21 - ema50) / ema50, np.nan)

        vol_20 = log_ret_s.rolling(20).std(ddof=1)
        vol_60 = log_ret_s.rolling(60).std(ddof=1)
        df["vol_20"] = vol_20.values
        df["vol_60"] = vol_60.values

        prev_c = np.roll(c, 1)
        prev_c[0] = np.nan
        tr = np.maximum(
            hi - lo,
            np.maximum(np.abs(hi - prev_c), np.abs(lo - prev_c)),
        )
        tr[0] = np.nan
        tr_s = pd.Series(tr)
        atr14 = tr_s.rolling(14).mean()
        df["atr_14_norm"] = np.where(c > 0, atr14.values / c, np.nan)

        volume_sma_20 = vs.rolling(20).mean()
        volume_sma_60 = vs.rolling(60).mean()
        df["volume_sma_20"] = volume_sma_20.values
        df["volume_rel_20"] = np.where(volume_sma_20 > 0, v / volume_sma_20, np.nan)
        df["taker_buy_vol_ratio"] = np.where(v > 0, tbv / v, np.nan)

        rsi_14 = pd.Series(_rsi(c, 14))
        df["rsi_14"] = rsi_14.values

        macd_line, signal_line, histogram = _macd(c)
        df["macd"] = macd_line
        df["macd_signal"] = signal_line
        df["macd_hist"] = histogram
        macd_hist_s = pd.Series(histogram)

        bb_mid = sma20
        bb_std = cs.rolling(20).std()
        bb_upper = bb_mid + 2 * bb_std
        bb_lower = bb_mid - 2 * bb_std
        df["bb_upper"] = bb_upper.values
        df["bb_lower"] = bb_lower.values
        bb_width = np.where(bb_mid > 0, (bb_upper - bb_lower) / bb_mid, np.nan)
        df["bb_width"] = bb_width
        bb_range = bb_upper - bb_lower
        df["bb_pct"] = np.where(bb_range > 0, (c - bb_lower) / bb_range, np.nan)

        df["obv"] = _obv(c, v)

        df["returns_skew_20"] = log_ret_s.rolling(20).skew().values
        df["returns_kurt_20"] = log_ret_s.rolling(20).kurt().values

        peak = cs.cummax()
        df["drawdown"] = np.where(peak > 0, (c - peak) / peak, np.nan)

        abs_ret = np.abs(log_ret)
        df["amihud_illiquidity"] = np.where(qv > 0, abs_ret / qv, np.nan)

        # --- NEW FEATURES ---

        # Return statistics
        return_mean_20 = log_ret_s.rolling(20).mean()
        return_std_20 = log_ret_s.rolling(20).std(ddof=1)
        df["return_mean_20"] = return_mean_20.values
        df["return_std_20"] = return_std_20.values
        df["return_zscore_20"] = np.where(return_std_20 > 0, (log_ret_s - return_mean_20) / return_std_20, np.nan)

        return_mean_60 = log_ret_s.rolling(60).mean()
        return_std_60 = log_ret_s.rolling(60).std(ddof=1)
        df["return_zscore_60"] = np.where(return_std_60 > 0, (log_ret_s - return_mean_60) / return_std_60, np.nan)

        # Candle wick patterns
        real_body_high = np.maximum(o, c)
        real_body_low = np.minimum(o, c)
        upper_wick = hi - real_body_high
        lower_wick = real_body_low - lo
        candle_range = hi - lo
        df["upper_wick"] = upper_wick
        df["lower_wick"] = lower_wick
        df["upper_wick_ratio"] = np.where(candle_range > 0, upper_wick / candle_range, np.nan)
        df["lower_wick_ratio"] = np.where(candle_range > 0, lower_wick / candle_range, np.nan)
        df["body_to_range"] = np.where(candle_range > 0, np.abs(c - o) / candle_range, np.nan)

        # Price z-scores
        std_20 = cs.rolling(20).std()
        std_50 = cs.rolling(50).std()
        std_200 = cs.rolling(200).std()
        df["price_zscore_20"] = np.where(std_20 > 0, (cs - sma20) / std_20, np.nan)
        df["price_zscore_50"] = np.where(std_50 > 0, (cs - sma50) / std_50, np.nan)
        df["price_zscore_200"] = np.where(std_200 > 0, (cs - sma200) / std_200, np.nan)

        # Distance from high/low
        rolling_high_20 = hs.rolling(20).max()
        rolling_low_20 = ls.rolling(20).min()
        df["high_distance_20"] = np.where(rolling_high_20 > 0, (rolling_high_20 - hs) / rolling_high_20, np.nan)
        df["low_distance_20"] = np.where(rolling_low_20 > 0, (ls - rolling_low_20) / rolling_low_20, np.nan)

        # Volume features
        volume_std_20 = vs.rolling(20).std()
        volume_std_60 = vs.rolling(60).std()
        df["volume_zscore_20"] = np.where(volume_std_20 > 0, (vs - volume_sma_20) / volume_std_20, np.nan)
        df["volume_zscore_60"] = np.where(volume_std_60 > 0, (vs - volume_sma_60) / volume_std_60, np.nan)
        df["volume_change_1"] = np.where(vs.shift(1) > 0, v / vs.shift(1).values - 1, np.nan)
        df["volume_change_5"] = np.where(vs.shift(5) > 0, v / vs.shift(5).values - 1, np.nan)
        df["vol_ratio_20_60"] = np.where(volume_sma_60 > 0, volume_sma_20 / volume_sma_60, np.nan)

        # Volume trend (linear regression slope over 20 bars, normalized)
        df["volume_trend_20"] = _rolling_slope(vs, 20)

        # Volatility changes
        vol_20_prev1 = vol_20.shift(1)
        vol_20_prev5 = vol_20.shift(5)
        df["vol_change_1"] = np.where(vol_20_prev1 > 0, vol_20 / vol_20_prev1 - 1, np.nan)
        df["vol_change_5"] = np.where(vol_20_prev5 > 0, vol_20 / vol_20_prev5 - 1, np.nan)
        df["atr_ratio"] = np.where(atr14.shift(14) > 0, atr14 / atr14.shift(14) - 1, np.nan)

        # Momentum changes
        df["rsi_change_1"] = (rsi_14 - rsi_14.shift(1)).values
        df["rsi_change_5"] = (rsi_14 - rsi_14.shift(5)).values
        df["macd_hist_change_1"] = (macd_hist_s - macd_hist_s.shift(1)).values
        df["macd_hist_change_5"] = (macd_hist_s - macd_hist_s.shift(5)).values
        macd_hist_mean_20 = macd_hist_s.rolling(20).mean()
        macd_hist_std_20 = macd_hist_s.rolling(20).std()
        df["macd_hist_zscore_20"] = np.where(
            macd_hist_std_20 > 0,
            (macd_hist_s - macd_hist_mean_20) / macd_hist_std_20,
            np.nan,
        )

        # Bollinger changes
        bb_width_s = pd.Series(bb_width)
        df["bb_width_change"] = (bb_width_s - bb_width_s.shift(1)).values
        bb_width_mean_20 = bb_width_s.rolling(20).mean()
        bb_width_std_20 = bb_width_s.rolling(20).std()
        df["bb_width_zscore_20"] = np.where(
            bb_width_std_20 > 0,
            (bb_width_s - bb_width_mean_20) / bb_width_std_20,
            np.nan,
        )
        bb_pct_s = pd.Series(df["bb_pct"].values)
        df["bb_pct_change"] = (bb_pct_s - bb_pct_s.shift(1)).values

        # Buy pressure change
        buy_pressure = pd.Series(df["taker_buy_vol_ratio"].values)
        df["buy_pressure_change"] = (buy_pressure - buy_pressure.shift(1)).values

        # Trade features
        tc_s = pd.Series(tc)
        df["trade_count_change"] = np.where(tc_s.shift(1) > 0, tc / tc_s.shift(1).values - 1, np.nan)
        tc_mean_20 = tc_s.rolling(20).mean()
        tc_std_20 = tc_s.rolling(20).std()
        df["trade_count_zscore_20"] = np.where(tc_std_20 > 0, (tc_s - tc_mean_20) / tc_std_20, np.nan)
        avg_trade = np.where(tc > 0, v / tc, np.nan)
        df["avg_trade_size"] = avg_trade
        avg_trade_s = pd.Series(avg_trade)
        avg_trade_mean_20 = avg_trade_s.rolling(20).mean()
        avg_trade_std_20 = avg_trade_s.rolling(20).std()
        df["avg_trade_size_zscore_20"] = np.where(
            avg_trade_std_20 > 0,
            (avg_trade_s - avg_trade_mean_20) / avg_trade_std_20,
            np.nan,
        )

        # Risk features
        drawdown_s = pd.Series(df["drawdown"].values)
        df["drawdown_change"] = (drawdown_s - drawdown_s.shift(1)).values

        peak_arr = peak.values
        dd_duration = np.full(len(c), np.nan)
        dd_recovery = np.full(len(c), np.nan)
        trough_since_peak = c[0]
        for i in range(1, len(c)):
            if peak_arr[i] == peak_arr[i - 1]:
                dd_duration[i] = dd_duration[i - 1] + 1 if not np.isnan(dd_duration[i - 1]) else 1
                trough_since_peak = min(trough_since_peak, c[i])
            else:
                dd_duration[i] = 0
                trough_since_peak = c[i]
            peak_val = peak_arr[i]
            if peak_val > trough_since_peak:
                dd_recovery[i] = (c[i] - trough_since_peak) / (peak_val - trough_since_peak)
            else:
                dd_recovery[i] = 1.0
        df["drawdown_duration"] = dd_duration
        df["recovery_from_drawdown"] = dd_recovery

        return df


def _rsi(closes: np.ndarray, period: int = 14) -> np.ndarray:
    deltas = np.diff(closes, prepend=closes[0])
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)

    avg_gain = np.full(len(closes), np.nan)
    avg_loss = np.full(len(closes), np.nan)

    if len(closes) < period + 1:
        return avg_gain

    avg_gain[period] = np.mean(gains[1 : period + 1])
    avg_loss[period] = np.mean(losses[1 : period + 1])

    for i in range(period + 1, len(closes)):
        avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gains[i]) / period
        avg_loss[i] = (avg_loss[i - 1] * (period - 1) + losses[i]) / period

    rs = np.where(avg_loss > 0, avg_gain / avg_loss, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def _macd(
    closes: np.ndarray,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    cs = pd.Series(closes)
    ema_fast = cs.ewm(span=fast, adjust=False).mean()
    ema_slow = cs.ewm(span=slow, adjust=False).mean()
    macd_line = (ema_fast - ema_slow).values
    signal_line = pd.Series(macd_line).ewm(span=signal, adjust=False).mean().values
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def _obv(closes: np.ndarray, volumes: np.ndarray) -> np.ndarray:
    direction = np.sign(np.diff(closes, prepend=closes[0]))
    obv = np.cumsum(direction * volumes)
    return obv


def _rolling_slope(series: pd.Series, window: int) -> np.ndarray:
    x = np.arange(window, dtype=float)
    x_mean = x.mean()
    x_var = ((x - x_mean) ** 2).sum()
    result = np.full(len(series), np.nan)
    vals = series.values
    for i in range(window - 1, len(vals)):
        y = vals[i - window + 1 : i + 1]
        if np.any(np.isnan(y)):
            continue
        y_mean = y.mean()
        if x_var == 0:
            result[i] = 0.0
        else:
            result[i] = ((x - x_mean) * (y - y_mean)).sum() / x_var
    return result


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


class FAHistory:
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
                df_sym = FAHistory._compute_fundamental_features(df_sym)
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
