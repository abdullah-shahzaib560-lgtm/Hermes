export type DocLink = {
  title: string;
  href: string;
  description?: string;
};

export type DocSection = {
  title: string;
  links: DocLink[];
};

export const docsNav: DocSection[] = [
  {
    title: "Getting Started",
    links: [
      { title: "Overview", href: "/docs/overview", description: "What Hermes is and why it matters" },
      { title: "Quickstart", href: "/docs/quickstart", description: "Install and run your first pipeline" },
    ],
  },
  {
    title: "Core Concepts",
    links: [
      { title: "Connectors", href: "/docs/connectors", description: "Every source, one contract" },
      { title: "Features", href: "/docs/features", description: "Country risk & financial feature engine" },
    ],
  },
  {
    title: "Reference",
    links: [
      { title: "API Reference", href: "/docs/api-reference", description: "The Hermes facade & core objects" },
      { title: "Roadmap", href: "/docs/roadmap", description: "Where the platform is headed" },
    ],
  },
];
