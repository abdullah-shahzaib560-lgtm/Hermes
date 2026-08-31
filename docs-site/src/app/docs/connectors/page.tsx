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
  title: "Connectors",
  description:
    "Every Hermes connector: class, fetch() signature, source, endpoints and cache TTL. World Bank, IMF, FRED, Binance, Finnhub, yfinance, SEC, OpenSanctions, GDELT, public datasets.",
};

export default function ConnectorsPage() {
  return (
    <article>
      <DocTitle kicker="Core Concepts">Connectors</DocTitle>
      <Lead>
        Ten source connectors ship with Hermes, each exposing an async <code>fetch()</code> that
        returns canonical records and sits behind the shared <code>RawCache</code>.
      </Lead>

      <H2 id="contract">The connector contract</H2>
      <P>
        A connector answers one question: <em>how do I get this source&apos;s data?</em> In
        Hermes, each connector package pairs its <code>fetch()</code> with a parser, a normalizer
        and field mappings. Connectors can provide authentication, requests, pagination, rate
        limiting, retries and source-specific parsing — but generic retry, caching and validation
        belong to Hermes infrastructure, not to the connector.
      </P>
      <P>
        Connectors use <code>aiohttp</code> with exponential-backoff retries (sleeps{" "}
        <code>2**attempt</code> seconds) and resolve keys through <code>RawCache.get_or_fetch</code>.
      </P>

      <H2 id="world-bank">World Bank</H2>
      <Table
        head={["Item", "Detail"]}
        rows={[
          ["Class", "hermes.connectors.World_bank"],
          ["Base URL", "https://api.worldbank.org/v2"],
          ["Cache source", "world_bank · TTL 7 days"],
          [
            "fetch()",
            "fetch(country_code, indicator_code, frequency=None, most_recent=None, per_page=1000, page=1, force=False)",
          ],
          ["Return", "DataFrame with date, indicator_id, indicator_name, country, value, source"],
        ]}
      />
      <CodeBlock
        title="python"
        code={`from hermes import Hermes
hermes = Hermes(opensanction_api="x", new_data_api="x",
                sec_username="x", sec_email="x")

df = hermes.world_bank.fetch(
    country_code="BR",
    indicator_code="SP.POP.TOTL",   # total population
    frequency="Y",
)`}
      />

      <H2 id="imf">IMF (SDMX)</H2>
      <Table
        head={["Item", "Detail"]}
        rows={[
          ["Class", "hermes.connectors.IMF"],
          ["Base URL", "https://api.imf.org/external/sdmx/3.0/data/dataflow/"],
          ["Cache source", "imf · TTL 7 days"],
          [
            "fetch()",
            "fetch(country, agency, dataflow_id, key, version='~', force=False)",
          ],
          ["Return", "Normalized SDMX DataFrame; empty DataFrame on 404"],
        ]}
      />
      <CodeBlock
        title="python"
        code={`# IMF WEO government debt (% of GDP)
df = hermes.imf.fetch(
    country="US",
    agency="IMF.RES",
    dataflow_id="WEO",
    key="GGXWDG_NGDP",
)`}
      />

      <H2 id="fred">FRED</H2>
      <Table
        head={["Item", "Detail"]}
        rows={[
          ["Class", "hermes.connectors.FRED"],
          ["Base URL", "https://api.stlouisfed.org/fred/series/observations"],
          ["Cache source", "fred · TTL 30 days"],
          ["fetch()", "fetch(series_id, timeout=30.0, retries=3, force=False)"],
        ]}
      />
      <P>
        23 curated macro series are defined in <code>fred/mappings.py</code>, including{" "}
        <code>GDPC1</code>, <code>A191RL1Q225SBEA</code>, <code>INDPRO</code>,{" "}
        <code>CPIAUCSL</code>, <code>CPILFESL</code>, <code>PCEPI</code>, <code>UNRATE</code>,{" "}
        <code>PAYEMS</code>, <code>CIVPART</code>, <code>FEDFUNDS</code>, <code>DGS10</code>,{" "}
        <code>DGS2</code>, <code>DGS3MO</code>, <code>T10Y2Y</code>, <code>T10Y3M</code>,{" "}
        <code>M2SL</code>, <code>TOTBKCR</code>, <code>HOUST</code>, <code>EXHOSLUSM495S</code>,{" "}
        <code>SP500</code>, <code>VIXCLS</code>, <code>DTWEXBGS</code>.
      </P>
      <CodeBlock
        title="python"
        code={`fd = hermes.fred.fetch(series_id="CPIAUCSL")  # CPI`}
      />

      <H2 id="binance">Binance</H2>
      <Table
        head={["Item", "Detail"]}
        rows={[
          ["Class", "hermes.connectors.Binance"],
          ["Base URL", "api.binance.com (spot) / fapi.binance.com (future)"],
          ["Cache source", "binance · TTL 1 day"],
          [
            "fetch()",
            "fetch(mode, endpoint, symbol, interval=None, limit=None, period=None, retries=3, timeout=30.0, force=False)",
          ],
          [
            "fetch_history()",
            "fetch_history(symbol, interval='1d', market='future', years=2, max_concurrent=10)",
          ],
        ]}
      />
      <P>
        Endpoints (per <code>binance/mappings.py</code>): <code>ohlcv</code>, <code>trades</code>,{" "}
        <code>aggregated_trades</code>, <code>order_book</code>, <code>best_bid_ask</code>,{" "}
        <code>24hr</code>, <code>exchangeInfo</code>; plus future-only <code>fundingRate</code>,{" "}
        <code>openInterest</code>, <code>premiumIndex</code>, <code>openInterestHist</code>,{" "}
        <code>longShortRatio</code>, <code>topLongShortAccountRatio</code>,{" "}
        <code>topLongShortPositionRatio</code>. <code>fetch_history</code> splits the range into
        1000-bar windows fetched concurrently (semaphore = 10).
      </P>
      <CodeBlock
        title="python"
        code={`# 2 years of daily BTCUSDT futures candles
df = hermes.binance.fetch_history(
    symbol="BTCUSDT", interval="1d",
    market="future", years=2,
)`}
      />

      <H2 id="finnhub">Finnhub</H2>
      <Table
        head={["Item", "Detail"]}
        rows={[
          ["Class", "hermes.connectors.FINNHUB"],
          ["Base URL", "https://finnhub.io/api/v1"],
          ["Cache source", "finnhub · TTL 7 days"],
          [
            "fetch()",
            "fetch(endpoint, symbol, resolution=None, _from=None, _to=None, force=False)",
          ],
          [
            "fetch_candles_history()",
            "fetch_candles_history(symbol, resolution='D', years=2)",
          ],
        ]}
      />
      <P>
        Endpoints: <code>candles</code>, <code>quote</code>, <code>profile</code>,{" "}
        <code>metric</code>, <code>peers</code>, <code>earnings</code>, <code>insider</code>,{" "}
        <code>eps</code>, <code>ebitda</code>, <code>revenue</code>, <code>news</code>,{" "}
        <code>symbol</code>. Lookback is capped by <code>FINNHUB_MAX_DAYS</code> per resolution
        (e.g. 1m/5m → 7d, 15m–1h → 30d, D/W/M → 365d).
      </P>

      <H2 id="yfinance">Yfinance</H2>
      <Table
        head={["Item", "Detail"]}
        rows={[
          ["Class", "hermes.connectors.Yfinance"],
          ["Cache source", "yfinance · TTL 1 day"],
          [
            "fetch()",
            "fetch(endpoint, symbol, force=False) — endpoints: quote, eps_estimate, revenue_estimate, earnings_history",
          ],
          [
            "fetch_history()",
            "fetch_history(symbol, interval='1d', years=2)",
          ],
        ]}
      />
      <P>
        Raised restricted intervals (raises <code>ValueError</code> for unsupported ones). The
        interval map: <code>1m/5m/15m/30m/1h/1d</code> map to themselves, <code>1w → 1wk</code>,{" "}
        <code>1M → 1mo</code>.
      </P>

      <H2 id="sec">SEC EDGAR</H2>
      <Table
        head={["Item", "Detail"]}
        rows={[
          ["Class", "hermes.connectors.SECEDGAR"],
          ["Base URL", "https://data.sec.gov/api/xbrl/companyfacts"],
          ["Cache source", "sec_edgar · TTL 7 days"],
          ["fetch()", "fetch(symbol, timeout=30.0, retries=3, force=False)"],
        ]}
      />
      <P>
        Resolves a ticker to its CIK via <code>sec-cik-mapper</code> and requests{" "}
        <code>&lt;user-agent&gt; &lt;email&gt;</code> as required by the SEC. The{" "}
        <code>SEC_TAG_MAP</code> (<code>sec/tags.py</code>) maps canonical fields to XBRL GAAP tags
        — e.g. <code>revenue</code>, <code>net_income</code>, <code>operating_cash_flow</code>,{" "}
        <code>long_term_debt</code>, <code>shares_outstanding</code>, <code>dividends</code>,{" "}
        <code>buybacks</code>, etc.
      </P>

      <H2 id="opensanctions">OpenSanctions</H2>
      <Table
        head={["Item", "Detail"]}
        rows={[
          ["Class", "hermes.connectors.OpenSanction"],
          ["Base URL", "https://api.opensanctions.org"],
          ["Auth", "Authorization: ApiKey &lt;key&gt;"],
          ["Cache source", "OpenSanction · TTL 30 days"],
          [
            "fetch()",
            "fetch(country, dataset, limit=50, changed_since=None, topic=None, facets=None, force=False)",
          ],
        ]}
      />
      <P>
        Supports datasets such as <code>us_ofac_sdn</code>, <code>eu_fsf</code>,{" "}
        <code>uk_fcdos</code> and <code>un_sc</code>. Country ISO3 is converted to ISO2 internally
        before filtering.
      </P>

      <H2 id="gdelt">GDELT</H2>
      <Table
        head={["Item", "Detail"]}
        rows={[
          ["Class", "hermes.connectors.GDELT"],
          ["Status", "Stub (empty class)"],
        ]}
      />
      <P>
        The GDELT connector is scaffolded but not yet implemented — global news/event data
        powers the geopolitical features, which are similarly stubbed.
      </P>

      <H2 id="public">Bundled public datasets</H2>
      <Table
        head={["Item", "Detail"]}
        rows={[
          ["Class", "hermes.connectors.PUBLIC_DATASET"],
          ["Location", "hermes/connectors/lib/datasets/"],
        ]}
      />
      <P>Reads bundled local CSVs, country-filtered with years converted to <code>datetime</code>:</P>
      <ListRows />

      <H2 id="retries">Retries & timeouts</H2>
      <Callout title="Every connector" tone="cedar">
        All HTTP connectors default to <code>retries=3</code> and <code>timeout=30.0</code>,
        retrying with exponential backoff. Pass <code>force=True</code> to bypass the cache.
      </Callout>

      <PrevNext
        prev={{ title: "Quickstart", href: "/docs/quickstart" }}
        next={{ title: "Features", href: "/docs/features" }}
      />
    </article>
  );
}

function ListRows() {
  return (
    <div className="my-4 grid gap-2 sm:grid-cols-2">
      {[
        ["fetch_hrs(country)", "human_right_score"],
        ["fetch_hdi(country)", "human development index (iso3, year, score)"],
        ["fetch_cpi(country)", "global CPI"],
        ["fetch_fsi(country)", "fragile states index (Total 0–120)"],
        ["fetch_nato(country)", "NATO membership"],
        ["fetch_crs(country)", "climate readiness score"],
        ["fetch_cvs(country)", "climate vulnerability score"],
        ["fetch_sipri(country)", "SIPRI military expenditure"],
      ].map(([fn, desc]) => (
        <div key={fn} className="rounded-xl border border-line bg-white px-3 py-2">
          <code className="font-mono text-[12.5px] font-semibold text-ink">{fn}</code>
          <div className="mt-0.5 font-body text-[13px] text-ink">{desc}</div>
        </div>
      ))}
    </div>
  );
}
