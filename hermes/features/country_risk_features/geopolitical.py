import numpy as np
import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import Literal
from hermes.sources.gdelt import GDELT
from hermes.sources.world_bank import World_bank

logger = logging.getLogger(__name__)

WGI_INDICATORS = ["CC.EST", "GE.EST", "PV.EST", "RQ.EST", "RL.EST", "VA.EST"]


class geopolitical_features:

    def __init__(self):
        self._gdelt = GDELT()
        self._wb = World_bank()


    def _query(self, country: str, themes: list[str], days: int) -> pd.DataFrame:
        now = datetime.utcnow()
        return self._gdelt.query_events(
            countries=[country],
            themes=themes,
            start_date=now - timedelta(days=days),
            end_date=now,
        )


    def conflict_event_count_30d(self, country_code: str) -> int:
        return len(self._query(country_code, ["CONFLICT"], 30))

    def conflict_event_count_90d(self, country_code: str) -> int:
        return len(self._query(country_code, ["CONFLICT"], 90))

    def conflict_trend(self, country_code: str) -> Literal["escalating", "stable", "de-escalating"]:
        now = datetime.utcnow()
        recent = self._gdelt.query_events(
            countries=[country_code], themes=["CONFLICT"],
            start_date=now - timedelta(days=30), end_date=now,
        )
        prior = self._gdelt.query_events(
            countries=[country_code], themes=["CONFLICT"],
            start_date=now - timedelta(days=60), end_date=now - timedelta(days=30),
        )
        ratio = len(recent) / max(len(prior), 1)
        if ratio > 1.2:
            return "escalating"
        if ratio < 0.8:
            return "de-escalating"
        return "stable"

    def goldstein_scale_avg_30d(self, country_code: str) -> float:
        df = self._query(country_code, ["CONFLICT"], 30)
        return float(df["severity"].mean()) if not df.empty else 0.0

    def goldstein_scale_trend(self, country_code: str) -> float:
        now = datetime.utcnow()
        recent = self._gdelt.query_events(
            countries=[country_code], themes=["CONFLICT"],
            start_date=now - timedelta(days=30), end_date=now,
        )
        prior = self._gdelt.query_events(
            countries=[country_code], themes=["CONFLICT"],
            start_date=now - timedelta(days=60), end_date=now - timedelta(days=30),
        )
        cur = float(recent["severity"].mean()) if not recent.empty else 0.0
        prv = float(prior["severity"].mean()) if not prior.empty else 0.0
        return cur - prv

    def battle_deaths_30d(self, country_code: str) -> int:
        now = datetime.utcnow()
        raw = self._gdelt.query_events(
            countries=[country_code], themes=["ASSAULT", "FIGHT"],
            start_date=now - timedelta(days=30), end_date=now,
            normalize=False,
        )
        if raw.empty:
            return 0
        return int(pd.to_numeric(raw.get("nummentions", pd.Series([0])), errors="coerce").sum())

    def battle_deaths_90d(self, country_code: str) -> int:
        now = datetime.utcnow()
        raw = self._gdelt.query_events(
            countries=[country_code], themes=["ASSAULT", "FIGHT"],
            start_date=now - timedelta(days=90), end_date=now,
            normalize=False,
        )
        if raw.empty:
            return 0
        return int(pd.to_numeric(raw.get("nummentions", pd.Series([0])), errors="coerce").sum())

    def protest_event_count_30d(self, country_code: str) -> int:
        return len(self._query(country_code, ["PROTEST"], 30))

    def protest_violence_level(self, country_code: str) -> float:
        df = self._query(country_code, ["PROTEST"], 30)
        if df.empty:
            return 0.0
        s = float(df["severity"].mean())
        return float(max(0.0, min(1.0, -s / 10.0)))


    def diplomatic_event_count_30d(self, country_code: str) -> int:
        return len(self._query(country_code, ["DIPLOMACY"], 30))

    def diplomatic_intensity_avg(self, country_code: str) -> float:
        df = self._query(country_code, ["DIPLOMACY"], 30)
        return float(df["severity"].mean()) if not df.empty else 0.0


    def rule_of_law_score(self, country_code: str) -> float:
        data = self._wb.fetch(country_code=country_code, indicator_code="RL.EST")
        if data.empty:
            return 0.0
        return float(data["value"].iloc[0])

    def regulatory_quality(self, country_code: str) -> float:
        data = self._wb.fetch(country_code=country_code, indicator_code="RQ.EST")
        if data.empty:
            return 0.0
        return float(data["value"].iloc[0])

    def governance_wgi_composite(self, country_code: str) -> float:
        values = []
        for ind in WGI_INDICATORS:
            data = self._wb.fetch(country_code=country_code, indicator_code=ind)
            if not data.empty:
                values.append(float(data["value"].iloc[0]))
        return float(np.mean(values)) if values else 0.0


    def sanctions_count_active(self, country_code: str) -> int:
        return 0

    def sanctions_new_30d(self, country_code: str) -> int:
        return 0

    def sanctions_sector_coverage(self, country_code: str) -> float:
        return 0.0

    def corruption_perception_index(self, country_code: str) -> int:
        return 0

    def democracy_index(self, country_code: str) -> float:
        return 0.0

    def regime_type(self, country_code: str) -> Literal["democracy", "hybrid", "autocracy"]:
        return "hybrid"

    def press_freedom_score(self, country_code: str) -> int:
        return 0