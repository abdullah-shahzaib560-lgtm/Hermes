import type { Metadata } from "next";
import {
  DocTitle,
  Lead,
  H2,
  P,
  Callout,
  DocLink,
  PrevNext,
  Table,
} from "@/components/Doc";
import { CodeBlock } from "@/components/CodeBlock";
import { Sparkle, WobbleCircle } from "@/components/Doodle";

export const metadata: Metadata = {
  title: "Quickstart",
  description:
    "Install hermes-plt and run your first pipeline: instantiate the facade, fetch from a connector, compute features and inspect the cache.",
};

const INSTALL_CODE = `pip install hermes-plt`;

const CONSTRUCTOR_CODE = `from hermes import Hermes

hermes = Hermes(
    opensanction_api="",
    new_data_api="",
    fred_api="",
    sec_username="",
    sec_email="",
    finnhub_api="",
    cache_dir=None,   # defaults to ~/.hermes_cache/raw
    use_cache=True,
)`;

const WORLD_BANK_CODE = `import asyncio
from hermes import Hermes

hermes = Hermes(
    opensanction_api="x",
    new_data_api="x",
    sec_username="me@example.com",
    sec_email="me@example.com",
)

# Annual GDP growth (%) for the United States
df = hermes.world_bank.fetch(
    country_code="US",
    indicator_code="NY.GDP.MKTP.KD.ZG",
    frequency="Y",
    per_page=1000,
)

print(df.head())
#       date indicator_id  ...   value   source
# 0  2023-01-01  NY.GDP.MKTP.KD.ZG  ...  2.54  world_bank`;

const FEATURES_CODE = `# Country-risk economic features for the US (mode="F" → scalar)
gdp = await hermes.country_features.get_country_risk_features("USA")

# Or compute a single economic feature directly
growth = await hermes.lf.eco.gdp_growth_yoy(
    country_code="USA",
    mode="F",          # "F" → float, "ML" → pd.Series indexed by year
)

print(growth)  # e.g. 2.54`;

const CACHE_CODE = `stats = hermes.cache_stats()
print(stats)
# {
#   "total_files": 3,
#   "by_source": {"world_bank": 2, "imf": 1},
#   "hits": {"world_bank": 5},
#   "misses": {"world_bank": 2},
#   "hit_rate": {"world_bank": 0.71},
#}

# Purge cached files older than 7 days
hermes.clear_cache(older_than="7d")`;

