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
  title: "Features",
  description: "The Hermes feature engine: country risk and financial features with lineage.",
};

const DECORATOR = `from hermes.features import feature

@feature(name="gdp_growth_5y", group="economic", deps=["gdp_growth"])
def compute_growth(df, config):
    return df["gdp_growth"].rolling(5).mean()`;

export default function FeaturesPage() {
  return (
    <article>
      <DocTitle kicker="Core Concepts">Features</DocTitle>
      <Lead>
        Hermes turns raw datasets into derived intelligence through a tiered, dependency-aware
        feature engine that records lineage at every step.
      </Lead>

      <H2 id="what">What is a feature group?</H2>
      <P>
        A feature group is a themed collection of computed signals. Hermes ships two today:
        <strong> country risk</strong> and <strong>financial</strong>. Each group is a facade over
        individual features that declare their dependencies.
      </P>

      <H2 id="country-risk">Country risk features</H2>
      <P>
        Five pillars of country-risk engineering, designed to be combined into sovereign / country
        scores:
      </P>
      <List
        items={[
          "Economic — growth, inflation, fiscal and monetary signals.",
          "Environmental — climate and resource stress indicators.",
          "Geopolitical — currently a stub (NotImplementedError) while the data model matures.",
          "Security — safety and conflict-related features.",
          "Social — human development and societal indicators.",
        ]}
      />
      <P>
        Deep-dives are documented under{" "}
        <DocLink href="/docs/api-reference" external={false}>
          the analysis docs
        </DocLink>{" "}
        in the repository (<code>docs/analysis/</code>).
      </P>

      <H2 id="financial">Financial features</H2>
      <P>
        Three financial groups compute signals from market and filing data:
      </P>
      <Table
        head={["Group", "Domain", "Examples"]}
        rows={[
          ["Technical", "Markets", "Moving averages, momentum, oscillators."],
          ["Fundamental", "Companies", "Valuation and ratio analysis."],
          ["Crypto", "Crypto", "History-backed crypto signals."],
          ["Filing", "Companies", "Signals derived from SEC filings."],
        ]}
      />

      <H2 id="registry">The registry & decorator</H2>
      <P>
        Features register themselves with metadata and dependencies via a{" "}
        <code>@feature</code> decorator. The engine resolves them in dependency order — the same
        idea as a build system for your data.
      </P>
      <CodeBlock code={DECORATOR} title="python" />

      <Callout title="LineageGraph" tone="cedar">
        Every computed feature is added to a <strong>LineageGraph</strong>, so a single artifact
        can tell you exactly which inputs produced it.
      </Callout>

      <H2 id="compute">Computing features</H2>
      <P>Compute a full group against a dataset through the facade:</P>
      <CodeBlock
        title="python"
        code={`from hermes import Hermes

hermes = Hermes()
features = hermes.economic_features.compute(dataset=data)
print(features.head())`}
      />

      <PrevNext
        prev={{ title: "Connectors", href: "/docs/connectors" }}
        next={{ title: "API Reference", href: "/docs/api-reference" }}
      />
    </article>
  );
}
