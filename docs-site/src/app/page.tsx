import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { CodeBlock } from "@/components/CodeBlock";
import { Arrow, Sparkle, Spiral, Squiggle, WobbleCircle, Plant } from "@/components/Doodle";

const valueProps = [
  {
    title: "Acquire",
    body: "Pull data from APIs, CSVs, JSON and public datasets through a unified connector layer with retries, rate limiting and a shared cache built in.",
    color: "#ff4328",
    icon: "⇣",
  },
  {
    title: "Validate",
    body: "Check integrity, schema and provenance before anything dirty ever reaches a dataset. Catch bad data at the source, not downstream.",
    color: "#ff4328",
    icon: "✓",
  },
  {
    title: "Normalize",
    body: "Bring messy sources into one canonical shape with consistent codes, units and timestamps across every connector.",
    color: "#ff4328",
    icon: "≈",
  },
  {
    title: "Serve",
    body: "Query, export and feed features into models — lineage tracked every step of the way, ready for ML and analytics.",
    color: "#ff4328",
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
            <Plant className="absolute left-8 top-40 hidden h-28 w-24 opacity-50 sm:block" color="#ff4328" />
            <Sparkle className="absolute right-4 top-20 h-10 w-10 opacity-70 sm:right-16 sm:top-32 sm:h-16 sm:w-16" color="#ff4328" />
            <Spiral className="absolute right-1/3 top-16 hidden h-14 w-14 opacity-40 sm:block" color="#ff4328" />
            <WobbleCircle className="absolute bottom-10 left-1/2 h-16 w-16 opacity-50 sm:h-24 sm:w-24" color="#ff4328" />
            <Sparkle className="absolute bottom-24 right-6 h-8 w-8 opacity-50 sm:right-24 sm:h-12 sm:w-12" color="#ff4328" />
          </div>

          <div className="relative mx-auto max-w-6xl px-4 pt-16 pb-12 text-center sm:px-6 sm:pt-24 sm:pb-20 md:pt-36 md:pb-28">
            <div className="relative mx-auto mb-6 inline-flex items-center gap-2 rounded-full border border-line bg-white/60 px-3 py-1.5 font-body text-xs font-medium text-ink-soft backdrop-blur sm:mb-8 sm:px-4 sm:text-sm">
              <Sparkle className="h-3.5 w-3.5 sm:h-4 sm:w-4" color="#ff4328" strokeWidth={4} />
              The Data Engine for Python
              <Sparkle className="h-3.5 w-3.5 sm:h-4 sm:w-4" color="#ff4328" strokeWidth={4} />
            </div>

            <h1 className="relative mx-auto max-w-4xl font-heading text-4xl font-extrabold leading-[1.05] tracking-tight text-ink sm:text-5xl md:text-6xl lg:text-7xl">
              Intelligence data,
              <br />
              <span className="relative inline-block">
                end to end.
                <Squiggle className="absolute -bottom-2 left-0 w-full sm:-bottom-3" color="#ff4328" strokeWidth={5} />
              </span>
            </h1>

            <p className="relative mx-auto mt-6 max-w-2xl font-body text-base leading-relaxed text-ink-soft sm:mt-10 sm:text-lg md:text-xl">
              Hermes is a foundational intelligence data platform. Acquire, validate, normalize,
              store and serve datasets — with provenance baked into every row.
            </p>

            {/* Install + docs */}
            <div className="relative mx-auto mt-8 max-w-xl sm:mt-12">
              <CodeBlock
                code="pip install hermes-plt"
                title="terminal"
              />
              <Arrow className="pointer-events-none absolute -top-8 -right-12 hidden h-16 w-24 md:block" color="#ff4328" />
            </div>

            <div className="relative mt-6 flex flex-col items-center justify-center gap-3 sm:mt-8 sm:flex-row sm:gap-4">
              <Link
                href="/docs/overview"
                className="group relative inline-flex w-full items-center justify-center gap-2 rounded-full bg-accent px-6 py-3 font-body text-sm font-semibold text-white shadow-soft transition-all hover:-translate-y-0.5 hover:bg-accent-dark sm:w-auto sm:px-7 sm:py-3.5 sm:text-base"
              >
                Documentation
                <span className="transition-transform group-hover:translate-x-1">→</span>
              </Link>
              <Link
                href="/docs/quickstart"
                className="inline-flex w-full items-center justify-center gap-2 rounded-full border-2 border-black/15 px-6 py-3 font-body text-sm font-semibold text-black transition-colors hover:border-black sm:w-auto sm:px-7 sm:py-3.5 sm:text-base"
              >
                Read the quickstart
              </Link>
            </div>

            <p className="relative mt-6 inline-block font-mono text-xs text-ink-soft sm:mt-8">
              Python 3.11+ · pandas, polars, arrow & duckdb friendly
            </p>
          </div>

          {/* stats bar */}
          <div className="relative mx-auto max-w-5xl px-4 pb-12 sm:px-6 sm:pb-16">
            <div className="grid grid-cols-2 gap-px overflow-hidden rounded-3xl border border-line bg-line shadow-card sm:grid-cols-4">
              {stats.map((s) => (
                <div key={s.label} className="bg-cream/90 px-4 py-4 text-center sm:px-6 sm:py-6">
                  <div className="font-heading text-2xl font-extrabold text-ink sm:text-3xl md:text-4xl">{s.value}</div>
                  <div className="mt-1 font-body text-xs text-ink-soft sm:text-sm">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ------- VALUE PROPS ------- */}
        <section className="relative border-t border-line/60 bg-cream-soft/60 py-14 md:py-20">
          <div className="mx-auto max-w-6xl px-4 sm:px-6">
            <div className="mb-10 flex flex-col items-center text-center md:mb-12">
              <h2 className="font-heading text-2xl font-extrabold tracking-tight sm:text-3xl md:text-4xl">
                One pipeline. <span className="hairline text-accent">Every source.</span>
              </h2>
              <p className="mt-4 max-w-2xl font-body text-ink-soft">
                From raw fetch to production-ready features in a single, repeatable pipeline.
              </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 sm:gap-5 lg:grid-cols-4">
              {valueProps.map((v, i) => (
                <div
                  key={v.title}
                  className="group relative rounded-3xl border border-line bg-cream p-6 shadow-card transition-all hover:-translate-y-1 sm:p-7"
                >
                  <div className="mb-6 flex items-center justify-between">
                    <span
                      className="flex h-10 w-10 items-center justify-center rounded-2xl text-lg font-bold sm:h-11 sm:w-11 sm:text-xl"
                      style={{ backgroundColor: `color-mix(in srgb, ${v.color} 14%, transparent)`, color: v.color }}
                    >
                      {v.icon}
                    </span>
                    <span className="font-heading text-sm font-bold text-ink/25">0{i + 1}</span>
                  </div>
                  <h3 className="font-heading text-lg font-bold sm:text-xl">{v.title}</h3>
                  <p className="mt-2 font-body text-sm leading-relaxed text-ink-soft">{v.body}</p>
                  <Squiggle className="mt-5 w-20 opacity-60" color={v.color} strokeWidth={4} />
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ------- FEATURES ------- */}
        <section className="relative overflow-hidden py-14 md:py-20">
          <div className="pointer-events-none absolute right-0 top-10 opacity-40">
            <Plant className="h-32 w-24 sm:h-36 sm:w-28" color="#ff4328" />
          </div>
          <div className="mx-auto max-w-6xl px-4 sm:px-6">
            <div className="grid items-center gap-10 lg:grid-cols-2 lg:gap-12">
              <div>
                <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-line bg-white/60 px-3 py-1 font-body text-xs font-bold uppercase tracking-wider text-accent">
                  Built for trust
                </div>
                <h2 className="font-heading text-2xl font-extrabold tracking-tight sm:text-3xl md:text-4xl">
                  Provenance you can <span className="hairline text-accent">point at.</span>
                </h2>
                <p className="mt-4 max-w-lg font-body leading-relaxed text-black">
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
                    <li key={item} className="flex items-start gap-3 font-body text-black">
                      <Sparkle className="mt-1 h-4 w-4 shrink-0" color="#ff4328" strokeWidth={4} />
                      <span dangerouslySetInnerHTML={{ __html: item }} />
                    </li>
                  ))}
                </ul>
                <Link
                  href="/docs/features"
                  className="group mt-8 inline-flex items-center gap-2 rounded-full border-2 border-black/15 px-6 py-3 font-body font-semibold transition-colors hover:border-black"
                >
                  Explore the feature engine
                  <span className="transition-transform group-hover:translate-x-1">→</span>
                </Link>
              </div>

              <div className="relative">
                <WobbleCircle className="absolute -left-6 -top-6 hidden h-20 w-20 opacity-60 sm:block sm:h-24 sm:w-24" color="#ff4328" />
                <div className="relative overflow-hidden rounded-3xl border border-line bg-white p-5 shadow-soft sm:p-8">
                  <div className="mb-6 flex items-center gap-2">
                    <span className="h-3 w-3 rounded-full bg-accent" />
                    <span className="h-3 w-3 rounded-full bg-line" />
                    <span className="h-3 w-3 rounded-full bg-line" />
                    <span className="ml-3 font-mono text-xs text-black/60">hermes.py</span>
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
                  <Sparkle className="absolute -bottom-3 -right-3 h-12 w-12 opacity-60 sm:-bottom-4 sm:-right-4 sm:h-14 sm:w-14" color="#ff4328" />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ------- CTA ------- */}
        <section className="relative border-t border-line/60 py-14 md:py-20">
          <div className="mx-auto max-w-4xl px-4 text-center sm:px-6">
            <div className="relative overflow-hidden rounded-[2rem] border border-line bg-white p-8 text-black shadow-soft sm:rounded-[2.5rem] sm:p-10 md:p-16">
              <Sparkle className="absolute -top-6 left-10 h-10 w-10 opacity-80 sm:h-12 sm:w-12" color="#ff4328" />
              <Sparkle className="absolute -bottom-4 right-14 h-8 w-8 opacity-60 sm:h-10 sm:w-10" color="#ff4328" />
              <h2 className="font-heading text-2xl font-extrabold tracking-tight sm:text-3xl md:text-5xl">
                Ship trustable data <span className="text-accent">today.</span>
              </h2>
              <p className="mx-auto mt-4 max-w-xl font-body text-sm text-black/70 sm:text-base">
                Get the full pipeline running in under a minute. No accounts, no API keys required
                to start.
              </p>
              <div className="mt-7 flex flex-col items-center justify-center gap-3 sm:mt-8 sm:flex-row sm:gap-4">
                <Link
                  href="/docs/quickstart"
                  className="inline-flex w-full items-center justify-center gap-2 rounded-full bg-accent px-7 py-3.5 font-body font-semibold text-white shadow transition-transform hover:-translate-y-0.5 hover:bg-accent-dark sm:w-auto"
                >
                  Start the quickstart →
                </Link>
                <Link
                  href="/docs/overview"
                  className="inline-flex w-full items-center justify-center gap-2 rounded-full border-2 border-black/15 px-7 py-3.5 font-body font-semibold text-black transition-colors hover:border-black sm:w-auto"
                >
                  Read the docs
                </Link>
              </div>
              <div className="mt-6 flex items-center justify-center gap-3 sm:gap-4">
                <a
                  href="https://discord.gg/KrxwaR3Uu"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 rounded-full bg-black px-5 py-2.5 font-body text-sm font-semibold text-white transition-transform hover:-translate-y-0.5"
                >
                  <DiscordIcon className="h-4 w-4" />
                  Join Discord
                </a>
                <a
                  href="https://github.com/ryomenhaider/Hermes"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 rounded-full bg-black px-5 py-2.5 font-body text-sm font-semibold text-white transition-transform hover:-translate-y-0.5"
                >
                  <GithubIcon className="h-4 w-4" />
                  GitHub
                </a>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}

function DiscordIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M20.317 4.37a19.79 19.79 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z" />
    </svg>
  );
}

function GithubIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
    </svg>
  );
}
