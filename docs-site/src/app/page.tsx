import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { CodeBlock } from "@/components/CodeBlock";
import { Arrow, Sparkle, Spiral, Squiggle, WobbleCircle, Plant } from "@/components/Doodle";

const valueProps = [
  {
    title: "Acquire",
    body: "Pull data from APIs, CSVs, JSON and public datasets through a unified connector layer.",
    color: "#ff4126",
    icon: "⇣",
  },
  {
    title: "Validate",
    body: "Check integrity, schema and provenance before anything dirty ever reaches a dataset.",
    color: "#1f5f4b",
    icon: "✓",
  },
  {
    title: "Normalize",
    body: "Bring messy sources into one canonical shape with consistent codes and units.",
    color: "#b88a1f",
    icon: "≈",
  },
  {
    title: "Serve",
    body: "Query, export and feed features into models — lineage tracked every step of the way.",
    color: "#5b4bd9",
    icon: "➤",
  },
];

const stats = [
  { value: "10+", label: "connectors" },
  { value: "5", label: "feature groups" },
  { value: "3.11+", label: "Python" },
  { value: "α", label: "v0.2.14" },
];

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-cream text-ink">
      <Navbar />

      {/* ------- HERO ------- */}
      <main className="flex-1">
        <section className="relative overflow-hidden">
          {/* doodle background */}
          <div className="pointer-events-none absolute inset-0">
            <Plant className="absolute left-8 top-40 h-28 w-24 opacity-50" color="#1f5f4b" />
            <Sparkle className="absolute right-16 top-32 h-16 w-16 opacity-70" color="#ff4126" />
            <Spiral className="absolute right-1/3 top-16 h-14 w-14 opacity-40" color="#0a0a07" />
            <WobbleCircle className="absolute bottom-10 left-1/2 h-24 w-24 opacity-50" color="#b88a1f" />
            <Sparkle className="absolute bottom-24 right-24 h-12 w-12 opacity-50" color="#1f5f4b" />
          </div>

          <div className="relative mx-auto max-w-6xl px-6 pt-24 pb-20 text-center md:pt-36 md:pb-28">
            <div className="relative mx-auto mb-8 inline-flex items-center gap-2 rounded-full border border-line bg-white/60 px-4 py-1.5 font-body text-sm font-medium text-ink-soft backdrop-blur">
              <Sparkle className="h-4 w-4" color="#ff4126" strokeWidth={4} />
              The Data Engine for Python
              <Sparkle className="h-4 w-4" color="#ff4126" strokeWidth={4} />
            </div>

            <h1 className="relative mx-auto max-w-4xl font-heading text-5xl font-extrabold leading-[1.05] tracking-tight text-ink sm:text-6xl md:text-7xl">
              Intelligence data,
              <br />
              <span className="relative inline-block">
                end to end.
                <Squiggle className="absolute -bottom-3 left-0 w-full" color="#ff4126" strokeWidth={5} />
              </span>
            </h1>

            <p className="relative mx-auto mt-10 max-w-2xl font-body text-lg leading-relaxed text-ink-soft md:text-xl">
              Hermes is a foundational intelligence data platform. Acquire, validate, normalize,
              store and serve datasets — with provenance baked into every row.
            </p>

            {/* Install + docs */}
            <div className="relative mx-auto mt-12 max-w-xl">
              <CodeBlock
                code="pip install hermes-plt"
                title="terminal"
              />
              <Arrow className="pointer-events-none absolute -top-8 -right-12 hidden h-16 w-24 md:block" color="#ff4126" />
            </div>

            <div className="relative mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Link
                href="/docs/overview"
                className="group relative inline-flex items-center gap-2 rounded-full bg-ink px-7 py-3.5 font-body text-base font-semibold text-cream shadow-soft transition-all hover:-translate-y-0.5 hover:bg-accent"
              >
                Documentation
                <span className="transition-transform group-hover:translate-x-1">→</span>
              </Link>
              <Link
                href="/docs/quickstart"
                className="inline-flex items-center gap-2 rounded-full border-2 border-ink/15 px-7 py-3.5 font-body text-base font-semibold text-ink transition-colors hover:border-ink"
              >
                Read the quickstart
              </Link>
            </div>

            <p className="relative mt-8 inline-block font-mono text-xs text-ink-soft">
              Python 3.11+ · pandas, polars, arrow & duckdb friendly
            </p>
          </div>

          {/* stats bar */}
          <div className="relative mx-auto max-w-5xl px-6 pb-16">
            <div className="grid grid-cols-2 gap-px overflow-hidden rounded-3xl border border-line bg-line shadow-card sm:grid-cols-4">
              {stats.map((s) => (
                <div key={s.label} className="bg-cream/90 px-6 py-6 text-center">
                  <div className="font-heading text-3xl font-extrabold text-ink md:text-4xl">{s.value}</div>
                  <div className="mt-1 font-body text-sm text-ink-soft">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ------- VALUE PROPS ------- */}
        <section className="relative border-t border-line/60 bg-cream-soft/60 py-20">
          <div className="mx-auto max-w-6xl px-6">
            <div className="mb-12 flex flex-col items-center text-center">
              <h2 className="font-heading text-3xl font-extrabold tracking-tight md:text-4xl">
                One pipeline. <span className="hairline text-accent">Every source.</span>
              </h2>
              <p className="mt-4 max-w-2xl font-body text-ink-soft">
                From raw fetch to production-ready features in a single, repeatable pipeline.
              </p>
            </div>

            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
              {valueProps.map((v, i) => (
                <div
                  key={v.title}
                  className="group relative rounded-3xl border border-line bg-cream p-7 shadow-card transition-all hover:-translate-y-1"
                >
                  <div className="mb-6 flex items-center justify-between">
                    <span
                      className="flex h-11 w-11 items-center justify-center rounded-2xl text-xl font-bold"
                      style={{ backgroundColor: `color-mix(in srgb, ${v.color} 14%, transparent)`, color: v.color }}
                    >
                      {v.icon}
                    </span>
                    <span className="font-heading text-sm font-bold text-ink/25">0{i + 1}</span>
                  </div>
                  <h3 className="font-heading text-xl font-bold">{v.title}</h3>
                  <p className="mt-2 font-body text-sm leading-relaxed text-ink-soft">{v.body}</p>
                  <Squiggle className="mt-5 w-20 opacity-60" color={v.color} strokeWidth={4} />
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ------- FEATURES ------- */}
        <section className="relative overflow-hidden py-20">
          <div className="pointer-events-none absolute right-0 top-10 opacity-40">
            <Plant className="h-36 w-28" color="#1f5f4b" />
          </div>
          <div className="mx-auto max-w-6xl px-6">
            <div className="grid items-center gap-12 lg:grid-cols-2">
              <div>
                <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-line bg-white/60 px-3 py-1 font-body text-xs font-bold uppercase tracking-wider text-accent">
                  Built for trust
                </div>
                <h2 className="font-heading text-3xl font-extrabold tracking-tight md:text-4xl">
                  Provenance you can <span className="hairline text-accent">point at.</span>
                </h2>
                <p className="mt-4 max-w-lg font-body leading-relaxed text-ink-soft">
                  Every Hermes dataset carries metadata, provenance and lineage. Know where data
                  came from, how it changed and what depends on it — without a separate system.
                </p>
                <ul className="mt-6 space-y-4">
                  {[
                    "Unified connector&nbsp;contract for every source",
                    "Tiered, dependency-aware feature resolution",
                    "Parquet-backed caching with per-source TTLs",
                    "Works with pandas, polars, arrow & duckdb",
                  ].map((item) => (
                    <li key={item} className="flex items-start gap-3 font-body text-ink">
                      <Sparkle className="mt-1 h-4 w-4 shrink-0" color="#1f5f4b" strokeWidth={4} />
                      <span dangerouslySetInnerHTML={{ __html: item }} />
                    </li>
                  ))}
                </ul>
                <Link
                  href="/docs/features"
                  className="group mt-8 inline-flex items-center gap-2 rounded-full border-2 border-ink/15 px-6 py-3 font-body font-semibold transition-colors hover:border-ink"
                >
                  Explore the feature engine
                  <span className="transition-transform group-hover:translate-x-1">→</span>
                </Link>
              </div>

              <div className="relative">
                <WobbleCircle className="absolute -left-8 -top-8 h-24 w-24 opacity-60" color="#b88a1f" />
                <div className="relative overflow-hidden rounded-3xl border border-line bg-cream p-8 shadow-soft">
                  <div className="mb-6 flex items-center gap-2">
                    <span className="h-3 w-3 rounded-full bg-accent" />
                    <span className="h-3 w-3 rounded-full bg-line" />
                    <span className="h-3 w-3 rounded-full bg-line" />
                    <span className="ml-3 font-mono text-xs text-ink-soft">hermes.py</span>
                  </div>
                  <CodeBlock
                    title="python"
                    code={`from hermes import Hermes

hermes = Hermes()

# Fetch global macro + country risk
world = hermes.world_bank.fetch(
    indicator="NY.GDP.MKTP.KD.ZG"
)

# Compute economic features with lineage
features = hermes.economic_features.compute(
    dataset=world
)

stats = hermes.cache.stats()
print(f"cached: {stats['hits']} hits")`}
                  />
                  <Sparkle className="absolute -bottom-4 -right-4 h-14 w-14 opacity-60" color="#ff4126" />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ------- CTA ------- */}
        <section className="relative border-t border-line/60 py-20">
          <div className="mx-auto max-w-4xl px-6 text-center">
            <div className="relative rounded-[2.5rem] border border-line bg-ink p-10 text-cream shadow-soft md:p-16">
              <Sparkle className="absolute -top-6 left-10 h-12 w-12 opacity-80" color="#ff4126" />
              <Sparkle className="absolute -bottom-4 right-14 h-10 w-10 opacity-60" color="#b88a1f" />
              <h2 className="font-heading text-3xl font-extrabold tracking-tight md:text-5xl">
                Ship trustable data <span className="text-accent">today.</span>
              </h2>
              <p className="mx-auto mt-4 max-w-xl font-body text-cream/70">
                Get the full pipeline running in under a minute. No accounts, no API keys required
                to start.
              </p>
              <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
                <Link
                  href="/docs/quickstart"
                  className="inline-flex items-center gap-2 rounded-full bg-accent px-7 py-3.5 font-body font-semibold text-white shadow transition-transform hover:-translate-y-0.5"
                >
                  Start the quickstart →
                </Link>
                <Link
                  href="/docs/overview"
                  className="inline-flex items-center gap-2 rounded-full border border-cream/30 px-7 py-3.5 font-body font-semibold text-cream transition-colors hover:border-cream"
                >
                  Read the docs
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
