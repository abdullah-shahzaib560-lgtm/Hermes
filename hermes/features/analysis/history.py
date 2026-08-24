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

        log_ret = np.full(len(c), np.nan)
        log_ret[1:] = np.log(c[1:] / c[:-1])
        df["ret_1b"] = log_ret

        df["ret_open_to_close"] = np.where(o > 0, c / o - 1, np.nan)

        df["hl_range"] = np.where(c > 0, (hi - lo) / c, np.nan)
        df["body_range"] = np.where(c > 0, np.abs(c - o) / c, np.nan)

        cs = pd.Series(c)
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

        df["vol_20"] = pd.Series(log_ret).rolling(20).std(ddof=1)
        df["vol_60"] = pd.Series(log_ret).rolling(60).std(ddof=1)

        prev_c = np.roll(c, 1)
        prev_c[0] = np.nan
        tr = np.maximum(
            hi - lo,
            np.maximum(np.abs(hi - prev_c), np.abs(lo - prev_c)),
        )
        tr[0] = np.nan
        atr14 = pd.Series(tr).rolling(14).mean()
        df["atr_14_norm"] = np.where(c > 0, atr14 / c, np.nan)

        df["volume_sma_20"] = pd.Series(v).rolling(20).mean()
        df["volume_rel_20"] = np.where(
            df["volume_sma_20"] > 0, v / df["volume_sma_20"], np.nan
        )
        df["taker_buy_vol_ratio"] = np.where(v > 0, tbv / v, np.nan)

        df["rsi_14"] = _rsi(c, 14)

        macd_line, signal_line, histogram = _macd(c)
        df["macd"] = macd_line
        df["macd_signal"] = signal_line
        df["macd_hist"] = histogram

        bb_mid = sma20
        bb_std = pd.Series(c).rolling(20).std()
        df["bb_upper"] = bb_mid + 2 * bb_std
        df["bb_lower"] = bb_mid - 2 * bb_std
        df["bb_width"] = np.where(
            bb_mid > 0, (df["bb_upper"] - df["bb_lower"]) / bb_mid, np.nan
        )
        bb_range = df["bb_upper"] - df["bb_lower"]
        df["bb_pct"] = np.where(
            bb_range > 0, (c - df["bb_lower"]) / bb_range, np.nan
        )

        df["obv"] = _obv(c, v)

        rets = pd.Series(log_ret)
        df["returns_skew_20"] = rets.rolling(20).skew()
        df["returns_kurt_20"] = rets.rolling(20).kurt()

        peak = pd.Series(c).cummax()
        df["drawdown"] = np.where(peak > 0, (c - peak) / peak, np.nan)

        abs_ret = np.abs(log_ret)
        df["amihud_illiquidity"] = np.where(qv > 0, abs_ret / qv, np.nan)

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
            raise ValueError(
                f"Interval {interval!r} not supported for stocks. "
                f"Supported: {SUPPORTED_STOCK_FREQS}"
            )

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

        logger.info(
            f"Finnhub returned {len(df_finn)} rows for {symbol}, "
            f"falling back to yfinance"
        )

        df_yf = await self.yf.fetch_history(
            symbol=symbol,
            interval=interval,
            years=years,
        )

        if not df_yf.empty:
            df_yf["symbol"] = symbol
            df_yf["interval"] = interval

        return df_yf

    async def get_filing_history(
        self,
        symbol: str,
        quarters: int = 8,
    ) -> pd.DataFrame:
        raw = await self.sec.fetch(symbol=symbol)
        facts = raw["facts"]["us-gaap"]

        rows = []
        seen_periods = set()

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
                        rows.append({
                            "fiscal_year": fy,
                            "fiscal_period": fp,
                            "filing_date": entry.get("filed"),
                            "filing_type": entry.get("form"),
                        })
                    break
                if rows:
                    break
            if rows:
                break

        rows.sort(key=lambda r: (r["fiscal_year"], r["fiscal_period"]), reverse=True)
        rows = rows[:quarters]

        if not rows:
            return pd.DataFrame()

        result_rows = []
        for row in rows:
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
                            if (
                                entry.get("fy") == row["fiscal_year"]
                                and entry.get("fp") == row["fiscal_period"]
                            ):
                                period_facts[field] = entry.get("val")
                                break
                        if period_facts[field] is not None:
                            break
                    if period_facts[field] is not None:
                        break

            result_rows.append({
                "ticker": symbol,
                "filing_date": row["filing_date"],
                "fiscal_period": row["fiscal_period"],
                "fiscal_year": row["fiscal_year"],
                "filing_type": row["filing_type"],
                **period_facts,
            })

        return pd.DataFrame(result_rows)
