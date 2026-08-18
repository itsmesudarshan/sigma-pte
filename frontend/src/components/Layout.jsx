import { NavLink, Outlet } from 'react-router-dom';
import { LayoutDashboard, BookOpen, PenLine, Library } from 'lucide-react';

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/reading', label: 'Reading', icon: BookOpen },
  { to: '/writing', label: 'Writing', icon: PenLine },
  { to: '/question-bank', label: 'Question Bank', icon: Library },
];

export default function Layout() {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <aside
        style={{
          width: 232,
          borderRight: '1px solid var(--line)',
          background: 'var(--paper-raised)',
          padding: '28px 16px',
          flexShrink: 0,
        }}
      >
        <div style={{ padding: '0 12px', marginBottom: 36 }}>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: 22, fontWeight: 700, color: 'var(--ink)' }}>
            Prepwise
          </div>
          <div style={{ fontSize: 11, color: 'var(--text-muted)', letterSpacing: '0.06em', textTransform: 'uppercase', marginTop: 2 }}>
            PTE Academic Prep
          </div>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          {navItems.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              style={({ isActive }) => ({
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                padding: '10px 12px',
                borderRadius: 'var(--radius-sm)',
                fontSize: 14,
                fontWeight: 600,
                color: isActive ? 'var(--focus)' : 'var(--text-secondary)',
                background: isActive ? 'var(--focus-soft)' : 'transparent',
              })}
            >
              <Icon size={17} strokeWidth={2.2} />
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <main style={{ flex: 1, padding: '32px 40px', maxWidth: 1080 }}>
        <Outlet />
      </main>
    </div>
  );
}
