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
    <div className="relative overflow-hidden rounded-2xl border border-line bg-white text-black shadow-card">
      <div className="flex items-center justify-between border-b border-line px-4 py-2.5 bg-cream-soft/60">
        <div className="flex items-center gap-1.5">
          <span className="h-2.5 w-2.5 rounded-full bg-accent/80" />
          <span className="h-2.5 w-2.5 rounded-full bg-line" />
          <span className="h-2.5 w-2.5 rounded-full bg-line" />
        </div>
        <div className="flex items-center gap-3">
          {title && <span className="font-mono text-xs text-black/60">{title}</span>}
          <button
            onClick={copy}
            className="rounded-md px-2 py-0.5 font-mono text-[11px] text-black/60 transition-colors hover:bg-accent/10 hover:text-accent"
          >
            {copied ? "copied ✓" : "copy"}
          </button>
        </div>
      </div>
      <pre className="overflow-x-auto p-4 text-[13px] leading-relaxed text-black">
        <code>{code}</code>
      </pre>
    </div>
  );
}
