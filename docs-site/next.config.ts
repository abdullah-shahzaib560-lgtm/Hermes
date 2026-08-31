import type { NextConfig } from "next";
import { homedir, tmpdir } from "node:os";
import { join, isAbsolute } from "node:path";
import { mkdirSync, existsSync } from "node:fs";

function resolveDistDir(): string {
  const forced = process.env.HERMES_BUILD_DIR;
  if (forced && forced.trim()) return forced.trim();

  // The project lives on a slow/networked mount (/mnt/...). Turbopack's dev cache
  // corrupts there, so keep the build/dist cache on local disk instead.
  const localCandidates = [join(homedir(), ".cache", "hermes-plt-next"), join(tmpdir(), "hermes-plt-next")];

  for (const dir of localCandidates) {
    try {
      mkdirSync(dir, { recursive: true });
      if (existsSync(dir)) return dir;
    } catch {
      /* try next candidate */
    }
  }
  return ".next";
}

const distDir = resolveDistDir();

const nextConfig: NextConfig = {
  distDir: isAbsolute(distDir) ? distDir : join(process.cwd(), distDir),
  async redirects() {
    return [
      {
        source: "/documentations",
        destination: "/docs/overview",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
