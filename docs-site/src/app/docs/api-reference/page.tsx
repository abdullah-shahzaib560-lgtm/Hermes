import type { Metadata } from "next";
import {
  DocTitle,
  Lead,
  H2,
  P,
  Callout,
  PrevNext,
  Table,
} from "@/components/Doc";
import { CodeBlock } from "@/components/CodeBlock";

export const metadata: Metadata = {
  title: "API Reference",
  description:
    "Reference for the Hermes facade, RawCache, scheduler, feature registry, entities and constants.",
};

export default function ApiReferencePage() {
  return (
    <article>
      <DocTitle kicker="Reference">API Reference</DocTitle>
      <Lead>
        The public surface of Hermes, centered on the <code>Hermes</code> facade, the{" "}
        <code>RawCache</code>, the scheduler, entities and constants.
      </Lead>

      <H2 id="facade">Hermes facade</H2>
      <CodeBlock
        title="constructor"
        code={`Hermes(
    opensanction_api: str,
    new_data_api: str,
    fred_api: str,
    sec_username: str,
    sec_email: str,
    finnhub_api: str,
    cache_dir: str | None = None,
    use_cache: bool = True,
) -> Hermes`}
      />
      <P>
        Raises <code>KeyError</code> if both <code>opensanction_api</code> and{" "}
        <code>new_data_api</code> are empty. Creates a shared <code>RawCache(cache_dir)</code>{" "}
        unless <code>use_cache=False</code>.
      </P>
      <Table
        head={["Attribute", "Type", "Notes"]}
        rows={[
          ["list_countries", "list[str]", "249 ISO-3 codes"],
          ["lf", "features", "feature registry facade"],
          ["list_features", "list[Callable]", "= lf.list_features() (~57 features)"],
          ["country_features", "pipeline", "country-risk pipeline"],
          ["ta_feature", "TAfeatures", "technical analysis"],
          ["fa_features", "FAfeatures", "fundamental analysis"],
          ["crypto_history", "CryptoHistory", "crypto history"],
          ["filling_history", "CompanyFiling", "company filing history"],
          ["world_bank, imf, fred", "connector", "global macro"],
          ["gdelt", "GDELT", "stub"],
          ["opensanction", "OpenSanction", "sanctions"],
          ["binance, finnhub, yfin", "connector", "markets"],
          ["sec_edger", "SECEDGAR", "SEC filings (sic)"],
          ["datasets", "PUBLIC_DATASET", "bundled CSVs"],
        ]}
      />
      <CodeBlock
        title="methods"
        code={`def clear_cache(self, older_than: str | None = None) -> None
    # older_than: e.g. "7d", "24h", "2w" — parsed into timedelta

def cache_stats(self) -> dict
    # -> {"total_files", "by_source", "hits", "misses", "hit_rate"}`}
      />

      <H2 id="cache">RawCache</H2>
      <P>
        In <code>hermes/acquisition/cache.py</code>. Default dir{" "}
        <code>~/.hermes_cache/raw</code>, default TTL 24h. Cache keys are{" "}
        <code>sha256(source + json_params)[:16]</code>, stored as{" "}
        <code>&lt;dir&gt;/&lt;source&gt;/&lt;hash&gt;.parquet</code>.
      </P>
      <CodeBlock
        title="python"
        code={`RawCache(cache_dir: str | Path | None = None)

get(source, params, ttl=None)                    # raises CacheMiss on miss/expiry/corruption
put(source, params, df)                          # writes parquet + .meta.json
get_or_fetch(source, params, fetch_fn,           # cache unless force, else await & cache
             force=False, ttl=None)
clear(older_than: timedelta | None = None)       # delete .parquet (+ meta)
stats() -> {"total_files", "by_source",
            "hits", "misses", "hit_rate"}`}
      />

      <H2 id="scheduler">Scheduler</H2>
      <P>
        A full asyncio scheduler in <code>hermes/core/scheduler.py</code> supporting interval and
        cron specs.
      </P>
      <CodeBlock
        title="python"
        code={`from hermes.core.scheduler import schedule, start, stop, run_now, list_jobs

@schedule(time="daily", name="nightly_refresh", timeout=600.0, retries=3)
async def refresh(dataset):
    ...

start()                     # runs loop until KeyboardInterrupt
stop()
run_now("nightly_refresh")  # async: run_now_async; sync wrapper via asyncio.run
list_jobs()                 # name, schedule, next_run, last_run, last_status, runs, failures`}
      />
      <Table
        head={["Spec", "Meaning"]}
        rows={[
          ['"hourly" / "daily" / "weekly"', "1h / 1d / 1w aliases"],
          ['"30m" / "2d" / "3w"', "Numeric interval suffixes (m, h, d, w)"],
          ['"0 3 * * *"', "5-field cron: min hour day month weekday (Sun=0)"],
        ]}
      />
      <P>
        Cron supports <code>*</code>, ranges <code>a-b</code>, steps <code>*/n</code> and{" "}
        <code>a-b/n</code>, and comma lists. Retries use exponential backoff capped at 60s.
      </P>

      <H2 id="entities">Entities</H2>
      <CodeBlock
        title="python"
        code={`from hermes.entities.countries import countries, iso3_to_iso2, check_iso3
from hermes.entities.companies import get_cik

countries          # list[str] of 249 ISO-3 codes
iso3_to_iso2("USA")   # -> "US"
check_iso3("USA")     # -> None; raises RuntimeError if not ISO3
get_cik("AAPL")       # -> "CIK0320193" or "Not Found"`}
      />

      <H2 id="constants">Constants</H2>
      <Table
        head={["Constant", "Content"]}
        rows={[
          ["SYMBOLS", "20 crypto symbols: BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, DOGEUSDT, TRXUSDT, ADAUSDT, LINKUSDT, AVAXUSDT, SUIUSDT, LTCUSDT, BCHUSDT, HBARUSDT, NEARUSDT, UNIUSDT, DOTUSDT, APTUSDT, ARBUSDT, OPUSDT"],
          ["TICKERS", "18 US equities: NVDA, AAPL, GOOGL, MSFT, AMZN, AVGO, META, TSLA, LLY, WMT, AMD, V, XOM, JNJ, ORCL, COST, NFLX, CRM"],
          ["CANONICAL_FREQS", "15 intervals: 1s, 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M"],
          ["SUPPORTED_STOCK_FREQS", "1m, 5m, 15m, 30m, 1h, 1d, 1w, 1M"],
          ["BINANCE_INTERVAL_* / FINNHUB_* / YFINANCE_*", "Canonical ↔ provider interval maps and max lookbacks"],
        ]}
      />

      <H2 id="dataset">Dataset</H2>
      <P>
        A pydantic <code>BaseModel</code> in <code>hermes/core/dataset.py</code>:
      </P>
      <CodeBlock
        title="python"
        code={`class Dataset(BaseModel):
    id: uuid.UUID          # default_factory=uuid4
    name: str
    version: str
    schema_ref: ...
    metadata: MetaData
    provenance: Provenance
    lineage: Lineage`}
      />
      <P>
        The composable parse/normalize/validate/query methods and the{" "}
        <code>Lineage</code>/<code>Provenance</code>/<code>MetaData</code>/<code>DataVersion</code>/
        <code>Result</code> model classes are the target architecture and are being built out.
      </P>

      <H2 id="feature-registry">Feature registry (reference)</H2>
      <CodeBlock
        title="python"
        code={`@feature(name, group, deps, compute)
def fn(...): ...

class LineageGraph:
    register_feature(name, group, deps, compute, fn)
    get_feature(name) -> dict | None
    get_group_features(group) -> list[str]
    resolve_group(group) -> TieredPlan
    save(path) / load(path)

class TieredPlan:
    tiers: list[list[str]]
    all_features: list[str]`}
      />

      <Callout title="Alpha status" tone="gold">
        Hermes is at <strong>v0.2.14</strong>. Connectors and features are actively tested (pytest
        with asyncio auto-mode; ruff + mypy in CI). Several core lifecycle modules remain
        placeholders while the platform matures.
      </Callout>

      <PrevNext
        prev={{ title: "Features", href: "/docs/features" }}
        next={{ title: "Roadmap", href: "/docs/roadmap" }}
      />
    </article>
  );
}
