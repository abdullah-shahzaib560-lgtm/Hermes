"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { docsNav } from "@/lib/docs";

export function DocsSidebar() {
  const pathname = usePathname();

  const nav = (
    <nav className="flex h-full flex-col px-4 py-6 md:px-6 md:py-10">
      <div className="mb-8 hidden px-2 font-heading text-xs font-bold uppercase tracking-[0.2em] text-black/50 md:block">
        Hermes Docs
      </div>

      <div className="flex-1">
        {docsNav.map((section) => {
          const active = section.links.some((l) => pathname.includes(l.href));
          return (
            <div key={section.title} className="mb-8">
              <div
                className={`px-2 font-heading text-sm font-bold ${active ? "text-accent" : "text-black"}`}
              >
                {section.title}
              </div>
              <ul className="mt-2 space-y-0.5">
                {section.links.map((link) => {
                  const isActive =
                    pathname === link.href ||
                    (link.href !== "/docs/overview" && pathname.startsWith(link.href));
                  return (
                    <li key={link.href}>
                      <Link
                        href={link.href}
                        className={`flex items-center gap-2 rounded-xl px-3 py-2 font-body text-[15px] font-medium transition-colors ${
                          isActive
                            ? "bg-accent text-white shadow-soft"
                            : "text-black hover:bg-cream-soft"
                        }`}
                      >
                        <span
                          className={`h-1.5 w-1.5 rounded-full ${isActive ? "bg-white/80" : "bg-line"}`}
                        />
                        {link.title}
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </div>
          );
        })}
      </div>

      <Link
        href="/"
        className="mt-4 flex items-center gap-2 rounded-xl border border-line px-3 py-2 font-body text-sm text-black transition-colors hover:border-ink"
      >
        <span>←</span> Back to home
      </Link>
    </nav>
  );

  // The mobile hamburger in the Navbar already lists every docs page, so the
  // sidebar is only shown as a sticky column on md+ screens. No separate
  // mobile drawer/toggle here to avoid a second overlapping drawer.
  return (
    <aside className="sticky top-[65px] hidden h-[calc(100vh-65px)] w-64 shrink-0 overflow-y-auto border-r border-line/60 md:block">
      {nav}
    </aside>
  );
}
