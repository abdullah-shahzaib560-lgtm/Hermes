import type { Metadata } from "next";
import {
  DocTitle,
  Lead,
  H2,
  P,
  List,
  Callout,
  DocLink,
  PrevNext,
  Table,
} from "@/components/Doc";
import { CodeBlock } from "@/components/CodeBlock";

export const metadata: Metadata = {
  title: "API Reference",
  description: "Reference for the Hermes facade, connectors, feature engine and core objects.",
};

export default function ApiReferencePage() {
  return (
    <article>
      <DocTitle kicker="Reference">API Reference</DocTitle>
      <Lead>
        The public surface of Hermes, centered on the <code>Hermes</code> facade, connectors,
        feature groups and core objects.
      </Lead>

      <H2 id="facade">Hermes</H2>
      <P>
        The single entry point. Instantiating it wires up every connector, feature group and the
        raw cache.
      </P>
      <CodeBlock
        title="python"
        code={`from hermes import Hermes

hermes = Hermes()

# Connectors
hermes.world_bank, hermes.imf, hermes.fred
hermes.yfinance, hermes.finnhub, hermes.binance
hermes.secedgar, hermes.open_sanction
hermes.public_dataset, hermes.gdelt

# Feature groups
hermes.economic_features, hermes.enviromental_features
hermes.geopolitical_features, hermes.security_features
hermes.social_features

hermes.ta_features, hermes.fa_features
hermes.crypto_history, hermes.company_filing

# Cache
hermes.cache`}
      />

      <H2 id="dataset">Dataset</H2>
      <P>
        A pydantic-backed collection of canonical records. Datasets are what connectors return
        and what feature groups consume.
      </P>
      <Table
        head={["Field", "Type", "Description"]}
        rows={[
          ["records", "list", "Canonical, validated records."],
          ["source", "str", "The originating connector / dataset."],
          ["metadata", "dict", "Provenance and description metadata."],
          ["version", "str", "Dataset version for lineage tracking."],
        ]}
      />

      <H2 id="cache">RawCache</H2>
      <P>
        Every fetch is cached per-source. Caching is parquet-backed with per-source TTLs.
      </P>
      <CodeBlock
        title="python"
        code={`stats = hermes.cache.stats()
# {'hits': ..., 'misses': ..., ...}

records = hermes.cache.get(source="world_bank", key=...)`}
      />

      <H2 id="entities">Entities</H2>
      <List
        items={[
          "countries — ISO3 conversion helpers.",
          "companies — ticker → CIK mapping for SEC filings.",
        ]}
      />

      <H2 id="lineage">Lineage, provenance, versioning</H2>
      <P>
        Hermes tracks how data and features were produced. These subsystems are evolving through
        the <DocLink href="/docs/roadmap">roadmap</DocLink> and currently expose skeletal APIs in
        <code> hermes/core</code>.
      </P>

      <Callout title="Alpha software" tone="gold">
        Hermes is at <strong>v0.2.14</strong> (alpha). Connectors and the feature engine are
        actively tested; some core subsystems are placeholders while the platform matures.
      </Callout>

      <PrevNext
        prev={{ title: "Features", href: "/docs/features" }}
        next={{ title: "Roadmap", href: "/docs/roadmap" }}
      />
    </article>
  );
}