export default function QuickstartPage() {
  return (
    <article className="relative">
      <div className="pointer-events-none absolute -left-6 top-16 hidden opacity-40 sm:block">
        <WobbleCircle className="h-20 w-20" color="#ff4328" />
      </div>
      <DocTitle kicker="Getting Started">Quickstart</DocTitle>
      <Lead>
        Install Hermes, instantiate the facade, fetch data from a connector and compute features —
        no API keys required for the World Bank source.
      </Lead>

      <Callout title="What you'll walk away with" tone="accent">
        An installed <code>hermes-plt</code> environment, a working <code>Hermes()</code> facade,
        one fetched dataset, two computed country-risk features, and a peek inside the cache.
        Roughly 10 minutes start to finish.
      </Callout>

      <H2 id="1">1. Install</H2>
      <P>
        Hermes requires <strong>Python 3.11 or newer</strong>. It is distributed on PyPI as{" "}
        <code>hermes-plt</code>:
      </P>
      <CodeBlock code={INSTALL_CODE} title="terminal" />
      <P>Runtime dependencies include <code>aiohttp</code>, <code>pandas</code>,{" "}
        <code>pyarrow</code>, <code>fastparquet</code>, <code>pycountry</code>,{" "}
        <code>pydantic</code>, <code>sdmx</code>, <code>sec-cik-mapper</code> and{" "}
        <code>yfinance</code> — installed automatically.
      </P>
      <P>Sanity-check the install by importing the facade and listing what ships with it:</P>
      <CodeBlock
        title="terminal"
        code={`$ python -c "import hermes; print(hermes.__version__)"
0.2.14

$ python -c "from hermes import Hermes; print(Hermes.__name__)"
Hermes`}
      />

      <H2 id="2">2. Instantiate the facade</H2>
      <P>
        The <code>Hermes</code> class is the single entry point. Its constructor takes the API
        credentials it may need and sets up a shared cache:
      </P>
      <CodeBlock code={CONSTRUCTOR_CODE} title="python" />
      <Callout title="KeyError guard" tone="gold">
        The constructor raises <code>KeyError</code> if both <code>opensanction_api</code> and{" "}
        <code>new_data_api</code> are empty. Pass any placeholder to proceed — only connectors you
        actually use need real keys.
      </Callout>
      <P>
        Setting <code>use_cache=False</code> disables the <code>RawCache</code>; otherwise all
        connectors share one <code>RawCache(cache_dir)</code>.
      </P>

      <H2 id="3">3. Fetch a dataset</H2>
      <P>
        Connectors are async (built on <code>aiohttp</code> with exponential-backoff retries). Pull
        annual GDP growth for the US from the World Bank:
      </P>
      <CodeBlock code={WORLD_BANK_CODE} title="python" />
      <P>
        The returned DataFrame follows the canonical connector schema:{" "}
        <code>date, indicator_id, indicator_name, country, value, source</code>. Flag{" "}
        <code>force=True</code> to bypass the cache for a fresh pull.
      </P>

      <H2 id="4">4. Compute country-risk features</H2>
      <P>
        Feed a country through the country-risk pipeline to derive intelligence across all five
        feature groups. Each feature accepts <code>mode=&quot;F&quot;</code> (latest scalar) or{" "}
        <code>mode=&quot;ML&quot;</code> (a <code>pd.Series</code> indexed by year 2000–2025, forward-filled):
      </P>
      <CodeBlock code={FEATURES_CODE} title="python" />

      <H2 id="5">5. Inspect the cache</H2>
      <P>Check per-source hit/miss statistics and purge entries older than a threshold:</P>
      <CodeBlock code={CACHE_CODE} title="python" />
      <Callout title="Cache path" tone="cedar">
        Files live under <code>~/.hermes_cache/raw/&lt;source&gt;/&lt;hash&gt;.parquet</code> with a{" "}
        <code>.meta.json</code> sidecar. Keys are a 16-char <code>sha256</code> of the source plus
        sorted JSON params.
      </Callout>

      <H2 id="env">Environment variables</H2>
      <P>
        Copy <code>.env.example</code> to <code>.env</code> and fill in the keys used by the
        connectors you need:
      </P>
      <CodeBlock
        title=".env"
        code={`OPEN_SANCTIONS_API=
NEWS_DATA_API=
FRED_API=
FINNHUB_API=
SEC_USERNAME=
SEC_EMAIL=`}
      />
      <Table
        head={["Variable", "Used by"]}
        rows={[
          ["OPEN_SANCTIONS_API", "OpenSanctions connector"],
          ["NEWS_DATA_API", "OpenSanctions connector"],
          ["FRED_API", "FRED connector (macro series)"],
          ["FINNHUB_API", "Finnhub connector + financial features"],
          ["SEC_USERNAME / SEC_EMAIL", "SEC EDGAR connector (User-Agent)"],
        ]}
      />

      <H2 id="troubleshooting">Troubleshooting</H2>
      <P>Stuck? Here are the most common snags and their fixes:</P>
      <Table
        head={["Symptom", "Cause & fix"]}
        rows={[
          ["KeyError at construction", "Both opensanction_api and new_data_api empty — pass any placeholder"],
          ["World Bank fetch returns empty", "Check country_code / indicator_code spelling; try force=True"],
          ["Rate limited / timeouts", "Retries are built in; raise retries or throttle with per-source TTL"],
          ["Slow first fetch", "Expected — cache is cold; later calls hit the parquet cache"],
          ["cached: 0 hits", "You haven't re-run after the first fetch; force=False reuses cache"],
        ]}
      />

      <H2 id="next">Next steps</H2>
      <P>
        You now have a live pipeline. A few natural next moves: explore the other{" "}
        <DocLink href="/docs/connectors">connectors</DocLink>, see how the{" "}
        <DocLink href="/docs/features">feature engine</DocLink> turns this data into derived
        intelligence, or dive into the <DocLink href="/docs/api-reference">API reference</DocLink>{" "}
        for the full surface.
      </P>
      <Sparkle className="mt-8 h-10 w-10 opacity-50" color="#ff4328" strokeWidth={4} />

      <PrevNext
        prev={{ title: "Overview", href: "/docs/overview" }}
        next={{ title: "Connectors", href: "/docs/connectors" }}
      />
    </article>
  );
}
