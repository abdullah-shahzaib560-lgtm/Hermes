"use client";

import { useState } from "react";

export function CodeBlock({ code, title }: { code: string; title?: string }) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch {
      /* clipboard unavailable */
    }
  }

  return (
    <div className="relative overflow-hidden rounded-2xl border border-ink/10 bg-ink text-cream shadow-card">
      <div className="flex items-center justify-between border-b border-cream/10 px-4 py-2.5">
        <div className="flex items-center gap-1.5">
          <span className="h-2.5 w-2.5 rounded-full bg-accent/70" />
          <span className="h-2.5 w-2.5 rounded-full bg-cream/30" />
          <span className="h-2.5 w-2.5 rounded-full bg-cream/30" />
        </div>
        <div className="flex items-center gap-3">
          {title && <span className="font-mono text-xs text-cream/60">{title}</span>}
          <button
            onClick={copy}
            className="rounded-md px-2 py-0.5 font-mono text-[11px] text-cream/60 transition-colors hover:bg-cream/10 hover:text-cream"
          >
            {copied ? "copied ✓" : "copy"}
          </button>
        </div>
      </div>
      <pre className="overflow-x-auto p-4 text-[13px] leading-relaxed">
        <code>{code}</code>
      </pre>
    </div>
  );
}
