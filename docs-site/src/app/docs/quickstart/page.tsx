import type { Metadata } from "next";
import {
  DocTitle,
  Lead,
  H2,
  P,
  Callout,
  DocLink,
  PrevNext,
} from "@/components/Doc";
import { CodeBlock } from "@/components/CodeBlock";

export const metadata: Metadata = {
  title: "Quickstart",
  description: "Install mypy—install Hermes and run your first data pipeline.",
};

const INSTALL_CODE = `# create a virtual environment, then:
pip install hermes-plt`;

const FACADE_CODE = `from hermes import Hermes

hermes = Hermes()`;

const FETCH_CODE = `# Pull annual GDP growth for the world
world = hermes.world_bank.fetch(
    indicator="NY.GDP.MKTP.KD.ZG",
    years=[2020, 2021, 2022],
)

print(len(world), "records fetched")`;

const FEATURES_CODE = `# Derive economic country-risk features with lineage
features = hermes.economic_features.compute(
    dataset=world,
)
print(features.head())`;

const CACHE_CODE = `stats = hermes.cache.stats()
print(stats)
# {'hits': 12, 'misses': 3, ...}`;

export default function QuickstartPage() {
  return (
    <article>
      <DocTitle kicker="Getting Started">Quickstart</DocTitle>
      <Lead>
        Get Hermes installed and pull your first dataset in under a minute — no accounts or API
        keys required to start.
      </Lead>

      <H2 id="1">1. Install</H2>
      <P>
        Hermes requires <strong>Python 3.11+</strong>. Install it with pip (or uv if you prefer).
      </P>
      <CodeBlock code={INSTALL_CODE} title="terminal" />

      <H2 id="2">2. Create the facade</H2>
      <P>
        The <code>Hermes</code> class is your single entry point. It wires up every connector,
        feature group and the cache for you.
      </P>
      <CodeBlock code={FACADE_CODE} title="python" />

      <H2 id="3">3. Fetch a dataset</H2>
      <P>
        Pick any connector and call <code>fetch()</code>. Here we grab annual GDP growth from the
        World Bank.
      </P>
      <CodeBlock code={FETCH_CODE} title="python" />

      <Callout title="Async by default" tone="accent">
        Connectors are built on <code>aiohttp</code> and are asynchronous. In notebooks or plain
        scripts you may need to run them with an event loop — Hermes handles that for you inside
        the facade.
      </Callout>

      <H2 id="4">4. Compute features</H2>
      <P>
        Feed a dataset into a feature group to derive intelligence. The engine resolves
        dependencies in tiers and records lineage automatically.
      </P>
      <CodeBlock code={FEATURES_CODE} title="python" />

      <H2 id="5">5. Inspect the cache</H2>
      <P>
        Every fetch is cached per-source in parquet. Check hits and misses to see what&apos;d be
        served instantly next time.
      </P>
      <CodeBlock code={CACHE_CODE} title="python" />

      <H2 id="env">Environment variables</H2>
      <P>
        Some connectors need API keys. Copy <code>.env.example</code> to <code>.env</code> and add
        the keys you need:
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

      <H2 id="next">Next steps</H2>
      <P>
        Browse every <DocLink href="/docs/connectors">connector</DocLink> and its options, learn
        the <DocLink href="/docs/features">feature engine</DocLink>, or jump straight to the{" "}
        <DocLink href="/docs/api-reference">API reference</DocLink>.
      </P>

      <PrevNext
        prev={{ title: "Overview", href: "/docs/overview" }}
        next={{ title: "Connectors", href: "/docs/connectors" }}
      />
    </article>
  );
}
