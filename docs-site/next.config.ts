import type { NextConfig } from "next";

const nextConfig: NextConfig = {
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
