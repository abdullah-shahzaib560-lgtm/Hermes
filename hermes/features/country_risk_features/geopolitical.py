import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Literal
from urllib.parse import urlencode

import aiohttp
import numpy as np
import pandas as pd

from hermes.core.feature_decorator import feature
from hermes.core.helper import adjust_year_range
from hermes.sources.gdelt import GDELT
from hermes.sources.lib.gdlet_help import GDELT_DOC_API
from hermes.sources.opensanctions import OpenSanction
from hermes.sources.public_data import PUBLIC_DATASET
from hermes.sources.world_bank import World_bank

logger = logging.getLogger(__name__)

WGI_INDICATORS = ["CC.EST", "GE.EST", "PV.EST", "RQ.EST", "RL.EST", "VA.EST"]
GDELT_HISTORY_START = datetime(2000, 1, 1)
_GDELT_SEMAPHORE = asyncio.Semaphore(1)
_GDELT_LAST_CALL = 0.0
_GDELT_MIN_INTERVAL = 5.0
_gdelt_session_cache: dict[str, pd.DataFrame] = {}
_gdelt_available: bool | None = None


class geopolitical_features:
    def __init__(self, os_api: str):
        self._gdelt = GDELT()
        self._wb = World_bank()
        self._os = OpenSanction(api_key=os_api)
        self._p_data = PUBLIC_DATASET()

    async def _gdelt_rate_limit(self):
        global _GDELT_LAST_CALL
        now = time.monotonic()
        wait = _GDELT_MIN_INTERVAL - (now - _GDELT_LAST_CALL)
        if wait > 0:
            await asyncio.sleep(wait)
        _GDELT_LAST_CALL = time.monotonic()

    async def _gdelt_health_check(self) -> bool:
        global _gdelt_available
        if _gdelt_available is not None:
            return _gdelt_available
        async with _GDELT_SEMAPHORE:
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as client:
                    resp = await client.get(GDELT_DOC_API + "?" + urlencode({"query": "test", "mode": "artlist", "format": "json", "maxrecords": 1}))
                    text = await resp.text()
                    _gdelt_available = not text.lstrip().startswith("<") and resp.status == 200
                    if not _gdelt_available:
                        logger.warning("GDELT Doc API unavailable (status=%d)", resp.status)
                    return _gdelt_available
            except Exception:
                _gdelt_available = False
                logger.warning("GDELT Doc API unreachable")
                return False

    def _gdelt_cache_key(self, country: str, themes: list[str]) -> str:
        return f"{country}:{','.join(sorted(themes))}"

    async def _query(self, country: str, themes: list[str], days: int) -> pd.DataFrame:
        now = datetime.utcnow()
        cache_key = self._gdelt_cache_key(country, themes) + f":{days}d"
        if cache_key in _gdelt_session_cache:
            return _gdelt_session_cache[cache_key]
        if not await self._gdelt_health_check():
            return pd.DataFrame()
        async with _GDELT_SEMAPHORE:
            await self._gdelt_rate_limit()
            df = await self._gdelt.query_events(
                countries=[country],
                themes=themes,
                start_date=now - timedelta(days=days),
                end_date=now,
            )
        if not df.empty:
            _gdelt_session_cache[cache_key] = df
        return df

    async def _gdelt_ml_raw(self, country: str, themes: list[str]) -> pd.DataFrame:
        now = datetime.utcnow()
        cache_key = self._gdelt_cache_key(country, themes) + ":ml"
        if cache_key in _gdelt_session_cache:
            return _gdelt_session_cache[cache_key]
        if not await self._gdelt_health_check():
            return pd.DataFrame()
        async with _GDELT_SEMAPHORE:
            await self._gdelt_rate_limit()
            raw = await self._gdelt.query_events(
                countries=[country],
                themes=themes,
                start_date=GDELT_HISTORY_START,
                end_date=now,
                normalize=False,
            )
        if raw.empty:
            return pd.DataFrame()
        raw["date"] = pd.to_datetime(
            raw.get("seendate", raw.get("SQLDATE", pd.Series())).astype(str).str[:14],
            format="%Y%m%d%H%M%S",
            errors="coerce",
        )
        result = raw.dropna(subset=["date"])
        if not result.empty:
            _gdelt_session_cache[cache_key] = result
        return result

    @staticmethod
    def _monthly_rolling(daily: pd.Series, window: int, how: str = "sum") -> pd.Series:
        if how == "mean":
            rolled = daily.rolling(window, min_periods=1).mean()
        else:
            rolled = daily.rolling(window, min_periods=1).sum()
        return rolled.resample("ME").last()

    @feature(
        name="conflict_event_count_30d",
        group="geopolitical_features",
        deps=["GDELT:CONFLICT"],
        compute="conflict_event_count_30d from the GDELT",
    )
    async def conflict_event_count_30d(self, country_code: str, mode: Literal["F", "ML"] = "F") -> int | pd.Series:
        if mode == "ML":
            raw = await self._gdelt_ml_raw(country_code, ["CONFLICT"])
            if raw.empty:
                return pd.Series(dtype=float)
            daily = raw.set_index("date").resample("D").size()
            daily.index = pd.to_datetime(daily.index)
            daily["year"] = daily.index.year
            daily = adjust_year_range(daily.reset_index(), "year", 2000, 2025, fill_method="ffill")
            daily = daily.set_index("date")
            s = self._monthly_rolling(daily, 30, "sum")
            s.name = "conflict_event_count_30d"
            return s
        return len(await self._query(country_code, ["CONFLICT"], 30))

    @feature(
        name="conflict_event_count_90d",
        group="geopolitical_features",
        deps=["GDELT:CONFLICT"],
        compute="conflict_event_count_90d from the GDELT",
    )
    async def conflict_event_count_90d(self, country_code: str, mode: Literal["F", "ML"] = "F") -> int | pd.Series:
        if mode == "ML":
            raw = await self._gdelt_ml_raw(country_code, ["CONFLICT"])
            if raw.empty:
                return pd.Series(dtype=float)
            daily = raw.set_index("date").resample("D").size()
            daily.index = pd.to_datetime(daily.index)
            daily["year"] = daily.index.year
            daily = adjust_year_range(daily.reset_index(), "year", 2000, 2025, fill_method="ffill")
            daily = daily.set_index("date")
            s = self._monthly_rolling(daily, 90, "sum")
            s.name = "conflict_event_count_90d"
            return s
        return len(await self._query(country_code, ["CONFLICT"], 90))

    @feature(
        name="conflict_trend",
        group="geopolitical_features",
        deps=["GDELT:CONFLICT"],
        compute="conflict_trend from the GDELT",
    )
    async def conflict_trend(
        self, country_code: str, mode: Literal["F", "ML"] = "F"
    ) -> Literal["escalating", "stable", "de-escalating"] | pd.Series:
        if mode == "ML":
            raw = await self._gdelt_ml_raw(country_code, ["CONFLICT"])
            if raw.empty:
                return pd.Series(dtype=str)
            daily = raw.set_index("date").resample("D").size()
            daily.index = pd.to_datetime(daily.index)
            daily["year"] = daily.index.year
            daily = adjust_year_range(daily.reset_index(), "year", 2000, 2025, fill_method="ffill")
            daily = daily.set_index("date")
            rolling_30 = daily.rolling(30, min_periods=1).sum()
            monthly = rolling_30.resample("ME").last()
            prior = monthly.shift(1).fillna(1).replace(0, 1)
            ratio = monthly / prior

            def classify(r):
                if r > 1.2:
                    return "escalating"
                if r < 0.8:
                    return "de-escalating"
                return "stable"

            s = ratio.apply(classify)
            s.name = "conflict_trend"
            return s
        recent = await self._query(country_code, ["CONFLICT"], 30)
        prior_all = await self._query(country_code, ["CONFLICT"], 60)
        cutoff = datetime.utcnow() - timedelta(days=30)
        prior = prior_all[prior_all.index < cutoff] if not prior_all.empty else prior_all
        ratio = len(recent) / max(len(prior), 1)
        if ratio > 1.2:
            return "escalating"
        if ratio < 0.8:
            return "de-escalating"
        return "stable"

    @feature(
        name="goldstein_scale_avg_30d",
        group="geopolitical_features",
        deps=["GDELT:CONFLICT"],
        compute="goldstein_scale_avg_30d from the GDELT",
    )
    async def goldstein_scale_avg_30d(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pd.Series:
        if mode == "ML":
            raw = await self._gdelt_ml_raw(country_code, ["CONFLICT"])
            if raw.empty:
                return pd.Series(dtype=float)
            daily = raw.set_index("date").resample("D")["severity"].mean().fillna(0)
            daily.index = pd.to_datetime(daily.index)
            daily["year"] = daily.index.year
            daily = adjust_year_range(daily.reset_index(), "year", 2000, 2025, fill_method="ffill")
            daily = daily.set_index("date")
            s = self._monthly_rolling(daily, 30, "mean")
            s.name = "goldstein_scale_avg_30d"
            return s
        df = await self._query(country_code, ["CONFLICT"], 30)
        return float(df["severity"].mean()) if not df.empty else 0.0

    @feature(
        name="goldstein_scale_trend",
        group="geopolitical_features",
        deps=["GDELT:CONFLICT"],
        compute="goldstein_scale_trend from the GDELT",
    )
    async def goldstein_scale_trend(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pd.Series:
        if mode == "ML":
            raw = await self._gdelt_ml_raw(country_code, ["CONFLICT"])
            if raw.empty:
                return pd.Series(dtype=float)
            daily = raw.set_index("date").resample("D")["severity"].mean().fillna(0)
            daily.index = pd.to_datetime(daily.index)
            daily["year"] = daily.index.year
            daily = adjust_year_range(daily.reset_index(), "year", 2000, 2025, fill_method="ffill")
            daily = daily.set_index("date")
            rolling_30 = daily.rolling(30, min_periods=1).mean()
            monthly = rolling_30.resample("ME").last()
            s = monthly - monthly.shift(1).fillna(0)
            s.name = "goldstein_scale_trend"
            return s
        recent = await self._query(country_code, ["CONFLICT"], 30)
        prior_all = await self._query(country_code, ["CONFLICT"], 60)
        cutoff = datetime.utcnow() - timedelta(days=30)
        prior = prior_all[prior_all.index < cutoff] if not prior_all.empty else prior_all
        cur = float(recent["severity"].mean()) if not recent.empty else 0.0
        prv = float(prior["severity"].mean()) if not prior.empty else 0.0
        return cur - prv

    @feature(
        name="battle_deaths_30d",
        group="geopolitical_features",
        deps=["GDELT:ASSAULT:FIGHT"],
        compute="battle_deaths_30d from the GDELT",
    )
    async def battle_deaths_30d(self, country_code: str, mode: Literal["F", "ML"] = "F") -> int | pd.Series:
        if mode == "ML":
            raw = await self._gdelt_ml_raw(country_code, ["ASSAULT", "FIGHT"])
            if raw.empty:
                return pd.Series(dtype=float)
            raw["mentions"] = pd.to_numeric(raw.get("nummentions", pd.Series([0])), errors="coerce").fillna(0)
            daily = raw.set_index("date").resample("D")["mentions"].sum()
            daily.index = pd.to_datetime(daily.index)
            daily["year"] = daily.index.year
            daily = adjust_year_range(daily.reset_index(), "year", 2000, 2025, fill_method="ffill")
            daily = daily.set_index("date")
            s = self._monthly_rolling(daily, 30, "sum")
            s.name = "battle_deaths_30d"
            return s
        raw = await self._query(country_code, ["ASSAULT", "FIGHT"], 30)
        if raw.empty:
            return 0
        return int(pd.to_numeric(raw.get("nummentions", pd.Series([0])), errors="coerce").sum())

    @feature(
        name="battle_deaths_90d",
        group="geopolitical_features",
        deps=["GDELT:ASSAULT:FIGHT"],
        compute="battle_deaths_90d from the GDELT",
    )
    async def battle_deaths_90d(self, country_code: str, mode: Literal["F", "ML"] = "F") -> int | pd.Series:
        if mode == "ML":
            raw = await self._gdelt_ml_raw(country_code, ["ASSAULT", "FIGHT"])
            if raw.empty:
                return pd.Series(dtype=float)
            raw["mentions"] = pd.to_numeric(raw.get("nummentions", pd.Series([0])), errors="coerce").fillna(0)
            daily = raw.set_index("date").resample("D")["mentions"].sum()
            daily.index = pd.to_datetime(daily.index)
            daily["year"] = daily.index.year
            daily = adjust_year_range(daily.reset_index(), "year", 2000, 2025, fill_method="ffill")
            daily = daily.set_index("date")
            s = self._monthly_rolling(daily, 90, "sum")
            s.name = "battle_deaths_90d"
            return s
        raw = await self._query(country_code, ["ASSAULT", "FIGHT"], 90)
        if raw.empty:
            return 0
        return int(pd.to_numeric(raw.get("nummentions", pd.Series([0])), errors="coerce").sum())

    @feature(
        name="protest_event_count_30d",
        group="geopolitical_features",
        deps=["GDELT:PROTEST"],
        compute="protest_event_count_30d from the GDELT",
    )
    async def protest_event_count_30d(self, country_code: str, mode: Literal["F", "ML"] = "F") -> int | pd.Series:
        if mode == "ML":
            raw = await self._gdelt_ml_raw(country_code, ["PROTEST"])
            if raw.empty:
                return pd.Series(dtype=float)
            daily = raw.set_index("date").resample("D").size()
            daily.index = pd.to_datetime(daily.index)
            daily["year"] = daily.index.year
            daily = adjust_year_range(daily.reset_index(), "year", 2000, 2025, fill_method="ffill")
            daily = daily.set_index("date")
            s = self._monthly_rolling(daily, 30, "sum")
            s.name = "protest_event_count_30d"
            return s
        return len(await self._query(country_code, ["PROTEST"], 30))

    @feature(
        name="protest_violence_level",
        group="geopolitical_features",
        deps=["GDELT:PROTEST"],
        compute="protest_violence_level from the GDELT",
    )
    async def protest_violence_level(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pd.Series:
        if mode == "ML":
            raw = await self._gdelt_ml_raw(country_code, ["PROTEST"])
            if raw.empty:
                return pd.Series(dtype=float)
            daily = raw.set_index("date").resample("D")["severity"].mean().fillna(0)
            daily.index = pd.to_datetime(daily.index)
            daily["year"] = daily.index.year
            daily = adjust_year_range(daily.reset_index(), "year", 2000, 2025, fill_method="ffill")
            daily = daily.set_index("date")
            rolling = daily.rolling(30, min_periods=1).mean()
            monthly = rolling.resample("ME").last()
            s = monthly.apply(lambda x: max(0.0, min(1.0, -x / 10.0)))
            s.name = "protest_violence_level"
            return s
        df = await self._query(country_code, ["PROTEST"], 30)
        if df.empty:
            return 0.0
        s = float(df["severity"].mean())
        return float(max(0.0, min(1.0, -s / 10.0)))

    @feature(
        name="diplomatic_event_count_30d",
        group="geopolitical_features",
        deps=["GDLET:DIPLOMACY"],
        compute="diplomatic_event_count_30d from the GDELT",
    )
    async def diplomatic_event_count_30d(self, country_code: str, mode: Literal["F", "ML"] = "F") -> int | pd.Series:
        if mode == "ML":
            raw = await self._gdelt_ml_raw(country_code, ["DIPLOMACY"])
            if raw.empty:
                return pd.Series(dtype=float)
            daily = raw.set_index("date").resample("D").size()
            daily.index = pd.to_datetime(daily.index)
            daily["year"] = daily.index.year
            daily = adjust_year_range(daily.reset_index(), "year", 2000, 2025, fill_method="ffill")
            daily = daily.set_index("date")
            s = self._monthly_rolling(daily, 30, "sum")
            s.name = "diplomatic_event_count_30d"
            return s
        return len(await self._query(country_code, ["DIPLOMACY"], 30))

    @feature(
        name="diplomatic_intensity_avg",
        group="geopolitical_features",
        deps=["GDLET:DIPLOMACY"],
        compute="diplomatic_intensity_avg from the GDELT",
    )
    async def diplomatic_intensity_avg(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pd.Series:
        if mode == "ML":
            raw = await self._gdelt_ml_raw(country_code, ["DIPLOMACY"])
            if raw.empty:
                return pd.Series(dtype=float)
            daily = raw.set_index("date").resample("D")["severity"].mean().fillna(0)
            daily.index = pd.to_datetime(daily.index)
            daily["year"] = daily.index.year
            daily = adjust_year_range(daily.reset_index(), "year", 2000, 2025, fill_method="ffill")
            daily = daily.set_index("date")
            s = self._monthly_rolling(daily, 30, "mean")
            s.name = "diplomatic_intensity_avg"
            return s
        df = await self._query(country_code, ["DIPLOMACY"], 30)
        return float(df["severity"].mean()) if not df.empty else 0.0

    async def _wb_annual_to_monthly(self, data: pd.DataFrame, name: str) -> pd.Series:
        data["year"] = pd.to_datetime(data["date"]).dt.year
        data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
        s = data.set_index("date")["value"]
        s.name = name
        return s

    @feature(
        name="rule_of_law_score",
        group="geopolitical_features",
        deps=["world_bank:RL.EST"],
        compute="rule_of_law_score from the World Bank data",
    )
    async def rule_of_law_score(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pd.Series:
        data = await self._wb.fetch(country_code=country_code, indicator_code="RL.EST")
        if data.empty:
            return 0.0 if mode == "F" else pd.Series(dtype=float)
        if mode == "ML":
            return await self._wb_annual_to_monthly(data, "rule_of_law_score")
        return float(data["value"].iloc[0])

    @feature(
        name="regulatory_quality",
        group="geopolitical_features",
        deps=["world_bank:RQ.EST"],
        compute="regulatory_quality from the World Bank data",
    )
    async def regulatory_quality(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pd.Series:
        data = await self._wb.fetch(country_code=country_code, indicator_code="RQ.EST")
        if data.empty:
            return 0.0 if mode == "F" else pd.Series(dtype=float)
        if mode == "ML":
            return await self._wb_annual_to_monthly(data, "regulatory_quality")
        return float(data["value"].iloc[0])

    @feature(
        name="governance_wgi_composite",
        group="geopolitical_features",
        deps=[f"world_bank:{WGI_INDICATORS}"],
        compute="governance_wgi_composite from the World Bank data",
    )
    async def governance_wgi_composite(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pd.Series:
        if mode == "F":
            values = []
            for ind in WGI_INDICATORS:
                data = await self._wb.fetch(country_code=country_code, indicator_code=ind)
                if not data.empty:
                    values.append(float(data["value"].iloc[0]))
            return float(np.mean(values)) if values else 0.0

        all_series = []
        for ind in WGI_INDICATORS:
            data = await self._wb.fetch(country_code=country_code, indicator_code=ind)
            if not data.empty:
                all_series.append(await self._wb_annual_to_monthly(data, ind))
        if not all_series:
            return pd.Series(dtype=float)
        composite = pd.concat(all_series, axis=1).mean(axis=1)
        composite.name = "governance_wgi_composite"
        return composite

    @feature(
        name="sanctions_count_active",
        group="geopolitical_features",
        deps=["opensanction:us_ofac_sdn"],
        compute="sanctions_count_active from the OpenSanction",
    )
    async def sanctions_count_active(self, country_code: str, mode: str = "F") -> int:
        data = await self._os.fetch(country=country_code, dataset="us_ofac_sdn", limit=1000)
        active_count = 0
        for result in data.get("results", []):
            status = result.get("properties", {}).get("status", [])
            if "Active" in status:
                active_count += 1

        return active_count

    @feature(
        name="sanctions_new_30d",
        group="geopolitical_features",
        deps=["opensanction:us_ofac_sdn"],
        compute="sanctions_new_30d from the OpenSanction",
    )
    async def sanctions_new_30d(self, country_code: str, mode: str = "F") -> int:
        from datetime import datetime, timedelta

        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        data = await self._os.fetch(country=country_code, dataset="us_ofac_sdn", limit=1000)
        new_count = 0
        for result in data.get("results", []):
            created = result.get("properties", {}).get("createdAt", [])
            if created and created[0] >= thirty_days_ago:
                new_count += 1
        return new_count

    @feature(
        name="sanctions_sector_coverage",
        group="geopolitical_features",
        deps=["opensanction:us_ofac_sdn"],
        compute="sanctions_sector_coverage from the OpenSanction",
    )
    async def sanctions_sector_coverage(self, country_code: str, mode: str = "F") -> float | pd.Series:
        data = await self._os.fetch(country=country_code, dataset="us_ofac_sdn", limit=1000)
        sectors = set()
        for result in data.get("results", []):
            topics = result.get("properties", {}).get("topics", [])
            sectors.update(topics)

        return len(sectors) / 10 * 100

    @feature(
        name="corruption_perception_index",
        group="geopolitical_features",
        deps=["world_bank:SL.TLF.CACT.ZS"],
        compute="corruption_perception_index from the orld HDX CPI downloaded dataset",
    )
    async def corruption_perception_index(self, country_code: str, mode: str = "F") -> int:
        data = await self._p_data.fetch_cpi(country=country_code)

        if data.empty:
            return 0 if mode == "F" else pd.Series(dtype="float64")
        data = data.set_index("year")
        data["score"] = pd.to_numeric(data["score"], errors="coerce")
        data.sort_index(ascending=False, inplace=True)

        if mode == "F":
            return float(data["score"].iloc[0])

        if mode == "ML":
            data = data.reset_index()
            data["year"] = data["year"].dt.year
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            data = data.set_index("year")
            return data["score"]

    @feature(
        name="democracy_index",
        group="geopolitical_features",
        deps=[],
        compute="democracy_index",
    )
    async def democracy_index(self, country_code: str, mode: str = "F") -> float:
        return 0.0

    @feature(
        name="regime_type",
        group="geopolitical_features",
        deps=[],
        compute="regime_type",
    )
    async def regime_type(self, country_code: str, mode: str = "F") -> Literal["democracy", "hybrid", "autocracy"]:
        return "hybrid"

    @feature(
        name="press_freedom_score",
        group="geopolitical_features",
        deps=[],
        compute="press_freedom_score",
    )
    async def press_freedom_score(self, country_code: str, mode: str = "F") -> int:
        return 0

from collections.abc import Callable
from typing import Any


async def _await_group(fns: dict[str, Callable[..., Any]]) -> dict[str, Any]:
    async def _safe_call(fn):
        try:
            return await fn()
        except Exception as e:
            logger.warning(f"Feature failed: {e}")
            return None

    values = await asyncio.gather(*(_safe_call(f) for f in fns.values()))
    return dict(zip(fns.keys(), values))

if __name__ == "__main__":
    import asyncio

    async def main():
        geo = geopolitical_features(os_api='af5a744cd01ccf9a6b9b90c599bd5430')

        geopolitical = await _await_group(
            {
                "conflict_event_count_30d": lambda: geo.conflict_event_count_30d(
                    country_code="USA", mode="F"
                ),  # int
                "conflict_event_count_90d": lambda: geo.conflict_event_count_90d(
                    country_code="USA", mode="F"
                ),  # int
                "conflict_trend": lambda: geo.conflict_trend(
                    country_code="USA", mode="F"
                ),  # string: escalating/stable/de-escalating
                "goldstein_scale_avg_30d": lambda: geo.goldstein_scale_avg_30d(
                    country_code="USA", mode="F"
                ),  # float, -10 to +10
                "goldstein_scale_trend": lambda: geo.goldstein_scale_trend(
                    country_code="USA", mode="F"
                ),  # float, change vs prev period
                "battle_deaths_30d": lambda: geo.battle_deaths_30d(country_code="USA", mode="F"),  # int
                "battle_deaths_90d": lambda: geo.battle_deaths_90d(country_code="USA", mode="F"),  # int
                "protest_event_count_30d": lambda: geo.protest_event_count_30d(
                    country_code="USA", mode="F"
                ),  # int
                "protest_violence_level": lambda: geo.protest_violence_level(
                    country_code="USA", mode="F"
                ),  # float, 0-1
                "diplomatic_event_count_30d": lambda: geo.diplomatic_event_count_30d(
                    country_code="USA", mode="F"
                ),  # int
                "diplomatic_intensity_avg": lambda: geo.diplomatic_intensity_avg(
                    country_code="USA", mode="F"
                ),  # float, 0-10 scale
                "sanctions_count_active": lambda: geo.sanctions_count_active(country_code="USA"),  # int
                "sanctions_new_30d": lambda: geo.sanctions_new_30d(country_code="USA"),  # int
                "sanctions_sector_coverage": lambda: geo.sanctions_sector_coverage(
                    country_code="USA"
                ),  # float, 0-1
                "governance_wgi_composite": lambda: geo.governance_wgi_composite(
                    country_code="USA", mode="F"
                ),  # float, -2.5 to +2.5
                "corruption_perception_index": lambda: geo.corruption_perception_index(
                    country_code="USA", mode="F"
                ),  # int, 0-100
                "rule_of_law_score": lambda: geo.rule_of_law_score(
                    country_code="USA", mode="F"
                ),  # float, -2.5 to +2.5
                "regulatory_quality": lambda: geo.regulatory_quality(
                    country_code="USA", mode="F"
                ),  # float, -2.5 to +2.5
                "democracy_index": lambda: geo.democracy_index(country_code="USA", mode="F"),  # float, 0-1
                "regime_type": lambda: geo.regime_type(
                    country_code="USA", mode="F"
                ),  # string: democracy/hybrid/autocracy
                "press_freedom_score": lambda: geo.press_freedom_score(
                    country_code="USA", mode="F"
                ),  # int, 0-100
            }

        )

        print(geo)
    asyncio.run(main())
