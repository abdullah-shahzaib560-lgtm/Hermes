import { Link, useLocation } from 'react-router-dom';
import { useState } from 'react';

const sections = [
  { label: 'Home', path: '/' },
  { label: 'Getting Started', path: '/docs/getting-started' },
  {
    label: 'Hermes SDK',
    children: [
      { label: 'Hermes Class', path: '/docs/hermes' },
      { label: 'Data Cache', path: '/docs/cache' },
      { label: 'Country Data', path: '/docs/countries' },
      { label: 'Data Export', path: '/docs/export' },
      {
        label: 'Connectors',
        children: [
          { label: 'World Bank', path: '/docs/world-bank' },
          { label: 'IMF', path: '/docs/imf' },
          { label: 'GDELT', path: '/docs/gdelt' },
          { label: 'OpenSanctions', path: '/docs/opensanctions' },
          { label: 'HDX CPI', path: '/docs/hdx-cpi' },
        ],
      },
      { label: 'Canonical Schemas', path: '/docs/schemas' },
    ],
  },
  {
    label: 'Features Pipeline',
    children: [
      { label: 'Features API', path: '/docs/features' },
    ],
  },
];

function SidebarItem({ item, depth = 0 }) {
  const location = useLocation();
  const [open, setOpen] = useState(depth < 2);

  if (item.children) {
    return (
      <div>
        <button
          onClick={() => setOpen(!open)}
          className="w-full flex items-center gap-2 px-3 py-1.5 text-sm font-medium hover:bg-black hover:text-white transition-colors"
          style={{ paddingLeft: `${12 + depth * 16}px` }}
        >
          <span className="text-xs">{open ? '▾' : '▸'}</span>
          {item.label}
        </button>
        {open && item.children.map((child, i) => (
          <SidebarItem key={i} item={child} depth={depth + 1} />
        ))}
      </div>
    );
  }

  const isActive = location.pathname === item.path;
  return (
    <Link
      to={item.path}
      className={`block px-3 py-1.5 text-sm border-l-2 transition-colors ${
        isActive
          ? 'border-black bg-black text-white font-medium'
          : 'border-transparent hover:border-black hover:bg-gray-100'
      }`}
      style={{ paddingLeft: `${12 + depth * 16}px` }}
    >
      {item.label}
    </Link>
  );
}

export default function Sidebar() {
  return (
    <aside className="w-64 min-w-64 border-r border-black h-full overflow-y-auto bg-white">
      <div className="p-4 border-b border-black">
        <Link to="/" className="text-lg font-bold tracking-tight hover:underline">
          Hermes Docs
        </Link>
      </div>
      <nav className="py-2">
        {sections.map((section, i) => (
          <SidebarItem key={i} item={section} />
        ))}
      </nav>
    </aside>
  );
}
