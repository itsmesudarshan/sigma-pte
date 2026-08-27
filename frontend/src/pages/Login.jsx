import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mail, Lock, AlertCircle } from 'lucide-react';
import { authApi } from '../api/authClient';
import { useAuth } from '../context/AuthContext';

const ALLOWED_DOMAIN_DISPLAY = 'Gmail, Yahoo, or Outlook';

function isAllowedDomain(email) {
  const domain = email.split('@')[1]?.toLowerCase();
  const allowed = ['gmail.com', 'googlemail.com', 'yahoo.com', 'ymail.com', 'rocketmail.com', 'outlook.com', 'hotmail.com', 'live.com', 'msn.com'];
  return allowed.includes(domain);
}

export default function Login() {
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setError('');

    if (mode === 'signup' && !isAllowedDomain(email)) {
      setError(`Only ${ALLOWED_DOMAIN_DISPLAY} email addresses are allowed.`);
      return;
    }

    setSubmitting(true);
    try {
      const data = mode === 'signup'
        ? await authApi.signup(email, password)
        : await authApi.login(email, password);
      login(data.token, data.user);
      navigate('/');
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--paper)', padding: 20 }}>
      <div style={{ width: '100%', maxWidth: 380 }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: 28, fontWeight: 700, color: 'var(--ink)' }}>Prepwise</div>
          <div style={{ fontSize: 12, color: 'var(--text-muted)', letterSpacing: '0.06em', textTransform: 'uppercase', marginTop: 2 }}>PTE Academic Prep</div>
        </div>

        <div style={{ background: 'var(--paper-raised)', border: '1px solid var(--line)', borderRadius: 'var(--radius-lg)', padding: 28, boxShadow: 'var(--shadow-raised)' }}>
          <div style={{ display: 'flex', gap: 4, marginBottom: 22, background: 'var(--paper)', borderRadius: 999, padding: 4 }}>
            {['login', 'signup'].map((m) => (
              <button
                key={m}
                onClick={() => { setMode(m); setError(''); }}
                style={{
                  flex: 1, padding: '8px 0', borderRadius: 999, border: 'none', fontSize: 13, fontWeight: 700,
                  background: mode === m ? 'var(--focus)' : 'transparent',
                  color: mode === m ? '#fff' : 'var(--text-secondary)',
                }}
              >
                {m === 'login' ? 'Log In' : 'Sign Up'}
              </button>
            ))}
          </div>

          {mode === 'signup' && (
            <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 16, padding: '10px 12px', background: 'var(--focus-soft)', borderRadius: 'var(--radius-sm)' }}>
              Only {ALLOWED_DOMAIN_DISPLAY} email addresses can sign up.
            </p>
          )}

          <form onSubmit={submit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div style={{ position: 'relative' }}>
              <Mail size={15} style={{ position: 'absolute', left: 12, top: 13, color: 'var(--text-muted)' }} />
              <input
                type="email"
                required
                placeholder="you@gmail.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={{ width: '100%', padding: '11px 12px 11px 36px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--line-strong)', fontSize: 14 }}
              />
            </div>

            <div style={{ position: 'relative' }}>
              <Lock size={15} style={{ position: 'absolute', left: 12, top: 13, color: 'var(--text-muted)' }} />
              <input
                type="password"
                required
                minLength={6}
                placeholder="Password (min 6 characters)"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ width: '100%', padding: '11px 12px 11px 36px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--line-strong)', fontSize: 14 }}
              />
            </div>

            {error && (
              <div style={{ display: 'flex', gap: 8, alignItems: 'flex-start', padding: '10px 12px', background: 'var(--error-soft)', borderRadius: 'var(--radius-sm)' }}>
                <AlertCircle size={15} color="var(--error)" style={{ flexShrink: 0, marginTop: 1 }} />
                <span style={{ fontSize: 12, color: 'var(--error)' }}>{error}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={submitting}
              style={{ padding: '12px 0', borderRadius: 999, border: 'none', background: 'var(--focus)', color: '#fff', fontSize: 14, fontWeight: 700, opacity: submitting ? 0.6 : 1, marginTop: 6 }}
            >
              {submitting ? 'Please wait…' : mode === 'login' ? 'Log In' : 'Create Account'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
