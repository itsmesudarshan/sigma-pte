import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mail, Lock, AlertCircle, ShieldCheck, Sun, Moon } from 'lucide-react';
import { authApi } from '../api/authClient';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

const ALLOWED_DOMAIN_DISPLAY = 'Gmail, Yahoo, or Outlook';
const ALLOWED_DOMAINS = ['gmail.com', 'googlemail.com', 'yahoo.com', 'ymail.com', 'rocketmail.com', 'outlook.com', 'hotmail.com', 'live.com', 'msn.com'];

function isAllowedDomain(email) {
  const domain = email.split('@')[1]?.toLowerCase();
  return ALLOWED_DOMAINS.includes(domain);
}

export default function Login() {
  const [mode, setMode] = useState('login'); // 'login' | 'signup' | 'otp'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [otp, setOtp] = useState('');
  const [error, setError] = useState('');
  const [info, setInfo] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [cooldown, setCooldown] = useState(0);
  const { login } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  useEffect(() => {
    if (cooldown <= 0) return;
    const t = setTimeout(() => setCooldown((c) => c - 1), 1000);
    return () => clearTimeout(t);
  }, [cooldown]);

  const submitLogin = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      const data = await authApi.login(email, password);
      login(data.token, data.user);
      navigate('/');
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const requestOtp = async (e) => {
    e.preventDefault();
    setError('');

    if (!isAllowedDomain(email)) {
      setError(`Only ${ALLOWED_DOMAIN_DISPLAY} email addresses are allowed.`);
      return;
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    setSubmitting(true);
    try {
      const data = await authApi.requestSignupOtp(email, password);
      setInfo(data.message);
      setMode('otp');
      setCooldown(60);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const verifyOtp = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      const data = await authApi.verifySignupOtp(email, otp);
      login(data.token, data.user);
      navigate('/');
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const resendOtp = async () => {
    if (cooldown > 0) return;
    setError('');
    setSubmitting(true);
    try {
      const data = await authApi.requestSignupOtp(email, password);
      setInfo(data.message);
      setCooldown(60);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--paper)', padding: 20, position: 'relative' }}>
      <button
        onClick={toggleTheme}
        style={{ position: 'absolute', top: 20, right: 20, width: 38, height: 38, borderRadius: '50%', border: '1px solid var(--line)', background: 'var(--paper-raised)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)' }}
      >
        {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
      </button>
      <div style={{ width: '100%', maxWidth: 380 }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: 28, fontWeight: 700, color: 'var(--ink)' }}>Prepwise</div>
          <div style={{ fontSize: 12, color: 'var(--text-muted)', letterSpacing: '0.06em', textTransform: 'uppercase', marginTop: 2 }}>PTE Academic Prep</div>
        </div>

        <div style={{ background: 'var(--paper-raised)', border: '1px solid var(--line)', borderRadius: 'var(--radius-lg)', padding: 28, boxShadow: 'var(--shadow-raised)' }}>
          {mode !== 'otp' && (
            <div style={{ display: 'flex', gap: 4, marginBottom: 22, background: 'var(--paper)', borderRadius: 999, padding: 4 }}>
              {['login', 'signup'].map((m) => (
                <button
                  key={m}
                  onClick={() => { setMode(m); setError(''); setInfo(''); }}
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
          )}

          {mode === 'signup' && (
            <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 16, padding: '10px 12px', background: 'var(--focus-soft)', borderRadius: 'var(--radius-sm)' }}>
              Only {ALLOWED_DOMAIN_DISPLAY} email addresses can sign up. We'll email you a verification code.
            </p>
          )}

          {mode === 'login' && (
            <form onSubmit={submitLogin} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <EmailField email={email} setEmail={setEmail} />
              <PasswordField password={password} setPassword={setPassword} placeholder="Password" />
              {error && <ErrorBox message={error} />}
              <SubmitButton submitting={submitting} label="Log In" />
            </form>
          )}

          {mode === 'signup' && (
            <form onSubmit={requestOtp} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <EmailField email={email} setEmail={setEmail} />
              <PasswordField password={password} setPassword={setPassword} placeholder="Password (min 6 characters)" />
              {error && <ErrorBox message={error} />}
              <SubmitButton submitting={submitting} label="Send Verification Code" />
            </form>
          )}

          {mode === 'otp' && (
            <form onSubmit={verifyOtp} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <div style={{ display: 'flex', gap: 8, alignItems: 'flex-start', padding: '10px 12px', background: 'var(--success-soft)', borderRadius: 'var(--radius-sm)' }}>
                <ShieldCheck size={15} color="var(--success)" style={{ flexShrink: 0, marginTop: 1 }} />
                <span style={{ fontSize: 12, color: 'var(--success)' }}>{info}</span>
              </div>

              <input
                type="text"
                required
                inputMode="numeric"
                maxLength={6}
                placeholder="6-digit code"
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
                className="mono"
                style={{ width: '100%', padding: '13px 14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--line-strong)', fontSize: 22, fontWeight: 700, letterSpacing: 8, textAlign: 'center' }}
              />

              {error && <ErrorBox message={error} />}

              <SubmitButton submitting={submitting} label="Verify & Create Account" />

              <button
                type="button"
                onClick={resendOtp}
                disabled={cooldown > 0 || submitting}
                style={{ background: 'none', border: 'none', fontSize: 12, color: cooldown > 0 ? 'var(--text-muted)' : 'var(--focus)', fontWeight: 600 }}
              >
                {cooldown > 0 ? `Resend code in ${cooldown}s` : 'Resend code'}
              </button>

              <button
                type="button"
                onClick={() => { setMode('signup'); setOtp(''); setError(''); }}
                style={{ background: 'none', border: 'none', fontSize: 12, color: 'var(--text-secondary)' }}
              >
                ← Use a different email
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}

function EmailField({ email, setEmail }) {
  return (
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
  );
}

function PasswordField({ password, setPassword, placeholder }) {
  return (
    <div style={{ position: 'relative' }}>
      <Lock size={15} style={{ position: 'absolute', left: 12, top: 13, color: 'var(--text-muted)' }} />
      <input
        type="password"
        required
        minLength={6}
        placeholder={placeholder}
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ width: '100%', padding: '11px 12px 11px 36px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--line-strong)', fontSize: 14 }}
      />
    </div>
  );
}

function ErrorBox({ message }) {
  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'flex-start', padding: '10px 12px', background: 'var(--error-soft)', borderRadius: 'var(--radius-sm)' }}>
      <AlertCircle size={15} color="var(--error)" style={{ flexShrink: 0, marginTop: 1 }} />
      <span style={{ fontSize: 12, color: 'var(--error)' }}>{message}</span>
    </div>
  );
}

function SubmitButton({ submitting, label }) {
  return (
    <button
      type="submit"
      disabled={submitting}
      style={{ padding: '12px 0', borderRadius: 999, border: 'none', background: 'var(--focus)', color: '#fff', fontSize: 14, fontWeight: 700, opacity: submitting ? 0.6 : 1, marginTop: 6 }}
    >
      {submitting ? 'Please wait…' : label}
    </button>
  );
}
