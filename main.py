import asyncio
import cProfile
import os
import pstats
import time
import tracemalloc
from io import StringIO

from dotenv import load_dotenv

from hermes import Hermes
from hermes.core.feature_decorator import lineagegraph

load_dotenv()

COUNTRY = "USA"
COUNTRIES_ML = ["USA", "GBR", "DEU"]

os_api = os.getenv("OPEN_SANCTIONS_API", "")

GDELT_FEATURES = {
    "conflict_event_count_30d", "conflict_event_count_90d", "conflict_trend",
    "goldstein_scale_avg_30d", "goldstein_scale_trend",
    "battle_deaths_30d", "battle_deaths_90d",
    "protest_event_count_30d", "protest_violence_level",
    "diplomatic_event_count_30d", "diplomatic_intensity_avg",
}


def section(title: str):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


async def profile_async(label: str, fn, *args, **kwargs):
    start = time.perf_counter()
    try:
        result = await fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {label}: {elapsed:.3f}s")
        return result
    except Exception as e:
        elapsed = time.perf_counter() - start
        print(f"  {label}: SKIPPED ({type(e).__name__}) [{elapsed:.3f}s]")
        return None


async def main():
    tracemalloc.start()
    snap_before = tracemalloc.take_snapshot()

    hr = Hermes(opensanction_api=os_api, new_data_api="")

    section("Lineage Graph")
    print(f"  Registered features: {len(lineagegraph.features)}")
    print(f"  Groups: {list(lineagegraph.groups.keys())}")
    for grp, fns in lineagegraph.groups.items():
        print(f"    {grp}: {len(fns)} features")

    section("Source Connectors — single country F mode")
    await profile_async("World Bank",
                        hr.world_bank.fetch, country_code=COUNTRY, indicator_code="NY.GDP.MKTP.KD.ZG")
    await profile_async("IMF",
                        hr.imf.fetch, country=COUNTRY, agency="IMF.STA", dataflow_id="PPI", key="PPI.IX.A")
    await profile_async("OpenSanctions",
                        hr.opensanction.fetch, country=COUNTRY, dataset="us_ofac_sdn", limit=100)

    section("Economic Features — F mode")
    eco = hr.features.eco
    for name, fn in [
        ("gdp_growth_yoy", eco.gdp_growth_yoy),
        ("gdp_growth_qoq", eco.gdp_growth_qoq),
        ("industrial_production_yoy", eco.industrial_production_yoy),
        ("inflation_cpi_yoy", eco.inflation_cpi_yoy),
        ("inflation_volatility_12m", eco.inflation_volatility_12m),
        ("ppi_yoy", eco.ppi_yoy),
        ("inflation_yoy", eco.inflation_yoy),
        ("unemployment_rate", eco.unemployment_rate),
        ("youth_unemployment", eco.youth_unemployment),
        ("labor_force_participation", eco.labor_force_participation),
        ("current_account_gdp_ratio", eco.current_account_gdp_ratio),
        ("fx_reserves_months_import", eco.fx_reserves_months_import),
        ("external_debt_gdp_ratio", eco.external_debt_gdp_ratio),
        ("fiscal_deficit_gdp", eco.fiscal_deficit_gdp),
        ("government_debt_gdp", eco.government_debt_gdp),
        ("reer_misalignment", eco.reer_misalignment),
        ("banking_sector_health", eco.banking_sector_health),
        ("gdp_per_capita_ppp", eco.gdp_per_capita_ppp),
    ]:
        await profile_async(name, fn, country_code=COUNTRY, mode="F")

    section("Geopolitical Features — F mode")
    geo = hr.features.geo
    geo_features = [
        ("conflict_event_count_30d", geo.conflict_event_count_30d, {"country_code": COUNTRY, "mode": "F"}),
        ("conflict_event_count_90d", geo.conflict_event_count_90d, {"country_code": COUNTRY, "mode": "F"}),
        ("conflict_trend", geo.conflict_trend, {"country_code": COUNTRY, "mode": "F"}),
        ("goldstein_scale_avg_30d", geo.goldstein_scale_avg_30d, {"country_code": COUNTRY, "mode": "F"}),
        ("goldstein_scale_trend", geo.goldstein_scale_trend, {"country_code": COUNTRY, "mode": "F"}),
        ("battle_deaths_30d", geo.battle_deaths_30d, {"country_code": COUNTRY, "mode": "F"}),
        ("battle_deaths_90d", geo.battle_deaths_90d, {"country_code": COUNTRY, "mode": "F"}),
        ("protest_event_count_30d", geo.protest_event_count_30d, {"country_code": COUNTRY, "mode": "F"}),
        ("protest_violence_level", geo.protest_violence_level, {"country_code": COUNTRY, "mode": "F"}),
        ("diplomatic_event_count_30d", geo.diplomatic_event_count_30d, {"country_code": COUNTRY, "mode": "F"}),
        ("diplomatic_intensity_avg", geo.diplomatic_intensity_avg, {"country_code": COUNTRY, "mode": "F"}),
        ("sanctions_count_active", geo.sanctions_count_active, {"country_code": COUNTRY}),
        ("sanctions_new_30d", geo.sanctions_new_30d, {"country_code": COUNTRY}),
        ("sanctions_sector_coverage", geo.sanctions_sector_coverage, {"country_code": COUNTRY}),
        ("governance_wgi_composite", geo.governance_wgi_composite, {"country_code": COUNTRY, "mode": "F"}),
        ("corruption_perception_index", geo.corruption_perception_index, {"country_code": COUNTRY, "mode": "F"}),
        ("rule_of_law_score", geo.rule_of_law_score, {"country_code": COUNTRY, "mode": "F"}),
        ("regulatory_quality", geo.regulatory_quality, {"country_code": COUNTRY, "mode": "F"}),
        ("democracy_index", geo.democracy_index, {"country_code": COUNTRY, "mode": "F"}),
        ("regime_type", geo.regime_type, {"country_code": COUNTRY, "mode": "F"}),
        ("press_freedom_score", geo.press_freedom_score, {"country_code": COUNTRY, "mode": "F"}),
    ]
    for name, fn, kwargs in geo_features:
        await profile_async(name, fn, **kwargs)

    section("Security Features — F mode")
    sec = hr.features.sec
    await profile_async("military_spending_gdp", sec.military_spending_gdp, country_code=COUNTRY, mode="F")
    await profile_async("military_spending_growth_yoy", sec.military_spending_growth_yoy, country_code=COUNTRY, mode="F")
    await profile_async("nato_member", sec.nato_member, country_code=COUNTRY, mode="F")

    section("Social Features — F mode")
    soc = hr.features.soc
    for name, fn in [
        ("human_rights_score", soc.human_rights_score),
        ("fragile_state_index", soc.fragile_state_index),
        ("human_development_index", soc.human_development_index),
        ("gini_coefficient", soc.gini_coefficient),
        ("poverty_headcount_ratio", soc.poverty_headcount_ratio),
    ]:
        await profile_async(name, fn, country_code=COUNTRY, mode="F")

    section("Environmental Features — F mode")
    env = hr.features.env
    for name, fn in [
        ("climate_vulnerability_score", env.climate_vulnerability_score),
        ("climate_readiness_score", env.climate_readiness_score),
        ("energy_dependence_ratio", env.energy_dependence_ratio),
        ("water_stress_index", env.water_stress_index),
    ]:
        await profile_async(name, fn, country_code=COUNTRY, mode="F")

    section("Full Pipeline — F mode (all features concurrently)")
    t0 = time.perf_counter()
    result = await hr.features.get_country_risk_features(COUNTRY)
    elapsed = time.perf_counter() - t0
    print(f"  Total: {elapsed:.3f}s")
    for group in ["economic", "geopolitical", "security", "social", "environmental"]:
        vals = result[group]
        filled = sum(1 for v in vals.values() if v is not None and v != 0 and v != "" and v != 0.0)
        print(f"    {group}: {filled}/{len(vals)} non-empty")

    section("Training Panel — ML mode (3 countries, GDELT-free)")
    fns = [f for f in hr.list_features if f.__name__ not in GDELT_FEATURES]
    print(f"  Features: {len(fns)} (skipped {len(hr.list_features) - len(fns)} GDELT-dependent)")
    t0 = time.perf_counter()
    panel = await hr.features.build_training_panel(fns, COUNTRIES_ML)
    elapsed = time.perf_counter() - t0
    print(f"  Total: {elapsed:.3f}s")
    if not panel.empty:
        print(f"  Shape: {panel.shape}")
        print(f"  Countries: {panel.index.get_level_values('country_iso3').nunique()}")
        try:
            dates = panel.index.get_level_values('date')
            print(f"  Date range: {dates.min()} -> {dates.max()}")
        except TypeError:
            print("  Date range: mixed types in index")
        print(f"  Columns: {list(panel.columns)}")
    else:
        print("  Empty panel")

    section("Memory Usage")
    snap_after = tracemalloc.take_snapshot()
    stats = snap_after.compare_to(snap_before, "lineno")
    total = sum(s.size_diff for s in stats)
    print(f"  Delta: {total / 1024:.1f} KB")
    for s in stats[:5]:
        frame = s.traceback[0] if s.traceback else None
        loc = f"{frame.filename}:{frame.lineno}" if frame else "?"
        print(f"    {loc}  {s.size_diff / 1024:+.1f} KB")
    tracemalloc.stop()

    section("Cache Stats")
    cache = hr.cache_stats()
    print(f"  Total files: {cache.get('total_files', 0)}")
    for src, hits in cache.get("hits", {}).items():
        misses = cache.get("misses", {}).get(src, 0)
        rate = cache.get("hit_rate", {}).get(src, 0)
        print(f"    {src}: {hits} hits, {misses} misses ({rate:.0%})")

    print(f"\n{'=' * 60}")
    print("  Profiling complete.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    asyncio.run(main())
    profiler.disable()

    print(f"\n{'=' * 60}")
    print("  cProfile — top 30 by cumulative time")
    print(f"{'=' * 60}")
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative")
    stats.print_stats(30)
    print(stream.getvalue())

    print(f"{'=' * 60}")
    print("  cProfile — top 30 by tottime")
    print(f"{'=' * 60}")
    stream2 = StringIO()
    stats2 = pstats.Stats(profiler, stream=stream2)
    stats2.sort_stats("tottime")
    stats2.print_stats(30)
    print(stream2.getvalue())
