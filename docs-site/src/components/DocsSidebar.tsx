"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { docsNav } from "@/lib/docs";

export function DocsSidebar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  const currentSection = docsNav.find((s) =>
    s.links.some((l) => pathname.includes(l.href))
  );

  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={() => setOpen((o) => !o)}
        className="mx-auto mt-6 flex w-[calc(100%-3rem)] items-center justify-center gap-2 rounded-xl border border-line bg-white/60 px-4 py-2.5 font-body text-sm font-semibold shadow-card md:hidden"
      >
        {open ? "Close" : "Menu"} · {currentSection?.title ?? "Docs"}
      </button>

      <aside
        className={`${open ? "block" : "hidden"} md:block md:h-[calc(100vh-65px)] md:sticky md:top-[65px] md:overflow-y-auto md:w-64 md:shrink-0 md:border-r md:border-line/60`}
      >
        <nav className="px-4 py-6 md:px-6 md:py-10">
          <div className="mb-8 hidden px-2 font-heading text-xs font-bold uppercase tracking-[0.2em] text-ink-soft/70 md:block">
            Hermes Docs
          </div>

          {docsNav.map((section) => {
            const active = section.links.some((l) => pathname.includes(l.href));
            return (
              <div key={section.title} className="mb-8">
                <div
                  className={`px-2 font-heading text-sm font-bold ${active ? "text-accent" : "text-ink"}`}
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
                          onClick={() => setOpen(false)}
                          className={`flex items-center gap-2 rounded-xl px-3 py-2 font-body text-[15px] font-medium transition-colors ${
                            isActive
                              ? "bg-ink text-cream shadow-soft"
                              : "text-ink hover:bg-cream-soft"
                          }`}
                        >
                          <span
                            className={`h-1.5 w-1.5 rounded-full ${isActive ? "bg-accent" : "bg-line"}`}
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

          <Link
            href="/"
            className="mt-4 flex items-center gap-2 rounded-xl border border-line px-3 py-2 font-body text-sm text-ink transition-colors hover:border-ink"
          >
            <span>←</span> Back to home
          </Link>
        </nav>
      </aside>
    </>
  );
}
