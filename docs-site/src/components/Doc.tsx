import Link from "next/link";
import { Sparkle, Squiggle, WobbleCircle, Arrow } from "./Doodle";

export function DocTitle({ children, kicker }: { children: React.ReactNode; kicker?: string }) {
  return (
    <div className="relative mb-10 rounded-3xl border border-line bg-white p-6 shadow-card md:p-8">
      <WobbleCircle className="pointer-events-none absolute -right-3 -top-4 h-16 w-16 opacity-40" color="#ff4328" />
      {kicker && (
        <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-line bg-cream-soft/60 px-3 py-1 font-body text-xs font-bold uppercase tracking-wider text-accent">
          <Sparkle className="h-3.5 w-3.5" color="#ff4328" strokeWidth={4} />
          {kicker}
        </div>
      )}
      <h1 className="font-heading text-4xl font-extrabold tracking-tight text-black md:text-5xl">
        {children}
      </h1>
      <Squiggle className="pointer-events-none absolute -bottom-2 left-8 w-24 opacity-70" color="#ff4328" strokeWidth={4} />
    </div>
  );
}

export function H2({ children, id }: { children: React.ReactNode; id?: string }) {
  return (
    <div className="mt-14 mb-4 flex items-center gap-2">
      <h2
        id={id}
        className="flex items-center gap-3 font-heading text-2xl font-extrabold tracking-tight text-black"
      >
        {children}
        <Sparkle className="h-5 w-5 opacity-70" color="#ff4328" strokeWidth={4} />
      </h2>
    </div>
  );
}

export function P({ children }: { children: React.ReactNode }) {
  return <p className="my-4 font-body text-[16.5px] leading-relaxed text-black">{children}</p>;
}

export function Lead({ children }: { children: React.ReactNode }) {
  return (
    <p className="mb-6 text-lg font-body leading-relaxed text-black">{children}</p>
  );
}

export function List({ items }: { items: string[] }) {
  return (
    <ul className="dot-bullet my-4 space-y-2.5">
      {items.map((item) => (
        <li key={item} className="font-body text-[16.5px] text-black">
          {item}
        </li>
      ))}
    </ul>
  );
}

export function Callout({
  title,
  children,
  tone = "accent",
}: {
  title: string;
  children: React.ReactNode;
  tone?: "accent" | "cedar" | "gold";
}) {
  const map = {
    accent: { bg: "#ff4328", label: "Note" },
    cedar: { bg: "#1f5f4b", label: "Tip" },
    gold: { bg: "#b88a1f", label: "Warning" },
  };
  const t = map[tone];
  return (
    <div className="my-7 overflow-hidden rounded-2xl border border-line bg-white shadow-card">
      <div className="flex items-center gap-2 px-4 py-2.5" style={{ backgroundColor: `${t.bg}` }}>
        <Sparkle className="h-4 w-4 text-white" color="#fff" strokeWidth={4} />
        <span className="font-heading text-sm font-bold text-white">{title}</span>
      </div>
      <div className="px-5 py-4 font-body text-[15px] leading-relaxed text-black">{children}</div>
    </div>
  );
}

export function DocLink({ href, children, external }: { href: string; children: React.ReactNode; external?: boolean }) {
  return (
    <Link
      href={href}
      target={external ? "_blank" : undefined}
      rel={external ? "noopener noreferrer" : undefined}
      className="font-medium text-accent underline decoration-accent/40 underline-offset-4 transition-colors hover:text-accent-dark hover:decoration-accent"
    >
      {children}
    </Link>
  );
}

export function PrevNext({ prev, next }: { prev?: { title: string; href: string }; next?: { title: string; href: string } }) {
  return (
    <div className="mt-14 grid gap-4 border-t border-line/70 pt-8 sm:grid-cols-2">
      {prev ? (
        <Link
          href={prev.href}
          className="group relative rounded-2xl border border-line bg-white p-5 transition-all hover:-translate-y-0.5 hover:shadow-card"
        >
          <div className="font-body text-xs uppercase tracking-wider text-black/50">← Previous</div>
          <div className="mt-1 font-heading font-bold text-black group-hover:text-accent">{prev.title}</div>
          <Arrow className="pointer-events-none absolute -right-2 -bottom-2 h-8 w-12 opacity-0 transition-opacity group-hover:opacity-60" color="#ff4328" strokeWidth={3} />
        </Link>
      ) : (
        <span />
      )}
      {next ? (
        <Link
          href={next.href}
          className="group relative rounded-2xl border border-line bg-white p-5 text-right transition-all hover:-translate-y-0.5 hover:shadow-card"
        >
          <div className="font-body text-xs uppercase tracking-wider text-black/50">Next →</div>
          <div className="mt-1 font-heading font-bold text-black group-hover:text-accent">{next.title}</div>
          <Arrow className="pointer-events-none absolute -left-2 -bottom-2 h-8 w-12 rotate-180 opacity-0 transition-opacity group-hover:opacity-60" color="#ff4328" strokeWidth={3} />
        </Link>
      ) : (
        <span />
      )}
    </div>
  );
}

export function Table({ head, rows }: { head: string[]; rows: (string | React.ReactNode)[][] }) {
  return (
    <div className="my-6 overflow-x-auto rounded-2xl border border-line bg-white shadow-card">
      <table className="w-full text-left font-body text-[15px]">
        <thead>
          <tr className="border-b border-line bg-cream-soft/70">
            {head.map((h) => (
              <th key={h} className="px-4 py-3 font-heading text-sm font-bold text-black">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} className="border-b border-line/50 last:border-0">
              {row.map((cell, j) => (
                <td key={j} className="px-4 py-3 align-top text-black">
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
