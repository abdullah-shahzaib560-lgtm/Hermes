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
        <div className="flex items-center gap-2">
          <a
            href="https://discord.gg/KrxwaR3Uu"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden items-center gap-2 rounded-full border-2 border-black/15 px-4 py-2.5 font-body text-sm font-semibold text-black transition-colors hover:border-accent hover:text-accent sm:inline-flex"
          >
            <DiscordIcon className="h-4 w-4" />
            Join Discord
          </a>
          <Link
            href="/docs/quickstart"
            className="group relative inline-flex items-center gap-2 rounded-full bg-accent px-5 py-2.5 font-body text-sm font-semibold text-white shadow-soft transition-all hover:-translate-y-0.5 hover:bg-accent-dark"
          >
            Get Started
            <span className="transition-transform group-hover:translate-x-1">→</span>
            <Squiggle className="pointer-events-none absolute -bottom-2 left-4 w-16" color="#ff4328" strokeWidth={3} />
          </Link>
        </div>
      </div>
    </header>
  );
}

function DiscordIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M20.317 4.37a19.79 19.79 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z" />
    </svg>
  );
}
