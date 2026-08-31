import Link from "next/link";
import { Plant, WobbleCircle } from "./Doodle";

export function Footer() {
  const cols = [
    {
      title: "Docs",
      links: [
        { label: "Overview", href: "/docs/overview" },
        { label: "Quickstart", href: "/docs/quickstart" },
        { label: "Connectors", href: "/docs/connectors" },
        { label: "Features", href: "/docs/features" },
        { label: "API Reference", href: "/docs/api-reference" },
      ],
    },
    {
      title: "Project",
      links: [
        { label: "Roadmap", href: "/docs/roadmap" },
        { label: "GitHub", href: "https://github.com/ryomenhaider/Hermes" },
        { label: "PyPI", href: "https://pypi.org/project/hermes-plt/" },
        { label: "License", href: "/docs/overview#license" },
      ],
    },
  ];

  return (
    <footer className="relative mt-auto overflow-hidden border-t border-line/70 bg-cream-soft">
      <div className="pointer-events-none absolute -right-10 -top-8 opacity-60">
        <Plant className="h-40 w-32" color="#1f5f4b" />
      </div>
      <div className="pointer-events-none absolute -left-6 top-10 opacity-40">
        <WobbleCircle className="h-28 w-28" color="#ff4126" />
      </div>

      <div className="relative mx-auto max-w-6xl px-6 py-14">
        <div className="grid gap-10 md:grid-cols-[1.5fr_1fr_1fr]">
          <div>
            <div className="mb-4 flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-ink text-cream">
                <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" aria-hidden="true">
                  <path
                    d="M12 4C14.5 7 15.5 9 15.5 12C15.5 15 14 18.5 12 20C10 18.5 8.5 15 8.5 12C8.5 9 9.5 7 12 4Z"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    strokeLinejoin="round"
                  />
                  <path d="M4 12H20" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                </svg>
              </span>
              <span className="font-heading text-xl font-bold">Hermes</span>
            </div>
            <p className="max-w-xs font-body text-sm leading-relaxed text-ink-soft">
              The Data Engine for Python. Acquire, validate, normalize and serve intelligence
              datasets with provenance baked in.
            </p>
          </div>

          {cols.map((col) => (
            <div key={col.title}>
              <h3 className="font-heading text-base font-bold">{col.title}</h3>
              <ul className="mt-4 space-y-3">
                {col.links.map((l) => (
                  <li key={l.label}>
                    <Link
                      href={l.href}
                      target={l.href.startsWith("http") ? "_blank" : undefined}
                      rel={l.href.startsWith("http") ? "noopener noreferrer" : undefined}
                      className="font-body text-sm text-ink-soft transition-colors hover:text-accent"
                    >
                      {l.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 flex flex-col items-start justify-between gap-3 border-t border-line/70 pt-6 sm:flex-row sm:items-center">
          <p className="font-body text-xs text-ink-soft">
            Hermes Non-Commercial License · Built by Haider Ali
          </p>
          <a
            href="https://pypi.org/project/hermes-plt/"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-full border border-line px-4 py-1.5 font-mono text-xs font-medium text-ink-soft transition-colors hover:border-accent hover:text-accent"
          >
            pip install hermes-plt
          </a>
        </div>
      </div>
    </footer>
  );
}
