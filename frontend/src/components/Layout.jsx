import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { LayoutDashboard, BookOpen, PenLine, Mic, Headphones, ClipboardCheck, LogOut, Sun, Moon } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/reading', label: 'Reading', icon: BookOpen },
  { to: '/writing', label: 'Writing', icon: PenLine },
  { to: '/speaking', label: 'Speaking', icon: Mic },
  { to: '/listening', label: 'Listening', icon: Headphones },
  { to: '/mock-test', label: 'Mock Test', icon: ClipboardCheck },
];

export default function Layout() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <aside style={{ width: 232, borderRight: '1px solid var(--line)', background: 'var(--paper-raised)', padding: '28px 16px', flexShrink: 0, display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '0 12px', marginBottom: 36 }}>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: 22, fontWeight: 700, color: 'var(--ink)' }}>Prepwise</div>
          <div style={{ fontSize: 11, color: 'var(--text-muted)', letterSpacing: '0.06em', textTransform: 'uppercase', marginTop: 2 }}>PTE Academic Prep</div>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: 4, flex: 1 }}>
          {navItems.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              style={({ isActive }) => ({
                display: 'flex', alignItems: 'center', gap: 10, padding: '10px 12px', borderRadius: 'var(--radius-sm)',
                fontSize: 14, fontWeight: 600, color: isActive ? 'var(--focus)' : 'var(--text-secondary)',
                background: isActive ? 'var(--focus-soft)' : 'transparent',
              })}
            >
              <Icon size={17} strokeWidth={2.2} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div style={{ borderTop: '1px solid var(--line)', paddingTop: 14, marginTop: 14 }}>
          <button
            onClick={toggleTheme}
            style={{ display: 'flex', alignItems: 'center', gap: 10, width: '100%', padding: '10px 12px', borderRadius: 'var(--radius-sm)', border: 'none', background: 'transparent', fontSize: 13, fontWeight: 600, color: 'var(--text-secondary)', marginBottom: 4 }}
          >
            {theme === 'dark' ? <Sun size={16} strokeWidth={2.2} /> : <Moon size={16} strokeWidth={2.2} />}
            {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
          </button>
          <p style={{ fontSize: 12, color: 'var(--text-muted)', padding: '6px 12px 10px', wordBreak: 'break-all' }}>{user?.email}</p>
          <button
            onClick={handleLogout}
            style={{ display: 'flex', alignItems: 'center', gap: 10, width: '100%', padding: '10px 12px', borderRadius: 'var(--radius-sm)', border: 'none', background: 'transparent', fontSize: 13, fontWeight: 600, color: 'var(--text-secondary)' }}
          >
            <LogOut size={16} strokeWidth={2.2} />
            Log Out
          </button>
        </div>
      </aside>

      <main style={{ flex: 1, padding: '32px 40px', maxWidth: 1080 }}>
        <Outlet />
      </main>
    </div>
  );
}
