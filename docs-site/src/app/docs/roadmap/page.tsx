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
import { CodeBlock } from "@/components/CodeBlock";
import { Plant, Sparkle } from "@/components/Doodle";

export const metadata: Metadata = {
  title: "Roadmap",
  description:
    "Hermes roadmap and architecture phases: connectors & features today; the core lifecycle subsystems built out over time.",
};

export default function RoadmapPage() {
  return (
    <article className="relative">
      <div className="pointer-events-none absolute -right-8 top-24 hidden opacity-40 sm:block">
        <Plant className="h-28 w-24" color="#ff4328" />
      </div>
      <DocTitle kicker="Project">Roadmap</DocTitle>
      <Lead>
        Hermes ships a working foundation and builds the general-purpose core out progressively.
        The target architecture is specified in <code>docs/architecture/hermes-core.md</code>.
      </Lead>

      <H2 id="summary">The journey at a glance</H2>
      <Table
        head={["Phase", "Focus", "ETA-ish"]}
        rows={[
          ["Phase 1 — Foundation", "fetch, parse, normalize, validate, Dataset, schema system", "Now → next"],
          ["Phase 2 — Reliable infra", "storage, snapshots, provenance, lineage, query interface", "In progress"],
          ["Phase 3 — Ecosystem", "Hermes Finance, Defense, Healthcare, Trade, Energy, Climate…", "Next"],
          ["Phase 4 — Scale", "object storage, distributed processing, continuous ingestion", "Later"],
          ["Phase 5 — Cloud", "hosted datasets, APIs, catalogs, versioned data, team access", "Future"],
        ]}
      />

      <H2 id="now">Today (v0.2.x)</H2>
      <Table
        head={["Area", "Status"]}
        rows={[
          ["Connectors (10)", "Working & tested"],
          ["Feature engine (@feature, LineageGraph, TieredPlan)", "Working"],
          ["Country-risk features (5 groups)", "Working; geopolitical stubbed, others partial"],
          ["Financial features (technical / fundamental / crypto / filing)", "Working"],
          ["RawCache (parquet, TTLs, hit/miss)", "Working"],
          ["Asyncio scheduler (@schedule, cron/interval)", "Working"],
          ["Entities (countries, companies)", "Working"],
          [
            "Core lifecycle modules (parse/normalize/validate/schema/metadata/query/storage/api)",
            "Scaffolded — being built out",
          ],
        ]}
      />

      <H2 id="core-spec">The core life-cycle specification</H2>
      <P>
        <code>hermes-core.md</code> describes the general-purpose data-lifecycle engine Hermes is
        building toward. Lifecycle subsystems:
      </P>
      <List
        items={[
          "Acquisition — fetch, ingest, source, connect, read, stream",
          "Parsing — parse, detect_format, read_raw, decode (CSV/JSON/JSONL/XML/Parquet/Arrow/compressed)",
          "Data Contract / Schema — schema, infer_schema, validate_schema, migrate_schema",
          "Normalization — normalize, map, cast, standardize, convert_units, align_time",
          "Quality — validate, check, profile, deduplicate, detect_anomalies (ML-extensible)",
          "Transformation — transform, pipe, select, filter, join, aggregate (Polars/Arrow/DuckDB)",
          "Identity / Resolution — resolve, identify, match, link, entity (extension point)",
          "Storage — save, load, delete (FS/Parquet/Arrow/DuckDB/PostgreSQL)",
          "Query — query, sql with filter/project/join/aggregate/order/limit",
          "Versioning — version, snapshot, diff (immutable snapshots)",
          "Provenance & Lineage — lineage, provenance, trace",
        ]}
      />
      <P>
        Cross-cutting design rules: a <strong>registry</strong> for every component, a defined{" "}
        <strong>error hierarchy</strong>, an <strong>extension architecture</strong>, and the{" "}
        <strong>dependency rule</strong> — Core never depends on a domain package. The public API
        target is <code>hr.fetch/ingest/parse/normalize/validate/profile/inspect/transform/query/
        save/load/export</code>.
      </P>

      <H2 id="phases">The phases</H2>
      <CodeBlock title="phases" code={`Phase 1 — Foundation
  fetch, ingest, parse, normalize, validate, profile, inspect,
  transform, export, Dataset, connector system, schema system

Phase 2 — Reliable infrastructure
  storage, versions, snapshots, provenance, lineage,
  better validation & profiling, caching, query interface

Phase 3 — Ecosystem
  Hermes Finance, Defense, Healthcare, Trade, Energy, Climate,
  Geopolitics, Corporate, Entity, Features

Phase 4 — Scale
  remote datasets, object storage, distributed processing,
  continuous ingestion, large-dataset querying, cloud execution

Phase 5 — Hermes Cloud
  hosted datasets, APIs, dataset catalogs, continuous pipelines,
  versioned data, team access, usage controls, enterprise infra`} />
      <P>
        The guiding philosophy: make high-quality data infrastructure accessible through one
        consistent developer experience. One engine, one ecosystem, any data.
      </P>

      <Callout title="Get involved" tone="cedar">
        Hermes is open source. The repository ships GitHub labels (type / area / difficulty) and
        a contributing guide (<code>docs/engineering_team_guide.md</code>) that defines the
        vertical-slice build order (e.g. World Bank: acquire → parse → normalize → validate →
        metadata → provenance → Dataset).
      </Callout>
      <Sparkle className="mt-8 h-10 w-10 opacity-50" color="#ff4328" strokeWidth={4} />

      <PrevNext prev={{ title: "API Reference", href: "/docs/api-reference" }} />
    </article>
  );
}
