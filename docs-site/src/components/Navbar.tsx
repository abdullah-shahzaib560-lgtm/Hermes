import Link from "next/link";
import { Squiggle } from "./Doodle";
import { Logo } from "./Logo";

export function Navbar() {
  const links = [
    { label: "Docs", href: "/docs/overview" },
    { label: "Quickstart", href: "/docs/quickstart" },
    { label: "API", href: "/docs/api-reference" },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-line/70 bg-cream/85 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Logo />
        <nav className="hidden items-center gap-8 md:flex">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="relative font-body text-[15px] font-semibold text-ink-soft transition-colors hover:text-ink"
            >
              {l.label}
              <span className="absolute -bottom-1 left-0 h-[3px] w-0 rounded-full bg-accent transition-all duration-300 hover:w-full" />
            </Link>
          ))}
        </nav>
        <Link
          href="/docs/quickstart"
          className="group relative inline-flex items-center gap-2 rounded-full bg-ink px-5 py-2.5 font-body text-sm font-semibold text-cream shadow-soft transition-all hover:-translate-y-0.5"
        >
          Get Started
          <span className="transition-transform group-hover:translate-x-1">→</span>
          <Squiggle className="pointer-events-none absolute -bottom-2 left-4 w-16" color="#ff4126" strokeWidth={3} />
        </Link>
      </div>
    </header>
  );
}
