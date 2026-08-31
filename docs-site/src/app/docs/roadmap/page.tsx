import type { Metadata } from "next";
import {
  DocTitle,
  Lead,
  H2,
  P,
  List,
  Callout,
  PrevNext,
  Table,
} from "@/components/Doc";

export const metadata: Metadata = {
  title: "Roadmap",
  description: "Where the Hermes platform is headed, phase by phase.",
};

export default function RoadmapPage() {
  return (
    <article>
      <DocTitle kicker="Project">Roadmap</DocTitle>
      <Lead>
        Hermes is built in phases. Today the connectors and feature engine are the working core;
        the rest of the platform is being built out.
      </Lead>

      <H2 id="now">Where we are now (v0.2.x)</H2>
      <List
        items={[
          "10 source connectors with a unified async fetch() contract.",
          "Country-risk feature engine across five pillars (economic, environmental, geopolitical, security, social).",
          "Financial features: technical, fundamental, crypto and filing signals.",
          "Parquet-backed RawCache with per-source TTLs.",
          "Lineage graph and tiered, dependency-aware feature resolution.",
        ]}
      />

      <H2 id="phases">The build-out</H2>
      <Table
        head={["Area", "Status", "Plan"]}
        rows={[
          ["Connectors", "Working", "Actively expanded & tested."],
          ["Features", "Working", "Depth of signals growing; geopolitical stub pending."],
          ["Core (Dataset, scheduler)", "Skeletal", "Hardening the data model and scheduling."],
          [
            "Metadata / provenance / lineage / versioning",
            "Stubs",
            "Full tracking across the lifecycle.",
          ],
          [
            "Parsing, normalization, validation, schemas",
            "Placeholder dirs",
            "Dedicated subsystems for each stage.",
          ],
          [
            "Storage, query, export, API",
            "Placeholder dirs",
            "Serve platforms: query layer + public API.",
          ],
        ]}
      />

      <H2 id="roadmap-note">A note on direction</H2>
      <P>
        The detailed internal build checklist lives in{" "}
        <code>docs/architecture/hermes-core.md</code> in the repository. The goal is a complete
        data lifecycle platform — bring data in, trust it, and serve it — with zero vendor lock-in.
      </P>

      <Callout title="Get involved" tone="cedar">
        Hermes is open source. The repository carries GitHub labels (type / area / difficulty) to
        help new contributors find a good first issue.
      </Callout>

      <PrevNext prev={{ title: "API Reference", href: "/docs/api-reference" }} />
    </article>
  );
}
