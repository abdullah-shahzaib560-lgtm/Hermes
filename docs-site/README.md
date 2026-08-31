# Hermes Docs Site

The official marketing + documentation website for **Hermes — The Data Engine for Python**,
built with Next.js (App Router), Tailwind CSS v4 and TypeScript.

- Landing page at `/` — premium hero with the `pip install hermes-plt` installer and a
  "Documentation" CTA.
- Docs at `/docs/*` (Overview, Quickstart, Connectors, Features, API Reference, Roadmap) with a
  sidebar layout.
- `/documentations` permanently redirects to `/docs/overview`.

## Design

- Background: `#f6f5ef` (cream) with near-black `#0a0a07` text — high contrast, no brown/gray body tones
- Accent: `#ff4126` orange-red, matched to the `Hermes.png` logo mark
- Doodle-style SVG illustrations (hand-drawn strokes, wobble circles, squiggles, sparkles)
- Headings: `font-heading` (JA JayaGiri Sans stack)
- Body: `font-body` (Nunito Sans)
- Logo & favicon: `public/Hermes.png`

> **Font note:** *JA JayaGiri Sans* is a commercial font and is not bundled. The heading stack
> in `src/app/globals.css` lists `"JA JayaGiri Sans"` first (used when you own the license /
> install it locally) and falls back to the bundled rounded display font so the site looks right
> out of the box. To use the real font, add your licensed `@font-face` and it will take
> precedence automatically.

## Getting started

```bash
npm install
npm run dev        # http://localhost:3000
```

Production build:

```bash
npm run build
npm run start
```

## Structure

```
src/
  app/
    page.tsx              # landing page
    layout.tsx            # fonts + global layout
    docs/
      layout.tsx          # sidebar + content shell
      overview|quickstart|connectors|features|api-reference|roadmap/
  components/
    Navbar.tsx  Footer.tsx  DocsSidebar.tsx  CodeBlock.tsx
    Doodle.tsx            # hand-drawn SVG illustrations
    Doc.tsx               # reusable doc primitives (H2, P, Callout, Table…)
  lib/docs.ts             # sidebar navigation data
```
